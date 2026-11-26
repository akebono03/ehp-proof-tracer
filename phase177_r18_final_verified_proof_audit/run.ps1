param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$package = 'phase177_r18_final_verified_proof_audit'
if ($DryRun) {
    python -B -m "$package.audit" --dry-run
} else {
    python -B -m "$package.audit"
}
if ($LASTEXITCODE -ne 0) { throw 'R18 audit failed; inspect the printed report' }
