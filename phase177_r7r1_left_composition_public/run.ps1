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
    python -B -m phase177_r7r1_left_composition_public.installer --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Phase177 R7R1 preflight failed' }
    if (-not $DryRun) {
        python -B -m phase177_r7r1_left_composition_public.installer
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R7R1 install failed' }
        python -B -m pytest -q -s --import-mode=importlib -p no:cacheprovider phase177_r7r1_left_composition_public/tests phase177_r7_left_composition_reuse_audit/tests phase177_r6_general_suspension_public/tests/test_public.py phase176_r3r39_public_equality_transport/tests/test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R7R1 focused tests failed; installed hook remains for inspection' }
        python -B -m phase177_r7r1_left_composition_public.installer --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R7R1 postflight failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R7R1 git diff check failed' }
        Write-Output 'PHASE177_R7R1_NEW_MATH_RULES=0'
        Write-Output 'PHASE177_R7R1_NEW_GIVEN=0'
        Write-Output 'PHASE177_R7R1_DELTA_CONNECTION=NOT_ADDED'
        Write-Output 'PHASE177_R7R1_FULL_PYTEST=NOT_RUN'
        Write-Output 'PHASE177_R7R1_GATE=PASS_R7R1_GENERAL_LEFT_COMPOSITION_PUBLIC'
    }
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $previousBytecode
    $env:PYTHONUTF8 = $previousUtf8
    Pop-Location
}
