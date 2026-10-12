$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 (Join-Path $PSScriptRoot 'audit.py')
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python (Join-Path $PSScriptRoot 'audit.py')
} else {
    throw 'Python 3 was not found.'
}
if ($LASTEXITCODE -ne 0) { throw "Audit failed: $LASTEXITCODE" }
Write-Host 'R6 read-only audit complete. Full pytest NOT run.'
