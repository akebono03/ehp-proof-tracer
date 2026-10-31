param(
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Previous = (Get-Location).Path

try {
    Set-Location $Root
    $env:PYTHONUTF8 = "1"
    $env:PYTHONDONTWRITEBYTECODE = "1"
    if ($DryRun) {
        & python -B (Join-Path $PSScriptRoot "audit.py") --root $Root
    }
    else {
        & python -B (Join-Path $PSScriptRoot "audit.py") --root $Root --run-focused
    }
    $PythonExitCode = $LASTEXITCODE
    if ($PythonExitCode -ne 0) {
        throw "Phase 171 Closeout R1 audit exited with code $PythonExitCode"
    }
}
finally {
    Set-Location $Previous
}
