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
    python -B -m phase177_r6_general_suspension_public.installer --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Phase177 R6 preflight failed' }
    if (-not $DryRun) {
        python -B -m phase177_r6_general_suspension_public.installer
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R6 install failed' }
        python -B -m pytest -q -s --import-mode=importlib -p no:cacheprovider phase177_r6_general_suspension_public/tests phase177_r5_general_suspension_equality_isolated/tests/test_rule.py phase177_r4_general_iterated_suspension_audit/tests/test_audit.py
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R6 focused tests failed; installed hook remains for inspection' }
        python -B -m phase177_r6_general_suspension_public.installer --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R6 postflight failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R6 git diff check failed' }
        Write-Output 'PHASE177_R6_NEW_MATH_RULES=0'
        Write-Output 'PHASE177_R6_NEW_GIVEN=0'
        Write-Output 'PHASE177_R6_DELTA_CONNECTION=NOT_ADDED'
        Write-Output 'PHASE177_R6_FULL_PYTEST=NOT_RUN'
        Write-Output 'PHASE177_R6_GATE=PASS_R6_GENERAL_SUSPENSION_EQUALITY_PUBLIC'
    }
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $previousBytecode
    $env:PYTHONUTF8 = $previousUtf8
    Pop-Location
}
