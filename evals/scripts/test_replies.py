"""The post skill's replies.py: which comments still wait for an answer, and the exact replies a yes sends.
Standard library only, no network.

    python3 evals/scripts/test_replies.py

Each test is a promise the skill makes: a comment the user already answered, the keyword DM answers, or an earlier
batch answered is never answered again; the replies sent are the words the table showed, under the right comment
and account; a reply over its platform's length, with a slot left unfilled, or to a comment answered since is
stopped before anything is sent.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = Path(os.environ.get('REPLIES_PY', ROOT / 'plugins/vamos/skills/post/scripts/replies.py'))
FIXTURES = Path(__file__).resolve().parent / 'fixtures/zernio-replies'


class RepliesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)

    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=self.dir, text=True, capture_output=True)

    def save(self, name, obj):
        path = self.dir / name
        path.write_text(json.dumps(obj), encoding='utf-8')
        return path

    def pick(self, *extra):
        return self.run_script('pick', FIXTURES / 'list.json', FIXTURES / 'comments-ig.json',
                               FIXTURES / 'comments-tt.json', '--now', '2026-11-24T16:00:00Z',
                               '--days', '14', '--words', 'GUIDE', '--replied', FIXTURES / 'replied.json', *extra)

    def test_pick_buckets_and_order(self):
        result = self.pick()
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((self.dir / 'waiting.json').read_text())
        self.assertEqual([c['author'] for c in data['comments']], ['noah.k', 'cash.guru.99', 'jess.rivera', 'dana.saves'])
        self.assertEqual([c['n'] for c in data['comments']], [1, 2, 3, 4])
        self.assertEqual(data['set_aside'], dict(own=1, hidden=1, cannot_reply=1, too_old=1, replied_before=1,
                                                 answered=3, unsure=1, keyword=1, no_words=1, ads=1))
        self.assertEqual(len(data['skipped_accounts']), 2)
        self.assertIn('SKIPPED @penny (twitter)', result.stdout)
        self.assertIn('(pinterest)', result.stdout)
        self.assertIn('comments answered in earlier batches', result.stdout)
        self.assertEqual(data['your_replies'], ['thank youuu 🫶 took me 3 tries', 'It does! Connect it under Accounts.',
                                                'Sent, check your DMs', 'Thanks everyone for watching!'])

    def test_folder_duplicate_max_and_replies_dedupe(self):
        duplicate = self.dir / 'duplicate.json'
        duplicate.write_text((FIXTURES / 'comments-tt.json').read_text())
        result = self.run_script('pick', FIXTURES, duplicate, '--now', '2026-11-24T16:00:00Z', '--words', 'GUIDE',
                                 '--replied', FIXTURES / 'replied.json', '--max', '2')
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((self.dir / 'waiting.json').read_text())
        self.assertEqual([c['author'] for c in data['comments']], ['noah.k', 'cash.guru.99'])
        self.assertEqual(data['set_aside']['answered'], 3)
        self.assertEqual(len(data['your_replies']), len(set(data['your_replies'])))
        self.assertIn('MORE 2 more waiting', result.stdout)
        self.assertIn('UNREAD', result.stdout)

    def test_since_sets_aside_older_comments(self):
        result = self.run_script('pick', FIXTURES, '--now', '2027-03-01T00:00:00Z', '--since', '2026-11-22',
                                 '--words', 'GUIDE', '--replied', FIXTURES / 'replied.json')
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((self.dir / 'waiting.json').read_text())
        # --since wins over the 14-day default, so a replay months later reads the same comments.
        self.assertEqual([c['author'] for c in data['comments']], ['noah.k', 'cash.guru.99', 'jess.rivera'])
        self.assertIn('older than 2026-11-22', result.stdout)

    def test_unreadable_time_is_not_too_old(self):
        page = json.loads((FIXTURES / 'comments-tt.json').read_text())
        page['comments'][0]['createdTime'] = '2026-11-22T18:00:00+0000'
        page['comments'][1]['createdTime'] = 'yesterday'
        path = self.save('tt.json', page)
        result = self.run_script('pick', path, '--now', '2026-11-24T16:00:00Z', '--replied', FIXTURES / 'replied.json')
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((self.dir / 'waiting.json').read_text())
        self.assertEqual({c['author'] for c in data['comments']}, {'noah.k', 'cash.guru.99'})
        # No ledger at the default path: pick says so, since an earlier batch's replies would be answered again.
        self.assertIn('no file here, so no earlier batch was counted', self.run_script('pick', path).stdout)

    def test_plan_calls_ask_skip_and_flag(self):
        self.pick()
        drafts = self.save('drafts.json', [{'n': 1, 'reply': ' yes | indeed 📸 '}, {'n': 2, 'skip': 'spam'},
                                           {'n': 3, 'reply': ' YES | INDEED 📸 '}, {'n': 4, 'ask': 'Price?'}])
        result = self.run_script('plan', drafts)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = json.loads((self.dir / 'send.json').read_text())['calls']
        self.assertEqual([c['n'] for c in calls], [1, 3])
        self.assertEqual(calls[0]['arguments'], {'post_id': '7701234567890123456',
                         'account_id': '66b2e19d8c3f5a7e9d0b1c2f', 'comment_id': '7302000000000000001',
                         'message': ' yes | indeed 📸 '})
        self.assertIn('FLAG', result.stdout)
        self.assertIn('ASK #4', result.stdout)
        self.assertIn(r'yes \| indeed', result.stdout)
        # The model may write n as "3" or "#3"; it is still that comment.
        drafts = self.save('drafts.json', [{'n': '1', 'reply': 'snap it'}, {'n': '#3', 'reply': 'rent first'}])
        result = self.run_script('plan', drafts)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual([c['n'] for c in json.loads((self.dir / 'send.json').read_text())['calls']], [1, 3])

    def test_defects_and_limits(self):
        self.pick()
        cases = [[{'n': 99, 'reply': 'x'}], [{'n': 1, 'reply': 'x'}, {'n': 1, 'skip': 'x'}],
                 [{'n': 1}], [{'n': 1, 'reply': 'x', 'skip': 'x'}], [{'n': 1, 'reply': ' '}],
                 [{'n': 1, 'reply': 'x' * 151}], [{'n': 1, 'reply': '[name]'}],
                 [{'n': 1, 'reply': '{{name}}'}], [{'n': 1, 'reply': 'TODO'}], [{'n': 1, 'reply': 'XXX'}]]
        for case in cases:
            with self.subTest(case=case):
                path = self.save('drafts.json', case)
                result = self.run_script('plan', path)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn('DEFECT', result.stdout)
                self.assertFalse((self.dir / 'send.json').exists())
        path = self.save('drafts.json', [{'n': 1, 'reply': 'x' * 150}])
        self.assertEqual(self.run_script('plan', path).returncode, 0)
        (self.dir / 'send.json').unlink()
        waiting = json.loads((self.dir / 'waiting.json').read_text())
        waiting['comments'][0]['platform'] = 'pinterest'
        self.save('waiting.json', waiting)
        self.assertIn('no reply through Zernio on pinterest', self.run_script('plan', path).stdout)
        waiting['comments'][0]['platform'] = 'tiktok'
        self.save('waiting.json', waiting)
        ledger = self.save('ledger.json', [waiting['comments'][0]['comment_id']])
        self.assertEqual(self.run_script('plan', path, '--replied', ledger).returncode, 1)


if __name__ == '__main__':
    unittest.main()
