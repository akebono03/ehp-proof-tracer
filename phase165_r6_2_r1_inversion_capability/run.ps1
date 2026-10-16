$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
python .\audit.py
if ($LASTEXITCODE -ne 0) { throw "R6-2 inversion audit failed" }
python -m pytest -q .\test_audit.py
if ($LASTEXITCODE -ne 0) { throw "Focused audit tests failed" }
Write-Host "R6-2 R1 rule-shape audit finished. No production edits. Full pytest NOT run."
