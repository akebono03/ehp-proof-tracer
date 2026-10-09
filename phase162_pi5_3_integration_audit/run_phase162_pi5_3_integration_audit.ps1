$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $repoRoot
python -m pytest -q (Join-Path $PSScriptRoot 'test_phase162_pi5_3_integration_audit.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Focused integration audit passed. Full suite not run.'
