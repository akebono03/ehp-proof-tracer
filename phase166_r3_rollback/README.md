# Phase 166 R3 rollback

This package restores **only** `phase165_r3_recursive_search.py` from the exact backup created before the Phase 166 R3 citation-gate patch. It first copies the current version to the package's `backups` directory, restores the old file and verifies the SHA-256 hash. It then runs `py_compile` only. It does not run the full pytest suite or claim a successful proof.

Run from the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase166_r3_rollback.zip" -DestinationPath '.' -Force
powershell -ExecutionPolicy Bypass -File '.\phase166_r3_rollback\run.ps1'
```

Expected original backup: `phase166_r3_lookup_gate_fix/backups/phase165_r3_recursive_search_20261019T150915Z.py`. If absent, the script stops without replacing the target. This rollback also removes the recently added citation gate from the restored file, so that security change must be revisited separately.
