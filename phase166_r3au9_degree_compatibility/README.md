# Phase 166 R3-AU-9: Degree Compatibility Audit

This package inspects composition-factor metadata (`n`, `k`, `stable`) from `data/HyoujiGen.csv` for the `Element` IDs in `data/sphere.csv`. It reports whether the **unadjusted base degrees** match at composition boundaries. It does not infer suspensions or certify typed expressions.

Run `powershell -ExecutionPolicy Bypass -File ".\phase166_r3au9_degree_compatibility\run.ps1"` from the repository root. Results appear in `results/`.

Read-only: no production source changes and no full test suite.
