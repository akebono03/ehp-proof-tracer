$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Set-Location $root
python (Join-Path $folder 'apply.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q (Join-Path $folder 'test_installer.py') (Join-Path $folder 'test_patch.py')
exit $LASTEXITCODE
