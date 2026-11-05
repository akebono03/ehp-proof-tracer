# EHP Proof Tracer — Phase 174 R3-R6-R3R2 Pytest Import Mode Fix

This package corrects only the **test collection** failure after the successful
R3-R6-R3R1 production patch. The earlier runner used pytest's default import
mode and collected multiple files named `test_projection.py` and `test_source.py`.
Python therefore associated one module basename with another file and aborted
before executing the focused tests.

The replacement runner specifies `--import-mode=importlib` and gives pytest the
same six focused test files as the preceding runner, plus three small tests of
the collection fix itself. A DryRun validates the installed two-function
renderer transformation and performs `--collect-only`. A regular run executes
those focused tests. **Neither mode reapplies the preceding patch**, and neither
mode edits proof modules, the renderer, or existing test files.

## Baseline and requirements

- Repository: `akebono03/ehp-proof-tracer`, branch `develop`.
- Reviewed local and remote HEAD: `ecbb2fea225c5b88000629d9c025934fcc2d7075`.
- R3-R6-R3 original package and R3-R6-R3R1 guarded installer must already be extracted.
- R3-R6-R3R1 must have printed `PHASE174_R3R6R3R1_APPLIED=PASS`.
- Python, pytest, PowerShell, Git, and the repository's existing dependencies.

## Run from the repository root (PowerShell)

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase174_R3_R6_R3R2_PYTEST_IMPORTMODE_FIX.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r6_r3r2_pytest_importmode_fix\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw "R3R2 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r6_r3r2_pytest_importmode_fix\run.ps1"
if ($LASTEXITCODE -ne 0) { throw "R3R2 focused tests failed" }
git status -sb
git diff --stat
```

No full-suite pytest run is performed during Phase 174.
