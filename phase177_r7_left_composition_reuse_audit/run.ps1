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
    python -B -m phase177_r7_left_composition_reuse_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Phase177 R7 preflight failed' }
    if (-not $DryRun) {
        $before = @(git status --porcelain --untracked-files=all) -join "`n"
        if ($LASTEXITCODE -ne 0) { throw 'git status failed' }
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase177_r7_left_composition_reuse_audit/tests phase176_r3r39_public_equality_transport/tests/test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R7 focused tests failed' }
        python -B -m phase177_r7_left_composition_reuse_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R7 audit failed' }
        $after = @(git status --porcelain --untracked-files=all) -join "`n"
        if ($LASTEXITCODE -ne 0 -or $before -cne $after) { throw 'Phase177 R7 repository status changed' }
    }
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $previousBytecode
    $env:PYTHONUTF8 = $previousUtf8
    Pop-Location
}
