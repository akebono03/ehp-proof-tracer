# Phase 173 R4-R1 Public Connection

This package connects the previously verified, source-bound Toda Proposition 4.4 / Lemma 5.4 decomposition for $\pi_7^4$ to the normal typed proof search used by Group query and Group proof.

## Scope

- Production change: **one existing function**, `search_shared_group_goal()` in `phase165_r52_r9_shared_math.py`.
- No top-level import changes. The existing function receives a conditional, local import for `(n,k)=(4,3)` only.
- Added package: `phase173_r4_r1_public_connection/` with a verified helper, guarded installer, focused tests, public/Web verification, and PowerShell runner.
- No change to DB goals, typed proof validator, narrative renderer or any other group-specific route.
- The original source is backed up outside the repository under `%LOCALAPPDATA%\EHPProofTracerRecovery`.

## Run

From the repository root after extraction:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r1_public_connection\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r1_public_connection\run.ps1"
```

A mismatch in source hashes, local staged edits, branch tracking or the inspected target function stops the installer without overwriting the search function. A completed isolated proof is **not** treated as evidence of public/Web completion; the public selector and Web view are checked separately.

The project's full pytest suite is intentionally not run at R4-R1: it belongs at the end of Phase 173.
