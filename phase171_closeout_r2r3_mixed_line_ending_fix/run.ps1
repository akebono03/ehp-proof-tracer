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
    $Arguments = @("-B", (Join-Path $PSScriptRoot "install.py"))
    if ($DryRun) {
        $Arguments += "--dry-run"
    }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 171 R2R3 full-document patch failed with exit $LASTEXITCODE"
    }
}
finally {
    Set-Location $Previous
}
