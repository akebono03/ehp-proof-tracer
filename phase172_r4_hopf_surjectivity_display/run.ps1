param(
    [switch]$DryRun,
    [switch]$RunFocusedTests
)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $env:PYTHONUTF8 = '1'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $arguments = @('-B', '-m', 'phase172_r4_hopf_surjectivity_display.install')
    if ($DryRun) { $arguments += '--dry-run' }
    if ($RunFocusedTests) { $arguments += '--run-focused-tests' }
    & python @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 R4 failed with exit code $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}
