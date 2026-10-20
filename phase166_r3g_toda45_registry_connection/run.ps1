$ErrorActionPreference = 'Stop'
$root = (Resolve-Path '.').Path
$package = Join-Path $root 'phase166_r3g_toda45_registry_connection'
if (-not (Test-Path (Join-Path $package 'install.py'))) { throw 'Execute from ehp_proof repository root.' }
python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R3-G installation failed.' }
python -m pytest -q `
  (Join-Path $package 'test_r3g.py') `
  'phase165_r52_r27_r5_typed_references/test_r5_typed_references.py' `
  'tests/test_phase46_toda_45_theorem_semantics.py' `
  'test_phase165_r52_r9_shared_math.py::test_r9_pi32_regenerated_by_shared_mathematical_expansion' `
  'test_phase165_r52_r9_shared_math.py::test_r9_pi43_is_a_real_typed_goal_even_if_not_proved' `
  'tests/test_phase49_probe.py::test_phase49_probe_derives_final_pi_3_2_group' `
  'tests/test_phase49_probe.py::test_phase49_probe_all_derived_steps_preserve_inference_rule'
if ($LASTEXITCODE -ne 0) { throw 'R3-G focused tests failed.' }
Write-Host 'R3-G focused tests PASS; full pytest NOT run.'
