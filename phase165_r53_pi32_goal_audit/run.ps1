$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'phase165_r52_r9_shared_math.py'))) {
    throw 'Run from the ehp_proof project root.'
}
Copy-Item (Join-Path $package 'phase165_r53_pi32_goal_audit.py') $root -Force
Copy-Item (Join-Path $package 'test_phase165_r53_pi32_goal_audit.py') $root -Force
python -m pytest -q test_phase165_r53_pi32_goal_audit.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m phase165_r53_pi32_goal_audit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R53 read-only audit complete. Full pytest NOT run.'
