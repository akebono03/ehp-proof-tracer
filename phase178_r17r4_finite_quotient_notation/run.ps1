param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Push-Location (Split-Path -Parent $PSScriptRoot)
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $package = 'phase178_r17r4_finite_quotient_notation'
    python -B -m "$package.installer" --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R17R4 preflight failed' }
    if ($DryRun) { exit 0 }
    python -B -m "$package.installer"
    if ($LASTEXITCODE -ne 0) { throw 'R17R4 install failed' }
    python -B -m pytest -q -s --import-mode=importlib -p no:cacheprovider `
        phase178_r17r3_common_renderer/tests `
        phase177_r17r6r1_suspension_composition_display/tests `
        phase177_r17r3_rank_two_quotient_display/tests `
        phase168_r3_27_typed_projection/tests `
        phase178_r17_finite_cyclic_quotient_isolated/tests `
        phase178_r17r2_cited_512_priority/tests/test_priority.py
    if ($LASTEXITCODE -ne 0) { throw 'R17R4 focused tests failed; changes retained for inspection' }
    python -B -m "$package.installer" --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R17R4 postflight failed' }
    git diff --check
    if ($LASTEXITCODE -ne 0) { throw 'R17R4 diff check failed' }
    Write-Output 'PHASE178_R17R4_NEW_MATH_RULES=0'
    Write-Output 'PHASE178_R17R4_NEW_GIVEN=0'
    Write-Output 'PHASE178_R17R4_FULL_PYTEST=NOT_RUN'
    Write-Output 'PHASE178_R17R4_GATE=PASS_R17R4_FINITE_QUOTIENT_NOTATION'
} finally {
    Pop-Location
}
