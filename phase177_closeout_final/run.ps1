param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$Package = 'phase177_closeout_final'
if ($DryRun) {
    python -B -m "$Package.gate" --dry-run
} else {
    python -B -m "$Package.gate"
}
if ($LASTEXITCODE -ne 0) { throw "Phase177 final document gate failed ($LASTEXITCODE)" }
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
