$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r3a - canonical Prop44 Reference tests"
Write-Host "=============================================================="

Write-Host "[1/6] Apply test-only repair"
python ".\phase157_r20_repair53_r3a_canonical_prop44_reference_tests\apply_phase157_r20_repair53_r3a.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""

Write-Host "[2/6] Focused attribution + pi15 tests"
python -m pytest `
  tests/test_phase157_r20_repair53_r3_fixed_reference_attribution.py `
  tests/test_phase134_24_pi15_8_narrative.py `
  tests/test_phase150_rc4_7a_cross_group_reference_normalization.py `
  -x -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""

Write-Host "[3/6] repair53 fragment + dedicated route tests"
python -m pytest `
  tests/test_phase157_r20_repair53_display_closing_fragment_normalization.py `
  tests/test_phase134_9_pi8_5_narrative.py `
  tests/test_phase134_24_v2_raw_group_renderer.py `
  -x -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""

Write-Host "[4/6] Recent Phase157 focused regression"
python -m pytest `
  tests/test_phase157_r20_repair48_injective_image_reason_ordering.py `
  tests/test_phase157_r20_repair47_injective_image_order_reason.py `
  tests/test_phase157_r20_repair45_relation_dependency_and_unique_step_dedup.py `
  tests/test_phase157_r20_repair43_dangling_connector_cleanup.py `
  tests/test_phase157_r20_repair42_repeated_reference_restatements.py `
  -x -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""

Write-Host "[5/6] Re-run residual 112-group display audit"
python ".\phase157_r20_repair51_residual_display_defect_audit\audit_phase157_r20_repair51.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""

Write-Host "[6/6] Render pi_15^8 Reference section"
@'
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay

report = build_standard_toda_report(
    n=8,
    k=7,
)
group_result = report.candidates[0].source_candidate.group_result
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

if "## 使用する結果" in rendered:
    section = rendered.split(
        "## 使用する結果",
        1,
    )[1]
    if "## 証明" in section:
        section = section.split(
            "## 証明",
            1,
        )[0]
    print(section.strip())
else:
    print("(no reference section)")
'@ | python -

Write-Host ""
Write-Host "Repository-wide pytest is intentionally not run."
