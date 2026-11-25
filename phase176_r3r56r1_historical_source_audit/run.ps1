param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$Package = 'phase176_r3r56r1_historical_source_audit'
$Runner = 'phase176_r3r46r1_prior_group_availability.pytest_runner'
function Invoke-PythonChecked {
    & python -B @args
    if ($LASTEXITCODE -ne 0) { throw "Python failed ($LASTEXITCODE): $args" }
}
Invoke-PythonChecked -m "$Package.audit" --dry-run
Invoke-PythonChecked -m $Runner --check-only
if ($DryRun) { exit 0 }
Invoke-PythonChecked -m $Runner "$Package/tests/test_audit.py"
Invoke-PythonChecked -m "$Package.audit"
# Run only after the original two failures have been reproduced without the R55 insertion.
# These are separate checks; the historical suite is NOT declared passing.
Invoke-PythonChecked -m $Runner 'phase176_r3r56_cited_source_display_isolated/tests/test_projection.py'
Invoke-PythonChecked -m $Runner 'phase176_r3r55_equality_display_isolated/tests/test_projection.py'
Invoke-PythonChecked -m $Runner 'phase168_r3_27_typed_projection/tests/test_phase168_r3_27_typed_projection.py'
Invoke-PythonChecked -m phase176_r3r56_cited_source_display_isolated.audit
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
Write-Output 'PHASE176_R3R56R1_GATE=PASS_R3R56R1_DIAGNOSTIC_AND_R56_ISOLATED_AUDIT_HISTORICAL_GUARD_OPEN'
