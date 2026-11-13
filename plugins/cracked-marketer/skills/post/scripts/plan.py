#!/usr/bin/env python3
"""Plan a batch of posts on the user's own Zernio and hold the posting rules in code. Standard library only;
ffprobe (FFmpeg) reads each file's size and length when it's installed.

  python3 plan.py batch.json [--urls urls.json] [--out plan.json]

batch.json:
  {"timezone": "Europe/Madrid", "times": ["09:00", "13:00", "19:00"],
   "accounts": [{"id": "<Zernio accountId>", "platform": "instagram", "handle": "@brand", "times": ["12:00"]}],
   "existing": [{"account": "<accountId>", "at": "2026-11-14T09:00:00+01:00", "file": "hook-1.mp4"}],
   "posts": [{"file": "cuts/hook-1.mp4", "to": ["<accountId>", ...], "at": "2026-11-14T19:00" or "now"}]}
  "times" are the daily slots (an account's own "times" win); "existing" is what's already on them: Zernio's
  scheduled posts and those published in the last 24 hours, each with its file from metadata.vamos_file when it has
  one, so slots, caps and repeats count it. "start" (a date) and "now" (ISO) are optional. "tiktok_drafts": true
  sends TikTok rows to the account's TikTok inbox, for the user to post there (the standing-yes path).

Each file's post sheet is <file>.post.json beside it (make-video writes one), or "sheet": {...} on the post:
  {"caption": "...", "title": "YouTube title", "ai": true, "people": "made", "disclosure": "Made with AI.",
   "promotes": "own"}
  ai        the video holds AI-made footage, an AI face or an AI voice (true or false, never left out)
  people    none | filmed (real people, filmed, who agreed) | made (a character the user made) |
            agreed (an AI version of a real person who agreed: the user, or someone with their written yes) |
            likeness (an AI version of a real person who hasn't agreed): a likeness is never posted
  promotes  own (the user's own brand or product) | partner (paid by a brand: "partner": "@brand") | none

--urls maps each file to the publicUrl Zernio's upload gave it; without it the payloads hold UPLOAD:<file>.

Prints the batch table to show for the user's yes, then DEFECT lines (fix before anything is sent: exit 1)
and FLAG lines (show them with the table). plan.json holds each row's validate_post and posts_create_post
arguments: send them as they are.
"""
import argparse, datetime as dt, hashlib, json, os, re, shutil, subprocess, sys
from zoneinfo import ZoneInfo

# Per account, per rolling 24 hours: the lower of Zernio's cap and the platform's own (read 2026-11-13:
# docs.zernio.com/guides/rate-limits; Meta's content-publishing and Reels docs; TikTok's Content Posting API).
CAPS = {'instagram': 100, 'facebook': 30, 'tiktok': 15, 'youtube': 50, 'twitter': 50, 'threads': 250,
        'linkedin': 50, 'pinterest': 25}
# Where each platform's AI label goes in Zernio's posts_create_post (docs.zernio.com, read 2026-11-13).
# Facebook, Threads and LinkedIn take none through the API: AI footage there is posted by hand with the label.
LABEL = {'instagram': ('platformSpecificData', 'isAiGenerated'),
         'youtube': ('platformSpecificData', 'containsSyntheticMedia'),
         'twitter': ('platformSpecificData', 'madeWithAi'),
         'pinterest': ('platformSpecificData', 'isAiGenerated'),
         'tiktok': ('tiktok_settings', 'videoMadeWithAi')}
CAPTION_MAX = {'instagram': 2200, 'tiktok': 2200, 'youtube': 5000, 'facebook': 63206, 'twitter': 280,
               'threads': 500, 'linkedin': 3000, 'pinterest': 500}
VERTICAL = {'instagram', 'tiktok', 'youtube', 'facebook'}
NO_LINKS = {'instagram', 'tiktok', 'youtube'}
LINK = re.compile(r'https?://|www\.|\b[\w-]+\.(com|ai|io|app|co|net|org)\b', re.I)
DAY = dt.timedelta(hours=24)
LEAD = dt.timedelta(minutes=15)
DRAFTS = 5        # TikTok holds 5 pending inbox drafts per account in any 24 hours (docs.zernio.com, TikTok, 11-13)
X_POST = 0.015    # X bills each post through the API; Zernio passes it on: $0.015, $0.20 with a link (11-13)


def probe(path):
    if not shutil.which('ffprobe'):
        return None
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                          'stream=width,height:format=duration', '-of', 'json', path], capture_output=True, text=True)
    if out.returncode:
        return None
    j = json.loads(out.stdout)
    s = (j.get('streams') or [{}])[0]
    return {'w': s.get('width'), 'h': s.get('height'), 'secs': float(j.get('format', {}).get('duration') or 0)}


def digest(path):
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def fits(times, t, cap):
    """True when adding t keeps every rolling 24 hours on the account at or under the cap."""
    new = sorted(times + [t])
    return all(sum(1 for q in new if p - DAY < q <= p) <= cap for p in new if abs(p - t) < DAY)


def parse_at(text, tz):
    t = dt.datetime.fromisoformat(text.replace('Z', '+00:00'))
    return t.astimezone(tz) if t.tzinfo else t.replace(tzinfo=tz)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('batch')
    ap.add_argument('--urls')
    ap.add_argument('--out', default='plan.json')
    a = ap.parse_args()
    b = json.load(open(a.batch))
    base = os.path.dirname(os.path.abspath(a.batch))
    tz = ZoneInfo(b.get('timezone') or 'UTC')
    now = parse_at(b['now'], tz) if b.get('now') else dt.datetime.now(tz)
    urls = json.load(open(a.urls)) if a.urls else {}
    accounts = {x['id']: x for x in b.get('accounts', [])}
    taken = {k: [] for k in accounts}
    earlier = []   # (account, file name, time) already on Zernio
    for e in b.get('existing', []):
        if e.get('account') in taken:
            t = parse_at(e['at'], tz)
            taken[e['account']].append(t)
            if e.get('file'):
                earlier.append((e['account'], os.path.basename(e['file']), t))
    drafts = bool(b.get('tiktok_drafts'))
    cap = lambda p: min(CAPS[p], DRAFTS) if drafts and p == 'tiktok' else CAPS[p]
    start = dt.date.fromisoformat(b['start']) if b.get('start') else now.date()
    defects, flags, rows, uploads = [], [], [], []
    seen_file = {}   # (sha, platform) -> handles

    def next_slot(acc):
        times = acc.get('times') or b.get('times') or ['09:00', '13:00', '19:00']
        for d in range(60):
            day = start + dt.timedelta(days=d)
            for hhmm in times:
                h, m = (int(x) for x in hhmm.split(':'))
                t = dt.datetime(day.year, day.month, day.day, h, m, tzinfo=tz)
                if t < now + LEAD or any(abs(t - q) < dt.timedelta(minutes=1) for q in taken[acc['id']]):
                    continue
                if fits(taken[acc['id']], t, cap(acc['platform'])):
                    return t
        return None

    for i, post in enumerate(b.get('posts', []), 1):
        path = os.path.join(base, post['file'])
        name = os.path.basename(post['file'])
        if not os.path.exists(path):
            defects.append(f'{name}: the file is not there')
            continue
        sheet = post.get('sheet')
        if sheet is None:
            sp = next((x for x in (os.path.splitext(path)[0] + '.post.json', path + '.post.json') if os.path.exists(x)), None)
            sheet = json.load(open(sp)) if sp else None
        if sheet is None:
            defects.append(f'{name}: no post sheet; ask for its caption, whether it holds AI footage, faces or a voice, and whose face is in it')
            continue
        missing = [k for k in ('caption', 'ai', 'people') if sheet.get(k) in (None, '')]
        if missing:
            defects.append(f'{name}: the sheet lacks {", ".join(missing)}; ask the user, never guess (ai and people decide the label)')
            continue
        if sheet['people'] == 'likeness':
            defects.append(f'{name}: an AI version of a real person who hasn\'t agreed is never posted; offer their own character or their own footage')
            continue
        if sheet['people'] not in ('none', 'filmed', 'made', 'agreed'):
            defects.append(f'{name}: people is "{sheet["people"]}", want none, filmed, made, agreed or likeness')
            continue
        ai = bool(sheet['ai']) or sheet['people'] in ('made', 'agreed')
        promotes = sheet.get('promotes', 'none')
        caption = sheet['caption'].strip()
        disclosure = (sheet.get('disclosure') or ('Made with AI.' if ai else '')).strip()
        if ai and disclosure.lower() not in caption.lower():
            caption += '\n\n' + disclosure
        if promotes == 'partner' and not re.search(r'#ad\b|paid partnership', caption, re.I):
            caption += ' #ad'
            disclosure = (disclosure + ' #ad').strip()
        info = probe(path)
        sha = digest(path)
        if post['file'] not in uploads:
            uploads.append(post['file'])
        url = urls.get(post['file'], f'UPLOAD:{post["file"]}')
        for acc_id in post.get('to', []):
            acc = accounts.get(acc_id)
            if not acc:
                defects.append(f'{name}: account {acc_id} is not in the batch\'s accounts (accounts_list)')
                continue
            p = acc['platform']
            who = acc.get('handle') or acc_id
            if p not in CAPS:
                defects.append(f'{name} → {who}: {p} is not a platform this skill posts video to')
                continue
            if len(caption) > CAPTION_MAX[p]:
                defects.append(f'{name} → {who}: the caption is {len(caption)} characters, over {p}\'s {CAPTION_MAX[p]}')
            if p == 'instagram' and len(re.findall(r'#\w', caption)) > 30:
                defects.append(f'{name} → {who}: more than 30 hashtags; Instagram refuses the post')
            if p in NO_LINKS and LINK.search(caption):
                flags.append(f'{name} → {who}: a link in the caption isn\'t clickable on {p}; say it in the video or the bio')
            if info and p in VERTICAL and info['w'] and info['h'] and abs(info['w'] / info['h'] - 9 / 16) > 0.02:
                flags.append(f'{name} → {who}: {info["w"]}x{info["h"]} is not 9:16, so {p} shows it with bars or cropped')
            if info and p == 'youtube' and info['secs'] > 180:
                flags.append(f'{name} → {who}: {info["secs"]:.0f} s posts as a long video, not a Short')
            seen_file.setdefault((sha, p), []).append(who)

            when, how = None, 'scheduled'
            if ai and p not in LABEL:
                how = f'by hand in the {p} app, AI label on: the API can\'t set it'
            if post.get('at') == 'now':
                when = now
                how = how if how != 'scheduled' else 'now'
                if not fits(taken[acc_id], when, cap(p)):
                    defects.append(f'{name} → {who}: posting now goes over {p}\'s {cap(p)} posts in 24 hours on this account')
            elif post.get('at'):
                when = parse_at(post['at'], tz)
                if when < now + LEAD:
                    defects.append(f'{name} → {who}: {when:%a %d %b %H:%M} is past or under 15 minutes away; pick a later time or say "now"')
                elif not fits(taken[acc_id], when, cap(p)):
                    defects.append(f'{name} → {who}: {when:%a %d %b %H:%M} goes over {p}\'s {cap(p)} posts in 24 hours on this account')
            else:
                when = next_slot(acc)
                if when is None:
                    defects.append(f'{name} → {who}: no free slot in the next 60 days at {p}\'s cap of {cap(p)} a day')
                    continue
            same = [r for r in rows if r['account'] == acc_id and r['sha'] == sha and abs(r['_t'] - when) < DAY]
            same += [e for e in earlier if e[0] == acc_id and e[1] == name and abs(e[2] - when) < DAY]
            if same:
                defects.append(f'{name} → {who}: the same video twice on one account within 24 hours; Zernio refuses the second')
            taken[acc_id].append(when)

            psd, tik = {}, None
            if p == 'youtube':
                psd.update({'title': (sheet.get('title') or caption.split('\n')[0])[:100], 'visibility': 'public',
                            'madeForKids': False})
            if p == 'facebook':
                psd['contentType'] = 'reel'
            if p == 'pinterest' and sheet.get('title'):
                psd['title'] = sheet['title'][:100]
            if p == 'instagram' and promotes == 'partner':
                psd['brandedContentSponsors' if sheet.get('partner') else 'isPaidPartnership'] = (
                    [sheet['partner'].lstrip('@')] if sheet.get('partner') else True)
            if p == 'tiktok' and drafts:
                # nobody saw this row's table: TikTok gets it as an inbox draft, and the user posts it there
                tik = {'draft': True}
                how = 'to your TikTok inbox: paste the caption' + (', switch on the AI label' if ai else '') + ', then Post'
            elif p == 'tiktok':
                # the user's yes to the table is TikTok's consent: they saw each video, caption and setting
                tik = {'privacyLevel': 'PUBLIC_TO_EVERYONE', 'allowComment': True, 'allowDuet': True,
                       'allowStitch': True, 'contentPreviewConfirmed': True, 'expressConsentGiven': True,
                       'commercialContentType': {'own': 'brand_organic', 'partner': 'brand_content'}.get(promotes, 'none')}
            if p in LABEL:
                where, key = LABEL[p]
                (tik if where == 'tiktok_settings' else psd)[key] = ai
            entry = {'platform': p, 'accountId': acc_id}
            if psd:
                entry['platformSpecificData'] = psd
            create = {'content': caption, 'media_items': [{'type': 'video', 'url': url}], 'platforms': [entry],
                      'metadata': {'vamos_file': name, 'vamos_row': len(rows) + 1}}
            if post.get('at') == 'now':   # by the asked time, not `how`: a TikTok draft rewrites how
                create['publish_now'] = True
            else:
                create['scheduled_for'] = when.strftime('%Y-%m-%dT%H:%M:%S')
                create['timezone'] = str(tz)
            if tik:
                create['tiktok_settings'] = tik
            validate = {'content': caption, 'media_items': create['media_items'],
                        'platforms': [dict(entry, platformSpecificData={**psd, **({'tiktokSettings': tik} if tik else {})},
                                           customMedia=[])]}
            row = {'n': len(rows) + 1, 'account': acc_id, 'handle': who, 'platform': p, 'file': post['file'],
                   'sha': sha, 'at': when.isoformat(), 'how': how, 'ai': ai,
                   'label': ('on' if ai else 'off') if p in LABEL and not (drafts and p == 'tiktok') else ('set by hand' if ai else 'off'),
                   'disclosure': disclosure if (ai or promotes == 'partner') else '', 'caption': caption,
                   'secs': info and round(info['secs'], 1), '_t': when}
            if p == 'twitter':
                row['cost'] = 0.2 if LINK.search(caption) else X_POST
            if not how.startswith('by hand'):
                row['validate'] = validate
                row['create'] = {'name': 'posts_create_post', 'arguments': create}
                if p == 'tiktok' and post.get('at') != 'now' and not drafts:
                    row['dry_run'] = {'name': 'posts_create_post', 'arguments': {**create, 'dry_run': True}}
            rows.append(row)

    for (sha, p), who in seen_file.items():
        if len(set(who)) > 1:
            flags.append(f'the same video goes to {len(set(who))} {p} accounts ({", ".join(sorted(set(who)))}): {p} '
                         'treats reposts across accounts as unoriginal and keeps them from new viewers; give each account its own cut')

    # the table for the user's yes
    print(f'| # | Account | When ({tz}) | File | Caption | AI label | Disclosure | How |')
    print('|---|---|---|---|---|---|---|---|')
    for r in rows:
        cap = r['caption'].replace('\n', ' ').replace('|', '/')
        tail = r['disclosure'] if r['disclosure'] and cap.endswith(r['disclosure']) else ''
        if len(cap) > 70:   # cut the middle, never the disclosure at the end: the yes covers it
            keep = 68 - len(tail)
            cap = cap[:keep].rstrip() + '… ' + tail if tail else cap[:67] + '…'
        length = f' ({r["secs"]} s)' if r['secs'] else ''
        print(f'| {r["n"]} | {r["handle"]} ({r["platform"]}) | {r["_t"]:%a %d %b %H:%M} | {os.path.basename(r["file"])}{length} '
              f'| {cap} | {r["label"]} | {r["disclosure"] or "—"} | {r["how"]} |')
    for d in defects:
        print('DEFECT', d)
    for f in flags:
        print('FLAG  ', f)
    sent = [r for r in rows if 'create' in r]
    hand = len(rows) - len(sent)
    days = sorted({r['_t'].date() for r in rows})
    x = sum(r.get('cost', 0) for r in sent)
    print(f'BATCH: {len(rows)} posts on {len({r["account"] for r in rows})} accounts over {len(days)} day(s); '
          f'{len(sent)} through Zernio, {hand} by hand.' + (f' X bills ${x:.3f} for its {sum(1 for r in sent if r["platform"] == "twitter")} '
          'post(s), from your Zernio balance.' if x else ''))
    need = [u for u in uploads if u not in urls]
    if need and sent:
        print('UPLOAD first, then run this again with --urls:', ', '.join(need))
    for r in rows:
        r.pop('_t')
    json.dump({'timezone': str(tz), 'rows': rows, 'uploads': need}, open(a.out, 'w'), indent=1)
    print(f'{"FAIL" if defects else "PASS"}: {a.out}')
    sys.exit(1 if defects else 0)


if __name__ == '__main__':
    main()
