# Phase 169 R10EJ-R1 — Pytest cache isolation

This package re-runs the unchanged Phase 169 R10EJ installer, limited pytest tests, and narrative audit without allowing pytest to update a Git-tracked `.pytest_cache/v/cache/nodeids` file.

## Scope

This package adds no mathematical rule, changes no repository production module, and does not modify the original R10EJ runner. It verifies the exact SHA-256 of the original runner extracted from `phase169_r10ej_cyclic_verified_projection.zip`, then invokes it with `PYTEST_ADDOPTS=-p no:cacheprovider` in a child PowerShell process.

The original runner still performs its own reviewed-source checks, temporary installation, focused tests, full proof-tree narrative audit, Git status check, and byte-for-byte rollback on failure. A successful run retains the R10EJ single-function production patch for later review and commit.

An existing modification to the tracked `.pytest_cache/v/cache/nodeids` from an earlier failed run is neither deleted nor reverted. The wrapper checks that the cache file does not change during this run.

## Usage

From the repository root in Windows PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r10ejr1_pytest_cache_isolation.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10ejr1_pytest_cache_isolation\run.ps1"
git status -sb
```

The `phase169_r10ej_cyclic_verified_projection` folder must already exist, as it does after the first R10EJ attempt.

The wrapper runs five new focused tests, then delegates to the original R10EJ limited tests and audit. The full pytest suite is not run until the Phase 169 closeout.
