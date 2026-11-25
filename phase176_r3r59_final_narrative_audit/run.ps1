param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$Package = 'phase176_r3r59_final_narrative_audit'
$Runner = 'phase176_r3r46r1_prior_group_availability.pytest_runner'
function Invoke-PythonChecked {
    & python -B @args
    if ($LASTEXITCODE -ne 0) { throw "Python failed ($LASTEXITCODE): $args" }
}
Invoke-PythonChecked -m "$Package.audit" --dry-run
Invoke-PythonChecked -m $Runner --check-only
if ($DryRun) { exit 0 }
foreach ($test in @(
    "$Package/tests/test_audit.py",
    'phase176_r3r54_narrative_audit/tests/test_audit.py',
    'phase176_r3r58r1_public_finite_cyclic_lift_display/tests/test_connection.py'
)) {
    Write-Output "PHASE176_R3R59_TEST_GROUP=$test"
    Invoke-PythonChecked -m $Runner $test
}
Invoke-PythonChecked -m "$Package.audit"
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
