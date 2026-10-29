# Phase 170 R3-R12 — Full-document closeout

This package updates exactly five documentation files, preserving their complete existing content. It does not modify proof rules, tests, data, or citations. It **does not rerun the active repository-wide pytest suite**, which passed in the earlier Phase 170 R3-R11R2 gate.

## Reviewed inputs

- Branch: `develop`; the passing full-suite Gate ran at `84db682e179203dcbddc1c2c88bc3ccbb31a830f`. Current `develop` must be that commit or a descendant that **only adds files** under the three reviewed R3-R11 audit package paths (verified with `git -c core.quotePath=false diff --name-status`).
- Five documents must match the reviewed Git blobs, with no pre-existing tracked changes or staged changes.
- The immutable fresh audit must report 33/33 `COMPLETE_AND_WEB_VERIFIED` for `n=2, k=1..33`.
- The immutable phase-end report must record `3546 passed in 34.94s`, zero exit code, unchanged tracked state, and the same 33/33 audit SHA-256.
- The current `origin/develop` must match the local `develop` HEAD, while all five document Git blobs must remain exactly as reviewed.

## Execute from PowerShell

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase170_r3_r12_document_closeout.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r12_document_closeout\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r12_document_closeout\run.ps1"
git status -sb
git diff --stat
```

The dry run writes the **five complete proposed Markdown files** to `phase170_r3_r12_document_closeout/output/` without touching tracked files. Review the complete outputs before running the apply command. The apply run writes those same complete files to `README.md` and the four files under `docs/`; it saves each entire original file in a timestamped directory under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase170_r3_r12_docs_*\before\`.

The output folder also contains `report.json` with the SHA-256 and size of each resulting document. Never run the apply command twice: a second run intentionally refuses pre-existing document changes or a duplicate section marker. Git commits and remote pushes are **not** performed.

## Scope

Only documentation is modified. The active Phase 170 closeout already passed with 3,546 tests; the focused tests in this package validate the document-generation contract only. The success of the audited finite database domain does not certify arbitrary homotopy groups or original editions of cited sources.
