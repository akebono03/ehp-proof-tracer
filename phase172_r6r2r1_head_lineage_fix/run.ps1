param(
    [switch]$DryRun,
    [switch]$Apply
)
$ErrorActionPreference = 'Stop'
if ($DryRun -eq $Apply) {
    throw 'Choose exactly one of -DryRun and -Apply'
}
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $mode = if ($DryRun) { '--dry-run' } else { '--apply' }
    & python -B -m phase172_r6r2r1_head_lineage_fix.fix $mode
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 R6R2R1 correction failed: $LASTEXITCODE"
    }
} finally {
    Pop-Location
}
