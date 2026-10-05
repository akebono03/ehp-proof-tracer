$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair5 - import generic eta normalizer"
Write-Host "=============================================================="

Write-Host "[1/5] Apply repair5"
python ".\phase157_r20_repair5_import_eta_normalizer\apply_phase157_r20_repair5.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""

Write-Host "[2/5] Proposition 2.2 / Equation 5.7 / architecture"
python -m pytest `
  tests/test_phase30_prop22.py `
  tests/test_phase65_equation57_injectivity.py `
  tests/test_phase157_r20_generic_dependency_architecture.py `
  tests/test_phase157_r20_generic_dependency_rendering.py `
  -x -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""

Write-Host "[3/5] Phase157 Narrative focused regression"
python -m pytest `
  tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py `
  tests/test_phase157_r11_reference_reason_punctuation.py `
  tests/test_phase157_r11_r17_residual_narrative_defects.py `
  tests/test_phase157_r3_pi6_3_reference_boundary.py `
  -x -q
Write-Host "Narrative focused exit code: $LASTEXITCODE"
Write-Host ""

Write-Host "[4/5] Generic renderer focused tests"
if (Test-Path ".\tests\test_phase143_generic_narrative_renderer.py") {
  python -m pytest `
    tests/test_phase143_generic_narrative_renderer.py `
    -x -q
  Write-Host "Generic renderer exit code: $LASTEXITCODE"
}
else {
  Write-Host "Generic renderer focused test file not present; skipped."
}
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
