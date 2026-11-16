---
name: month-end-expense-review
description: Review two user-attached, fictional month-end finance files to find unbooked approvals, allocation mismatches and human-review items, and present a concise audit-friendly summary.
---

# Month-end expense controls — fictional portfolio demo

## Purpose
You are assisting an analyst with a *review*, not executing an accounting adjustment. For the selected month, answer:
1. Which approved expense lines might be missing from the booked overview?
2. Which current-month bookings could need reassignment, and which need only informational follow-up?

Inputs are sample data for educational demonstration only. Never describe sample values as a company's real financial results.

## Required inputs and boundaries
Ask for the month in `MM.YYYY` and **both attached files**:
- `approval_journal.xlsx` or `approval_journal.csv` with columns: `vendor`, `invoice`, `account`, `cost_center`, `project`, `month`, `approved_on`, `amount`.
- `ledger_overview.xlsx` or `ledger_overview.csv` with columns: `vendor`, `invoice`, `account`, `cost_center`, `project`, `month`, `description`, `currency`, `transaction_amount`, `reporting_eur`, `event_type`, `category`.

Use only the attached data. Do not retrieve records from cloud services. Do not modify inputs or post accounting entries. If either is missing/unreadable, stop and ask for it. Use a new output file.

## Fictional demo mappings
- Operating center: `TEAM-OPS`
- Shared-services center: `TEAM-TRANSIT` — show for information only, not automatically an error
- Expense accounts: `61110` (operational services) and `61120` (administrative fees)
- Example non-expense account: `13880` (balance-sheet) — blank cost center is not automatically a problem
- **These mapping values are invented for this demo. Do not assume they represent a real ledger.**

## Scope and normalization
- Review month `M` and closing cutoff = **7th of the next month** (fictional demo setting).
- Eligible approvals: `month == M` approved by cutoff, plus `month == M-1` approved between 1st of M and cutoff.
- Do not infer a provision for credit notes with invoice prefix `CN-`.
- Exclude previous accrual reversals from new-booking reallocation checks.
- In-scope new bookings are `posted` or `new_accrual` on either expense account during month M.
- Match invoice identifiers case-insensitively after trimming whitespace. If a reference is ambiguous, mark it for human review; do not silently merge invoices.
- Match **invoice + account** for booked versus approved, preserving multi-account invoices.

## Currency
- Where an invoice exists in the ledger, trust ledger `currency` for that invoice.
- Otherwise use the explicit approval-journal amount symbol (`€`, `£`, `$`) when available.
- If there is no reliable currency, flag uncertainty rather than silently assuming a large value.
- For foreign-currency approvals not booked this period, an observed same-currency transaction conversion rate may be used for an **estimated** EUR comparison only. Explicitly say `EUR estimated` and show the source of the estimate. Never call an estimate a booked amount.
- Sum decision totals in EUR only and retain original-currency context.

## Question 1 — approved but not booked
Give each candidate one action:
- `Add provision`: complete, in-scope approved line, no corresponding booked invoice on the required account, and no evidence of the invoice booked on a different in-scope account.
- `Check first`: incomplete approval (date/account/amount), unreliable currency, or ledger amount at least **EUR 400 below** the comparable approved EUR amount (fictional demo threshold).
- When the same invoice is already booked on a different expense account, surface a **Reclass** rather than suggesting both a new provision and a reclass for the same economic item.
- A line is not a confirmed adjustment until the reviewer verifies the source document and Finance agrees.

## Question 2 — booked in the wrong place
Inspect current-month **new** postings on 61110/61120 only; group lines per invoice and preserve account-split details.
- `Reclass`: an operating booking uses another cost center, the project differs from the approval journal, the account mapping differs, or a clearly marked out-of-scope expense was booked to the demo expense accounts.
- `For info – shared services`: booked on `TEAM-TRANSIT`, even if another feature differs; mention the difference in the finding but do not automatically classify it as an error.
- State whether the invoice appears in the approval journal.

## Extra review flags
- Flag suspected duplicate posted-plus-new-accrual patterns at/above **EUR 1,200** for review; do not assert that a duplicate is proven.
- If the approval journal may be wrong (copy/paste error, amount, month, invoice ID, currency or account split), write `Check first`, not a definitive accrual or reclass instruction.
- Do not duplicate the same proposed financial action in different action totals. Info-only values are not added to reclass totals.

## Outputs
Deliver:
1. **Chat summary (max ~8 concise lines):** ledger source total (EUR), deadline applied, suggested provisions (EUR/count), check-first count, reclass (EUR/count), shared-services info (EUR/count), major review flags and excluded period boundary.
2. **Excel workbook with exactly three sheets:**
   - `Summary`: `Topic | EUR | Count | What to do`, with notes on files, cutoff and control total.
   - `Missing`: `Supplier | Invoice | Account | Month | Amount | Currency | Amount (EUR) | Action | Note`. Add a total for `Add provision` only.
   - `Reclass`: `Type | Supplier | Invoice | Account(s) | Amount (EUR) | Currency | Booked to | Expected | Finding | In approval journal?`. Separate informational lines and totals from reclass values.
3. **Short draft email** seeking human validation of the results.

Use professional, plain language and avoid claiming the review is proof of accounting accuracy. Keep source values traceable. Never invent absent financial fields. If unable to create Excel in this Claude environment, provide the three data tables and explicitly disclose that an XLSX file was not generated.

## Quality checklist
Before presenting results, validate that:
- The chosen date cutoff and month scope were applied.
- Approval journal data were not assumed to be correct by default.
- Multi-account invoices do not create artificial duplicates.
- Amount and currency logic are internally consistent.
- A source ledger control total is shown without pretending it is an independent accounting reconciliation.
- `Check first` and informational items are not counted as automatic adjustments.
- Files contain synthetic data only.
