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
    python -B -m phase177_r11_composition_associativity_public.installer --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Phase177 R11 preflight failed' }
    if (-not $DryRun) {
        python -B -m phase177_r11_composition_associativity_public.installer
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R11 install failed' }
        python -B -m pytest -q -s --import-mode=importlib -p no:cacheprovider phase177_r11_composition_associativity_public/tests phase177_r10_composition_associativity_isolated/tests/test_rule.py phase174_r3_r7_r9_composition_associativity/tests/test_rule.py phase177_r8_unsigned_delta_public/tests/test_public.py
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R11 focused tests failed; installed hook remains for inspection' }
        python -B -m phase177_r11_composition_associativity_public.installer --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R11 postflight failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R11 git diff check failed' }
        Write-Output 'PHASE177_R11_NEW_MATH_RULES=0'
        Write-Output 'PHASE177_R11_NEW_GIVEN=0'
        Write-Output 'PHASE177_R11_TRANSITIVITY_CONNECTION=NOT_ADDED'
        Write-Output 'PHASE177_R11_FULL_PYTEST=NOT_RUN'
        Write-Output 'PHASE177_R11_GATE=PASS_R11_COMPOSITION_ASSOCIATIVITY_PUBLIC'
    }
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $previousBytecode
    $env:PYTHONUTF8 = $previousUtf8
    Pop-Location
}
