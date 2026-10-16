$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
python (Join-Path $PSScriptRoot "apply.py")
if ($LASTEXITCODE -ne 0) { throw "Patch failed" }
python -m pytest -q (Join-Path $PSScriptRoot "test_independent_source.py")
if ($LASTEXITCODE -ne 0) { throw "Focused tests failed" }
Write-Host "R6-1 source inventory decoupled; full pytest NOT run."
