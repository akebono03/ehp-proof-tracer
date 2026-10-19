$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
Write-Host 'Phase 165 R6: bounded focused check (no full collection)' -ForegroundColor Cyan
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 "$PSScriptRoot\check.py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python "$PSScriptRoot\check.py"
} else {
    throw 'Python 3 was not found on PATH.'
}
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
