$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
python "$PSScriptRoot\install.py"
if ($LASTEXITCODE -ne 0) { throw "R52-R7 installation failed" }
python -m pytest -q test_phase165_r52_r7_registered_common_proof.py
if ($LASTEXITCODE -ne 0) { throw "R52-R7 targeted tests failed" }
Write-Output "R52-R7 targeted tests passed; full pytest NOT run."
