"""content-log's ads.py on two small Ads Manager exports. Standard library only, no network.

    python3 evals/scripts/test_ads.py

The exports use Meta's real column names (with the currency in the header and a totals row), so a
renamed column or a totals row counted as an ad shows up here first.
"""
import csv, json, os, subprocess, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ADS = os.path.join(ROOT, 'plugins', 'vamos', 'skills', 'content-log', 'scripts', 'ads.py')
HEAD = ['Reporting starts', 'Reporting ends', 'Ad name', 'Amount spent (USD)', 'Purchases', 'Purchases conversion value', 'Impressions', 'Cost per purchase (USD)']


def export(path, rows, label='', start='2026-11-02', end='2026-11-08', head=HEAD):
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(head)
        w.writerow(['', '', label, sum(r[1] for r in rows), sum(r[2] for r in rows), '', '', ''])
        for name, spend, buys, value in rows:
            w.writerow([start, end, name, f'{spend:.2f}', buys, f'{value:.2f}', spend * 100, ''])


class Ads(unittest.TestCase):
    def run_ads(self, *args):
        out = subprocess.run([sys.executable, ADS, *args, '--json'], capture_output=True, text=True, check=True).stdout
        return json.loads(out)

    def test_week(self):
        d = tempfile.mkdtemp()
        now, last, codes = (os.path.join(d, n) for n in ('now.csv', 'last.csv', 'codes.txt'))
        export(now, [('OF_UGC_Switch_v1', 1000, 20, 1800), ('OF_UGC_Switch_v2 WA-1105-2', 500, 5, 400),
                     ('OF_Static_Picky_v1', 300, 10, 900), ('OF_Static_Switch_v3', 200, 4, 300), ('OF_UGC_Picky_v2', 100, 1, 50)],
               label='Total')
        export(last, [('OF_UGC_Switch_v1', 600, 15, 1200), ('OF_Static_Picky_v1', 500, 10, 1000), ('OF_UGC_Picky_v2', 100, 2, 150),
                      ('OF_Static_Price_v1', 900, 9, 700)], start='2026-10-26', end='2026-11-01')
        open(codes, 'w').write('WA-1105-2 WA_1105_4 WA-1105-5')
        r = self.run_ads(now, '--last', last, '--codes', codes)
        self.assertEqual(r['this_week']['ads'], 5)  # the totals row isn't an ad
        self.assertEqual(r['this_week']['spend'], 2100)
        self.assertEqual(r['this_week']['cpa'], 52.5)
        self.assertEqual(r['this_week']['roas'], round(3450 / 2100, 2))
        self.assertEqual(r['top_by_spend'][0]['ad'], 'OF_UGC_Switch_v1')
        self.assertEqual(r['risers'][0]['ad'], 'OF_UGC_Switch_v1')
        self.assertEqual(r['fallers'][0]['ad'], 'OF_Static_Price_v1')  # switched off this week, so it fell most
        self.assertTrue(r['fallers'][0]['stopped'])
        self.assertEqual(r['read']['currency'], 'USD')
        self.assertEqual(r['read']['export_total'], 2100)
        self.assertIn('OF_UGC_Switch_v2 WA-1105-2', r['new_this_week'])
        switch = next(w for w in r['words'] if w['word'] == 'switch')
        self.assertEqual((switch['ads'], switch['spend']), (3, 1700))
        self.assertNotIn('of', [w['word'] for w in r['words']])  # a word on every ad says nothing
        self.assertEqual(list(r['codes_ran']), ['WA-1105-2'])
        self.assertEqual(r['codes_not_found'], ['WA-1105-4', 'WA-1105-5'])

    def test_names_and_codes(self):
        """A real ad named Total stays, an underscore code is found, a place name isn't a code, and a labelled summary row isn't an ad."""
        d = tempfile.mkdtemp()
        now = os.path.join(d, 'now.csv')
        export(now, [('Total Comfort UGC_v1', 1000, 10, 1500), ('Bowl_Static_v1 WA_1105_4', 400, 8, 700), ('Bowl_Video_v2', 300, 3, 200),
                     ('Ottawa_1105_9_Static', 100, 1, 90)],
               label='Results from 4 ads')
        r = self.run_ads(now)
        self.assertEqual((r['this_week']['ads'], r['this_week']['spend']), (4, 1800))  # a word ending in "wa" isn't a code
        self.assertEqual(list(r['codes_ran']), ['WA-1105-4'])

    def test_one_week_per_file(self):
        d = tempfile.mkdtemp()
        p = os.path.join(d, 'two-weeks.csv')
        export(p, [('A_v1', 100, 2, 150), ('B_v1', 50, 1, 60)], start='2026-10-26', end='2026-11-08')
        res = subprocess.run([sys.executable, ADS, p], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn('14 days', res.stderr)

    def test_results_is_not_purchases(self):
        """Ads Manager's default Results column counts clicks or views for other objectives."""
        d = tempfile.mkdtemp()
        p = os.path.join(d, 'results.csv')
        head = ['Reporting starts', 'Reporting ends', 'Ad name', 'Amount spent (GBP)', 'Results', 'Cost per result', 'CPM (cost per 1,000 impressions)', 'Impressions']
        export(p, [('A_v1', 100, 900, 0), ('B_v1', 50, 400, 0)], head=head)
        res = subprocess.run([sys.executable, ADS, p], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn('Purchases', res.stderr)

    def test_missing_columns(self):
        d = tempfile.mkdtemp()
        p = os.path.join(d, 'bad.csv')
        open(p, 'w').write('Campaign,Spend\nA,10\n')
        res = subprocess.run([sys.executable, ADS, p], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn('needs the Ad name', res.stderr)

    def test_no_summary_row(self):
        """A winner that spent what the rest did together stays an ad when the export has no total row."""
        d = tempfile.mkdtemp()
        p = os.path.join(d, 'now.csv')
        with open(p, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(HEAD)
            for name, spend, buys in (('Winner_v1', 500, 10), ('B_v1', 300, 6), ('C_v1', 198, 4)):
                w.writerow(['2026-11-02', '2026-11-08', name, spend, buys, spend * 2, spend * 100, ''])
        r = self.run_ads(p)
        self.assertEqual((r['this_week']['ads'], r['this_week']['spend']), (3, 998))
        self.assertEqual(r['top_by_spend'][0]['ad'], 'Winner_v1')

    def test_daily_rows_comma_decimals_and_no_delivery(self):
        """Daily rows sum per ad, 1.234,56 and 99,50 read as decimals, and an ad that didn't deliver shows as stopped."""
        d = tempfile.mkdtemp()
        now, last = os.path.join(d, 'now.csv'), os.path.join(d, 'last.csv')
        head = ['Reporting starts', 'Reporting ends', 'Ad name', 'Amount spent (EUR)', 'Purchases', 'Purchases conversion value', 'Impressions']
        with open(now, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(head)
            w.writerow(['', '', '', '1.334,06', '13', '', ''])
            w.writerow(['2026-11-02', '2026-11-02', 'A_v1', '1.234,56', '12', '2.000,00', '90000'])
            w.writerow(['2026-11-03', '2026-11-08', 'A_v1', '99,50', '1', '150,00', '8000'])
            w.writerow(['2026-11-02', '2026-11-08', 'B_v1', '0', '0', '0', '0'])
        export(last, [('A_v1', 900, 9, 1500), ('B_v1', 300, 3, 400)], start='2026-10-26', end='2026-11-01')
        r = self.run_ads(now, '--last', last)
        self.assertEqual((r['this_week']['ads'], r['this_week']['spend']), (1, 1334.06))
        self.assertEqual(r['read']['currency'], 'EUR')
        self.assertEqual(r['last_week']['spend'], 1200)
        self.assertEqual(r['read_last']['export_total'], 1200)
        self.assertTrue(next(m for m in r['fallers'] if m['ad'] == 'B_v1')['stopped'])

    def test_leads_account(self):
        """A lead-gen account has Leads, not Purchases: its CPA is cost per lead."""
        d = tempfile.mkdtemp()
        p = os.path.join(d, 'leads.csv')
        head = ['Reporting starts', 'Reporting ends', 'Ad name', 'Amount spent (GBP)', 'Leads', 'Lead value', 'Impressions', 'Cost per lead (GBP)']
        export(p, [('Coach_Webinar_v1', 200, 20, 0), ('Coach_Quiz_v1', 100, 4, 0)], head=head)
        r = self.run_ads(p)
        self.assertEqual((r['read']['counts'], r['this_week']['purchases'], r['this_week']['cpa']), ('leads', 24, 12.5))
        out = subprocess.run([sys.executable, ADS, p], capture_output=True, text=True, check=True).stdout
        self.assertIn('24 leads, cost per lead £12.50', out)

    def test_weeks_in_order(self):
        d = tempfile.mkdtemp()
        now, last = os.path.join(d, 'now.csv'), os.path.join(d, 'last.csv')
        export(now, [('A_v1', 100, 2, 150)], start='2026-10-26', end='2026-11-01')
        export(last, [('A_v1', 100, 2, 150)])
        res = subprocess.run([sys.executable, ADS, now, '--last', last], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn('must end before', res.stderr)


if __name__ == '__main__':
    unittest.main()
