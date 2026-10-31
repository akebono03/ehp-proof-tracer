param(
    [switch]$DryRun,
    [switch]$RunFocusedTests
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PreviousLocation = (Get-Location).Path
$PreviousPythonPath = $env:PYTHONPATH
$PreviousPythonUtf8 = $env:PYTHONUTF8
$PreviousPythonIoEncoding = $env:PYTHONIOENCODING
$PreviousDontWriteBytecode = $env:PYTHONDONTWRITEBYTECODE

try {
    Set-Location $Root
    $env:PYTHONPATH = "$Root;$PreviousPythonPath"
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $Arguments = @('-B', '-m', 'phase172_r2_suspension_relation_display.install')
    if ($DryRun) {
        $Arguments += '--dry-run'
    }
    if ($RunFocusedTests) {
        $Arguments += '--run-focused-tests'
    }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 R2 failed with exit code $LASTEXITCODE"
    }
}
finally {
    Set-Location $PreviousLocation
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONUTF8 = $PreviousPythonUtf8
    $env:PYTHONIOENCODING = $PreviousPythonIoEncoding
    $env:PYTHONDONTWRITEBYTECODE = $PreviousDontWriteBytecode
}
