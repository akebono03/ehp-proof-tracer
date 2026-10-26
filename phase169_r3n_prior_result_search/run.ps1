$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Write-Host 'Phase 169 R3N: prior DB result aliases through earlier screened FIXED statements'
Write-Host 'Scope: 1 solver function, 1 new generic rule module, 1 focused test file'
python -B -m phase169_r3n_prior_result_search.apply
if ($LASTEXITCODE -ne 0) { throw "R3N installation failed: $LASTEXITCODE" }
python -B -m pytest -q '.\phase169_r3n_prior_result_search\tests\test_r3n_prior_result_alias.py' '.\phase169_r3m_prior_result_catalog\tests\test_prior_results.py'
$focus = $LASTEXITCODE
Write-Host "R3N_FOCUSED_PYTEST_EXIT_CODE=$focus"
if ($focus -ne 0) { throw "R3N focused tests failed: $focus" }
python -B -m pytest -q '.\phase168_r3_41l_reasoned_prose\tests\test_phase168_r3_41l_reasoned_prose.py'
$regression = $LASTEXITCODE
Write-Host "R3N_ONE_STEM_PYTEST_EXIT_CODE=$regression"
if ($regression -ne 0) { throw "R3N 1-stem regression tests failed: $regression" }
python -B -m phase169_r3n_prior_result_search.audit
$audit = $LASTEXITCODE
Write-Host "R3N_AUDIT_EXIT_CODE=$audit"
if ($audit -ne 0) { throw "R3N audit failed: $audit" }
Write-Host 'R3N_COMPLETE: narrow source-result alias connection; no full pytest run.'
