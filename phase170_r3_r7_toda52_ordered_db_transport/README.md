# Phase 170 R3-R7 (revised): Toda (5.2) from ordered database priors

This package extends the already adopted Toda (5.2) isomorphism to finite cyclic, free cyclic, zero and direct-sum presentations for the n=2 groups. The existing citation-backed route is retained. All new group premises are independently admitted by the existing R10E4 `(k,n)` strict lexicographic gate and revalidated by the public proof-tree trust boundary.

The source relation is read **only** from the explicit `sphere.csv` row for `(n=3,k=m-3)`. No target answer is used as its own premise, and no DB row is relabeled as a Toda citation. Generator correspondence must match the typed eta_2 composite, with additive forms checked componentwise. The package changes only `phase168_r2_toda52_transport.py`.

## Windows execution

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase170_r3_r7_toda52_ordered_db_transport.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r7_toda52_ordered_db_transport\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r7_toda52_ordered_db_transport\run.ps1"
git status -sb
```

The second command must be run only after the dry-run reports `PHASE170_R3R7_DRY_RUN=PASS`. A failed focused test or active Web check causes the modified production file to be restored. Diagnostic logs and the original file are stored under `%LOCALAPPDATA%\EHPProofTracerRecovery` outside the Git tree. The installer never performs checkout or reset.

## Verification

Focused pytest includes the older Toda (5.2) tests, Phase 170 R3-R5 and R3-R6 checks, ordered DB gate tests, and new generic structure tests. Active search and public Web proof are checked for n=2 with k=3..10 and k=14. A full test suite is deferred until the Phase 170 closeout.

The first result at n=2, k=0 is outside Toda (5.2), whose scope is pi_i for i>=3. A proof is not claimed where a source DB row lacks an unambiguous typed generator presentation.
