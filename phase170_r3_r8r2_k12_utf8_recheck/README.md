# Phase 170 R3-R8R2: UTF-8 retry of the k=12 audit worker

This is an **audit-only** recovery package. It does not modify production code, existing tests, `sphere.csv`, `HyoujiGen.csv`, documents, the Git index, or any tracked file. It does not create or certify a mathematical proof by itself.

It is designed for the exact committed repository state `develop` at `114a67d708edba3d17da673a218034fcd804aa15` (`170-3-8`). The runner checks the branch and HEAD, rejects tracked changes, and checks committed Git blobs of the original R3-R8 audit worker, the Toda (5.2) transport, and the ordered-DB-prior helper. Untracked directories are allowed.

The previous exhaustive audit of n=2, k=0..33 finished with 32 complete Web-verified proofs and one crashed worker at k=12. The worker crashed while printing a Unicode subscript `₂` using Windows `cp932`, not while printing a search failure. The package reruns **only k=12** using the existing committed R3-R8 worker in a subprocess forced to UTF-8 (`PYTHONIOENCODING=utf-8`, `PYTHONUTF8=1`). The original worker and its proof and Web trust-boundary checks remain unchanged.

If a correctly shaped previous 32/33 audit report is found under `%LOCALAPPDATA%\EHPProofTracerRecovery`, the results are combined in a **new** report without changing the old report. Otherwise, only the k=12 result is reported. Any incomplete result or crash remains visible; no result is auto-promoted to complete.

## Run from the Windows repository root

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase170_r3_r8r2_k12_utf8_recheck.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r8r2_k12_utf8_recheck\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r8r2_k12_utf8_recheck\run.ps1"
git status -sb
```

The report appears under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase170_r3_r8r2_k12_*` as `audit.json` and `k_012.log`. Expected display keys include `PHASE170_R3R8R2_k=12_RESULT`, `PHASE170_R3R8R2_SCOPE`, `PHASE170_R3R8R2_DOMAIN_CHECKED`, `PHASE170_R3R8R2_DOMAIN_COMPLETE`, `PHASE170_R3R8R2_DOMAIN_GAPS`, and `PHASE170_R3R8R2_TRACKED_UNCHANGED`.

Only a `COMBINED_33_K` report with `DOMAIN_CHECKED=33`, `DOMAIN_COMPLETE=33`, and `DOMAIN_GAPS=0` establishes completeness across the previously audited DB domain. A `SINGLE_K` report establishes only the k=12 result. The package does not run the entire pytest suite.
