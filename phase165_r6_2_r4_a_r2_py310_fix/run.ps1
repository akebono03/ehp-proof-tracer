$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = $PSScriptRoot
if (-not (Test-Path (Join-Path $root 'phase165_r8_rule_provider.py'))) {
    throw 'Run from the ehp_proof repository root.'
}
$env:PYTHONDONTWRITEBYTECODE = '1'
python -B -m pytest -q -p no:cacheprovider (Join-Path $package 'test_runtime_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-A-R2 Python310 fix targeted tests failed.' }
python -B (Join-Path $package 'runtime_audit.py') --root $root --out (Join-Path $package 'reports')
if ($LASTEXITCODE -ne 0) { throw 'R4-A-R2 Python310 fix audit failed.' }
Write-Output 'Full pytest NOT run. Production source files unchanged.'
