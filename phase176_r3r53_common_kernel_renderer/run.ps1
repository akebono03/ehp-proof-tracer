param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$Package = 'phase176_r3r53_common_kernel_renderer'
$Runner = 'phase176_r3r46r1_prior_group_availability.pytest_runner'
function Invoke-PythonChecked {
    & python -B @args
    if ($LASTEXITCODE -ne 0) { throw "Python failed ($LASTEXITCODE): $args" }
}
Invoke-PythonChecked -m "$Package.apply" --dry-run
Invoke-PythonChecked -m $Runner --check-only
Write-Output 'PHASE176_R3R53_GATE=PASS_R3R53_DRYRUN'
if ($DryRun) { Write-Output '(END)'; exit 0 }
Invoke-PythonChecked -m "$Package.apply"
$Tests = @(
    "$Package/tests/test_common_kernel.py",
    'phase176_r3r47_finite_cyclic_kernel_frontier/tests/test_frontier.py',
    'phase176_r3r52_complete_renderer_boundary/tests/test_boundary.py',
    'phase168_r3_27_typed_projection/tests/test_phase168_r3_27_typed_projection.py',
    'phase176_r3r51_verified_db_subgroup_lift/tests/test_verified_prior.py'
)
foreach ($Test in $Tests) {
    Write-Output "PHASE176_R3R53_TEST_GROUP=$Test"
    Invoke-PythonChecked -m $Runner $Test
}
Write-Output 'PHASE176_R3R53_GATE=PASS_R3R53_FOCUSED_TESTS'
Invoke-PythonChecked -m "$Package.audit"
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
Write-Output 'PHASE176_R3R53_FULL_PYTEST=NOT_RUN'
Write-Output '(END)'
