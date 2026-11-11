#!/usr/bin/env python3
"""Fill the page kit with data.

    python3 fill.py data.json out.html [--embed]

Copies page.html (next to this file, or in ../assets as a skill ships it) to out.html with data.json in place of
the JSON block. With --embed, every "thumbnail", "avatar" and "poster" URL is
downloaded and inlined as a data: URI; a download that fails drops its field,
so the card falls back to its image-free variant. Standard library only.
"""
import base64, concurrent.futures, json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
FIELDS = ('thumbnail', 'avatar', 'poster')
MAX_BYTES = 600_000  # skip anything bigger than a thumbnail should be
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) vamos-page-kit/1'


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=20) as r:  # follows the cdn's 307 to the signed link
        kind = (r.headers.get('Content-Type') or '').split(';')[0].strip()
        body = r.read(MAX_BYTES + 1)
    if not kind.startswith('image/') or len(body) > MAX_BYTES or not body:
        raise ValueError(f'{kind or "no type"}, {len(body)} bytes')
    return f'data:{kind};base64,{base64.b64encode(body).decode()}'


def walk(node, found):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in FIELDS and isinstance(v, str) and v.startswith('http'):
                found.append((node, k, v))
            else:
                walk(v, found)
    elif isinstance(node, list):
        for v in node:
            walk(v, found)


def embed(data):
    found = []
    walk(data, found)
    urls = sorted({u for _, _, u in found})
    got, failed = {}, {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futs = {pool.submit(fetch, u): u for u in urls}
        for f in concurrent.futures.as_completed(futs):
            u = futs[f]
            try:
                got[u] = f.result()
            except Exception as e:  # 403s, timeouts, non-images
                failed[u] = str(e)
    for node, k, u in found:
        if u in got:
            node[k] = got[u]
        else:
            node.pop(k, None)
    for u, why in sorted(failed.items()):
        print(f'  dropped {u} ({why})', file=sys.stderr)
    print(f'embedded {len(got)} of {len(urls)} images', file=sys.stderr)


def main(argv):
    args = [a for a in argv if not a.startswith('--')]
    if len(args) != 2:
        sys.exit(__doc__)
    src, out = args
    data = json.load(open(src, encoding='utf-8'))
    if '--embed' in argv:
        embed(data)
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    blob = blob.replace('</', '<\\/').replace('<!--', '<\\!--')
    tpl = os.path.join(HERE, 'page.html')
    if not os.path.exists(tpl):
        tpl = os.path.join(HERE, '..', 'assets', 'page.html')
    page = open(tpl, encoding='utf-8').read()
    pat = re.compile(r'(<script type="application/json" id="data">)(.*?)(</script>)', re.S)
    if not pat.search(page):
        sys.exit('page.html has no <script type="application/json" id="data"> block')
    page = pat.sub(lambda m: m.group(1) + blob + m.group(3), page, count=1)
    title = ' '.join(x for x in (data.get('title'), data.get('title_pixel')) if x)
    if title:
        esc = title.replace('&', '&amp;').replace('<', '&lt;')
        page = re.sub(r'<title>.*?</title>', lambda m: f'<title>{esc}</title>', page, count=1)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(page)
    print(f'wrote {out} ({len(page.encode()):,} bytes)', file=sys.stderr)


if __name__ == '__main__':
    main(sys.argv[1:])
