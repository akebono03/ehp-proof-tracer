# Phase 173 R4-R1: narrative installer audit repair

This package fixes the installer preflight used by the already prepared,
source-faithful Web narrative for the complete proof of `pi_7^4`.

## Verified source states

The public-search hook can be present in one of two audited states:

1. **Installed in the worktree** against the reviewed pre-hook Git blob
   `2718c55789af7f442ac2c086d016d3d6f7ca3133`. The original public
   connection installer must report `ALREADY_INSTALLED`.
2. **Already committed** as the reviewed Git blob
   `3e4c5f9c62b04d618f845b0f82d1cb1cacccdf2e`. The installer checks
   the exact committed hook, its pre-hook blob, the reviewed public route,
   the public installer, the source dependencies, and the typed diagonal rule.
   The worktree must not contain an unreviewed search or dependency edit.

These two cases are mutually exclusive. Unknown Git blobs, staging changes,
worktree modifications, unexpected source provenance, or diverged
`develop`/`origin/develop` are rejected before any file is changed.

## Scope

Only the package's `install.py` and the installer tests change relative to
`EHP_Phase173_R4_R1_NARRATIVE_INSTALL_TEST_FIX.zip`.
The package's existing `projection.py`, `verify.py`, `run.ps1`, and complete
replacement function `build_partial_web_group_proof_view_FULL.py.txt` are
unchanged. On successful installation, the only production file edited is
`phase165_r52_r3_web_adapter.py`, within
`build_partial_web_group_proof_view()`; its top-level imports remain unchanged.
No proof search, mathematical rule, or other group's Web narrative is changed.

The installer creates a recovery backup outside the repository before any
production change. The script is idempotent and supports `-DryRun`.

## PowerShell usage

From the EHP Proof Tracer repository root after extracting the ZIP:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r1_narrative_source_fix\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r1_narrative_source_fix\run.ps1"
```

Only focused `pytest` tests are run. The full test suite remains reserved for
Phase 173 closeout. Inspect the actual browser's Group proof for `n=4, k=3`
after the script reports success.
