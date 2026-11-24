"""The post skill's plan.py: the rules it holds in code. Standard library and ffmpeg only, no network.

    python3 evals/scripts/test_post_plan.py

Each test is a promise the skill makes before anything is sent: the AI label goes on for AI footage, the
disclosure line is in the caption, a real person's likeness is never posted, a platform with no label field
gets AI footage only by hand, the caps hold, a reposted video is flagged before the yes, and a post that asks for a
comment word gets its keyword rule (or the ask for one) in the same table.
"""
import json, os, shutil, subprocess, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLAN = os.path.join(ROOT, 'plugins', 'vamos', 'skills', 'post', 'scripts', 'plan.py')
NOW = '2026-11-13T10:00:00+01:00'
ACCOUNTS = [{'id': 'x1', 'platform': 'twitter', 'handle': '@brandx', 'profile': 'pr1'},
            {'id': 'ig1', 'platform': 'instagram', 'handle': '@brand', 'profile': 'pr1'},
            {'id': 'ig2', 'platform': 'instagram', 'handle': '@brand.two', 'profile': 'pr1'},
            {'id': 'tt1', 'platform': 'tiktok', 'handle': '@brand.tt', 'profile': 'pr1'},
            {'id': 'yt1', 'platform': 'youtube', 'handle': '@brandyt', 'profile': 'pr1'},
            {'id': 'fb1', 'platform': 'facebook', 'handle': 'Brand Page', 'profile': 'pr1'}]

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

    def test_tiktok_draft_now_goes_now(self):
        """A draft asked for now is sent now, not scheduled for a minute already past."""
        r, plan = self.run_plan([{'file': 'n.mp4', 'to': ['tt1'], 'at': 'now'}],
                                {'n.mp4': {'caption': 'x', 'ai': False, 'people': 'none'}}, tiktok_drafts=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        args = plan['rows'][0]['create']['arguments']
        self.assertIs(args.get('publish_now'), True)
        self.assertNotIn('scheduled_for', args)
        self.assertIs(args['tiktok_settings']['draft'], True)

    def test_x_posts_are_priced(self):
        r, plan = self.run_plan([{'file': 'xx.mp4', 'to': ['x1']}],
                                {'xx.mp4': {'caption': 'x', 'ai': False, 'people': 'none'}})
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn('X bills $0.015', r.stdout)


class KeywordPlan(unittest.TestCase):
    setUp = Plan.setUp
    tearDown = Plan.tearDown
    run_plan = Plan.run_plan

    def keyword_plan(self, caption='Comment GUIDE and I will send it', comment_dm=None,
                     to=None, post_extra=None, sheet_extra=None, **extra):
        post = {'file': 'keyword.mp4', 'to': to or ['ig1']}
        if comment_dm is not None:
            post['comment_dm'] = comment_dm
        post.update(post_extra or {})
        sheet = {'caption': caption, 'ai': False, 'people': 'none', **(sheet_extra or {})}
        return self.run_plan([post], {'keyword.mp4': sheet}, **extra)

    def test_rules_on_instagram_tiktok_and_x(self):
        dm = {'word': 'guide', 'dm': 'Here is the full guide: https://example.com', 'reply': 'Find it in bio',
              'reply_after_dm': 'Sent, check your DMs'}
        r, plan = self.keyword_plan(comment_dm=dm, to=['ig1', 'tt1', 'x1'])
        self.assertEqual(r.returncode, 0, r.stdout)
        ig, tt, x = plan['rows']
        args = ig['dm_rule']['arguments']
        self.assertEqual((args['dm_message'], args['comment_reply'], args['match_mode'], args['post_id'], args['profile_id']),
                         (dm['dm'], dm['reply_after_dm'], 'word', 'POST_ID', 'pr1'))
        self.assertEqual(args['keywords'], ['guide'])
        self.assertEqual(tt['dm_rule']['arguments']['comment_reply'], dm['reply'])
        self.assertNotIn('dm_message', tt['dm_rule']['arguments'])
        self.assertNotIn('dm_rule', x)
        self.assertIn('twitter can\'t answer', r.stdout)
        self.assertIn('KEYWORD keyword.mp4:', r.stdout)
        self.assertIn(dm['dm'], r.stdout)
        self.assertIn('2 keyword rule(s)', r.stdout)

    def test_ask_holds_its_rows_and_plans_the_rest(self):
        r, plan = self.run_plan([{'file': 'k.mp4', 'to': ['ig1', 'tt1']}, {'file': 'o.mp4', 'to': ['ig1']}],
                                {'k.mp4': {'caption': 'Comment GUIDE and I will send it', 'ai': False, 'people': 'none'},
                                 'o.mp4': {'caption': 'Another one', 'ai': False, 'people': 'none'}})
        self.assertEqual(r.returncode, 0, r.stdout)   # a question for the user, not a fault in the plan
        self.assertIn('ASK    k.mp4: the caption asks people to comment GUIDE', r.stdout)
        waiting, waiting_tt, other = plan['rows']
        for row in (waiting, waiting_tt):
            self.assertIn('validate', row)             # still checked with Zernio before the yes
            self.assertNotIn('create', row)            # never sent before the answer
            self.assertNotIn('dry_run', row)
            self.assertTrue(row['how'].startswith('waits'))
        self.assertIn('create', other)
        self.assertIn('2 waiting for an answer', r.stdout)

    def test_none_is_an_explicit_answer(self):
        r, plan = self.keyword_plan(comment_dm='none')
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertNotIn('dm_rule', plan['rows'][0])

    def test_batch_wins_over_sheet(self):
        r, plan = self.keyword_plan(comment_dm={'word': 'BATCH', 'dm': 'batch'},
                                    sheet_extra={'comment_dm': {'word': 'SHEET', 'dm': 'sheet'}})
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(plan['rows'][0]['dm_rule']['arguments']['keywords'], ['BATCH'])

    def test_not_asks(self):
        for caption in ["Comment below what you'd add", 'comment your thoughts', 'Tell me in the comments', 'COMMENT BELOW']:
            with self.subTest(caption=caption):
                r, _ = self.keyword_plan(caption=caption)
                self.assertEqual(r.returncode, 0, r.stdout)
                self.assertNotIn('ASK', r.stdout)

    def test_asks(self):
        for caption, word in [('comment "guide"', 'GUIDE'), ('Comment the word HOOKS', 'HOOKS'),
                              ('Drop RIP in the comments', 'RIP'), ('type “template” below', 'TEMPLATE')]:
            with self.subTest(caption=caption):
                r, _ = self.keyword_plan(caption=caption)
                self.assertIn(f'ASK    keyword.mp4: the caption asks people to comment {word}', r.stdout)

    def test_missing_reply_flags_tiktok_only(self):
        r, plan = self.keyword_plan(comment_dm={'word': 'GUIDE', 'dm': 'Here', 'reply_after_dm': 'Sent'}, to=['ig1', 'tt1'])
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn('dm_rule', plan['rows'][0])
        self.assertNotIn('dm_rule', plan['rows'][1])
        self.assertIn("tiktok can't DM", r.stdout)

    def test_instagram_reply_only_after_dm_when_given(self):
        r, plan = self.keyword_plan(comment_dm={'word': 'GUIDE', 'dm': 'Here', 'reply': 'In my bio'}, to=['ig1'])
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertNotIn('comment_reply', plan['rows'][0]['dm_rule']['arguments'])   # reply is for platforms with no DM

    def test_missing_dm_is_a_defect(self):
        r, plan = self.keyword_plan(comment_dm={'word': 'GUIDE'})
        self.assertEqual(r.returncode, 1)
        self.assertIn("needs the DM's words", r.stdout)
        self.assertNotIn('dm_rule', plan['rows'][0])

    def test_long_dm_is_a_defect(self):
        r, plan = self.keyword_plan(comment_dm={'word': 'GUIDE', 'dm': 'x' * 1001})
        self.assertEqual(r.returncode, 1)
        self.assertIn("DM is 1001 characters, over Zernio's 1000", r.stdout)
        self.assertNotIn('dm_rule', plan['rows'][0])

    def test_missing_profile_is_a_defect(self):
        account = {'id': 'nop', 'platform': 'instagram', 'handle': '@nop'}
        r, plan = self.keyword_plan(comment_dm={'word': 'GUIDE', 'dm': 'Here'}, to=['nop'], accounts=[account])
        self.assertEqual(r.returncode, 1)
        self.assertIn("@nop: the keyword rule needs the account's profile id", r.stdout)
        self.assertNotIn('dm_rule', plan['rows'][0])

    def test_tiktok_draft_has_no_rule(self):
        r, plan = self.keyword_plan(comment_dm={'word': 'GUIDE', 'dm': 'Here', 'reply': 'Here'},
                                    to=['tt1'], tiktok_drafts=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertNotIn('dm_rule', plan['rows'][0])
        self.assertIn('TikTok inbox draft is posted by you', r.stdout)

    def test_facebook_ai_posted_by_hand_has_no_keyword_flag(self):
        r, plan = self.keyword_plan(comment_dm={'word': 'GUIDE', 'dm': 'Here'}, to=['fb1'],
                                    sheet_extra={'ai': True, 'people': 'made'})
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertTrue(plan['rows'][0]['how'].startswith('by hand'))
        self.assertNotIn('dm_rule', plan['rows'][0])
        self.assertNotIn('FLAG', r.stdout)

    def test_existing_row_has_no_keyword_fields(self):
        r, plan = self.keyword_plan(caption='A regular post')
        self.assertEqual(r.returncode, 0, r.stdout)
        for key in ('dm_rule', 'keyword', 'answer'):
            self.assertNotIn(key, plan['rows'][0])


if __name__ == '__main__':
    unittest.main()
