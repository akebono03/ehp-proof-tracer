param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$package = 'phase177_r17r5_duplicate_cited_equality'
python -B -m "$package.installer" --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R17R5 preflight failed' }
if ($DryRun) { exit 0 }
python -B -m "$package.installer"
if ($LASTEXITCODE -ne 0) { throw 'R17R5 installation failed' }
python -B -m pytest -q -s --import-mode=importlib -p no:cacheprovider `
  "$package/tests" `
  phase177_r17r4r2_prop25_equality_chain/tests `
  phase177_r17r4r1_prop25_suspension_elision/tests `
  phase177_r17r1_finite_delta_reason_display/tests `
  phase177_r17r3_rank_two_quotient_display/tests `
  phase168_r3_27_typed_projection/tests
if ($LASTEXITCODE -ne 0) { throw 'R17R5 focused tests failed; hook retained for inspection' }
python -B -m "$package.installer" --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R17R5 postflight failed' }
git diff --check
if ($LASTEXITCODE -ne 0) { throw 'R17R5 diff check failed' }
Write-Output 'PHASE177_R17R5_NEW_MATH_RULES=0'
Write-Output 'PHASE177_R17R5_NEW_GIVEN=0'
Write-Output 'PHASE177_R17R5_FULL_PYTEST=NOT_RUN'
Write-Output 'PHASE177_R17R5_GATE=PASS_R17R5_DUPLICATE_CITED_EQUALITY'
