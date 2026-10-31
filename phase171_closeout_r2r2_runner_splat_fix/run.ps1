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
            (Join-Path $PSScriptRoot "tests\test_repair.py")
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 171 R2R2 runner tests failed"
        }
    }
    $PythonArguments = @("-B", (Join-Path $PSScriptRoot "repair.py"))
    if ($DryRun) {
        $PythonArguments += "--dry-run"
    }
    & python @PythonArguments
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 171 R2R2 runner repair failed"
    }
    if ($DryRun) {
        & python -B ".\phase171_closeout_r2r1_committed_head_guard\install.py" --dry-run
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 171 R2R1 preflight failed"
        }
    }
    else {
        & powershell -NoProfile -ExecutionPolicy Bypass `
            -File ".\phase171_closeout_r2r1_committed_head_guard\run.ps1"
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 171 R2R1 document closeout failed"
        }
    }
}
finally {
    Set-Location $Previous
}
