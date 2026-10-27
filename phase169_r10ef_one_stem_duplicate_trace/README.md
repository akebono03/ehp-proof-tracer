# Phase 169 R10EF — One-stem competing-derivation trace

This package is **audit-only**. It observes the existing root candidate insertion in `phase165_r3_recursive_search.py` by delegating to the unchanged `append_unique_verified_derivation()` function. The audit neither selects nor discards any proof route and does not change a `partial` result to `complete`.

## Purpose

R10EE found that the searches for $\pi_5^4$ and $\pi_6^5$ are incomplete because two derivations of the same typed target remain. The two routes must be examined before any proof-search patch. This audit lists their actual inference-rule metadata, premise types, screened GIVEN sources, and existing equivalence checks. Rule names are observational metadata, **not mathematical proof identities**.

R10EE also reported that tracked Git status had changed without printing which paths. This runner snapshots the actual tracked status before and after the focused tests and audit, printing paths when they differ. It will not perform a checkout, hard reset, deletion, or automatic restore.

## Run (PowerShell)

From the repository root after extracting the ZIP:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase169_r10ef_one_stem_duplicate_trace\run.ps1"
```

## Files and exact scope

Only the new `phase169_r10ef_one_stem_duplicate_trace/` directory is added. `trace.py` defines `AppendObservation`, `is_exact_goal_conclusion`, `forward_and_observe`, and `pairwise_kept_indices`; `audit.py` defines `_short`, `describe_step`, `_comparison`, `inspect_case`, `make_report`, and `main`; the five tests in `tests/test_r10ef_trace.py` exercise observer noninterference. `run.ps1` checks reviewed Git blobs, runs five focused tests and two observed group searches, and writes diagnostic outputs under `output/`.

`output/duplicate_root_trace.json` contains complete candidate provenance, including source assertions where available. `output/tracked_status_before.txt` and `output/tracked_status_after.txt` show the Git comparison used by the runner.

No production imports, classes, functions, tests, or project-level documents are modified. There is no full-suite pytest in this audit.
