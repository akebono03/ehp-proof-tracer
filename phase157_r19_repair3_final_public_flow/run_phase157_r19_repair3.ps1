$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R19 repair3 — final public proof flow"
Write-Host "=============================================================="

Write-Host "[1/4] Apply repair3"
python ".\phase157_r19_repair3_final_public_flow\apply_phase157_r19_repair3.py"
Write-Host ""

Write-Host "[2/4] R19 tests only"
python -m pytest `
  tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py `
  -x -q
Write-Host ""

Write-Host "[3/4] Existing focused regression"
python -m pytest `
  tests/test_phase157_r11_reference_reason_punctuation.py `
  tests/test_phase157_r11_r17_residual_narrative_defects.py `
  tests/test_phase157_r3_pi6_3_reference_boundary.py `
  -x -q
Write-Host ""

Write-Host "[4/4] Render pi_6^3 Narrative"
@'
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay

report = build_standard_toda_report(n=3, k=3)
group_result = report.candidates[0].source_candidate.group_result
replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
)
presentation = build_toda_group_proof_presentation(replay)
print(render_toda_group_proof_narrative_markdown(presentation))
'@ | python -

Write-Host ""
Write-Host "Repository-wide pytest is intentionally not run."
