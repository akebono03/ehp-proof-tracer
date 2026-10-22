$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
$env:PYTHONPATH = $root
python (Join-Path $PSScriptRoot 'run_tests.py')
$code = $LASTEXITCODE
Write-Host "pytest exit code: $code"
if ($code -ne 0) {
    Write-Host 'Full pytest did not pass. See pytest_full.log and pytest_status.json.'
}
exit $code
