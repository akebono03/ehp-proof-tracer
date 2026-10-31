param(
    [switch]$DryRun,
    [switch]$RunCloseout
)
$ErrorActionPreference = 'Stop'
if ($DryRun -eq $RunCloseout) {
    throw 'Select exactly one of -DryRun or -RunCloseout'
}
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    if ($DryRun) {
        python -B -m phase172_r6_phase_closeout.audit --dry-run
    } else {
        python -B -m phase172_r6_phase_closeout.audit --run-closeout
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 R6 closeout gate failed with exit code $LASTEXITCODE"
    }
} finally {
    Pop-Location
}
