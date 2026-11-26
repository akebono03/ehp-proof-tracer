param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldUtf8 = $env:PYTHONUTF8
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONUTF8 = '1'
    python -B -m phase177_r15_finite_cyclic_delta_injective_public.installer --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Phase177 R15 preflight failed' }
    if (-not $DryRun) {
        python -B -m phase177_r15_finite_cyclic_delta_injective_public.installer
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R15 installation failed' }
        python -B -m pytest -q -s --import-mode=importlib -p no:cacheprovider phase177_r15_finite_cyclic_delta_injective_public/tests phase177_r14_finite_cyclic_delta_injective_isolated/tests/test_rule.py phase175_r4r12r9_delta_generator_image_bridge/tests/test_rule.py phase175_r4r12r13r2_delta_injective_e_surjective/tests/test_rule.py phase175_r4r12r13r4_hopf_zero_public/tests/test_rule.py phase175_r4r3_two_summand_quotient/tests/test_rule.py
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R15 focused tests failed; hook retained for inspection' }
        python -B -m phase177_r15_finite_cyclic_delta_injective_public.installer --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R15 postflight failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R15 git diff check failed' }
        Write-Output 'PHASE177_R15_NEW_MATH_RULES=0'
        Write-Output 'PHASE177_R15_NEW_GIVEN=0'
        Write-Output 'PHASE177_R15_FULL_PYTEST=NOT_RUN'
        Write-Output 'PHASE177_R15_GATE=PASS_R15_FINITE_CYCLIC_DELTA_INJECTIVITY_PUBLIC'
    }
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTHONUTF8 = $oldUtf8
    Pop-Location
}
