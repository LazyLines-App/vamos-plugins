"""content-log's count.py on a real https-style download. Standard library only, no network.

    python3 evals/scripts/test_count.py

A local server stands in for Vamos's data link and answers as Cloudflare does there: Python's
default User-Agent gets a 403 (error 1010), anything else gets the rows. Before fc5222a every real
json_url failed this way while the evals, which serve file: links, passed.
"""
import json, os, subprocess, sys, threading, unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COUNT = os.path.join(ROOT, 'plugins', 'vamos', 'skills', 'content-log', 'scripts', 'count.py')
ROWS = os.path.join(ROOT, 'plugins', 'vamos', 'evals', 'content-log-week-opusjake', 'mocks', 'vamos', 'chat_completion_poll.md')
BODY = json.dumps(json.load(open(ROWS, encoding='utf-8'))['data']).encode()


class Cdn(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.headers.get('User-Agent', '').startswith('Python-urllib'):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'error code: 1010')
        elif self.path.startswith('/data/rows.json'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(BODY)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *a):
        pass


class CountDownload(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('127.0.0.1', 0), Cdn)
        cls.base = f'http://127.0.0.1:{cls.server.server_address[1]}'
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def run_count(self, url):
        return subprocess.run([sys.executable, '-I', COUNT, url, '--since', '2026-11-03'],
                              capture_output=True, text=True, timeout=60)

    def test_link_downloads_past_the_user_agent_check(self):
        out = self.run_count(self.base + '/data/rows.json?e=1&s=2')
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn('usual: 42,606 views, the median of 34 posts', out.stdout)
        self.assertRegex(out.stdout, r'14\.4\s?x')

    def test_failed_download_says_what_to_do_in_one_line(self):
        out = self.run_count(self.base + '/data/missing.json')
        self.assertNotEqual(out.returncode, 0)
        self.assertNotIn('Traceback', out.stderr)
        self.assertIn("couldn't download the rows", out.stderr)
        self.assertIn('curl -sL', out.stderr)


def row(handle, i, day, views, likes=None, paid=False, caption='a post'):
    return {'id': f'{handle}{i}', 'url': f'https://www.instagram.com/p/{handle}{i}/', 'platform': 'INSTAGRAM',
            'creator': {'handle': handle}, 'views': views, 'likes': likes if likes is not None else views // 20,
            'comments': 5, 'posted_at': f'2026-{day}T12:00:00Z', 'counts_as_of': '2026-11-11T12:00:00Z',
            'paid_partnership': paid, 'caption_head': f'{caption} {i}', 'duration_seconds': 30 + i}


class CreatorResults(unittest.TestCase):
    """Creators the brand pays: their posts for the brand are judged against the account's own usual, never part of it."""

    @classmethod
    def setUpClass(cls):
        import tempfile
        d = tempfile.mkdtemp()
        own = [row('maker', i, f'10-{10 + i:02d}', 1000 * (i + 1)) for i in range(11)]  # usual 6,000
        brand = [row('brand', i, f'10-{10 + i:02d}', 20000) for i in range(10)]          # usual 20,000
        ours = [row('maker', 20, '11-05', 30000, paid=True, caption='#ad trying Potly'),  # 5x, tagged paid
                row('maker', 21, '11-06', 900, likes=2, paid=True, caption='#ad Potly'),  # under 1,000, likes 0.2%
                row('maker', 22, '11-10', 4000, paid=True),                              # too early
                row('brand', 23, '11-05', 10000, caption='no label')]                    # by @lee on the brand's account
        tags = {'maker20': {'ours': True, 'creator': '@maker', 'hook': 'Payday in nine minutes'},
                'maker21': {'ours': True, 'creator': '@maker', 'hook': 'Day ten and not broke'},
                'maker22': {'ours': True, 'creator': '@maker', 'hook': 'Payday in nine minutes'},
                'brand23': {'ours': True, 'creator': '@lee', 'hook': 'Payday in nine minutes', 'paid': 200}}
        pay = {'@maker': {'base': 60, 'bonus': [[18000, 60], [60000, 120]], 'due': 4, 'sales': 6},
               '@nobody': {'base': 50, 'due': 2}}
        for name, blob in (('rows.json', {'data': {'videos': own + brand + ours}}), ('tags.json', tags), ('pay.json', pay)):
            with open(os.path.join(d, name), 'w') as f:
                json.dump(blob, f)
        cls.out = subprocess.run([sys.executable, '-I', COUNT, os.path.join(d, 'rows.json'), '--since', '2026-11-01',
                                  '--tags', os.path.join(d, 'tags.json'), '--pay', os.path.join(d, 'pay.json')],
                                 capture_output=True, text=True, timeout=60)

    def test_runs(self):
        self.assertEqual(self.out.returncode, 0, self.out.stderr)

    def test_usual_leaves_out_the_posts_for_the_brand(self):
        self.assertIn('usual: 6,000 views, the median of 11 posts', self.out.stdout)
        self.assertIn('usual: 20,000 views, the median of 10 posts', self.out.stdout)

    def test_a_paid_post_for_the_brand_is_judged_not_set_aside(self):
        self.assertRegex(self.out.stdout, r'maker20 on @maker: 30,000 views, 5\.0x the usual of 6,000')
        self.assertNotIn('maker20 30,000 views, tagged paid', self.out.stdout)

    def test_the_brand_account_post_is_against_the_brand_usual(self):
        self.assertRegex(self.out.stdout, r'brand23 on @brand: 10,000 views, 0\.5x the usual of 20,000')
        self.assertRegex(self.out.stdout, r'brand23[^\n]*no paid-partnership label in the row')

    def test_cost_from_the_deal(self):
        self.assertRegex(self.out.stdout, r'maker20[^\n]*paid \$120 \(\$60 base \+\$60 at 18,000\), \$4\.00 per 1,000')
        self.assertRegex(self.out.stdout, r'brand23[^\n]*paid \$200 \(\$200 as tagged\)')

    def test_where_a_miss_broke_and_a_boost(self):
        self.assertRegex(self.out.stdout, r'maker21[^\n]*under 1,000: the opening failed[^\n]*likes under 0\.5%')

    def test_scorecard(self):
        self.assertRegex(self.out.stdout, r'scorecard: 3 posted of 4 due, 1 of 2 judged above usual[^\n]*paid \$240 for 34,900 views, \$6\.88 per 1,000; 6 sales from your numbers, \$40\.00 each')
        self.assertIn('@nobody:\n    scorecard: 0 posted of 2 due', self.out.stdout)

    def test_hooks_pooled_across_creators(self):
        self.assertIn('"Payday in nine minutes": 3 tries by 2 creators, 1 above usual, 1 too early, best 30,000, 5.0x (@maker)', self.out.stdout)

class CreatorEdges(unittest.TestCase):
    """Share links, a post before --since, a capped bonus pool, an unmatched link, hooks ranked by multiple."""

    @classmethod
    def setUpClass(cls):
        import tempfile
        d = tempfile.mkdtemp()
        own = [row('maker', i, f'10-{10 + i:02d}', 1000 * (i + 1)) for i in range(11)]  # usual 6,000
        brand = [row('brand', i, f'10-{10 + i:02d}', 20000) for i in range(10)]          # usual 20,000
        ours = [row('maker', 30, '10-25', 12000, caption='#ad'),                          # 2.0x, before --since
                row('maker', 32, '11-04', 25000, caption='#ad'),                          # 4.2x
                row('brand', 31, '11-05', 18000, caption='#ad')]                          # 0.9x on the brand's account
        tags = {'https://www.instagram.com/p/maker30/?igsh=abc123': {'ours': True, 'creator': '@maker', 'hook': 'B'},
                'maker32': {'ours': True, 'creator': '@maker', 'hook': 'C'},
                'brand31': {'ours': True, 'creator': '@maker', 'hook': 'A'},
                'https://vm.tiktok.com/ZMabc/': {'ours': True, 'creator': '@maker', 'hook': 'A'}}
        pay = {'@maker': {'base': 60, 'bonus': [[10000, 100]], 'due': 4}, 'pool': 150}
        for name, blob in (('rows.json', {'data': {'videos': own + brand + ours}}), ('tags.json', tags), ('pay.json', pay)):
            with open(os.path.join(d, name), 'w') as f:
                json.dump(blob, f)
        cls.out = subprocess.run([sys.executable, '-I', COUNT, os.path.join(d, 'rows.json'), '--since', '2026-11-01',
                                  '--tags', os.path.join(d, 'tags.json'), '--pay', os.path.join(d, 'pay.json')],
                                 capture_output=True, text=True, timeout=60).stdout

    def test_a_share_link_before_the_period_still_counts(self):
        self.assertRegex(self.out, r'maker30 on @maker: 12,000 views, 2\.0x the usual of 6,000')
        self.assertIn('usual: 6,000 views, the median of 11 posts', self.out)

    def test_the_pool_caps_the_bonuses_in_posting_order(self):
        self.assertIn('bonus pool $150: the tiers reached add $300, $150 past the pool', self.out)
        self.assertRegex(self.out, r'maker30[^\n]*paid \$160 \(\$60 base \+\$100 at 10,000\)')
        self.assertRegex(self.out, r'maker32[^\n]*paid \$110 \(\$60 base \+\$100 at 10,000 \(only \$50 left in the pool\)\)')
        self.assertRegex(self.out, r'brand31[^\n]*paid \$60 \(\$60 base \+\$100 at 10,000 \(pool spent\)\)')

    def test_a_link_that_matches_no_row_is_named(self):
        self.assertIn('tags that match no row', self.out)
        self.assertIn('ZMabc', self.out)

    def test_hooks_rank_by_beating_the_usual_not_raw_views(self):
        c, b, a = (self.out.index(f'    "{h}":') for h in 'CBA')
        self.assertLess(c, b)
        self.assertLess(b, a)


class AdRule(unittest.TestCase):
    """--ads holds a breakout to the comment rate of the account's posts its size, since that rate falls as views grow.
    On 10 brand accounts (11-12) the old test, the account's plain usual rate, passed 14 breakouts and the new one 32."""

    def rows(self, path):
        rows = []
        for i in range(20):  # 1,000 to 20,000 views, comments per 1,000 falling from about 10 to 2
            v = 1000 * (i + 1)
            rows.append({'id': f'p{i}', 'platform': 'instagram', 'handle': 'brand', 'posted_at': f'2026-10-{i + 1:02d}T12:00:00+00:00',
                         'views': v, 'likes': v // 20, 'comments': round(v * 10 / 1000 * (v / 1000) ** -0.5)})
        last = {'platform': 'instagram', 'handle': 'brand', 'likes': 30000}
        rows.append(dict(last, id='sells', posted_at='2026-11-05T12:00:00+00:00', views=100000, comments=200))  # 2.0 per 1,000
        rows.append(dict(last, id='only-reach', posted_at='2026-11-06T12:00:00+00:00', views=100000, comments=50))  # 0.5 per 1,000
        for r in rows:
            r['counts_as_of'] = '2026-11-12T12:00:00+00:00'
        with open(path, 'w') as f:
            json.dump(rows, f)

    def test_a_breakout_is_judged_against_posts_its_size(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, 'rows.json')
            self.rows(path)
            out = subprocess.run([sys.executable, '-I', COUNT, path, '--since', '2026-11-01', '--ads'],
                                 capture_output=True, text=True, timeout=60).stdout
        line = next(l for l in out.splitlines() if 'turn into an ad' in l)
        self.assertIn('what their posts that size get', line)
        self.assertIn('sells (', line)  # 2.0 per 1,000: under the usual 3.1, above the 1.2 its size gets
        self.assertNotIn('only-reach', line)


if __name__ == '__main__':
    unittest.main()
