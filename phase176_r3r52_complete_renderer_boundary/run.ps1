param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$Package = 'phase176_r3r52_complete_renderer_boundary'
$Runner = 'phase176_r3r46r1_prior_group_availability.pytest_runner'
function Invoke-PythonChecked {
    & python -B @args
    if ($LASTEXITCODE -ne 0) { throw "Python failed ($LASTEXITCODE): $args" }
}
Invoke-PythonChecked -m $Runner --check-only
Invoke-PythonChecked -m "$Package.audit" --dry-run
if ($DryRun) { Write-Output '(END)'; exit 0 }
$Tests = @(
    "$Package/tests/test_boundary.py",
    'phase176_r3r47_finite_cyclic_kernel_frontier/tests/test_frontier.py',
    'phase176_r3r51_verified_db_subgroup_lift/tests/test_verified_prior.py'
)
foreach ($Test in $Tests) {
    Write-Output "PHASE176_R3R52_TEST_GROUP=$Test"
    Invoke-PythonChecked -m $Runner $Test
}
Write-Output 'PHASE176_R3R52_GATE=PASS_R3R52_FOCUSED_TESTS'
Invoke-PythonChecked -m "$Package.audit"
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
Write-Output 'PHASE176_R3R52_FULL_PYTEST=NOT_RUN'
Write-Output '(END)'
