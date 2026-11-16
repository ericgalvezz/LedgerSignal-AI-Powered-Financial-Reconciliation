# Synthetic example data

All entities and numeric values here are made up. `demo/inputs/` contains a fictional approval journal and a ledger overview, both in CSV and Excel form. `demo/expected/` contains the independent demo script's output, a short human-readable summary, an email draft and a sample three-sheet workbook.

To recompute the CSV / JSON outputs:

```bash
python -m src.reconcile_demo --month 09.2026 --inputs demo/inputs --output demo/expected
```

The sample inputs intentionally include incorrect, incomplete and ambiguous entries. They should not be reused for posting any actual accounting entry.
