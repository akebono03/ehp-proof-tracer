# Phase 166 R3-AU-5 — DB Convention Audit

Read-only audit of `sphere.csv` and `HyoujiGen.csv`, based on the confirmed convention that `Element` is a composition of display-element IDs and `gen_coe` is a linear-combination coordinate vector. The `generator` string is optional reference text.

Run `powershell -ExecutionPolicy Bypass -File ".\phase166_r3au5_db_convention_audit\run.ps1"` from the repository root.

Results: `results/summary.json`, `results/all_rows.csv`, and `results/nontrivial_rows.csv`.

No production modifications or full pytest run.
