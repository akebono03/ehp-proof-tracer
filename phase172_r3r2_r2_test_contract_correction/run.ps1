param(
    [switch]$DryRun,
    [switch]$RunFocusedTests
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldLocation = (Get-Location).Path
$OldPath = $env:PYTHONPATH
$OldUtf8 = $env:PYTHONUTF8
$OldEncoding = $env:PYTHONIOENCODING
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE

try {
    Set-Location $Root
    $env:PYTHONPATH = "$Root;$OldPath"
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $Arguments = @('-B', '-m', 'phase172_r3r2_r2_test_contract_correction.install')
    if ($DryRun) {
        $Arguments += '--dry-run'
    }
    if ($RunFocusedTests) {
        $Arguments += '--run-focused-tests'
    }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 R3R2 failed with exit code $LASTEXITCODE"
    }
}
finally {
    Set-Location $OldLocation
    $env:PYTHONPATH = $OldPath
    $env:PYTHONUTF8 = $OldUtf8
    $env:PYTHONIOENCODING = $OldEncoding
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
}
