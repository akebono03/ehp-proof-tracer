$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:PYTHONPATH = "$PSScriptRoot$([IO.Path]::PathSeparator)$Root"
python -m pytest -q "$PSScriptRoot/test_phase165_r14_goal_frontier.py" tests/test_phase165_r12_typed_binding.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$PSScriptRoot/audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Phase 165 R14-R1: typed goal and unresolved frontier recorded; full pytest NOT run."
