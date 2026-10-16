$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
python (Join-Path $PSScriptRoot "apply.py")
if ($LASTEXITCODE -ne 0) { throw "Patch failed" }
python -m pytest -q (Join-Path $PSScriptRoot "test_independent_source.py") (Join-Path (Join-Path $PSScriptRoot "..") "phase165_r6_1_adopted_leaves_independent/test_independent_source.py")
if ($LASTEXITCODE -ne 0) { throw "Focused regression tests failed" }
Write-Host "R6-1 foundation index corrected; full pytest NOT run."
