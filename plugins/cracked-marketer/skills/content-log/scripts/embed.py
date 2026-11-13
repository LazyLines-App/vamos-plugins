#!/usr/bin/env python3
"""Make a finished page's pictures show inside an Artifact, which blocks remote images.

    python3 embed.py page.html [out.html]

Each <img> with a web link is downloaded and put in the page as a data: URI. An image that fails
(some thumbnails answer 403) is taken out with its tag, so no empty box is left. Writes back to
page.html unless out.html is given, then prints the size and any cloudfront.net link left (those
links die in about 102 minutes). Standard library only.
"""
import base64, concurrent.futures, html, re, sys, urllib.request

MAX_BYTES = 600_000  # a thumbnail is well under this
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) vamos-page/2'
IMG = re.compile(r'<img\b[^>]*>', re.I)
SRC = re.compile(r'''\ssrc\s*=\s*(["'])(https?://[^"']+)\1''', re.I)


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=20) as r:  # follows the cdn's redirect to the signed link
        kind = (r.headers.get('Content-Type') or '').split(';')[0].strip()
        body = r.read(MAX_BYTES + 1)
    if not kind.startswith('image/') or not body or len(body) > MAX_BYTES:
        raise ValueError(f'{kind or "no type"}, {len(body)} bytes')
    return f'data:{kind};base64,{base64.b64encode(body).decode()}'


def main(argv):
    if len(argv) not in (1, 2):
        sys.exit(__doc__)
    src, out = argv[0], argv[-1]
    page = open(src, encoding='utf-8').read()
    urls = sorted({html.unescape(m.group(2)) for tag in IMG.findall(page) for m in [SRC.search(tag)] if m})
    got, failed = {}, {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        jobs = {pool.submit(fetch, u): u for u in urls}
        for job in concurrent.futures.as_completed(jobs):
            u = jobs[job]
            try:
                got[u] = job.result()
            except Exception as e:  # 403s, timeouts, non-images
                failed[u] = str(e)

    def swap(m):
        tag = m.group(0)
        s = SRC.search(tag)
        if not s:
            return tag
        u = html.unescape(s.group(2))
        if u not in got:
            return ''
        return tag[:s.start(2)] + got[u] + tag[s.end(2):]

    page = IMG.sub(swap, page)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(page)
    for u, why in sorted(failed.items()):
        print(f'  removed {u} ({why})', file=sys.stderr)
    size = len(page.encode())
    print(f'embedded {len(got)} of {len(urls)} images; wrote {out} ({size / 1e6:.1f} MB)', file=sys.stderr)
    if size > 16_000_000:
        print('  over the 16 MB Artifact limit: show fewer pictures', file=sys.stderr)
    if 'cloudfront.net' in page:
        print(f'  {page.count("cloudfront.net")} cloudfront.net link(s) left: use the cdn.lazylines.ai link instead', file=sys.stderr)


if __name__ == '__main__':
    main(sys.argv[1:])
