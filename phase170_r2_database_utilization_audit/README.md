# Phase 170 R2 — Read-Only Database Utilization Audit

This package examines the existing EHP Proof Tracer data-to-goal pipeline against the actual Phase 170 R1 proof-search recordings. It does **not** modify production files, existing tests, mathematical statements, or Git state.

The audit uses the reviewed `develop` source (HEAD `790db364a8531693572fc510f969da831f1f9ffb`, or its handoff ancestor with verified identical production files). It refuses an unexpected branch or unreviewed source blob. All reports are written to a new folder below `%LOCALAPPDATA%\EHPProofTracerRecovery`.

It reads the current `sphere.csv`, `sphere_relation2.csv`, `HyoujiGen.csv`, and `TBtable.csv`, builds the standard typed registry, and calls the existing database candidate and group-goal selectors. It compares these with the twelve groups in the completed R1 `audit.json`, including which references were actually used in the searched proof. It does not rerun proof search or the full pytest suite.

Run from the repository root on Windows:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase170_r2_database_utilization_audit.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r2_database_utilization_audit\run.ps1"
git status -sb
```

By default, the runner selects the newest R1 `audit.json` in the recovery folder. Pass `-R1Report 'C:\path\audit.json'` to select an explicit report.

A `PASS` indicates that the audit itself completed and preserved the Git index, **not** that every database record was used or every group was proven. See `audit.md` and `audit.json` for unresolved connection classes and evidence. Source rows and selected goals are *not proof leaves* merely by being present.
