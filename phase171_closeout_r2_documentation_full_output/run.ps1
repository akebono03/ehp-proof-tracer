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
        & python -B (Join-Path $PSScriptRoot "update_docs.py") --dry-run
    }
    else {
        & python -B (Join-Path $PSScriptRoot "update_docs.py")
    }
    $Result = $LASTEXITCODE
    if ($Result -ne 0) {
        throw "Phase 171 Closeout R2 full-document update failed with exit $Result"
    }
}
finally {
    Set-Location $Previous
}
