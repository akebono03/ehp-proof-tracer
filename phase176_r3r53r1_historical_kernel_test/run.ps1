param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$Package = 'phase176_r3r53r1_historical_kernel_test'
$Runner = 'phase176_r3r46r1_prior_group_availability.pytest_runner'
function Invoke-PythonChecked {
    & python -B @args
    if ($LASTEXITCODE -ne 0) { throw "Python failed ($LASTEXITCODE): $args" }
}
Invoke-PythonChecked -m $Runner --check-only
Invoke-PythonChecked -m "$Package.apply" --dry-run
Write-Output 'PHASE176_R3R53R1_GATE=PASS_R3R53R1_DRYRUN'
if ($DryRun) { exit 0 }
Invoke-PythonChecked -m "$Package.apply"
Invoke-PythonChecked -m $Runner "$Package/tests/test_patch.py"
# Resume all the original focused checks and the public R3R53 audit.
& powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase176_r3r53_common_kernel_renderer\run.ps1'
if ($LASTEXITCODE -ne 0) { throw 'R3R53 regression run failed' }
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
Write-Output 'PHASE176_R3R53R1_GATE=PASS_R3R53R1_HISTORICAL_TEST_AND_PUBLIC_AUDIT'
Write-Output 'PHASE176_R3R53R1_FULL_PYTEST=NOT_RUN'
