$ErrorActionPreference = "Stop"

Write-Host "Phase 129-4 targeted tests"
python -m pytest tests/test_phase129_nu_prime_operation_query_handoff.py -q

Write-Host "Phase 129-4 focused regression tests"
python -m pytest `
  tests/test_phase110_5_minimal_operation_query_core.py `
  tests/test_phase110_8_operation_query_result_presentation.py `
  tests/test_phase114_3_nu5_operation_query_handoff.py `
  tests/test_phase115_sigma11_operation_query_handoff.py `
  tests/test_phase118_web_operation_query.py `
  tests/test_phase129_nu_prime_operation_query_handoff.py `
  -q

Write-Host "Manual CLI checks"
python main.py query "E(nu_prime)"
python main.py query-proof "E(nu_prime)" --depth 1
