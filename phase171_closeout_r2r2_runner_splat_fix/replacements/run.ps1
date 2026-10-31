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
    if (-not $DryRun) {
        & python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider `
          (Join-Path $PSScriptRoot "tests\test_install.py")
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 171 Closeout R2R1 installer guard tests failed"
        }
    }
    $PythonArguments = @("-B", (Join-Path $PSScriptRoot "install.py"))
    if ($DryRun) {
        $PythonArguments += "--dry-run"
    }
    & python @PythonArguments
    $Result = $LASTEXITCODE
    if ($Result -ne 0) {
        throw "Phase 171 Closeout R2R1 failed with exit $Result"
    }
}
finally {
    Set-Location $Previous
}
