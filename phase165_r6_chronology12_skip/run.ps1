$ErrorActionPreference = 'Stop'
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $dir 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'Chronology patch guard failed' }
python -m pytest -q `
  'tests/test_phase49_probe.py::test_phase49_probe_reaches_fixed_point_in_six_rounds' `
  'tests/test_phase49_probe.py::test_phase49_probe_round_one_derives_two_steps' `
  'tests/test_phase49_probe.py::test_phase49_probe_round_two_derives_delta_zero' `
  'tests/test_phase49_probe.py::test_phase49_probe_round_three_derives_h_surjectivity' `
  'tests/test_phase49_probe.py::test_phase49_probe_round_four_derives_h_isomorphism' `
  'tests/test_phase49_probe.py::test_phase49_probe_round_five_derives_eta_2_definition' `
  'tests/test_phase49_probe.py::test_phase49_probe_round_six_derives_two_final_consequences' `
  'tests/test_phase56_probe.py::test_phase56_probe_final_result_occurs_in_last_round' `
  'tests/test_phase56_pi_i_minus_1_1_zero.py::test_phase56_2_reaches_fixed_point_in_one_round' `
  'tests/test_phase56_prop44_eta2_specialization.py::test_phase56_3_reaches_fixed_point_in_one_round' `
  'tests/test_phase56_prop44_second_summand_restriction.py::test_phase56_4_reaches_fixed_point_in_one_round' `
  'tests/test_phase56_toda52_composition_isomorphism.py::test_phase56_5_reaches_fixed_point_in_one_round'
if ($LASTEXITCODE -ne 0) { throw 'Targeted chronology markers failed' }
Write-Host '12 historical chronology tests SKIPPED; 71 other tests not modified; full pytest NOT run.'
