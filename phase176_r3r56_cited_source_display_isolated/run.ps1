param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$Package = 'phase176_r3r56_cited_source_display_isolated'
$Runner = 'phase176_r3r46r1_prior_group_availability.pytest_runner'
function Invoke-PythonChecked {
    & python -B @args
    if ($LASTEXITCODE -ne 0) { throw "Python failed ($LASTEXITCODE): $args" }
}
Invoke-PythonChecked -m "$Package.audit" --dry-run
Invoke-PythonChecked -m $Runner --check-only
if ($DryRun) { Write-Output '(END)'; exit 0 }
$Tests = @(
    "$Package/tests/test_projection.py",
    'phase175_r3r11_cited_hopf_narrative/tests/test_projection.py',
    'phase176_r3r55_equality_display_isolated/tests/test_projection.py',
    'phase168_r3_27_typed_projection/tests/test_phase168_r3_27_typed_projection.py'
)
foreach ($Test in $Tests) {
    Write-Output "PHASE176_R3R56_TEST_GROUP=$Test"
    Invoke-PythonChecked -m $Runner $Test
}
Invoke-PythonChecked -m "$Package.audit"
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
Write-Output '(END)'
