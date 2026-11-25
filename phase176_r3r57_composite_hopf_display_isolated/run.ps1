param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$Package = 'phase176_r3r57_composite_hopf_display_isolated'
$Runner = 'phase176_r3r46r1_prior_group_availability.pytest_runner'
function Invoke-PythonChecked {
    & python -B @args
    if ($LASTEXITCODE -ne 0) { throw "Python failed ($LASTEXITCODE): $args" }
}
Invoke-PythonChecked -m "$Package.audit" --dry-run
Invoke-PythonChecked -m $Runner --check-only
if ($DryRun) { exit 0 }
foreach ($test in @(
    "$Package/tests/test_projection.py",
    'phase175_r3r11_cited_hopf_narrative/tests/test_projection.py',
    'phase176_r3r56r3_public_cited_source_display/tests/test_connection.py',
    'phase176_r3r55_equality_display_isolated/tests/test_projection.py'
)) {
    Write-Output "PHASE176_R3R57_TEST_GROUP=$test"
    Invoke-PythonChecked -m $Runner $test
}
Invoke-PythonChecked -m "$Package.audit"
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
