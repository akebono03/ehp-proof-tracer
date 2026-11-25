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
    python -B -m phase177_r12_reassociation_transitivity_public.installer --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Phase177 R12 preflight failed' }
    if (-not $DryRun) {
        python -B -m phase177_r12_reassociation_transitivity_public.installer
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R12 install failed' }
        python -B -m pytest -q -s --import-mode=importlib -p no:cacheprovider phase177_r12_reassociation_transitivity_public/tests phase177_r11_composition_associativity_public/tests phase177_r10_composition_associativity_isolated/tests/test_rule.py phase177_r8_unsigned_delta_public/tests/test_public.py
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R12 focused tests failed; installed hook remains for inspection' }
        python -B -m phase177_r12_reassociation_transitivity_public.installer --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R12 postflight failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R12 git diff check failed' }
        Write-Output 'PHASE177_R12_NEW_MATH_RULES=0'
        Write-Output 'PHASE177_R12_NEW_GIVEN=0'
        Write-Output 'PHASE177_R12_TRANSITIVITY_CONNECTION=ADDED'
        Write-Output 'PHASE177_R12_FULL_PYTEST=NOT_RUN'
        Write-Output 'PHASE177_R12_GATE=PASS_R12_REASSOCIATION_TRANSITIVITY_PUBLIC'
    }
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $previousBytecode
    $env:PYTHONUTF8 = $previousUtf8
    Pop-Location
}
