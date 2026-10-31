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
    $PythonArguments = @("-B", (Join-Path $PSScriptRoot "repair.py"))
    if ($DryRun) {
        $PythonArguments += "--dry-run"
    }
    & python @PythonArguments
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 171 Closeout R2R4 failed with exit $LASTEXITCODE"
    }
}
finally {
    Set-Location $Previous
}
