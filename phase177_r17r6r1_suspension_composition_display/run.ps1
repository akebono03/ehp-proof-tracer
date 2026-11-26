param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$package = 'phase177_r17r6r1_suspension_composition_display'
python -B -m "$package.installer" --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R17R6R1 preflight failed' }
if ($DryRun) { exit 0 }
python -B -m "$package.installer"
if ($LASTEXITCODE -ne 0) { throw 'R17R6R1 install failed' }
python -B -m pytest -q -s --import-mode=importlib -p no:cacheprovider `
  "$package/tests" `
  phase177_r17r5_duplicate_cited_equality/tests `
  phase177_r17r4r2_prop25_equality_chain/tests `
  phase177_r17r4r1_prop25_suspension_elision/tests `
  phase177_r17r3_rank_two_quotient_display/tests `
  phase177_r17r1_finite_delta_reason_display/tests `
  phase168_r3_27_typed_projection/tests `
  phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py
if ($LASTEXITCODE -ne 0) { throw 'R17R6R1 focused tests failed; changes retained for inspection' }
python -B -m "$package.installer" --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R17R6R1 postflight failed' }
git diff --check
if ($LASTEXITCODE -ne 0) { throw 'R17R6R1 diff check failed' }
Write-Output 'PHASE177_R17R6R1_NEW_MATH_RULES=0'
Write-Output 'PHASE177_R17R6R1_NEW_GIVEN=0'
Write-Output 'PHASE177_R17R6R1_FULL_PYTEST=NOT_RUN'
Write-Output 'PHASE177_R17R6R1_GATE=PASS_R17R6R1_SUSPENSION_COMPOSITION_DISPLAY'
