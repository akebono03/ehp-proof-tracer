# Phase 171 R1D — three incomplete registered 3-stem goals

This package reads the successful Phase 171 R1C audit report without repeating proof search or modifying application code, the database, Git-tracked files, or official documentation.

It validates the observed 32 registered `k=3` coordinates and the previously reported 29 complete / 3 incomplete classification. It then outputs the existing diagnostic fields for `n=3,4,5` (`pi_6^3`, `pi_7^4`, and `pi_8^5`). A symptom classification is not a new mathematical conclusion. No future phase inference rules are added.

## Windows usage

Extract the ZIP in the repository root:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase171_r1d_k3_three_gap_diagnostics.zip" -DestinationPath "." -Force
$Audit = Join-Path $env:LOCALAPPDATA 'EHPProofTracerRecovery\phase171_r1c_k3_20261029_061130_694213\audit.json'
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r1d_k3_three_gap_diagnostics\run.ps1" -ReportPath $Audit -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r1d_k3_three_gap_diagnostics\run.ps1" -ReportPath $Audit
git status -sb
```

Read `PHASE171_R1D_DETAIL` from the terminal or the generated `gap_details.json` and `gap_details.md` under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r1d_k3_gaps_*`.

The only new files are this package. No existing Python module, test, or official project document is edited. A targeted pytest runs; the repository-wide test suite must wait until the end of Phase 171.

## R1D-R2: fix for the changed Git HEAD (2026-10-29)

The original R1D diagnostic stopped **before reading** its R1C report because
`tracked_state()` accepted only `715b00d6`. The currently reported `develop`
and `origin/develop` are both `30c6c5ee`, a descendant commit whose changes
add only the Phase 171 R1 and R1C audit packages (GitHub compare checked).

R1D-R2 accepts **exactly** those two reviewed working-tree HEADs, always requires
`develop`, a matching local `origin/develop`, and no tracked changes. It keeps
the R1C audit's historical `preflight.head` strictly pinned to `715b00d6`.
The existing R1C `audit.json` is neither modified nor reinterpreted as a new
search. No `git reset`, checkout, fetch, commit or other Git write occurs.

Use the new ZIP, which replaces this same untracked audit package directory.
Run the original PowerShell commands above with the same existing R1C report.
The 13 existing tests and 5 additional regressions run; full pytest is not run.
