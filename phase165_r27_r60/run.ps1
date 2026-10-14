$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python -m pytest -q (Join-Path $PSScriptRoot 'test_check.py')
    if ($LASTEXITCODE -ne 0) { throw 'R60 checker tests failed' }
    python (Join-Path $PSScriptRoot 'check.py')
    if ($LASTEXITCODE -ne 0) { throw 'R60 regression checks failed; see phase165_r27_r60_results.json' }
    Write-Host 'R60 focused checks complete; full pytest NOT run.'
} finally { Pop-Location }
