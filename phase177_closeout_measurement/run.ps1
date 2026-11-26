param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
if ($DryRun) {
    & python -B -m phase177_closeout_measurement.gate --dry-run
} else {
    & python -B -m phase177_closeout_measurement.gate
}
if ($LASTEXITCODE -ne 0) { throw "Phase 177 measurement gate failed: $LASTEXITCODE" }
