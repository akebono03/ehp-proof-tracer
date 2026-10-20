$ErrorActionPreference = 'Stop'
$root = (Resolve-Path '.').Path
$package = Join-Path $root 'phase166_r3g_toda45_registry_connection'
if (-not (Test-Path (Join-Path $package 'test_r3g.py'))) { throw 'R3-G package/test_r3g.py not found. Execute from repository root after extracting the original R3-G ZIP.' }
$required = @(
  'phase165_r52_r27_r5_typed_references/test_r5_typed_references.py',
  'tests/test_phase46_toda_45_theorem_semantics.py',
  'test_phase165_r52_r9_shared_math.py'
)
foreach ($path in $required) {
  if (-not (Test-Path (Join-Path $root $path))) { throw "Expected targeted test not found: $path" }
}
$tests = @(
  (Join-Path $package 'test_r3g.py'),
  'phase165_r52_r27_r5_typed_references/test_r5_typed_references.py',
  'tests/test_phase46_toda_45_theorem_semantics.py',
  'test_phase165_r52_r9_shared_math.py::test_r9_pi32_regenerated_by_shared_mathematical_expansion',
  'test_phase165_r52_r9_shared_math.py::test_r9_pi43_is_a_real_typed_goal_even_if_not_proved'
)
Write-Host 'Running R3-G focused tests only (no code installation and no full pytest).'
python -m pytest -q @tests
if ($LASTEXITCODE -ne 0) { throw 'R3-G focused tests failed.' }
Write-Host 'R3-G focused tests PASS; full pytest NOT run.'
