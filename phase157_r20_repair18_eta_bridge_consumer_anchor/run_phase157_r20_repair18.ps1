$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair18 - eta bridge consumer anchor"
Write-Host "=============================================================="

Write-Host "[1/5] Apply repair18"
python ".\phase157_r20_repair18_eta_bridge_consumer_anchor\apply_phase157_r20_repair18.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""

Write-Host "[2/5] Repair16 + repair18 focused tests"
python -m pytest `
  tests/test_phase157_r20_repair16_proof_order_and_cleanup.py `
  tests/test_phase157_r20_repair18_eta_bridge_consumer_anchor.py `
  tests/test_phase157_r20_repair14_late_surjectivity_reference_support.py `
  tests/test_phase157_r20_generic_dependency_rendering.py `
  -x -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""

Write-Host "[3/5] Phase157 Narrative regression"
python -m pytest `
  tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py `
  tests/test_phase157_r11_reference_reason_punctuation.py `
  tests/test_phase157_r11_r17_residual_narrative_defects.py `
  tests/test_phase157_r3_pi6_3_reference_boundary.py `
  -x -q
Write-Host "Narrative exit code: $LASTEXITCODE"
Write-Host ""

Write-Host "[4/5] Phase156 Reference regression"
python -m pytest `
  tests/test_phase156_r5_repair11_reference_dependency_pruning.py `
  tests/test_phase156_r5_repair12_reference_frontier.py `
  tests/test_phase156_r5_repair4_bridge_reference_inference.py `
  -x -q
Write-Host "Reference exit code: $LASTEXITCODE"
Write-Host ""

Write-Host "[5/5] Render pi_6^3 Narrative"
@'
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay

report = build_standard_toda_report(
    n=3,
    k=3,
)
group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
)
replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
)
presentation = build_toda_group_proof_presentation(
    replay
)

print(
    render_toda_group_proof_narrative_markdown(
        presentation
    )
)
'@ | python -

Write-Host ""
Write-Host "Repository-wide pytest is intentionally not run."
