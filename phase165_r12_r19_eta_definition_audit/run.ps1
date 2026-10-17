$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$source = Join-Path $package 'phase165_r12_r19_eta_definition_audit.py'
$target = Join-Path $root 'phase165_r12_r19_eta_definition_audit.py'
if ((Test-Path $target) -and ((Get-FileHash $target).Hash -ne (Get-FileHash $source).Hash)) {
    throw 'Existing R12-R19 audit module differs; refusing overwrite'
}
Copy-Item -LiteralPath $source -Destination $target -Force
$env:PYTHONPATH = $root
python -m pytest -q (Join-Path $package 'tests/test_phase165_r12_r19_eta_definition_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R19 targeted pytest failed' }
python (Join-Path $package 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R19 audit failed' }
Write-Host 'R12-R19 eta-definition audit complete. Full pytest NOT run.'
