$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoDir = Split-Path -Parent $scriptDir
Push-Location $repoDir
try {
    python -m pytest -q "$scriptDir\test_audit.py"
    if ($LASTEXITCODE -ne 0) { throw "Targeted pytest failed" }
    python "$scriptDir\audit.py"
    if ($LASTEXITCODE -ne 0) { throw "Read-only audit failed" }
    Write-Host 'R24 retirement gate completed; production unchanged; full pytest NOT run.'
} finally { Pop-Location }
