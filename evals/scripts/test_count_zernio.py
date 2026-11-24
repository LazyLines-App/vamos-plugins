"""content-log's count.py on Zernio's answers: the user's own numbers, merged with Vamos's rows. Standard library only, no network.

    python3 evals/scripts/test_count_zernio.py

The analytics and follower answers are the content-log-zernio-numbers case's mocks (real readings of two of our
accounts, renamed; the follower series is derived), and its Vamos poll holds the same posts as public rows, so a merge
that counts a post twice or lets the rows win shows up here. Small single-post and YouTube answers sit in fixtures/zernio/.
"""
import json, os, subprocess, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COUNT = os.path.join(ROOT, 'plugins', 'vamos', 'skills', 'content-log', 'scripts', 'count.py')
CASE = os.path.join(ROOT, 'plugins', 'vamos', 'evals', 'content-log-zernio-numbers', 'mocks')
ZERNIO = os.path.join(CASE, 'zernio', 'fixtures', 'analytics_get_analytics.json')
FOLLOWERS = os.path.join(CASE, 'zernio', 'fixtures', 'accounts_get_follower_stats.json')
POLL = os.path.join(CASE, 'vamos', 'chat_completion_poll.md')
FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'zernio')


def run(*args):
    return subprocess.run([sys.executable, '-I', COUNT, *args], capture_output=True, text=True, timeout=60)


class Zernio(unittest.TestCase):
    def test_numbers_and_merge(self):
        for sources in ((ZERNIO,), (POLL, ZERNIO), (ZERNIO, POLL), (ZERNIO, ZERNIO)):
            p = run(*sources, '--since', '2026-11-09')
            self.assertEqual(p.returncode, 0, p.stderr)
            for text in ('numbers: 25 posts from Zernio, 0 from Vamos', '19 posts read', '6 posts read',
                         'median: 158 views, over 9 posts', 'median: 269 views, over 5 posts', '1,815 views, 6.7x outlier',
                         'reach 1,672, saves 8, shares 0, follows 2', '40% at 3 s', 'the biggest drop 0 to 1 s (25 points)',
                         'watched 6.7 s on average (of 50 s)', '1.2% watched to the end', '56.9% skipped in the first 3 s',
                         'saves and shares per 1,000 views: median'):
                self.assertIn(text, p.stdout, sources)

    def test_rows_alone_count_the_same(self):
        # Vamos's public rows of the same posts give the same medians: the merge changes where numbers come from, not the rule
        p = run(POLL, '--since', '2026-11-09')
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('median: 158 views, over 9 posts', p.stdout)
        self.assertNotIn('from Zernio', p.stdout)

    def test_paid_and_failed_entries(self):
        with open(ZERNIO, encoding='utf-8') as f:
            blob = json.load(f)
        hit = next(x for x in blob['posts'] if x['analytics']['views'] == 1815)
        hit['isAd'] = True
        late = next(x for x in blob['posts'] if x['analytics']['views'] == 167)
        late['platforms'][0]['status'] = 'failed'
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
            json.dump(blob, f)
        try:
            p = run(f.name, '--since', '2026-11-09')
        finally:
            os.unlink(f.name)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('1,815 views, paid delivery (Zernio)', p.stdout)
        self.assertIn('18 posts read', p.stdout)

    def test_vamos_fields_survive_the_merge(self):
        # Zernio has no paid-partnership tag and can leave the length null: the merged row keeps Vamos's
        with open(POLL, encoding='utf-8') as f:
            poll = json.load(f)
        next(r for r in poll['data']['videos'] if r['views'] == 293)['paid_partnership'] = True
        with open(ZERNIO, encoding='utf-8') as f:
            blob = json.load(f)
        next(x for x in blob['posts'] if x['analytics']['views'] == 1815)['analytics']['videoDurationSeconds'] = None
        paths = []
        for data in (poll, blob):
            with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
                json.dump(data, f)
            paths.append(f.name)
        try:
            p = run(*paths, '--since', '2026-11-09')
        finally:
            for path in paths:
                os.unlink(path)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('293 views, tagged paid', p.stdout)
        self.assertIn('median: 196 views, over 4 posts', p.stdout)
        self.assertIn('watched 6.7 s on average (of 50 s)', p.stdout)

    def test_quiet_poll(self):
        # a Vamos answer with no rows is a quiet period, not an unknown file, and Zernio's answers after it still count
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
            json.dump({'runId': 'r', 'chatId': 'c', 'status': 'done', 'result': 'Nothing was posted.'}, f)
        try:
            alone = run(f.name, '--since', '2026-11-09')
            with_zernio = run(f.name, ZERNIO, '--since', '2026-11-09')
        finally:
            os.unlink(f.name)
        self.assertNotEqual(alone.returncode, 0)
        self.assertIn('no rows with views and a date', alone.stderr)
        self.assertEqual(with_zernio.returncode, 0, with_zernio.stderr)
        self.assertIn('19 posts read', with_zernio.stdout)

    def test_single_post_and_youtube(self):
        p = run(os.path.join(FIX, 'single-post-saved.json'), '--since', '2026-11-01')
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('on TikTok, 1 posts read', p.stdout)
        p = run(os.path.join(FIX, 'youtube-analytics.json'), os.path.join(FIX, 'youtube-retention.json'), '--since', '2026-05-01')
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('1.70 at the start, 0.85 at half, 0.40 at the end', p.stdout)
        self.assertIn('0.61 against videos its length', p.stdout)

    def test_followers(self):
        p = run(ZERNIO, FOLLOWERS, '--since', '2026-11-09')
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('@vamos.demo on TikTok: 205 on 2026-11-09, 261 on 2026-11-24: +56 (+27.3%); the 15 days before: +7 (198 on 2026-10-25)', p.stdout)
        self.assertIn('@vamos.demo on Instagram: 1,187 on 2026-11-09, 1,196 on 2026-11-24: +9 (+0.8%)', p.stdout)

    def test_unknown_source_and_stdin_once(self):
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
            json.dump({'not': 'recognised'}, f)
        try:
            p = run(f.name)
        finally:
            os.unlink(f.name)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('unrecognised source:', p.stderr)
        self.assertNotIn('Traceback', p.stderr)
        self.assertNotEqual(run('-', '-').returncode, 0)


if __name__ == '__main__':
    unittest.main()
