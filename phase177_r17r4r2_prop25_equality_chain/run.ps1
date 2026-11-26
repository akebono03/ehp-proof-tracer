param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$package = 'phase177_r17r4r2_prop25_equality_chain'
python -B -m "$package.installer" --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R17R4R2 preflight failed' }
if ($DryRun) { exit 0 }
python -B -m "$package.installer"
if ($LASTEXITCODE -ne 0) { throw 'R17R4R2 installation failed' }
python -B -m pytest -q -s --import-mode=importlib -p no:cacheprovider `
  "$package/tests" `
  phase177_r17r4r1_prop25_suspension_elision/tests `
  phase177_r17r1_finite_delta_reason_display/tests `
  phase177_r17r3_rank_two_quotient_display/tests `
  phase168_r3_27_typed_projection/tests `
  phase177_r10_composition_associativity_isolated/tests `
  phase177_r3_unsigned_delta_composition_isolated/tests/test_rule.py
if ($LASTEXITCODE -ne 0) { throw 'R17R4R2R2 focused tests failed; changes retained for inspection' }
python -B -m "$package.installer" --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R17R4R2 postflight failed' }
git diff --check
if ($LASTEXITCODE -ne 0) { throw 'R17R4R2 diff check failed' }
Write-Output 'PHASE177_R17R4R2_NEW_MATH_RULES=0'
Write-Output 'PHASE177_R17R4R2_NEW_GIVEN=0'
Write-Output 'PHASE177_R17R4R2_FULL_PYTEST=NOT_RUN'
Write-Output 'PHASE177_R17R4R2R2_GATE=PASS_R17R4R2R2_SYMMETRY_CHAIN'
Write-Output 'PHASE177_R17R4R2_GATE=PASS_R17R4R2_PROP25_EQUALITY_CHAIN'
