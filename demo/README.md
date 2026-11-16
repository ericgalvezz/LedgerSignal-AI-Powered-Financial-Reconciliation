# Try LedgerSignal — fictional walkthrough

[Back to the project overview](../README.md)

This demo uses **made-up invoices and financial records**. It illustrates the review experience without including any real company's files or original internal Skill.

## What you will see

Two spreadsheets represent the same month from different perspectives:

- **[Approved invoices](inputs/approval_journal.xlsx):** what the business expects Finance to record.
- **[Recorded expenses](inputs/ledger_overview.xlsx):** what Finance appears to have recorded.

Compare them to see potentially missing items, possible allocation mistakes, and cases where a person should check the data before acting.

**[Open the example results workbook](expected/month_end_review.xlsx)** to see the sample Summary, Missing, and Reclass tabs. All financial amounts in it are invented.

## Option A — Explore the AI-assisted workflow

1. Open the [public example Claude Skill](../skills/month-end-expense-review/SKILL.md) in a compatible Claude Skill environment.
2. Attach `inputs/approval_journal.xlsx` and `inputs/ledger_overview.xlsx`.
3. Ask: **"Run the month-end expense controls review for 09.2026. Flag uncertain cases for human verification."**
4. Review the results and compare them with the [fictional examples](expected/).

The Skill is a **set of AI workflow instructions**, not executable Python code. Claude's output may vary with the model and file tools; matching the reference output is **not guaranteed**.

## Option B — Reproduce the example without AI

From the repository root, with Python 3.10+:

```bash
python -m src.reconcile_demo --month 09.2026 --inputs demo/inputs --output output/demo-run
python -m unittest discover -s tests -v
```

This standalone reference script reads the synthetic CSV inputs and produces `summary.json`, `missing.csv`, `reclass.csv`, `chat_summary.txt`, and `reply_draft.txt` in `output/demo-run/`.

**Note:** the script does not generate the formatted Excel workbook; that is an independently prepared, fictional display example included in `expected/`.

## Want more detail?

Read the [business case](../docs/business-case.md), [review rules](../docs/control-design.md), or [validation notes](../docs/validation.md). No suggested financial action should be treated as a confirmed accounting adjustment without human checking.
