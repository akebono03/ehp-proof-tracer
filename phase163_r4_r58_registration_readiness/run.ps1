$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$trial = Join-Path $root 'phase163_r4_r55_output\trial.json'
$scope = Join-Path $root 'phase163_r4_r56_output\scope.json'
$boundary = Join-Path $root 'phase163_r4_r57_output\boundary.json'
$output = Join-Path $root 'phase163_r4_r58_output'
foreach ($path in @($trial, $scope, $boundary)) {
    if (-not (Test-Path -LiteralPath $path)) { throw "Missing input: $path" }
}
$env:PYTHONPATH = "$package;$root"
$env:R58_TRIAL_PATH = $trial
$env:R58_SCOPE_PATH = $scope
$env:R58_BOUNDARY_PATH = $boundary
python -m pytest -q "$package\tests\test_phase163_r4_r58_registration_readiness.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$package\phase163_r4_r58_registration_readiness.py" --trial "$trial" --scope "$scope" --boundary "$boundary" --output "$output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R4-R58 readiness audit complete. No production changes. Full pytest not run.'
