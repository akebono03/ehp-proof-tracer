# Phase 169 R4C2 — Audit Already-Committed R4C

This package does not patch application code. The R4C suspension-isomorphism
provider and rule are already committed to `develop` as of
`75cbee31865594fa65202e4d49d6bef9a6b50816`.

Run from the repository root in Windows PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r4c2_committed_audit.zip" -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r4c2_committed_audit\run.ps1"
```

The verification checks five exact Git blob IDs and their local worktree
counterparts. It is insensitive to *unrelated* Git commits but intentionally
refuses to run after a change to audited production source. It invokes focused
pytest and the existing actual proof-reconstruction audit, then copies reports
to `output/`. No full pytest suite is run, and it does not fabricate conclusions.
