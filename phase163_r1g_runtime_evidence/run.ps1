$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot ".."))
python -B -m pytest -q ".\phase163_r1g_runtime_evidence\tests\test_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m phase163_r1g_runtime_evidence.audit --include-standard --output ".\phase163_r1g_output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Phase 163 R1G evidence collected; existing source unchanged. Full pytest suite not run."
