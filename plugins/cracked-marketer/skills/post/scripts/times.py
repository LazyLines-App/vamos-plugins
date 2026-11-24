#!/usr/bin/env python3
"""Each account's best times to post, from its own posts and, on Instagram, when its followers are online.
Standard library only.

    python3 times.py SOURCE [SOURCE ...] --tz Europe/Madrid [--slots 2] [--now ISO] [--out times.json]

SOURCE is a saved Zernio answer: a page of post analytics (analytics_get_analytics, view summary) or an Instagram
account's followers online (analytics_get_instagram_online_followers). --slots is how many times a day it proposes.

Per account: posts at least 7 days old count, ads and paid partnerships set aside. Each post is scored against the
median views of the up to 20 posts around it (10 before, 10 after), so the account's growth over the year doesn't
credit the hours used in its good months. Posts fall in 3-hour windows of the local day; a window counts from 5
posts. With 8 scored posts and 2 windows that count, a shuffle test of the posts' times says whether the best
window's lead is bigger than chance (a lead at 10% or under). Meta's followers-online hour h is read as h hours
after the day's start (endTime minus 24 h) and put on the local clock.

The proposed times, 3 hours apart: the leading window's hour, then the hours with at least 2/3 of the busiest hour's
followers online, then (after a lead) the other windows at or above the posts around them, else the window posted
at most, then tests at 19, 13, 10, 16, 22 and 7 where a window has under 5 posts. Prints each account's windows,
what they say and a last line "TIMES @handle (platform): ..."; times.json holds the same.
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
import json
import random
import re
import statistics
import sys
from zoneinfo import ZoneInfo

PAID = re.compile(r'#ad\b|#sponsored|paid partnership|\bsponsored\b|#partner', re.I)


def ts(value):
    value = re.sub(r'([+-]\d\d)(\d\d)$', r'\1:\2', value.replace('Z', '+00:00'))   # Meta's +0000, for Python 3.9
    t = datetime.fromisoformat(value)
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def load(path):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, list) and data and isinstance(data[0], dict) and data[0].get('type') == 'text':
        data = json.loads(''.join(item.get('text', '') for item in data))
    for _ in range(5):
        if isinstance(data, dict) and (isinstance(data.get('posts'), list) or
                                      data.get('metric') == 'online_followers' and isinstance(data.get('days'), list)):
            return data
        if not isinstance(data, dict):
            break
        data = data.get('data', data.get('result'))
    raise ValueError('not a Zernio analytics or followers-online answer')


def label(index):
    return f'{index * 3:02d}:00–{(index + 1) * 3:02d}:00'


def accounts_from(sources):
    accounts = {}
    def account(ident, platform, username=None):
        if ident not in accounts:
            accounts[ident] = {'account': ident, 'platform': platform or '?', 'handle': '@?', 'rows': {}, 'days': None}
        acc = accounts[ident]
        if platform:
            acc['platform'] = platform
        if username:
            acc['handle'] = '@' + username.lstrip('@')
        return acc

    serial = 0
    for data in sources:
        if 'posts' not in data:
            acc = account(data.get('accountId'), data.get('platform'))
            if acc['days'] is None:
                acc['days'] = {}
            for day in data['days']:
                acc['days'][day['endTime']] = day
            continue
        for post in data['posts']:   # the list holds one item per platform post, so its numbers are that account's
            if post.get('status', 'published') != 'published':
                continue
            entries = post.get('platforms') or [post]
            for entry in entries:
                if entry.get('status', 'published') != 'published':
                    continue
                acc = account(entry.get('accountId', post.get('accountId')),
                              entry.get('platform', post.get('platform')),
                              entry.get('accountUsername', post.get('accountUsername')))
                analytics = entry.get('analytics') if 'analytics' in entry else post.get('analytics')
                analytics = analytics or {}
                views = analytics.get('views')
                if views is None:
                    views = analytics.get('impressions')
                serial += 1
                ident = entry.get('platformPostId') or entry.get('platformPostUrl')
                if not ident:
                    ident = post.get('platformPostId') or post.get('platformPostUrl') or post.get('_id') or f'_row_{serial}'
                updated = ts(analytics['lastUpdated']) if analytics.get('lastUpdated') else datetime.min.replace(tzinfo=timezone.utc)
                row = {'at': ts(post['publishedAt']) if post.get('publishedAt') else None,
                       'views': views, 'paid': bool(post.get('isAd')) or bool(PAID.search(post.get('content') or '')),
                       'updated': updated}
                old = acc['rows'].get(ident)
                if old is None or updated > old['updated']:
                    acc['rows'][ident] = row
    return accounts


def followers(days, tz):
    if not days:
        return None
    hours = defaultdict(list)
    ends = []
    for day in days.values():
        end = ts(day['endTime']).astimezone(timezone.utc)
        ends.append(end)
        start = end - timedelta(hours=24)
        for h, value in day['hours'].items():
            local = (start + timedelta(hours=int(h))).astimezone(tz).hour
            hours[local].append(value)
    return {'days': len(days), 'to': (max(ends) - timedelta(hours=24)).date().isoformat(),
            'by_hour': {str(h): round(statistics.mean(values), 1) for h, values in sorted(hours.items())}}


def analyse(acc, now, tz, limit):
    eligible = [r for r in acc['rows'].values() if r['at'] is not None and r['at'] <= now - timedelta(days=7)
                and r['views'] is not None]
    aside = sum(r['paid'] for r in eligible)
    posts = sorted((r for r in eligible if not r['paid']), key=lambda r: r['at'])
    groups = defaultdict(list)
    scored = []
    for i, row in enumerate(posts):
        neighbours = posts[max(0, i - 10):i] + posts[i + 1:i + 11]
        baseline = statistics.median(r['views'] for r in neighbours) if neighbours else 0
        if baseline:
            hour = row['at'].astimezone(tz).hour
            score = row['views'] / baseline
            groups[hour // 3].append((score, hour))
            scored.append((score, hour // 3))
    windows = []
    medians = {}
    for index, values in sorted(groups.items()):
        counts = Counter(h for _, h in values)
        median = statistics.median(v for v, _ in values) if len(values) >= 5 else None
        if median is not None:
            medians[index] = median
        windows.append({'window': label(index), 'posts': len(values),
                        'median': round(median, 2) if median is not None else None,
                        'hour': min(counts, key=lambda h: (-counts[h], h))})
    chance = None
    if len(scored) < 8:
        verdict = 'too-few'
    elif len(medians) < 2:
        verdict = 'cant-compare'
    else:
        observed = max(medians.values())
        scores = [s for s, _ in scored]
        indexes = [i for _, i in scored]
        rng = random.Random(7)
        exceed = 0
        for _ in range(2000):
            rng.shuffle(indexes)
            shuffled = defaultdict(list)
            for score, index in zip(scores, indexes):
                shuffled[index].append(score)
            best = max(statistics.median(v) for v in shuffled.values() if len(v) >= 5)
            exceed += best >= observed - 1e-9
        chance = round((1 + exceed) / 2001, 3)
        verdict = 'lead' if (1 + exceed) / 2001 <= 0.10 else 'no-lead'
    online = followers(acc['days'], tz)
    slots = []
    def add(hour, source, why):
        if len(slots) < limit and all(min(abs(hour - x['hour']), 24 - abs(hour - x['hour'])) >= 3 for x in slots):
            slots.append({'hour': hour, 'time': f'{hour:02d}:00', 'source': source, 'why': why})
    by_index = {int(w['window'][:2]) // 3: w for w in windows}
    ranked = sorted(medians, key=lambda i: (-medians[i], i))
    def add_post(index):
        w = by_index[index]
        add(w['hour'], 'posts', f"your posts at {w['window']}: {w['median']}× the posts around them, over {w['posts']} posts")
    if verdict == 'lead':
        add_post(ranked[0])
    if online and online['by_hour']:
        hours = sorted(online['by_hour'], key=lambda h: (-online['by_hour'][h], int(h)))
        maximum = online['by_hour'][hours[0]]
        for h in hours:
            value = online['by_hour'][h]
            if value >= maximum * 2 / 3:
                add(int(h), 'followers', f"followers online: {value:.0f} on average, Meta's {online['days']} days to {online['to']}")
    if verdict == 'lead':
        for index in ranked[1:]:
            if medians[index] >= 1:
                add_post(index)
    elif medians:
        index = min(medians, key=lambda i: (-len(groups[i]), -medians[i], i))
        w = by_index[index]
        add(w['hour'], 'usual', f"your usual time: {w['posts']} of {len(scored)} posts went out at {w['window']}")
    for h in (19, 13, 10, 16, 22, 7):
        n = len(groups[h // 3])
        if n < 5:
            add(h, 'test', f"a test: {n} {'post' if n == 1 else 'posts'} at {label(h // 3)} so far")
    slots.sort(key=lambda s: s['hour'])
    for slot in slots:
        del slot['hour']
    result = {'account': acc['account'], 'platform': acc['platform'], 'handle': acc['handle'],
              'posts': len(posts), 'set_aside': aside, 'verdict': verdict, 'chance': chance,
              'windows': windows, 'online': online, 'times': [s['time'] for s in slots], 'slots': slots}
    return result, posts, len(scored)


def show(acc, posts, scored, tz, had_online):
    span = f" from {posts[0]['at'].astimezone(tz).date()} to {posts[-1]['at'].astimezone(tz).date()}" if posts else ''
    print(f"{acc['handle']} ({acc['platform']}), times in {tz}: {acc['posts']} posts at least 7 days old{span}, "
          f"{acc['set_aside']} set aside as ads or paid; each scored against the posts around it")
    print('| Went out | Posts | Median score |\n|---|---:|---:|')
    for w in acc['windows']:
        median = f"{w['median']}×" if w['median'] is not None else 'too few'
        print(f"| {w['window']} | {w['posts']} | {median} |")
    if acc['verdict'] == 'too-few':
        print(f"{scored} posts: too few to compare times (it takes 8, with 5 at each time compared).")
    elif acc['verdict'] == 'cant-compare':
        w = max(acc['windows'], key=lambda w: w['posts'])
        print(f"Can't compare times yet: {w['posts']} of {scored} posts went out {w['window']}, and a time needs 5 posts to count.")
    else:
        pct = round(acc['chance'] * 100)
        ending = "so it's unlikely to be chance" if acc['verdict'] == 'lead' else 'so the gaps are within chance'
        print(f"A lead this size came up in {pct}% of 2,000 shuffles of the same posts' times, {ending}.")
    online = acc['online']
    if online and online['by_hour']:
        hours = online['by_hour']
        ranked = sorted(hours, key=lambda h: (-hours[h], int(h)))
        quiet = min(hours, key=lambda h: (hours[h], int(h)))
        busy = ', '.join(f'{int(h):02d}:00 ({hours[h]:.0f})' for h in ranked[:3])
        print(f"Followers online, on average: busiest {busy}; quietest {int(quiet):02d}:00 ({hours[quiet]:.0f}) (Meta, {online['days']} days to {online['to']}).")
    elif had_online:
        print('Meta gives followers online only from 100 followers.')
    print(f"TIMES {acc['handle']} ({acc['platform']}): " + ', '.join(f"{s['time']} ({s['why']})" for s in acc['slots']))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('sources', nargs='+')
    ap.add_argument('--tz', required=True)
    ap.add_argument('--slots', type=int, default=2)
    ap.add_argument('--now')
    ap.add_argument('--out', default='times.json')
    args = ap.parse_args()
    tz = ZoneInfo(args.tz)
    now = ts(args.now) if args.now else datetime.now(timezone.utc)
    sources = []
    for path in args.sources:
        try:
            sources.append(load(path))
        except (OSError, ValueError, TypeError) as e:
            sys.exit(f'{path}: {e}')
    accounts = accounts_from(sources)
    results = []
    for acc in accounts.values():
        result, posts, scored = analyse(acc, now, tz, args.slots)
        results.append(result)
        show(result, posts, scored, tz, acc['days'] is not None and acc['platform'] == 'instagram')
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump({'timezone': args.tz, 'accounts': results}, f, indent=2)


if __name__ == '__main__':
    main()
