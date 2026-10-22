# Phase 168 R1 — pi_4^2 read-only audit

This package inspects the current repository's typed goal selection, registered references, source proof links, the common backward expansion provider, and the actual proof-search outcome for `n=2, k=2`.

No production files, database rows, or documentation files are changed. It does not assert a mathematical proof from a database goal. The Phase-wide test suite is not run.

From the repository root in Windows PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase168_r1_pi42_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r1_pi42_audit\run.ps1"
```

Inspect `phase168_r1_pi42_audit/results/audit.json` and `audit.md`. Share the JSON report to determine the smallest R2 changes. Errors are preserved in the JSON rather than silently treated as empty results.

Current-code entry points verified on GitHub `develop` before packaging: `phase165_r55_nk_only_goal.py`, `phase166_r3af_goal_adapter.py`, `phase166_r3aj_structured_generator.py`, `phase165_r52_r9_shared_math.py`, `phase165_r52_r2_search_adapter.py`, and `phase165_r52_r5_auto_search.py`.

R1 boundary: no new proof rule, no citation gate changes, no generic 2-stem transport, no renderer changes.
