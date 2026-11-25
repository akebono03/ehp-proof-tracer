param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$Package = 'phase176_r3r55r1_public_equality_projection'
$Runner = 'phase176_r3r46r1_prior_group_availability.pytest_runner'
function Invoke-PythonChecked {
    & python -B @args
    if ($LASTEXITCODE -ne 0) { throw "Python failed ($LASTEXITCODE): $args" }
}
Invoke-PythonChecked -m "$Package.apply" --dry-run
Invoke-PythonChecked -m $Runner --check-only
if ($DryRun) { Write-Output '(END)'; exit 0 }
Invoke-PythonChecked -m "$Package.apply"
$Tests = @(
    "$Package/tests/test_connection.py",
    'phase176_r3r55_equality_display_isolated/tests/test_projection.py',
    'phase172_r2_suspension_relation_display/tests/test_projection.py',
    'phase176_r3r50_strict_nu_prime_connection/tests/test_notation_connection.py',
    'phase168_r3_27_typed_projection/tests/test_phase168_r3_27_typed_projection.py',
    'phase176_r3r53_common_kernel_renderer/tests/test_common_kernel.py',
    'phase176_r3r53r1_historical_kernel_test/tests/test_patch.py'
)
foreach ($Test in $Tests) {
    Write-Output "PHASE176_R3R55R1_TEST_GROUP=$Test"
    Invoke-PythonChecked -m $Runner $Test
}
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
Write-Output 'PHASE176_R3R55R1_GATE=PASS_R3R55R1_FOCUSED_TESTS'
Invoke-PythonChecked -m "$Package.audit"
Write-Output '(END)'
