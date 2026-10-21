# Phase 166 R3-AU-2: Generator ID Join Audit

Read-only comparison of every row in `data/sphere.csv` (fallback `sphere(3).csv`) and `HyoujiGen.csv`. Records `Element` identifier resolution, `gen_coe` shape, base display / LaTeX metadata, and rows requiring review. Includes stems above the original 112-group coverage.

Run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\\phase166_r3au2_generator_join_audit\\run.ps1"
```

The generated `results/` directory contains `summary.json`, `all_rows.csv`, `review_rows.csv`, and `special_generators.csv`.

A successful ID lookup does not certify generator expressions or LaTeX rendering. No production changes and no full pytest.
