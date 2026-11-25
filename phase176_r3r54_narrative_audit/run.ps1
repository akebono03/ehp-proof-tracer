param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$Package = 'phase176_r3r54_narrative_audit'
$Runner = 'phase176_r3r46r1_prior_group_availability.pytest_runner'
function Invoke-PythonChecked {
    & python -B @args
    if ($LASTEXITCODE -ne 0) { throw "Python failed ($LASTEXITCODE): $args" }
}
Invoke-PythonChecked -m "$Package.audit" --dry-run
Invoke-PythonChecked -m $Runner --check-only
if ($DryRun) { Write-Output '(END)'; exit 0 }
$Tests = @(
    "$Package/tests/test_audit.py",
    'phase176_r3r53_common_kernel_renderer/tests/test_common_kernel.py',
    'phase176_r3r53r1_historical_kernel_test/tests/test_patch.py',
    'phase168_r3_27_typed_projection/tests/test_phase168_r3_27_typed_projection.py'
)
foreach ($Test in $Tests) {
    Write-Output "PHASE176_R3R54_TEST_GROUP=$Test"
    Invoke-PythonChecked -m $Runner $Test
}
Invoke-PythonChecked -m "$Package.audit"
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
Write-Output '(END)'
