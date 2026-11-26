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
    python -B -m phase177_r17r3_rank_two_quotient_display.installer --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Phase177 R17R3 preflight failed' }
    if (-not $DryRun) {
        python -B -m phase177_r17r3_rank_two_quotient_display.installer
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R17R3 installation failed' }
        python -B -m pytest -q -s --import-mode=importlib -p no:cacheprovider phase177_r17r3_rank_two_quotient_display/tests phase177_r17r1_finite_delta_reason_display/tests phase168_r3_27_typed_projection/tests phase177_r14_finite_cyclic_delta_injective_isolated/tests/test_rule.py phase177_r15_finite_cyclic_delta_injective_public/tests/test_public.py phase175_r4r3_two_summand_quotient/tests/test_rule.py
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R17R3 focused tests failed; hook retained for inspection' }
        python -B -m phase177_r17r3_rank_two_quotient_display.installer --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R17R3 postflight failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R17R3 git diff check failed' }
        Write-Output 'PHASE177_R17R3_NEW_MATH_RULES=0'
        Write-Output 'PHASE177_R17R3_NEW_GIVEN=0'
        Write-Output 'PHASE177_R17R3_FULL_PYTEST=NOT_RUN'
        Write-Output 'PHASE177_R17R3_GATE=PASS_R17R3_RANK_TWO_QUOTIENT_DISPLAY'
    }
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTHONUTF8 = $oldUtf8
    Pop-Location
}
