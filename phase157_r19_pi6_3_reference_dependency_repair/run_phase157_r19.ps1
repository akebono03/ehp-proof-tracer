$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R19 — pi_6^3 reference/dependency repair"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/4] Current git HEAD"
git rev-parse HEAD
git status --short
Write-Host ""

Write-Host "[2/4] Apply patch"
python ".\phase157_r19_pi6_3_reference_dependency_repair\apply_phase157_r19.py"
Write-Host ""

Write-Host "[3/4] Focused pytest"
python -m pytest `
  tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py `
  tests/test_phase157_r11_reference_reason_punctuation.py `
  tests/test_phase157_r11_r17_residual_narrative_defects.py `
  tests/test_phase157_r3_pi6_3_reference_boundary.py `
  -q
Write-Host ""

Write-Host "[4/4] Show pi_6^3 Narrative"
@'
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay

report = build_standard_toda_report(3, 3)
replay = build_toda_group_result_proof_replay(
    report.group_result,
    depth=2,
)
presentation = build_toda_group_proof_presentation(replay)
print(render_toda_group_proof_narrative_markdown(presentation))
'@ | python -

Write-Host ""
Write-Host "Full repository pytest is intentionally NOT run in this substep."
Write-Host "Run it only at Phase157 closure."
