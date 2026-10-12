$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo
$python = 'python'
& $python -m pytest -q '.\phase164_r7_r2_path_inventory\test_audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R7-R2 audit unit tests failed; project was not modified.' }
& $python '.\phase164_r7_r2_path_inventory\audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R7-R2 static audit failed; see audit output.' }
