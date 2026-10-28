# Phase 169 R10EO-R1A — Cache-safe audit runner

This narrowly scoped runner fixes a likely false-positive tracked-diff failure in the R10EO-R1 audit by disabling pytest's cache provider. It also reports the names of tracked files that change while the audit runs. It does not alter application code, existing tests, documentation, proof trees, citations, or repository state.

## Requirements

- Windows PowerShell, Python, pytest, and Git.
- Repository `akebono03/ehp-proof-tracer`, branch `develop`, checked-out commit `57f807901f87c8d66acf4ee4db16ce05b00dccd4`.
- The previously extracted `phase169_r10eo_r1_definition_audit/` folder in the repository root.

## Run

Extract `phase169_r10eo_r1a_cache_safe_runner.zip` into the repository root and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10eo_r1a_cache_safe_runner\run.ps1"
```

The runner executes only the five R10EO/R10B/R10D2/R10E8/R10E1 focused test files, with `-p no:cacheprovider`, then performs the existing read-only R10EO audit and the `pi_41^30` live search. Audit artifacts are written beneath `phase169_r10eo_r1_definition_audit/output/`.

It preserves the Git branch and reviewed-HEAD guards and rejects local edits to the audited production/source files. It compares tracked-diff filename sets before and after the run and prints new/cleared file names if the final comparison fails. Existing dirty tracked files are not reset, cleaned, or modified by this script. `pytest` cache files dirtied by a prior run remain as they were.

No full pytest suite is run. No automatic `git reset`, `git checkout`, or `git clean` is performed.
