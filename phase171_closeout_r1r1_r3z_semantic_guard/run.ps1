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
        & python -B (Join-Path $PSScriptRoot "install.py") --dry-run
    }
    else {
        & python -B (Join-Path $PSScriptRoot "install.py")
    }
    $Code = $LASTEXITCODE
    if ($Code -ne 0) {
        throw "Phase 171 R1R1 guarded test correction failed with exit $Code"
    }
}
finally {
    Set-Location $Previous
}
