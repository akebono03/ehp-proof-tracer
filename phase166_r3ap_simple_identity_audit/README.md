# Phase 166 R3-AP: Simple Generator Identity Audit

Read-only validation of the 28 simple-name typed goal groups, comparing their generators against `sphere.csv` `Element` IDs and `HyoujiGen.csv` generator records.

The audit reports `confirmed`, `mismatch`, or `unverifiable` and does not equate equal TeX strings with mathematical identity. It does not change production code or run proof search.

From the repository root, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase166_r3ap_simple_identity_audit\run.ps1
```

Outputs: `results/report.json` and `results/report.md`. Full pytest is not run.
