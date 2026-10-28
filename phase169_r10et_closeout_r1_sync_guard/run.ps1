$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    & python -B (Join-Path $PSScriptRoot 'audit.py') --repo $Repo
    $Code = $LASTEXITCODE
    exit $Code
} finally {
    Pop-Location
}
