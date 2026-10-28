# Phase 169 R10ET-R5B: Reviewed Committed-R4 Guard

This is a complete, independently extractable replacement of R10ET-R5. It corrects the precondition that previously required the Phase R4 source changes to be uncommitted. The R5 mathematical rule, five production/test changes, 16-case proof audit and rollback behavior are unchanged.

## Preconditions

- Windows PowerShell, Python and the existing repository pytest dependencies.
- The `develop` branch at exactly `3a8014efb91ddf76060c4d07d73153e55ea52c75` (the reviewed `10et4` commit) with no tracked changes. Alternatively, the earlier `5a8ad4a56c5407c0fbe15ba14516a1c1a99f0562` commit with **exactly** the two reviewed R4 tracked changes is accepted.
- Both R4 production files must match the byte-for-byte output of the reviewed R4 full-function patch, as checked against the original R4 baseline.
- The five R5 patch targets must match their reviewed Git blob SHA-1 hashes, in both the working tree and HEAD.
- The previously reviewed R10ET-R2 shadow audit output must be present in the repository.

## Execute in PowerShell

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r10et_r5b_committed_r4_guard.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10et_r5b_committed_r4_guard\run.ps1"
git status -sb
```

The run exports all five full replacement files and every changed complete function, applies only those files, runs focused pytest, and audits the 16 reviewed cases using the production provider. It prints `R10ET_R5B_COMPLETE=PASS` only after all checks. The full test suite is not executed.

If a test or audit fails after applying the patch, only R5B's five changes are rolled back. R4 remains committed and untouched. Neither `git checkout` nor `git reset` is performed.

The previous untracked `phase169_r10et_r5_common_definition_provider/` package can remain in place; this package uses a new module directory and does not overwrite it.
