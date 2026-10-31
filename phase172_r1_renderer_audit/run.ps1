param(
    [switch]$DryRun,
    [switch]$RunFocusedTests
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldLocation = (Get-Location).Path
$OldPythonPath = $env:PYTHONPATH
$OldPythonUtf8 = $env:PYTHONUTF8
$OldPythonEncoding = $env:PYTHONIOENCODING
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE
$OldNoCache = $env:PYTEST_ADDOPTS
try {
    Set-Location $Root
    $env:PYTHONPATH = "$Root;$OldPythonPath"
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = ''
    $PythonArguments = @('-B', '-m', 'phase172_r1_renderer_audit.audit')
    if ($DryRun) { $PythonArguments += '--dry-run' }
    if ($RunFocusedTests) { $PythonArguments += '--run-focused-tests' }
    & python @PythonArguments
    $ExitCode = $LASTEXITCODE
    if ($ExitCode -ne 0) { throw "Phase 172 R1 audit failed: exit $ExitCode" }
}
finally {
    Set-Location $OldLocation
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONUTF8 = $OldPythonUtf8
    $env:PYTHONIOENCODING = $OldPythonEncoding
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
    $env:PYTEST_ADDOPTS = $OldNoCache
}
