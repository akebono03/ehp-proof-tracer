$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python (Join-Path $PSScriptRoot 'install.py')
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -m pytest -q (Join-Path $PSScriptRoot 'test_sigma_power.py')
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host 'Targeted pytest PASS; full pytest NOT run.'
}
finally { Pop-Location }
