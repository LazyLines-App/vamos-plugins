"""The post skill's plan.py: the rules it holds in code. Standard library and ffmpeg only, no network.

    python3 evals/scripts/test_post_plan.py

Each test is a promise the skill makes before anything is sent: the AI label goes on for AI footage, the
disclosure line is in the caption, a real person's likeness is never posted, a platform with no label field
gets AI footage only by hand, the caps hold, and a reposted video is flagged before the yes.
"""
import json, os, shutil, subprocess, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLAN = os.path.join(ROOT, 'plugins', 'vamos', 'skills', 'post', 'scripts', 'plan.py')
NOW = '2026-11-13T10:00:00+01:00'
ACCOUNTS = [{'id': 'x1', 'platform': 'twitter', 'handle': '@brandx'},
            {'id': 'ig1', 'platform': 'instagram', 'handle': '@brand'},
            {'id': 'ig2', 'platform': 'instagram', 'handle': '@brand.two'},
            {'id': 'tt1', 'platform': 'tiktok', 'handle': '@brand.tt'},
            {'id': 'yt1', 'platform': 'youtube', 'handle': '@brandyt'},
            {'id': 'fb1', 'platform': 'facebook', 'handle': 'Brand Page'}]


N = iter(range(1, 10 ** 6))


def clip(path, colour=None, size='1080x1920'):
    """A 1 s clip; each one gets its own colour, so no two files are the same video."""
    colour = colour or f'0x{next(N) * 2654435761 % 0xFFFFFF:06x}'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=c={colour}:s={size}:d=1', '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p', path], check=True)


class Plan(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir)

    def run_plan(self, posts, sheets, **extra):
        for name, sheet in sheets.items():
            if not os.path.exists(os.path.join(self.dir, name)):
                clip(os.path.join(self.dir, name))
            if sheet is not None:
                json.dump(sheet, open(os.path.join(self.dir, os.path.splitext(name)[0] + '.post.json'), 'w'))
        batch = {'timezone': 'Europe/Madrid', 'now': NOW, 'times': ['09:00', '13:00', '19:00'],
                 'accounts': ACCOUNTS, 'posts': posts, **extra}
        bp = os.path.join(self.dir, 'batch.json')
        json.dump(batch, open(bp, 'w'))
        out = os.path.join(self.dir, 'plan.json')
        r = subprocess.run([sys.executable, PLAN, bp, '--out', out], capture_output=True, text=True)
        return r, json.load(open(out)) if os.path.exists(out) else None

    def test_ai_label_on_every_platform_that_takes_it(self):
        r, plan = self.run_plan([{'file': 'a.mp4', 'to': ['ig1', 'tt1', 'yt1']}],
                                {'a.mp4': {'caption': 'Our drama ad', 'ai': True, 'people': 'made', 'promotes': 'own'}})
        self.assertEqual(r.returncode, 0, r.stdout)
        ig, tt, yt = plan['rows']
        self.assertIs(ig['create']['arguments']['platforms'][0]['platformSpecificData']['isAiGenerated'], True)
        self.assertIs(tt['create']['arguments']['tiktok_settings']['videoMadeWithAi'], True)
        self.assertEqual(tt['create']['arguments']['tiktok_settings']['commercialContentType'], 'brand_organic')
        self.assertIs(yt['create']['arguments']['platforms'][0]['platformSpecificData']['containsSyntheticMedia'], True)
        for row in plan['rows']:
            self.assertIn('Made with AI.', row['create']['arguments']['content'])   # the disclosure line, added
            self.assertNotIn('publish_now', row['create']['arguments'])

    def test_label_off_for_filmed_footage(self):
        r, plan = self.run_plan([{'file': 'b.mp4', 'to': ['ig1']}],
                                {'b.mp4': {'caption': 'Filmed it myself', 'ai': False, 'people': 'filmed'}})
        self.assertEqual(r.returncode, 0, r.stdout)
        args = plan['rows'][0]['create']['arguments']
        self.assertIs(args['platforms'][0]['platformSpecificData']['isAiGenerated'], False)
        self.assertEqual(args['content'], 'Filmed it myself')

    def test_likeness_is_never_posted(self):
        r, plan = self.run_plan([{'file': 'c.mp4', 'to': ['ig1']}],
                                {'c.mp4': {'caption': 'x', 'ai': True, 'people': 'likeness'}})
        self.assertEqual(r.returncode, 1)
        self.assertIn('never posted', r.stdout)
        self.assertEqual(plan['rows'], [])

    def test_missing_ai_answer_blocks(self):
        r, _ = self.run_plan([{'file': 'd.mp4', 'to': ['ig1']}], {'d.mp4': {'caption': 'x', 'people': 'none'}})
        self.assertEqual(r.returncode, 1)
        self.assertIn('lacks ai', r.stdout)

    def test_no_sheet_blocks(self):
        r, _ = self.run_plan([{'file': 'e.mp4', 'to': ['ig1']}], {'e.mp4': None})
        self.assertEqual(r.returncode, 1)
        self.assertIn('no post sheet', r.stdout)

    def test_facebook_ai_goes_by_hand(self):
        r, plan = self.run_plan([{'file': 'f.mp4', 'to': ['fb1']}],
                                {'f.mp4': {'caption': 'x', 'ai': True, 'people': 'made'}})
        self.assertEqual(r.returncode, 0, r.stdout)
        row = plan['rows'][0]
        self.assertTrue(row['how'].startswith('by hand'))
        self.assertNotIn('create', row)

    def test_slots_fill_in_order_after_now(self):
        r, plan = self.run_plan([{'file': f'g{i}.mp4', 'to': ['ig1']} for i in range(4)],
                                {f'g{i}.mp4': {'caption': f'post {i}', 'ai': False, 'people': 'none'} for i in range(4)})
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual([x['at'][:16] for x in plan['rows']],
                         ['2026-11-13T13:00', '2026-11-13T19:00', '2026-11-14T09:00', '2026-11-14T13:00'])

    def test_tiktok_cap_moves_the_sixteenth_to_the_next_day(self):
        times = [f'{h:02d}:00' for h in range(6, 24)]
        r, plan = self.run_plan([{'file': f'h{i}.mp4', 'to': ['tt1']} for i in range(16)],
                                {f'h{i}.mp4': {'caption': f'p{i}', 'ai': False, 'people': 'none'} for i in range(16)},
                                start='2026-11-14', times=times)
        self.assertEqual(r.returncode, 0, r.stdout)
        days = [x['at'][:10] for x in plan['rows']]
        self.assertEqual(days.count('2026-11-14'), 15)
        self.assertEqual(days[-1], '2026-11-15')
        self.assertEqual(plan['rows'][-1]['at'][11:16], '06:00')   # the window after Sat 06:00 holds 14, so Sun 06:00 fits

    def test_fixed_time_over_the_cap_blocks(self):
        existing = [{'account': 'tt1', 'at': f'2026-11-14T{h:02d}:00:00+01:00'} for h in range(6, 21)]
        r, _ = self.run_plan([{'file': 'i.mp4', 'to': ['tt1'], 'at': '2026-11-14T22:00'}],
                             {'i.mp4': {'caption': 'x', 'ai': False, 'people': 'none'}}, existing=existing)
        self.assertEqual(r.returncode, 1)
        self.assertIn('15 posts in 24 hours', r.stdout)

    def test_same_video_on_two_accounts_of_one_platform_is_flagged(self):
        r, _ = self.run_plan([{'file': 'j.mp4', 'to': ['ig1', 'ig2', 'tt1']}],
                             {'j.mp4': {'caption': 'x', 'ai': False, 'people': 'none'}})
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn('FLAG', r.stdout)
        self.assertIn('2 instagram accounts', r.stdout)
        self.assertNotIn('tiktok accounts', r.stdout)

    def test_partner_gets_ad_and_the_label(self):
        r, plan = self.run_plan([{'file': 'k.mp4', 'to': ['ig1', 'tt1']}],
                                {'k.mp4': {'caption': 'Loving this serum', 'ai': False, 'people': 'filmed',
                                           'promotes': 'partner', 'partner': '@serumco'}})
        self.assertEqual(r.returncode, 0, r.stdout)
        ig, tt = plan['rows']
        self.assertIn('#ad', ig['create']['arguments']['content'])
        self.assertEqual(ig['create']['arguments']['platforms'][0]['platformSpecificData']['brandedContentSponsors'], ['serumco'])
        self.assertEqual(tt['create']['arguments']['tiktok_settings']['commercialContentType'], 'brand_content')

    def test_caption_over_the_limit_blocks(self):
        r, _ = self.run_plan([{'file': 'l.mp4', 'to': ['ig1']}],
                             {'l.mp4': {'caption': 'x' * 2300, 'ai': False, 'people': 'none'}})
        self.assertEqual(r.returncode, 1)
        self.assertIn('over instagram', r.stdout)

    def test_not_vertical_is_flagged(self):
        clip(os.path.join(self.dir, 'm.mp4'), 'red', '1920x1080')
        r, _ = self.run_plan([{'file': 'm.mp4', 'to': ['ig1']}],
                             {'m.mp4': {'caption': 'x', 'ai': False, 'people': 'none'}})
        self.assertIn('not 9:16', r.stdout)

    def test_urls_replace_the_upload_marker(self):
        self.run_plan([{'file': 'n.mp4', 'to': ['ig1']}], {'n.mp4': {'caption': 'x', 'ai': False, 'people': 'none'}})
        json.dump({'n.mp4': 'https://media.zernio.com/temp/n.mp4'}, open(os.path.join(self.dir, 'urls.json'), 'w'))
        bp, out = os.path.join(self.dir, 'batch.json'), os.path.join(self.dir, 'plan.json')
        r = subprocess.run([sys.executable, PLAN, bp, '--urls', os.path.join(self.dir, 'urls.json'), '--out', out],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        plan = json.load(open(out))
        self.assertEqual(plan['rows'][0]['create']['arguments']['media_items'][0]['url'], 'https://media.zernio.com/temp/n.mp4')
        self.assertEqual(plan['uploads'], [])
        self.assertNotIn('UPLOAD first', r.stdout)

    def test_time_with_an_offset_lands_in_the_batch_zone(self):
        """18:30 UTC is 19:30 in Madrid: the payload and the table say 19:30 (the review's late-hour bug)."""
        r, plan = self.run_plan([{'file': 'o.mp4', 'to': ['ig1'], 'at': '2026-11-15T18:30:00Z'}],
                                {'o.mp4': {'caption': 'x', 'ai': False, 'people': 'none'}})
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(plan['rows'][0]['create']['arguments']['scheduled_for'], '2026-11-15T19:30:00')
        self.assertIn('Sun 15 Nov 19:30', r.stdout)

    def test_same_video_already_on_zernio_is_refused(self):
        """A second "post these" for a video already scheduled on that account (its metadata.vamos_file) is refused."""
        r, plan = self.run_plan([{'file': 'rep.mp4', 'to': ['ig1']}],
                                {'rep.mp4': {'caption': 'x', 'ai': False, 'people': 'none'}},
                                existing=[{'account': 'ig1', 'at': '2026-11-13T13:00:00+01:00', 'file': 'rep.mp4'}])
        self.assertEqual(r.returncode, 1)
        self.assertIn('same video twice on one account', r.stdout)

    def test_agreed_likeness_posts_with_the_label(self):
        """The user's own AI twin (they agreed) posts, labelled, even when the sheet forgot ai."""
        r, plan = self.run_plan([{'file': 'twin.mp4', 'to': ['ig1']}],
                                {'twin.mp4': {'caption': 'My AI twin explains', 'ai': False, 'people': 'agreed'}})
        self.assertEqual(r.returncode, 0, r.stdout)
        args = plan['rows'][0]['create']['arguments']
        self.assertIs(args['platforms'][0]['platformSpecificData']['isAiGenerated'], True)
        self.assertIn('Made with AI.', args['content'])

    def test_standing_yes_sends_tiktok_to_the_inbox(self):
        """With no one looking at the table, TikTok rows go as inbox drafts (no consent claimed), 5 a day at most."""
        posts = [{'file': f'd{i}.mp4', 'to': ['tt1']} for i in range(6)]
        r, plan = self.run_plan(posts, {f'd{i}.mp4': {'caption': 'x', 'ai': True, 'people': 'made'} for i in range(6)},
                                tiktok_drafts=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        tik = plan['rows'][0]['create']['arguments']['tiktok_settings']
        self.assertIs(tik['draft'], True)
        self.assertNotIn('expressConsentGiven', tik)
        self.assertNotIn('dry_run', plan['rows'][0])
        self.assertIn('TikTok inbox', plan['rows'][0]['how'])
        days = {row['at'][:10] for row in plan['rows'][:5]}
        self.assertNotIn(plan['rows'][5]['at'][:10], days)   # the 6th waits for the next day

    def test_x_posts_are_priced(self):
        r, plan = self.run_plan([{'file': 'xx.mp4', 'to': ['x1']}],
                                {'xx.mp4': {'caption': 'x', 'ai': False, 'people': 'none'}})
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn('X bills $0.015', r.stdout)


if __name__ == '__main__':
    unittest.main()
