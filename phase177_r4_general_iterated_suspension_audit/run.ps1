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
    $before = @(git status --porcelain --untracked-files=all) -join "`n"
    if ($LASTEXITCODE -ne 0) { throw 'git status failed' }
    python -B -m phase177_r4_general_iterated_suspension_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Phase177 R4 preflight failed' }
    if (-not $DryRun) {
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase177_r4_general_iterated_suspension_audit/tests phase169_r10eq_r1_universal_stable_definition/tests/test_r10eq_stable_definition.py
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R4 focused tests failed' }
        python -B -m phase177_r4_general_iterated_suspension_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R4 audit failed' }
    }
    $after = @(git status --porcelain --untracked-files=all) -join "`n"
    if ($LASTEXITCODE -ne 0 -or $before -cne $after) { throw 'Phase177 R4 repository status changed' }
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $previousBytecode
    $env:PYTHONUTF8 = $previousUtf8
    Pop-Location
}
