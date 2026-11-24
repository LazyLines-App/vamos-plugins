"""The post skill's times.py: the user's best times to post, from their own posts and Instagram's followers online.
Standard library only, no network.

    python3 evals/scripts/test_times.py

Each test is a promise the skill makes: a time leads only when its posts beat the posts around them by more than
chance; a time with too few posts, or an account that always posts at one time, is said to be unknown, never ranked;
ads and posts under 7 days old stay out; Meta's followers-online hours land on the user's own clock across both
daylight-saving changes; the proposed times are their own numbers first, then their followers online, then their
usual time, then tests at times their numbers haven't tried.
"""
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = Path(os.environ.get('TIMES_PY', ROOT / 'plugins/vamos/skills/post/scripts/times.py'))
FIXTURES = Path(__file__).resolve().parent / 'fixtures/zernio-best-time'
MAD = ZoneInfo('Europe/Madrid')
NOW = '2026-11-24T18:00:00Z'


def post(n, local, views, account='acc-ig', platform='instagram', handle='brand', ad=False, caption='a post'):
    """One post in Zernio's analytics answer (view summary), published at `local` (a Madrid datetime)."""
    stamp = local.replace(tzinfo=MAD).astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    return {'_id': f'z{account}{n}', 'content': caption, 'publishedAt': stamp, 'status': 'published',
            'analytics': {'views': views, 'likes': views // 50, 'lastUpdated': '2026-11-24T12:00:00Z'},
            'platforms': [{'platform': platform, 'status': 'published', 'platformPostId': f'{account}-{n}',
                           'accountId': account, 'accountUsername': handle,
                           'platformPostUrl': f'https://example.com/{account}/{n}'}],
            'platform': platform, 'isExternal': True, 'isAd': ad}


def answer(posts):
    return {'posts': posts, 'pagination': {'page': 1, 'limit': 100, 'total': len(posts), 'pages': 1},
            'hasAnalyticsAccess': True}


FLAT = lambda h, i: [1000, 1100, 900, 1050][i % 4]   # views that don't depend on the time: each time gets the same mix


def rotation(hours, views, days=80, start=datetime(2026, 8, 1)):
    """A post every 2 days, cycling through local `hours`, each hour's posts getting `views(hour, i)`."""
    out = []
    for i in range(days // 2):
        h = hours[i % len(hours)]
        out.append(post(i, start + timedelta(days=2 * i, hours=h, minutes=12), views(h, i)))
    return out


class TimesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)

    def save(self, name, obj):
        path = self.dir / name
        path.write_text(json.dumps(obj), encoding='utf-8')
        return path

    def run_times(self, *sources, slots=2, tz='Europe/Madrid'):
        out = self.dir / 'times.json'
        r = subprocess.run([sys.executable, str(SCRIPT), *map(str, sources), '--tz', tz, '--slots', str(slots),
                            '--now', NOW, '--out', str(out)], cwd=self.dir, text=True, capture_output=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        result = json.loads(out.read_text())
        for acc in result['accounts']:
            hours = [int(t[:2]) for t in acc['times']]
            self.assertEqual(acc['times'], sorted(acc['times']), 'times are listed by the clock')
            self.assertEqual([s['time'] for s in acc['slots']], acc['times'])
            for a in hours:
                for b in hours:
                    if a != b:
                        self.assertGreaterEqual(min(abs(a - b), 24 - abs(a - b)), 3, 'slots stay 3 hours apart')
        return result, r.stdout

    def account(self, result, ident):
        return next(a for a in result['accounts'] if a['account'] == ident)

    def test_a_time_that_beats_the_posts_around_it_leads(self):
        rnd = random.Random(5)
        posts = rotation([10, 13, 19], lambda h, i: round((3000 if h == 19 else 1000) * rnd.uniform(0.85, 1.15)))
        result, out = self.run_times(self.save('a.json', answer(posts)))
        acc = self.account(result, 'acc-ig')
        self.assertEqual(acc['verdict'], 'lead')
        self.assertLessEqual(acc['chance'], 0.10)
        evening = next(w for w in acc['windows'] if w['window'] == '18:00–21:00')
        self.assertEqual(evening['hour'], 19)
        self.assertGreater(evening['median'], 2.0)
        slot = next(s for s in acc['slots'] if s['time'] == '19:00')
        self.assertEqual(slot['source'], 'posts')
        self.assertEqual(len(acc['times']), 2)
        self.assertIn('TIMES @brand (instagram): ', out)

    def test_gaps_within_chance_lead_nowhere(self):
        posts = rotation([10, 13, 19], FLAT)
        result, _ = self.run_times(self.save('a.json', answer(posts)))
        acc = self.account(result, 'acc-ig')
        self.assertEqual(acc['verdict'], 'no-lead')
        self.assertGreater(acc['chance'], 0.10)
        self.assertFalse([s for s in acc['slots'] if s['source'] == 'posts'], 'no time is sold as best')

    def test_one_posting_time_cannot_be_compared(self):
        posts = [post(i, datetime(2026, 8, 1) + timedelta(days=i, hours=17, minutes=30), 1000 + 10 * i) for i in range(25)]
        posts += [post(100 + i, datetime(2026, 9, 1) + timedelta(days=i, hours=21, minutes=5), 900) for i in range(3)]
        result, out = self.run_times(self.save('a.json', answer(posts)))
        acc = self.account(result, 'acc-ig')
        self.assertEqual(acc['verdict'], 'cant-compare')
        self.assertIsNone(acc['chance'])
        self.assertIn('25 of 28', out)
        self.assertEqual(acc['times'], ['13:00', '17:00'])
        self.assertEqual({s['time']: s['source'] for s in acc['slots']}, {'17:00': 'usual', '13:00': 'test'})

    def test_too_few_posts_get_test_times(self):
        posts = [post(i, datetime(2026, 9, 1) + timedelta(days=3 * i, hours=h), 500) for i, h in enumerate([9, 12, 15, 18, 21, 23])]
        result, _ = self.run_times(self.save('a.json', answer(posts)))
        acc = self.account(result, 'acc-ig')
        self.assertEqual(acc['verdict'], 'too-few')
        self.assertEqual(acc['posts'], 6)
        self.assertEqual(acc['times'], ['13:00', '19:00'])
        self.assertTrue(all(s['source'] == 'test' for s in acc['slots']))

    def test_ads_and_young_posts_stay_out(self):
        posts = rotation([10, 13, 19], FLAT, days=60)
        posts += [post(200 + i, datetime(2026, 9, 2) + timedelta(days=2 * i, hours=19), 90000, ad=True) for i in range(8)]
        posts += [post(300 + i, datetime(2026, 9, 3) + timedelta(days=2 * i, hours=19), 90000, caption='Loving it #ad') for i in range(2)]
        posts += [post(400 + i, datetime(2026, 11, 20) + timedelta(days=i, hours=19), 90000) for i in range(3)]
        result, _ = self.run_times(self.save('a.json', answer(posts)))
        acc = self.account(result, 'acc-ig')
        self.assertEqual(acc['posts'], 30)
        self.assertEqual(acc['set_aside'], 10)
        self.assertNotEqual(acc['verdict'], 'lead', 'boosted and young posts never make a time lead')

    def test_followers_online_lands_on_the_local_clock_across_daylight_saving(self):
        def day(end):
            hours = {str(h): 50 for h in range(24)}
            hours['13'] = 400
            return {'endTime': end, 'hours': hours}
        online = {'success': True, 'accountId': 'acc-ig', 'platform': 'instagram', 'metric': 'online_followers',
                  'days': [day('2026-10-20T07:00:00+0000'), day('2026-11-10T08:00:00+0000')]}
        result, _ = self.run_times(self.save('o.json', online), slots=1)
        acc = self.account(result, 'acc-ig')
        self.assertEqual(acc['online']['days'], 2)
        self.assertEqual(acc['online']['to'], '2026-11-09')
        self.assertEqual(max(acc['online']['by_hour'], key=lambda h: acc['online']['by_hour'][h]), '22')
        self.assertEqual(acc['times'], ['22:00'])
        self.assertEqual(acc['slots'][0]['source'], 'followers')

    def test_under_100_followers_says_so(self):
        online = {'success': True, 'accountId': 'acc-ig', 'platform': 'instagram', 'metric': 'online_followers', 'days': []}
        posts = rotation([10, 13, 19], FLAT)
        result, out = self.run_times(self.save('a.json', answer(posts)), self.save('o.json', online))
        self.assertIsNone(self.account(result, 'acc-ig')['online'])
        self.assertIn('100 followers', out)

    def test_followers_fill_after_a_lead_three_hours_apart(self):
        rnd = random.Random(5)
        posts = rotation([10, 13, 19], lambda h, i: round((3000 if h == 19 else 600) * rnd.uniform(0.9, 1.1)))
        peaks = {20: 500, 21: 480, 18: 460, 14: 380}   # 14:00 is busy (over 2/3 of the peak); the rest are not
        hours = {str(h): peaks.get(h, 40) for h in range(24)}
        # the hours keys are a Pacific day; build them so the peaks land on these Madrid hours (CET, UTC+1)
        start = datetime(2026, 11, 9, 8, tzinfo=timezone.utc)
        keyed = {str(h): hours[str((start + timedelta(hours=h)).astimezone(MAD).hour)] for h in range(24)}
        online = {'success': True, 'accountId': 'acc-ig', 'platform': 'instagram', 'metric': 'online_followers',
                  'days': [{'endTime': '2026-11-10T08:00:00+0000', 'hours': keyed}]}
        result, _ = self.run_times(self.save('a.json', answer(posts)), self.save('o.json', online), slots=3)
        acc = self.account(result, 'acc-ig')
        self.assertEqual(acc['verdict'], 'lead')
        self.assertEqual(acc['slots'][[s['time'] for s in acc['slots']].index('19:00')]['source'], 'posts')
        self.assertIn('14:00', acc['times'])
        self.assertNotIn('20:00', acc['times'])

    def test_each_account_on_its_own_and_a_wrapped_answer_counts_once(self):
        ig = rotation([10, 13, 19], FLAT)
        tt = [post(i, datetime(2026, 9, 1) + timedelta(days=3 * i, hours=20), 700, account='acc-tt', platform='tiktok')
              for i in range(4)]
        blob = answer(ig + tt)
        wrapped = [{'type': 'text', 'text': json.dumps(blob)}]
        result, out = self.run_times(self.save('a.json', blob), self.save('b.json', wrapped))
        self.assertEqual(self.account(result, 'acc-ig')['posts'], 40)
        tiktok = self.account(result, 'acc-tt')
        self.assertEqual((tiktok['platform'], tiktok['handle'], tiktok['posts']), ('tiktok', '@brand', 4))
        self.assertIsNone(tiktok['online'])
        self.assertIn('TIMES @brand (tiktok): ', out)

    def test_the_eval_case_answer_key(self):
        """post-best-time's Zernio answers: real readings of two of our accounts, the followers-online read derived."""
        result, out = self.run_times(FIXTURES / 'analytics_get_analytics.json',
                                     FIXTURES / 'analytics_get_instagram_online_followers.json')
        ig = self.account(result, '6b10a0c0ffee0000000000a1')
        self.assertEqual((ig['posts'], ig['verdict']), (29, 'cant-compare'))
        self.assertIn('23 of 29', out)
        self.assertEqual(ig['times'], ['14:00', '21:00'])
        self.assertTrue(all(s['source'] == 'followers' for s in ig['slots']))
        tt = self.account(result, '6b10a0c0ffee0000000000b2')
        self.assertEqual((tt['posts'], tt['verdict'], tt['times']), (6, 'too-few', ['13:00', '19:00']))

    def test_no_zernio_answer_fails_clearly(self):
        r = subprocess.run([sys.executable, str(SCRIPT), str(self.save('x.json', {'hello': 1})), '--tz', 'UTC'],
                           cwd=self.dir, text=True, capture_output=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('x.json', r.stdout + r.stderr)


if __name__ == '__main__':
    unittest.main()
