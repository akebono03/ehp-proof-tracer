$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Write-Host 'Phase 169 R3O: citation-backed Toda (4.5) composite eta transport'
Write-Host 'Only one existing provider function and one new rule module; no proof replay'
python -B -m phase169_r3o_toda45_composite_transport.apply
if ($LASTEXITCODE -ne 0) { throw "R3O guarded installation failed: $LASTEXITCODE" }
python -B -m pytest -q '.\phase169_r3o_toda45_composite_transport\tests\test_r3o_toda45_composite_transport.py'
$focus = $LASTEXITCODE
Write-Host "R3O_FOCUSED_PYTEST_EXIT_CODE=$focus"
if ($focus -ne 0) { throw "R3O focused pytest failed: $focus" }
python -B -m pytest -q '.\phase169_r3n_prior_result_search\tests\test_r3n_prior_result_alias.py' '.\phase169_r3m_prior_result_catalog\tests\test_prior_results.py'
$prior = $LASTEXITCODE
Write-Host "R3O_PRIOR_RESULT_PYTEST_EXIT_CODE=$prior"
if ($prior -ne 0) { throw "R3O prior result pytest failed: $prior" }
python -B -m pytest -q '.\phase168_r3_41l_reasoned_prose\tests\test_phase168_r3_41l_reasoned_prose.py'
$oneStem = $LASTEXITCODE
Write-Host "R3O_ONE_STEM_PYTEST_EXIT_CODE=$oneStem"
if ($oneStem -ne 0) { throw "R3O 1-stem pytest failed: $oneStem" }
python -B -m phase169_r3o_toda45_composite_transport.audit
$audit = $LASTEXITCODE
Write-Host "R3O_AUDIT_EXIT_CODE=$audit"
if ($audit -ne 0) { throw "R3O Web audit failed: $audit" }
Write-Host 'R3O_COMPLETE: only focused checks; full pytest NOT run.'
