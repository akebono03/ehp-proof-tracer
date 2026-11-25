param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$Package = 'phase176_r3r60r1_citation_premise_elision_isolated'
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
    'phase176_r3r60_citation_redundant_premise_audit/tests/test_audit.py',
    'phase176_r3r59r4_public_definitional_suspension_elision/tests/test_connection.py',
    'phase176_r3r10_right_zero_transport_isolated/tests/test_rule.py'
)) {
    Write-Output "PHASE176_R3R60R1_TEST_GROUP=$test"
    Invoke-PythonChecked -m $Runner $test
}
Invoke-PythonChecked -m "$Package.audit"
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
