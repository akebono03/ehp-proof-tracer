param(
    [switch]$DryRun,
    [switch]$RunFocusedTests
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldLocation = (Get-Location).Path
$OldPythonPath = $env:PYTHONPATH
$OldUTF8 = $env:PYTHONUTF8
$OldIOEncoding = $env:PYTHONIOENCODING
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE
try {
    Set-Location $Root
    $env:PYTHONPATH = "$Root;$OldPythonPath"
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $Arguments = @('-B', '-m', 'phase172_r3r1r1_committed_renderer_guard_fix.install')
    if ($DryRun) { $Arguments += '--dry-run' }
    if ($RunFocusedTests) { $Arguments += '--run-focused-tests' }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 R3R1R1 failed with exit code $LASTEXITCODE"
    }
}
finally {
    Set-Location $OldLocation
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONUTF8 = $OldUTF8
    $env:PYTHONIOENCODING = $OldIOEncoding
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
}
