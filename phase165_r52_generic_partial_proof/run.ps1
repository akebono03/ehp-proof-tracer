$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$src = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item -LiteralPath (Join-Path $src 'phase165_r52_partial_proof.py') -Destination (Join-Path $root 'phase165_r52_partial_proof.py') -Force
Copy-Item -LiteralPath (Join-Path $src 'test_phase165_r52_partial_proof.py') -Destination (Join-Path $root 'test_phase165_r52_partial_proof.py') -Force
python -m pytest -q test_phase165_r52_partial_proof.py
if ($LASTEXITCODE -ne 0) { throw 'R52 targeted pytest failed' }
Write-Host 'R52 common result model and renderer available; full pytest NOT run.'
