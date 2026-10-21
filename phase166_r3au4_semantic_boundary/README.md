# Phase 166 R3-AU-4 — Generator Data Semantic Boundary Audit

Read-only inventory of every row in `data/sphere.csv` or `data/sphere(3).csv`. It separates `Element` ID sequence lengths from `gen_coe` coefficient-vector lengths and preserves nonzero positions for examination. The optional `generator` text is reference-only and never treated as required data.

Run from the repository root after extracting:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase166_r3au4_semantic_boundary\run.ps1"
```

Outputs: `results/summary.json`, `all_rows.csv`, `nontrivial_coefficients.csv`, `zero_or_empty.csv`.

No production modifications. No full pytest.
