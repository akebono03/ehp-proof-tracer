$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot ".."))
python -B -m pytest -q ".\phase163_r1h_additional_fact_repositories\tests\test_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m phase163_r1h_additional_fact_repositories.audit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Phase 163 R1H read-only additional fact inventory complete. Full suite not run."
