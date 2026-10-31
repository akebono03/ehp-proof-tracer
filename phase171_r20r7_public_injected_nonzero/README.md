# Phase 171 R20R7R1 — Committed R20R6 Baseline Fix

This package fixes the R20R7 installer guard after the preceding R20R6 update was committed on the `develop` branch. It accepts only two explicitly reviewed, consistent Git blob pairs (the previous uncommitted baseline and the later committed baseline), rejects unknown or mixed versions, and preserves all existing mathematical inference rules and citation checks.

## Install

Extract the ZIP at the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r7_public_injected_nonzero\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r7_public_injected_nonzero\run.ps1"
```

A successful dry run changes no files. The full run creates backup files before modifying exactly `phase171_r2j_r4_r7_nonzero_nu_order/source.py` and `phase165_r52_r9_shared_math.py`. It runs focused tests and audits the public proof proposal. A second application is idempotent.

The proof expansion still requires an independently verified prior cyclic group presentation and a proven injective suspension map. It does not add GIVEN facts, import completed proofs into the public search, or claim Web completion.

The full changed code, supporting tests, and installer are documented in `CHANGED_CODE.md`. See `IMPLEMENTATION_NOTES_JA.md` for the Japanese audit notes.
