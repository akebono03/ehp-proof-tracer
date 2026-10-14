$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python (Join-Path $PSScriptRoot 'apply.py')
    if ($LASTEXITCODE -ne 0) { throw 'R59 installer failed' }
    python -m pytest -q (Join-Path $PSScriptRoot 'test_installer.py')
    if ($LASTEXITCODE -ne 0) { throw 'R59 targeted tests failed' }
    Write-Host 'R27-R59 targeted checks complete; full pytest NOT run.'
} finally { Pop-Location }
