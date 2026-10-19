$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python (Join-Path $PSScriptRoot 'verify.py')
    if ($LASTEXITCODE -ne 0) {
        Write-Host 'Verification incomplete. See report.json.'
        exit $LASTEXITCODE
    }
} finally {
    Pop-Location
}
