param([switch]$Repair)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$projectRoot = (Get-Location).Path
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path -LiteralPath (Join-Path $projectRoot '.git'))) {
    throw 'Run this from the EHP Proof Tracer repository root.'
}
$env:PYTHONDONTWRITEBYTECODE = '1'
if (-not $Repair) {
    python -B -m pytest -p no:cacheprovider -q (Join-Path $scriptRoot 'tests')
    if ($LASTEXITCODE -ne 0) { throw 'R1 tests failed' }
}
$arguments = @('-B', (Join-Path $scriptRoot 'recovery.py'), '--root', $projectRoot)
if ($Repair) { $arguments += '--repair' }
& python @arguments
if ($LASTEXITCODE -ne 0) {
    throw "R1 diagnostic returned code $LASTEXITCODE; review the printed status. No branch reset performed."
}
