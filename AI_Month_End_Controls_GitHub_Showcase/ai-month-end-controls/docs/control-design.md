# Control design — demonstration rules

## Data contract
Two inputs: an approval journal (expectations) and a booked-expense overview (observed postings). Neither is intrinsically error-free. Invoice number, period, account, org unit, project, amounts, currency and event type have different meanings and must not be conflated.

## Decision matrix
| Condition | Outcome | Why |
|---|---|---|
| Approved and complete, no corresponding booking | Add provision — subject to human validation | Potential missing cost |
| Missing approval amount/date/account | Check first | Source quality must be fixed first |
| Approved amount exceeds booked amount by >= EUR 400 | Check first | Partial booking or journal typo possible |
| Invoice booked to another expense account | Reclass | Avoid double-counting a supposed missing invoice |
| Wrong cost center or project | Reclass | Allocation differs from approval record |
| Posting to shared-services center | For info | May be a legitimate cross-team booking |
| Candidate duplicate posted + accrual | Please check | Requires inspection; not proof of duplication |
| Credit note in missing test | Exclude | Not comparable to ordinary positive accrual |
| Prior-period accrual reversal | Exclude from new-posting reclass | Not a new cost |
| Balance-sheet posting with blank cost center | Exclude from expense center test | Normal behavior can differ |

All account numbers, thresholds, cost center names and invoice references in this table are fictional design choices.

## Date examples
For `09.2026`, the fictional review cutoff is `2026-10-07`. A September approval dated `2026-10-08` is deferred; an August service invoice first approved on `2026-09-02` is considered; an August invoice approved in August is not included in this period's carryover window.

## Currency
The synthetic case includes a missing GBP 600 approval and another GBP invoice booked at GBP 500 → EUR 590, creating an illustrative estimated rate of 1.18 and missing value of EUR 708. This estimation does not equal a bank FX settlement or a verified transaction booked in an ERP.

## Limitation of the Python reference
The reference engine treats a mismatch on a booked account as a reclass and does not add an additional provision for the same invoice. It does not implement complex invoice-reference suffix parsing, many-to-many invoice allocation, reversals against originating accruals, journal row corrections or accounting configuration validation.
