param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$Package = 'phase176_closeout'
$Runner = 'phase176_r3r46r1_prior_group_availability.pytest_runner'
function Invoke-PythonChecked {
    & python -B @args
    if ($LASTEXITCODE -ne 0) { throw "Python failed ($LASTEXITCODE): $args" }
}
Invoke-PythonChecked -m "$Package.gate" --dry-run
Invoke-PythonChecked -m $Runner --check-only
if ($DryRun) { exit 0 }
Invoke-PythonChecked -m $Runner "$Package/tests/test_gate.py"
Invoke-PythonChecked -m $Runner 'phase176_r3r60r2_public_citation_premise_elision/tests/test_connection.py'
Invoke-PythonChecked -m "$Package.gate"
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
