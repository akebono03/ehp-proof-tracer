$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
python "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q "$PSScriptRoot\test_phase165_r13_r2_global_guard.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Phase 165 R13-R2: all legacy group-proof routes blocked; full pytest NOT run."
