param(
    [switch]$DryRun,
    [switch]$RunFocusedTests
)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    if ($DryRun -and $RunFocusedTests) {
        throw 'Specify either -DryRun or -RunFocusedTests.'
    }
    if (-not $DryRun -and -not $RunFocusedTests) {
        throw 'Specify -DryRun or -RunFocusedTests.'
    }
    if ($DryRun) {
        python -B -m phase172_r5_prior_reference_display.install --dry-run
    }
    else {
        python -B -m phase172_r5_prior_reference_display.install --run-focused-tests
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 R5 failed with exit code $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}
