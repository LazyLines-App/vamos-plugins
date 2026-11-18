"""Weekly-format consumer checks. Literal fixtures only; no network or model calls."""
import importlib.util
import json
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'plugins/vamos/skills/formats/scripts/price.py'
SPEC = importlib.util.spec_from_file_location('format_price', SCRIPT)
PRICE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PRICE)


def row(**changes):
    result = {'kind': 'format_week', 'format_id': 'f1', 'name': 'Action Label Montage',
              'niche': 'health_fitness', 'niche_role': 'yours', 'week_start': '2026-10-05',
              'weeks': 1, 'posts': 2, 'niche_posts': 40, 'share': 0.05, 'median_views': 200000.5,
              'views_posts': 2, 'median_multiple': 4, 'multiple_posts': 1, 'views_age_days': 4.8,
              'views_basis': 'latest', 'too_new': False}
    result.update(changes)
    return result


def data(*rows):
    return {'schema_version': 1, 'formats': [{'format_id': 'f1', 'name': 'Action Label Montage'}],
            'format_weeks': list(rows)}


class FormatPrice(unittest.TestCase):
    def test_actual_values_and_supporting_counts_are_preserved(self):
        summary = PRICE.summarise(data(row()))
        self.assertEqual(summary['formats'][0]['niches'][0]['weekly'][0], row())
        text = PRICE.to_markdown(summary)
        self.assertIn('median 200,000.5 views', text)
        self.assertIn('N=2', text)
        self.assertIn('median 4×', text)
        self.assertIn('N=1', text)

    def test_missing_optional_field_keeps_the_old_result(self):
        summary = PRICE.summarise({'schema_version': 1, 'formats': []})
        self.assertEqual(summary, {'formats': [], 'warnings': []})
        self.assertEqual(PRICE.to_markdown(summary), '')

    def test_only_named_formats_can_acquire_measurements(self):
        summary = PRICE.summarise(data(row(format_id='another-format')))
        self.assertEqual(summary['formats'], [])

    def test_uncited_turn_rows_do_not_become_a_recommendation(self):
        source = data(row())
        source['formats'][0]['cited'] = False
        self.assertEqual(PRICE.summarise(source)['formats'], [])

    def test_selected_ids_leave_other_cards_out(self):
        self.assertEqual(PRICE.summarise(data(row()), {'f2'})['formats'], [])

    def test_a_measured_zero_stays_zero(self):
        zero = row(posts=1, median_views=0, views_posts=1, median_multiple=0, multiple_posts=1)
        weekly = PRICE.summarise(data(zero))['formats'][0]['niches'][0]['weekly'][0]
        self.assertEqual(weekly['median_views'], 0)
        self.assertIn('0 views, N=1', PRICE.to_markdown(PRICE.summarise(data(zero))))

    def test_new_weeks_keep_their_post_count_but_no_price(self):
        new = row(week_start='2026-11-16', posts=7, too_new=True, median_views=None,
                  views_posts=0, median_multiple=None, multiple_posts=0, views_age_days=None)
        text = PRICE.to_markdown(PRICE.summarise(data(new)))
        self.assertIn('too new', text)
        self.assertIn('7', text)
        self.assertNotIn('0 views', text)

    def test_empty_week_is_not_a_zero_view_measurement(self):
        empty = row(posts=0, median_views=None, views_posts=0, median_multiple=None,
                    multiple_posts=0, views_age_days=None, share=0)
        text = PRICE.to_markdown(PRICE.summarise(data(empty)))
        self.assertIn('not measured', text)
        self.assertNotIn('0 views', text)

    def test_pooled_row_keeps_six_readable_weeks_and_its_own_median(self):
        pooled = row(week_start=None, weeks=6, posts=148, niche_posts=2010, share=0.073632,
                     median_views=217166.5, views_posts=148, median_multiple=7.25, multiple_posts=140)
        text = PRICE.to_markdown(PRICE.summarise(data(row(), pooled)))
        self.assertIn('6 readable weeks', text)
        self.assertIn('217,166.5', text)
        self.assertNotIn('8 readable weeks', text)
        self.assertIn('posts were a median 4.8 days old', text)
        self.assertNotIn('4.8 days ago', text)

    def test_missing_middle_week_is_a_chart_gap(self):
        summary = PRICE.summarise(data(row(), row(week_start='2026-10-19', median_views=400000)))
        text = PRICE.to_markdown(summary)
        self.assertIn('2026-10-12', text)
        self.assertIn('·', text)
        self.assertIn('not supplied', text)

    def test_malformed_boolean_and_nonfinite_numbers_are_rejected(self):
        for broken in [row(posts=True), row(median_views=float('nan')), row(week_start='not-a-date'),
                       row(views_basis='seven_days'), row(niche_role='guessed'), row(too_new='false')]:
            summary = PRICE.summarise(data(broken))
            self.assertEqual(summary['formats'], [])
            self.assertTrue(summary['warnings'])

    def test_duplicate_week_does_not_double_count_or_pick_a_winner(self):
        summary = PRICE.summarise(data(row(), row(median_views=999)))
        self.assertEqual(summary['formats'], [])
        self.assertTrue(summary['warnings'])

    def test_niches_stay_separate_and_are_library_counts(self):
        summary = PRICE.summarise(data(row(), row(niche='sports', niche_role='next_door', posts=3)))
        text = PRICE.to_markdown(summary)
        self.assertEqual(len(summary['formats'][0]['niches']), 2)
        self.assertIn('Library posts', text)
        self.assertIn('next door', text)
        self.assertIn('latest stored', text)

    def test_cli_handles_inline_poll_rows_and_json_output(self):
        run = subprocess.run([sys.executable, str(SCRIPT), '-', '--json'],
                             input=json.dumps({'data': data(row())}), capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)['formats'][0]['format_id'], 'f1')

    def test_cli_bad_input_is_bounded_and_has_no_traceback(self):
        run = subprocess.run([sys.executable, str(SCRIPT), '-'], input='not json', capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertNotIn('Traceback', run.stderr)

    def test_compact_output_retains_chart_and_pooled_values_without_the_large_table(self):
        summary = PRICE.summarise(data(row(), row(week_start='2026-10-19')))
        text = PRICE.to_markdown(summary, compact=True)
        self.assertIn('█·█', text)
        self.assertNotIn('| Published week |', text)
        self.assertIn('2026-10-12: not supplied.', text)
        self.assertIn('200,000.5 views, N=2', text)
        self.assertIn('2/40 library posts', text)
        self.assertIn('post age 4.8d', text)
        self.assertIn('4×, N=1', text)

    def test_compact_current_week_supply_is_not_hidden_by_pooled_summary(self):
        pooled = row(week_start=None, weeks=6, posts=148, niche_posts=2010,
                     median_views=217166.5, views_posts=148, multiple_posts=140)
        for posts in (7, 700):
            current = row(week_start='2026-11-16', posts=posts, niche_posts=1000,
                          too_new=True, median_views=None, views_posts=0,
                          median_multiple=None, multiple_posts=0, views_age_days=None)
            text = PRICE.to_markdown(PRICE.summarise(data(pooled, current)), compact=True)
            self.assertIn(f'{posts}/1,000 library posts; too new', text)
            self.assertIn('217,166.5 views, N=148', text)

    def test_zero_support_cannot_supply_a_measurement(self):
        for broken in (row(posts=0, views_posts=0, multiple_posts=0, median_views=0),
                       row(views_posts=0), row(multiple_posts=0)):
            summary = PRICE.summarise(data(broken))
            self.assertEqual(summary['formats'], [])
            self.assertTrue(summary['warnings'])

    def test_production_export_keeps_all_135_rows_and_source_medians(self):
        source = json.loads((ROOT / 'evals/scripts/fixtures/format-weeks-production.json').read_text())
        summary = PRICE.summarise(source)
        self.assertEqual(summary['warnings'], [])
        rows = [row for item in summary['formats'] for niche in item['niches']
                for row in [niche['summary'], *niche['weekly']] if row is not None]
        self.assertEqual(len(rows), 135)
        yours = next(n for f in summary['formats'] if f['name'] == 'This Vs That'
                     for n in f['niches'] if n['role'] == 'yours')['summary']
        self.assertEqual((yours['weeks'], yours['posts'], yours['median_views'], yours['views_posts']),
                         (6, 27, 293166, 27))
        empty = next(n for f in summary['formats'] if f['name'] == 'Meme Cut'
                     for n in f['niches'] if n['role'] == 'yours')['summary']
        self.assertEqual((empty['posts'], empty['median_views'], empty['views_posts']), (0, None, 0))

    def test_boolean_schema_version_is_not_the_number_one(self):
        source = data(row())
        source['schema_version'] = True
        with self.assertRaises(ValueError):
            PRICE.summarise(source)


if __name__ == '__main__':
    unittest.main()
