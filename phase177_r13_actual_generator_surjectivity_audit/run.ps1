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
    python -B -m phase177_r13_actual_generator_surjectivity_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Phase177 R13 preflight failed' }
    if (-not $DryRun) {
        python -B -m phase177_r13_actual_generator_surjectivity_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R13 audit failed' }
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase175_r4r12r9_delta_generator_image_bridge/tests/test_rule.py phase175_r4r12r13r2_delta_injective_e_surjective/tests/test_rule.py phase175_r4r12r13r4_hopf_zero_public/tests/test_rule.py phase175_r4r3_two_summand_quotient/tests/test_rule.py
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R13 focused tests failed' }
        python -B -m phase177_r13_actual_generator_surjectivity_audit.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R13 postflight failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R13 git diff check failed' }
        Write-Output 'PHASE177_R13_NEW_MATH_RULES=0'
        Write-Output 'PHASE177_R13_NEW_GIVEN=0'
        Write-Output 'PHASE177_R13_FULL_PYTEST=NOT_RUN'
        Write-Output 'PHASE177_R13_GATE=PASS_R13_ACTUAL_GENERATOR_IMAGE_AND_SURJECTIVITY_FRONTIER_AUDITED'
    }
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $previousBytecode
    $env:PYTHONUTF8 = $previousUtf8
    Pop-Location
}
