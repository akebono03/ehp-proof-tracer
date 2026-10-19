$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
$env:PYTHONPATH = $root
python -m pytest -q (Join-Path $PSScriptRoot 'tests\test_cleanup.py')
if ($LASTEXITCODE -ne 0) { throw 'Safety tests failed' }
python (Join-Path $PSScriptRoot 'cleanup.py') --root $root
if ($LASTEXITCODE -ne 0) { throw 'Cleanup stopped' }
Write-Host 'Now re-collecting tests (test bodies are NOT executed).'
python (Join-Path $root 'phase165_r6_recollect\recollect.py') --root $root
Write-Host 'If errors remain, closure is PENDING. Full pytest was NOT run.'
