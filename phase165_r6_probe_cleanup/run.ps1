$ErrorActionPreference = 'Stop'
$project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $project
try {
    python (Join-Path $PSScriptRoot 'cleanup.py') $project
    if ($LASTEXITCODE -ne 0) { throw "Probe cleanup failed: $LASTEXITCODE" }
    python -m pytest -q (Join-Path $PSScriptRoot 'tests\test_cleanup.py')
    if ($LASTEXITCODE -ne 0) { throw "Cleanup tool tests failed: $LASTEXITCODE" }
    Write-Host 'R6 scoped cleanup completed. Full pytest NOT run. Phase closure PENDING.'
} finally {
    Pop-Location
}
