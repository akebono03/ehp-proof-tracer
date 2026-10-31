# Phase 171 R20R8 — Public Nonzero Double Proposal

This guarded patch connects a source-anchored backward proposal for the already existing inference rule that transfers nonzeroness across a typed double equality. No new axioms, registered source records, or completed proof trees are added.

Run from the repository root with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r8_public_double_nonzero\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r8_public_double_nonzero\run.ps1"
```

The package checks the exact R20R7 source and provider contents reconstructed from the reviewed R20R6 Git commit, regardless of whether R20R7 has been committed. Backups are stored in this package's `output` directory. Only focused tests are run. The typed double equality is still a separate, unresolved public proof obligation; public completion is not claimed.
