param()

$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 semantic numbered-map-property reasoning repair25"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/4] Apply repair25"
python `
  ".\phase159_pi3_2_semantic_numbered_map_property_reasoning_repair25\apply_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair25.py"
if ($LASTEXITCODE -ne 0) {
  throw "repair25 apply failed"
}

Write-Host ""
Write-Host "[2/4] Compile changed production module and focused tests"
python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py" `
  ".\tests\test_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair25.py" `
  ".\tests\test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py" `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py"
if ($LASTEXITCODE -ne 0) {
  throw "compile failed"
}

Write-Host ""
Write-Host "[3/4] Run focused Phase 159 tests"
python -m pytest -q `
  ".\tests\test_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair25.py" `
  ".\tests\test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py" `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py"
if ($LASTEXITCODE -ne 0) {
  throw "focused pytest failed"
}

Write-Host ""
Write-Host "[4/4] Render pi_3^2 public narrative"
@'
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)

report = build_standard_toda_report(
  n=2,
  k=1,
)
group_result = (
  report.candidates[0]
  .source_candidate.group_result
)
replay = build_toda_group_result_proof_replay(
  group_result,
  max_depth=2,
)
presentation = build_toda_group_proof_presentation(
  replay
)
rendered = render_toda_group_proof_narrative_markdown(
  presentation
)

marker = "## 証明"
marker_index = rendered.find(marker)

if marker_index < 0:
  raise RuntimeError(
    "proof marker not found"
  )

print(
  rendered[
    marker_index:
  ]
)
'@ | python -
if ($LASTEXITCODE -ne 0) {
  throw "pi_3^2 render failed"
}

Write-Host ""
Write-Host "Focused verification complete."
Write-Host "Repository-wide pytest is intentionally NOT run during Phase 159."
