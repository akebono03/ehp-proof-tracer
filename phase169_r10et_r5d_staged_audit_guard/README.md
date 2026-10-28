# Phase 169 R10ET-R5D: Preserve Staged R5 Audit Bundles

This is a self-contained correction of the R5C Git-index preflight check. It does **not** change the mathematical implementation proposed in R5C. The runner accepts staged **additions only** within four explicitly reviewed R5/R5B/R5C/R5D audit directories, while rejecting staged changes to production code, unknown directories, modified files, deletions, and renames. It preserves the staged Git index throughout patching, testing, auditing, and rollback.

## Verified inputs

- Branch: `develop`; reviewed HEAD `3a8014efb91ddf76060c4d07d73153e55ea52c75` (committed R4). The previously reviewed R4 precommit state is also supported under its own strict dirty-file check.
- R4 implementation: both production file contents must match the reviewed R4 full-function transformation byte-for-byte.
- R5 inputs: the provider and four existing tests must match their independently reviewed Git blob hashes in both HEAD and working tree.
- Git staging area: empty or exclusively newly added files within `phase169_r10et_r5_common_definition_provider/`, `phase169_r10et_r5b_committed_r4_guard/`, `phase169_r10et_r5c_preserve_staged_r5/`, or this R5D directory. No complete-package requirement applies. Staged bytes are fingerprinted and compared after the audit.
- The R10ET-R2 shadow baseline must exist in the working tree.

## Run on Windows PowerShell

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r10et_r5d_staged_audit_guard.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10et_r5d_staged_audit_guard\run.ps1"
git status -sb
```

## Scope

The runner patches only `phase165_r52_r9_shared_math.py::shared_expansion_provider()` plus four existing affected tests; it exports complete replacement files and functions to `output/<timestamp>/full_sources`, then runs focused pytest and the same 16-case production proof/Trust/Reference/projection audit as R5C. It does not run the full suite. On failure, the five R5 modifications are restored without reverting R4 and without invoking `git add`, `git reset`, or `git restore --staged`.

The **only new behavior** in R5D compared with R5C is its Git staging-area guard and new targeted tests. No family-specific proof rule, new reference citation, or additional group assertion is introduced. The production-search implementation remains identical to the reviewed R5C implementation.

## Validation and review

Before deployment, this package's new guard and real-Git tests passed locally (23 tests). The production proof regression suite must be run on the user's existing repository; success cannot be asserted from these local tests alone. Run outputs begin with `R10ET_R5D_` and should end in `R10ET_R5D_INDEX_PRESERVED=True`, `R10ET_R5D_COMPLETE=PASS`, and `R10ET_R5D_EXIT=0`.
