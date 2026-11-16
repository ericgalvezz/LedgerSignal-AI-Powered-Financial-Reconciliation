"""Portable, standard-library validation reference for the FICTIONAL portfolio demo.

This is a newly authored demonstrator, NOT the original workplace Claude Skill.
Run: python -m src.reconcile_demo --month 09.2026 --inputs demo/inputs --output demo/expected
"""
from __future__ import annotations
import argparse, csv, json, re
from collections import defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

D = lambda x: Decimal(str(x))
EXPENSE_ACCOUNTS = {'61110', '61120'}
EXPECTED_CENTER = 'TEAM-OPS'
INFO_CENTER = 'TEAM-TRANSIT'
EURO = Decimal('0.01')

def money(x):
    return D(x).quantize(EURO, rounding=ROUND_HALF_UP)

def parse_amount(text):
    """Return Decimal for examples like '€ 1.250,00' or '£ 600,00'; blank -> None."""
    if text is None or not str(text).strip(): return None
    s = re.sub(r'[^0-9,.-]', '', str(text))
    if ',' in s: s = s.replace('.', '').replace(',', '.')
    try: return money(s)
    except InvalidOperation: return None

def key(s):
    return re.sub(r'\s+', '', str(s or '')).upper()

def month_parts(month):
    mm, yy = (int(p) for p in month.split('.'))
    if not 1 <= mm <= 12: raise ValueError('Month must be MM.YYYY')
    return mm,yy

def prev_month(mm, yy):
    return f'{12 if mm == 1 else mm - 1:02d}.{yy - 1 if mm == 1 else yy}'

def ddate(s): return date.fromisoformat(s)

def load_csv(path):
    with open(path, newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def write_csv(path, rows, cols):
    path.parent.mkdir(parents=True,exist_ok=True)
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(rows)

def resolve_currency(row, ledger_by_inv, fx_rates):
    """Return amount EUR, currency, note. Synthetic demo uses explicit journal symbols."""
    raw = row.get('amount','')
    amt = parse_amount(raw)
    postings=ledger_by_inv.get(key(row['invoice']),[])
    # Ledger currency is trusted when matching a transaction.
    currency = next((x['currency'] for x in postings if x['currency']), None)
    journal_ccy = 'GBP' if '£' in raw else 'USD' if '$' in raw else 'EUR' if '€' in raw else None
    note=''
    if not currency:
        currency=journal_ccy or 'EUR'
        if journal_ccy is None: note='Currency assumed; verify'
    elif journal_ccy and journal_ccy!=currency: note='Currency differs; check'
    if amt is None: return None,currency,note
    if currency=='EUR': return amt, currency, note
    candidate=fx_rates.get(currency)
    if candidate is None: return None,currency,'FX unavailable; check first'
    eur=money(amt*candidate)
    return eur,currency,(note + '; ' if note else '') + 'EUR estimated using observed demo ledger rate'

def review(month, approvals, ledger):
    m,year=month_parts(month)
    cutoff=date(year+1,1,7) if m==12 else date(year,m+1,7)
    m_start=date(year,m,1)
    last=prev_month(m,year)
    valid_types={'posted','new_accrual'}
    current=[r for r in ledger if r['month']==month and r['event_type'] in valid_types and r['account'] in EXPENSE_ACCOUNTS]
    # Reversals and unrelated balance-sheet records are not candidates for classification.
    ledger_by_inv=defaultdict(list)
    for r in current: ledger_by_inv[key(r['invoice'])].append(r)
    rates=defaultdict(list)
    for r in current:
        nat=parse_amount(r['transaction_amount']); eur=parse_amount(r['reporting_eur'])
        if nat and nat>0 and eur is not None and r['currency']!='EUR': rates[r['currency']].append(eur/nat)
    fx_rates={k:sum(v,Decimal(0))/len(v) for k,v in rates.items()}
    # Scope of approvals includes previous service month only when approved since current month began.
    eligible=[]
    for a in approvals:
        if key(a['invoice']).startswith('CN-'): continue
        try: approved=ddate(a['approved_on']) if a['approved_on'] else None
        except ValueError: approved=None
        if approved and approved>cutoff: continue
        if a['month']==month or (a['month']==last and approved and m_start<=approved<=cutoff):
            eligible.append(a)
    by_inv=defaultdict(list)
    for a in eligible: by_inv[key(a['invoice'])].append(a)
    missing=[]
    for a in eligible:
        inv=key(a['invoice'])
        amt,currency,note=resolve_currency(a,ledger_by_inv,fx_rates)
        booked_same=sum((parse_amount(b['reporting_eur']) or Decimal(0)) for b in ledger_by_inv.get(inv,[]) if b['account']==a['account'])
        booked_any=bool(ledger_by_inv.get(inv,[]))
        action=None
        if not a['amount'] or not a['account'] or not a['approved_on']:
            absent=', '.join(s for s,k in [('amount','amount'),('account','account'),('approval date','approved_on')] if not a[k])
            action='Check first';note= ('Missing ' + absent + (('; '+note) if note else ''))
        elif amt is None:
            action='Check first';note=note or 'Unable to convert approved amount'
        elif not booked_any:
            action='Add provision'
        elif any(x['account']!=a['account'] for x in ledger_by_inv.get(inv,[])) and booked_same==0:
            # A mapping error, not another unpaid liability; surfaced in Reclass instead.
            action=None
        elif booked_same==0:
            action='Add provision'
        elif amt-booked_same>=Decimal('400'):
            action='Check first'
            note=f'Approved {amt:.2f} EUR vs booked {booked_same:.2f} EUR; verify'
        if action:
            missing.append({'Supplier':a['vendor'],'Invoice':a['invoice'],'Account':a['account'],
                            'Month':a['month'],'Amount':str(parse_amount(a['amount']) or ''),
                            'Currency':currency,'Amount (EUR)':str(amt or ''),'Action':action,'Note':note})
    missing.sort(key=lambda r: (0 if r['Action']=='Add provision' else 1,r['Invoice'],r['Account']))
    reclass=[]
    for inv,entries in ledger_by_inv.items():
        total=sum((parse_amount(e['reporting_eur']) or Decimal(0)) for e in entries)
        a_rows=by_inv.get(inv,[])
        actual_accounts={e['account'] for e in entries}
        expect_accounts={a['account'] for a in a_rows if a['account']}
        centers={e['cost_center'] for e in entries};projs={e['project'] for e in entries}
        expected_projects={a['project'] for a in a_rows if a['project']}
        expected_center={a['cost_center'] for a in a_rows if a['cost_center']}
        # Movement-oriented cost centers are informative (not automatically erroneous).
        is_info=INFO_CENTER in centers
        findings=[]
        if centers-{EXPECTED_CENTER,INFO_CENTER}: findings.append('Organization mapping differs')
        if expected_projects and projs!=expected_projects: findings.append('Project allocation differs')
        if expect_accounts and actual_accounts!=expect_accounts: findings.append('Expense account differs')
        if any(e['category']=='out_of_scope' for e in entries): findings.append('Expense nature requires reclassification')
        if is_info: typ='For info – shared services';findings.insert(0,'Shared-services center; informational')
        elif findings: typ='Reclass'
        else: continue
        reclass.append({'Type':typ,'Supplier':entries[0]['vendor'],'Invoice':entries[0]['invoice'],
           'Account(s)':' + '.join(sorted(actual_accounts)),'Amount (EUR)':str(money(total)),
           'Currency':entries[0]['currency'],
           'Booked to': ' / '.join(sorted(centers))+' | '+', '.join(sorted(projs)),
           'Expected':(' / '.join(sorted(expected_center))+' | '+', '.join(sorted(expected_projects))) if a_rows else 'Not in approval journal',
           'Finding':'; '.join(dict.fromkeys(findings)),'In approval journal?':'Yes' if a_rows else 'No'})
    reclass.sort(key=lambda r:(0 if r['Type']=='Reclass' else 1,r['Invoice']))
    checks=[]
    for inv,entries in ledger_by_inv.items():
        types={e['event_type'] for e in entries}
        if len(entries)>=2 and 'posted' in types and 'new_accrual' in types:
            # Only flag substantial cases; these are not automatically duplicates in all systems.
            gross=sum((parse_amount(e['reporting_eur']) or Decimal(0)) for e in entries)
            if gross>=1200: checks.append(f'{entries[0]["invoice"]}: posted invoice and new accrual in same month; verify potential double booking')
    checks=checks[:4]
    provision=sum((parse_amount(x['Amount (EUR)']) or Decimal(0)) for x in missing if x['Action']=='Add provision')
    recl_total=sum((parse_amount(x['Amount (EUR)']) or Decimal(0)) for x in reclass if x['Type']=='Reclass')
    info_total=sum((parse_amount(x['Amount (EUR)']) or Decimal(0)) for x in reclass if x['Type']!='Reclass')
    ledger_control=sum((parse_amount(r['reporting_eur']) or Decimal(0)) for r in ledger if r['month']==month)
    summary={'month':month,'deadline':cutoff.isoformat(), 'ledger_control_total_eur':str(money(ledger_control)),
       'provision_total_eur':str(money(provision)),'provision_lines':sum(r['Action']=='Add provision' for r in missing),
       'check_first_lines':sum(r['Action']=='Check first' for r in missing),
       'reclass_total_eur':str(money(recl_total)),'reclass_invoices':sum(r['Type']=='Reclass' for r in reclass),
       'info_total_eur':str(money(info_total)),'info_invoices':sum(r['Type']!='Reclass' for r in reclass),
       'please_check':checks, 'fx_rates_for_demo':{k:str(v.quantize(Decimal('0.0001'))) for k,v in fx_rates.items()}}
    return summary,missing,reclass

def write_results(month,inputs,output):
    summary,missing,reclass=review(month,load_csv(inputs/'approval_journal.csv'),load_csv(inputs/'ledger_overview.csv'))
    output.mkdir(parents=True,exist_ok=True)
    write_csv(output/'missing.csv',missing,['Supplier','Invoice','Account','Month','Amount','Currency','Amount (EUR)','Action','Note'])
    write_csv(output/'reclass.csv',reclass,['Type','Supplier','Invoice','Account(s)','Amount (EUR)','Currency','Booked to','Expected','Finding','In approval journal?'])
    (output/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    lines=[f'Month-end review {month} | period deadline {summary["deadline"]}',
           f'Expense overview source total: EUR {summary["ledger_control_total_eur"]}',
           f'Provisions suggested: EUR {summary["provision_total_eur"]} ({summary["provision_lines"]} rows); check first: {summary["check_first_lines"]}.',
           f'Reclass: EUR {summary["reclass_total_eur"]} ({summary["reclass_invoices"]} invoices).',
           f'For info – shared services: EUR {summary["info_total_eur"]} ({summary["info_invoices"]} invoices).',
           'Please check: '+ (' | '.join(summary['please_check']) if summary['please_check'] else 'none'),
           'Excluded: older approval months, post-cutoff approvals, credit notes and previous accrual reversals.']
    (output/'chat_summary.txt').write_text('\n'.join(lines)+'\n',encoding='utf8')
    reply=[f'Hello team, here is the fictional expense reconciliation feedback for {month}:',
           f'- Proposed accruals: EUR {summary["provision_total_eur"]} ({summary["provision_lines"]} lines).',
           f'- Items to verify: {summary["check_first_lines"]}.',
           f'- Reallocations: EUR {summary["reclass_total_eur"]} ({summary["reclass_invoices"]} invoices).',
           f'- Shared-services items for information: EUR {summary["info_total_eur"]}.',
           'Please check the attached synthetic review before any accounting action.']
    (output/'reply_draft.txt').write_text('\n'.join(reply)+'\n',encoding='utf8')
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--month',default='09.2026');p.add_argument('--inputs',type=Path,default=Path('demo/inputs'));p.add_argument('--output',type=Path,default=Path('demo/expected'))
    a=p.parse_args();print(json.dumps(write_results(a.month,a.inputs,a.output),indent=2,ensure_ascii=False))
