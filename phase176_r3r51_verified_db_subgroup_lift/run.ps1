param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$Package = 'phase176_r3r51_verified_db_subgroup_lift'
$Runner = 'phase176_r3r46r1_prior_group_availability.pytest_runner'
function Invoke-PythonChecked {
    & python -B @args
    if ($LASTEXITCODE -ne 0) { throw "Python failed ($LASTEXITCODE): $args" }
}
Invoke-PythonChecked -m "$Package.apply" --dry-run
Invoke-PythonChecked -m $Runner --check-only
Write-Output 'PHASE176_R3R51_GATE=PASS_R3R51_DRYRUN'
if ($DryRun) { Write-Output '(END)'; exit 0 }
& python -B -c "from $Package.apply import planned_changes; p=planned_changes(); raise SystemExit(0 if any(a!=b for a,b in p.values()) else 3)"
$State = $LASTEXITCODE
if ($State -eq 0) {
    Invoke-PythonChecked -m "$Package.audit" --baseline
} elseif ($State -eq 3) {
    Write-Output 'PHASE176_R3R51_BASELINE=SKIPPED_ALREADY_APPLIED'
} else { throw "Unable to determine patch state ($State)" }
Invoke-PythonChecked -m "$Package.apply"
$Tests = @(
    "$Package/tests/test_verified_prior.py",
    'phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated/tests/test_finite_cyclic_subgroup_lift.py',
    'phase176_r3r44_public_subgroup_lift/tests/test_public_subgroup_lift.py',
    'phase176_r3r48_cited_finite_delta_kernel/tests/test_rule.py',
    'phase176_r3r49_hopf_image_frontier/tests/test_frontier.py',
    'phase176_r3r50_strict_nu_prime_connection/tests/test_notation_connection.py'
)
foreach ($Test in $Tests) {
    Write-Output "PHASE176_R3R51_TEST_GROUP=$Test"
    Invoke-PythonChecked -m $Runner $Test
}
Write-Output 'PHASE176_R3R51_GATE=PASS_R3R51_FOCUSED_TESTS'
Invoke-PythonChecked -m "$Package.audit"
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
Write-Output 'PHASE176_R3R51_FULL_PYTEST=NOT_RUN'
Write-Output '(END)'
