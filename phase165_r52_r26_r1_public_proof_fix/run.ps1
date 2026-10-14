$ErrorActionPreference = 'Stop'
$package = $PSScriptRoot
$root = Split-Path -Parent $package
python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$env:PYTHONPATH = "$package;$root" + $(if ($env:PYTHONPATH) { ";$env:PYTHONPATH" } else { '' })
python -m pytest -q (Join-Path $package 'test_r26_r1_public_proof_fix.py') (Join-Path $root 'test_phase165_r52_r9_shared_math.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R26-R1 targeted tests passed; full pytest NOT run.'
