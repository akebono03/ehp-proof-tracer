param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$package = 'phase177_r17r4r2r1_chain_boundary_audit'
if ($DryRun) {
    python -B -m "$package.audit" --dry-run
} else {
    python -B -m "$package.audit"
}
if ($LASTEXITCODE -ne 0) { throw 'R17R4R2R1 audit failed' }
git diff --check
if ($LASTEXITCODE -ne 0) { throw 'R17R4R2R1 diff check failed' }
