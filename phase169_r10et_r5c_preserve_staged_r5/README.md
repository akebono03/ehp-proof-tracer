# Phase 169 R10ET-R5C: Safely Preserve the Staged R5 Audit Package

This complete ZIP is an independently extractable replacement of R10ET-R5B. It fixes the Git guard to accept the *exact nine new, staged audit files* from R5, without modifying the Git index, restoring/staging any file, or changing application semantics. It also accepts an otherwise empty Git index. Other staged changes fail closed.

## Preconditions

- Git branch `develop` and reviewed HEAD `3a8014efb91ddf76060c4d07d73153e55ea52c75` (committed R4). The earlier reviewed R4 pre-commit HEAD remains accepted with exactly its two verified changes.
- The existing R4 production changes must match the reviewed output byte-for-byte.
- All five R5 production/test targets must match their reviewed working-tree and HEAD Git blob IDs.
- The Git index is either empty, or has exactly the nine `A` entries in `phase169_r10et_r5_common_definition_provider/` identified in this package. These files remain staged throughout the run.
- The reviewed R10ET-R2 shadow audit output must be available.

## Execute

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r10et_r5c_preserve_staged_r5.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10et_r5c_preserve_staged_r5\run.ps1"
git status -sb
```

The production change is limited to `phase165_r52_r9_shared_math.py::shared_expansion_provider` and four R5-related existing test files. The runner exports full replacement files and complete modified functions into `output/<timestamp>/full_sources`. It runs focused pytest and a 16-case real-provider audit. No full-suite test is run. In case of failure, it restores only the five R5 targets; R4 and all previously staged R5 audit files remain unchanged.

The guard-only modifications in this R5C package are the complete `run.py::reviewed_index_snapshot`, `run.py::verify_preconditions`, and `run.py::main`, plus new focused head-guard tests. `patch.py` and `audit.py` otherwise reproduce R5B behavior.
