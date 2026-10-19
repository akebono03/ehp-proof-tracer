# Phase 166 R2 — Generator and Group Correspondence Audit

Run from the root of `ehp_proof` on Windows after extracting the ZIP:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase166_r2_generator_group_audit\run.ps1
```

The script reads `HyoujiGen.csv` and `sphere(3).csv` from the project root or `data/`; it writes only to `phase166_r2_generator_group_audit/results`. It does not alter the production code or source CSVs. `Element` numbers are treated as lookup candidates, not mathematical proofs. Neither source/reference eligibility nor derived group identities are certified. The script runs four focused tests only.
