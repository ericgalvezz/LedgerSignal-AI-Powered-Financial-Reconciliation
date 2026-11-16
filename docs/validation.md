# Validation log — synthetic independent reconstruction

## What was executed
- Generated two fictional CSV inputs and three-sheet Excel examples.
- Ran the independent `src/reconcile_demo.py` engine for `09.2026`.
- Ran `python -m unittest discover -s tests -v`.
- Reviewed generated CSV results and totals for provision / check first / reclass / information-only categories.

## Expected synthetic results
| Check | Expected |
|---|---:|
| Source ledger signed EUR total, including reversal and balance-sheet movement | 7,640.00 |
| Add provision | 2,438.00 / 3 rows |
| Check first | 2 rows |
| Reclass | 1,780.00 / 4 invoices |
| For info | 820.00 / 1 invoice |
| Duplicate-risk human check | 1 |
| FX rate used for GBP sample | 1.1800, estimated |
| Automated Python tests | 14 passed |

## Coverage
The test suite checks totals, counts, missing versus wrong-account distinction, previous-month carryover, post-cutoff exclusion, credit notes, completeness, foreign currency approximation, informational center, reversal exclusion, duplicate-review classification, nonmutation of source inputs, localized amount parsing, period rollover, reference normalization and balance-sheet exception.

## What has **not** been validated
- Whether Claude executes the natural-language Skill with deterministic consistency across model versions.
- Whether the Skill correctly reconciles real financial statements.
- Whether the original private workplace artifact behaves exactly like this reference code.
- Any real company savings, financial exposure, or closed-loop posting rate.

A reviewer must check every suggested action against real source evidence and actual accounting policies if adapting the approach to another organization.
