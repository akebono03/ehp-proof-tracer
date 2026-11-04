# Phase 173 R4-R15R12R3 — Read-only n=4 proof status audit

This package audits **all 33 explicitly registered n=4 groups** (stems k=1 through k=33) against the current source-first proof search and the published model-backed Web route. It does not install rules, change any production Python file, or make a commit.

## Requirements

- Local checkout: `akebono03/ehp-proof-tracer`, branch `develop`.
- Reviewed HEAD: `715dff58df263c419cdcb45c51a1fa169a87de45`.
- Python and pytest installed in the existing project environment.
- Git remote `origin` configured to the same repository.

## Steps

Extract the ZIP into the repository root and run the following in PowerShell:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\EHP_Phase173_R4_R15R12R3_N4_ALL_33_STATUS_AUDIT.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r12r3_all_n4_status_audit\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw 'DryRun failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r12r3_all_n4_status_audit\run.ps1"
if ($LASTEXITCODE -ne 0) { throw 'Audit found errors; inspect report' }
```

## Outputs

The full run generates three files **inside this audit directory only**:

- `all_n4_status_report.json`: complete per-group evidence, error and open-goal diagnostics.
- `all_n4_status_report.csv`: sortable overview for Excel.
- `all_n4_status_report.md`: Japanese report including all 33 groups and pending-goal summaries.

Paste the terminal output or upload `all_n4_status_report.json` to discuss the measured results. A nonzero exit may mean a public Web verification or execution error; do not treat that as proof that a group is incomplete.

## Distinctions

`NAMED_COMPLETE` requires both a complete search result and a successful public Web verification. `ABSTRACT_ONLY_NAMED_PENDING` is not a complete named-generator proof. The audit separately records abstract group input-shape compatibility and named-generator alias compatibility as **necessary checks, not proofs**. It also records missing LaTeX renderers and raw diagnostic text without attempting to modify either.

Only focused audit tests run in DryRun; the repository-wide pytest suite is not run.
