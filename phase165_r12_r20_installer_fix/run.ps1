$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$root;$package"
python "$package\install.py"
if ($LASTEXITCODE -ne 0) { throw 'R12-R20 installation failed' }
python -m pytest -q "$package\tests\test_phase165_r12_r20_eta_definition.py" "$package\tests\test_r12_r20_installer_fix.py"
if ($LASTEXITCODE -ne 0) { throw 'R12-R20 pytest failed' }
python "$package\audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R12-R20 audit failed' }
Write-Host 'R12-R20 focused checks completed; full pytest NOT run.'
