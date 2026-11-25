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
    python -B -m phase177_r5_general_suspension_equality_isolated.audit
    if ($LASTEXITCODE -ne 0) { throw 'Phase177 R5 preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE177_R5_GATE=PASS_R5_READ_ONLY_DRYRUN'
    } else {
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase177_r5_general_suspension_equality_isolated/tests phase176_r3r34_composite_suspension_isolated/tests/test_source.py phase177_r4_general_iterated_suspension_audit/tests/test_audit.py
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R5 focused tests failed' }
        python -B -m phase177_r5_general_suspension_equality_isolated.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R5 postflight failed' }
        $after = @(git status --porcelain --untracked-files=all) -join "`n"
        if ($LASTEXITCODE -ne 0 -or $before -cne $after) { throw 'Phase177 R5 repository status changed' }
        Write-Output 'PHASE177_R5_GATE=PASS_R5_GENERAL_SUSPENSION_EQUALITY_ISOLATED'
    }
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $previousBytecode
    $env:PYTHONUTF8 = $previousUtf8
    Pop-Location
}
