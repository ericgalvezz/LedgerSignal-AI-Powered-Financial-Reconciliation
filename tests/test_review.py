"""End-to-end and edge-case tests against ONLY synthetic demo fixtures."""
import copy
import unittest
from decimal import Decimal
from pathlib import Path
from src.reconcile_demo import load_csv, parse_amount, key, review, prev_month

BASE=Path(__file__).resolve().parents[1]/'demo'/'inputs'

class DemoReviewTests(unittest.TestCase):
    def setUp(self):
        self.ap=load_csv(BASE/'approval_journal.csv')
        self.ledger=load_csv(BASE/'ledger_overview.csv')
        self.summary,self.missing,self.reclass=review('09.2026',self.ap,self.ledger)

    def test_evidence_totals(self):
        self.assertEqual(self.summary['provision_total_eur'],'2438.00')
        self.assertEqual(self.summary['reclass_total_eur'],'1780.00')
        self.assertEqual(self.summary['info_total_eur'],'820.00')
        self.assertEqual(self.summary['ledger_control_total_eur'],'7640.00')

    def test_counts(self):
        self.assertEqual((self.summary['provision_lines'],self.summary['check_first_lines']), (3,2))
        self.assertEqual((self.summary['reclass_invoices'],self.summary['info_invoices']), (4,1))

    def test_controlled_fx_estimate(self):
        row=next(x for x in self.missing if x['Invoice']=='DEMO-102')
        self.assertEqual(row['Currency'],'GBP')
        self.assertEqual(row['Amount (EUR)'],'708.00')
        self.assertIn('estimated',row['Note'])

    def test_account_mismatch_not_double_provision(self):
        self.assertNotIn('DEMO-107',[r['Invoice'] for r in self.missing])
        self.assertEqual(next(x for x in self.reclass if x['Invoice']=='DEMO-107')['Type'],'Reclass')

    def test_approval_cutoff_and_prior_month(self):
        ids={r['Invoice'] for r in self.missing}
        self.assertIn('DEMO-112',ids)
        self.assertNotIn('DEMO-110',ids)
        self.assertNotIn('DEMO-113',ids)
        self.assertNotIn('CN-111',ids)

    def test_source_not_mutated(self):
        a,b=copy.deepcopy(self.ap),copy.deepcopy(self.ledger)
        review('09.2026',self.ap,self.ledger)
        self.assertEqual(self.ap,a);self.assertEqual(self.ledger,b)

    def test_incomplete_approval_does_not_autopost(self):
        r=next(x for x in self.missing if x['Invoice']=='DEMO-104')
        self.assertEqual(r['Action'],'Check first')
        self.assertEqual(r['Amount (EUR)'],'')

    def test_shared_center_is_not_auto_error(self):
        r=next(x for x in self.reclass if x['Invoice']=='DEMO-108')
        self.assertEqual(r['Type'],'For info – shared services')

    def test_reversals_not_reclassed(self):
        self.assertNotIn('DEMO-115',[r['Invoice'] for r in self.reclass])

    def test_possible_double_booking_is_review_not_action(self):
        self.assertTrue(any('DEMO-109' in x for x in self.summary['please_check']))

    def test_european_number_parser(self):
        self.assertEqual(parse_amount('€ 1.250,40'),Decimal('1250.40'))
        self.assertEqual(parse_amount('£ 600,00'),Decimal('600.00'))
        self.assertIsNone(parse_amount(''))

    def test_period_rollover(self):
        self.assertEqual(prev_month(1,2027),'12.2026')

    def test_invoice_ref_whitespace_case_normalization(self):
        self.assertEqual(key(' demo-100\n'),key('DEMO-100'))

    def test_in_scope_balance_sheet_not_mislabeled(self):
        self.assertNotIn('DEMO-116',[r['Invoice'] for r in self.reclass])

if __name__=='__main__': unittest.main()
