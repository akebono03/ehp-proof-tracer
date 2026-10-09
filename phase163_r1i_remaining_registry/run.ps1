$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot ".."))
python -B -m pytest -q ".\phase163_r1i_remaining_registry\tests\test_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m phase163_r1i_remaining_registry.audit --source-root "." --output ".\phase163_r1i_output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Phase 163 R1I completed. Existing project code unchanged. Full suite not run."
