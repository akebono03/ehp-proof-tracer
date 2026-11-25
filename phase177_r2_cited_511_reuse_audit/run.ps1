param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
$previousBytecode = $env:PYTHONDONTWRITEBYTECODE
$previousUtf8 = $env:PYTHONUTF8
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONUTF8 = '1'
    if ($DryRun) {
        python -B -m phase177_r2_cited_511_reuse_audit.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R2 DryRun failed' }
    } else {
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase177_r2_cited_511_reuse_audit/tests
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R2 focused tests failed' }
        python -B -m phase177_r2_cited_511_reuse_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R2 audit failed' }
    }
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $previousBytecode
    $env:PYTHONUTF8 = $previousUtf8
    Pop-Location
}
