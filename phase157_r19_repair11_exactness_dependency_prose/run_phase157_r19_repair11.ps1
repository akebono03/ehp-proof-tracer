$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R19 repair11 - exactness dependency prose"
Write-Host "=============================================================="

Write-Host "[1/3] Apply repair11"
python ".\phase157_r19_repair11_exactness_dependency_prose\apply_phase157_r19_repair11.py"
Write-Host ""

Write-Host "[2/3] R19 + focused regression"
python -m pytest `
  tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py `
  tests/test_phase157_r11_reference_reason_punctuation.py `
  tests/test_phase157_r11_r17_residual_narrative_defects.py `
  tests/test_phase157_r3_pi6_3_reference_boundary.py `
  -x -q
Write-Host ""

Write-Host "[3/3] Render pi_6^3 Narrative"
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
