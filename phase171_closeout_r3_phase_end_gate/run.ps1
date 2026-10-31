param(
    [switch]$DryRun,
    [string]$ResumeReport = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldLocation = (Get-Location).Path
$OldPythonPath = $env:PYTHONPATH
$OldPythonUtf8 = $env:PYTHONUTF8
$OldPythonEncoding = $env:PYTHONIOENCODING
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE

try {
    Set-Location $Root
    $env:PYTHONPATH = "$Root;$OldPythonPath"
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $PythonArguments = @('-B', (Join-Path $PSScriptRoot 'closeout.py'), '--root', $Root)
    if ($DryRun) {
        $PythonArguments += '--dry-run'
    }
    if ($ResumeReport -ne '') {
        $PythonArguments += @('--resume-report', $ResumeReport)
    }
    & python @PythonArguments
    $ExitCode = $LASTEXITCODE
    if ($ExitCode -ne 0) {
        throw "Phase 171 final closeout did not pass: exit $ExitCode"
    }
}
finally {
    Set-Location $OldLocation
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONUTF8 = $OldPythonUtf8
    $env:PYTHONIOENCODING = $OldPythonEncoding
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
}
