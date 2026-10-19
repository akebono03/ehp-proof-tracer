$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $folder 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'Patch failed' }
python -m pytest -q `
  tests/test_phase49_probe.py::test_phase49_probe_derives_final_pi_3_2_group `
  tests/test_phase49_probe.py::test_phase49_probe_all_derived_steps_preserve_inference_rule `
  test_phase165_r52_r9_shared_math.py::test_r9_pi32_regenerated_by_shared_mathematical_expansion
if ($LASTEXITCODE -ne 0) { throw 'Targeted tests failed' }
Write-Host 'Targeted tests PASS; full pytest NOT run.'
