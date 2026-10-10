$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot ".."))
python -B -m pytest -q ".\phase163_r4_r14_catalog\tests\test_catalog.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Phase 163 R4-R14 focused tests complete. Full suite not run."
