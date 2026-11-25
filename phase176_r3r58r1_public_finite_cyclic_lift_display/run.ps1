param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$Package = 'phase176_r3r58r1_public_finite_cyclic_lift_display'
$Runner = 'phase176_r3r46r1_prior_group_availability.pytest_runner'
function Invoke-PythonChecked {
    & python -B @args
    if ($LASTEXITCODE -ne 0) { throw "Python failed ($LASTEXITCODE): $args" }
}
Invoke-PythonChecked -m "$Package.apply" --dry-run
Invoke-PythonChecked -m $Runner --check-only
if ($DryRun) { exit 0 }
Invoke-PythonChecked -m "$Package.apply"
foreach ($test in @(
    "$Package/tests/test_connection.py",
    'phase176_r3r58_finite_cyclic_lift_display_isolated/tests/test_projection.py',
    'phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated/tests/test_finite_cyclic_subgroup_lift.py',
    'phase176_r3r57r1_public_composite_hopf_display/tests/test_connection.py',
    'phase176_r3r57_composite_hopf_display_isolated/tests/test_projection.py',
    'phase176_r3r56r3_public_cited_source_display/tests/test_connection.py',
    'phase175_r3r11_cited_hopf_narrative/tests/test_projection.py',
    'phase171_r20r13_eta_sentence_layout/tests/test_projection.py',
    'phase176_r3r55_equality_display_isolated/tests/test_projection.py',
    'phase168_r3_27_typed_projection/tests/test_phase168_r3_27_typed_projection.py'
)) {
    Write-Output "PHASE176_R3R58R1_TEST_GROUP=$test"
    Invoke-PythonChecked -m $Runner $test
}
Write-Output 'PHASE176_R3R58R1_GATE=PASS_R3R58R1_FOCUSED_TESTS'
Invoke-PythonChecked -m "$Package.audit"
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
