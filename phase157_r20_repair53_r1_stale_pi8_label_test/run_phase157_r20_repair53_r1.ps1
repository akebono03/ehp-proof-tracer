$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r1 - stale pi8 label test"
Write-Host "=============================================================="

Write-Host "[1/5] Apply test-only repair"
python ".\phase157_r20_repair53_r1_stale_pi8_label_test\apply_phase157_r20_repair53_r1.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""

Write-Host "[2/5] Focused fragment + dedicated-route tests"
python -m pytest `
  tests/test_phase157_r20_repair53_display_closing_fragment_normalization.py `
  tests/test_phase134_9_pi8_5_narrative.py `
  tests/test_phase134_24_pi15_8_narrative.py `
  tests/test_phase134_24_v2_raw_group_renderer.py `
  -x -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""

Write-Host "[3/5] Recent Phase157 focused regression"
python -m pytest `
  tests/test_phase157_r20_repair48_injective_image_reason_ordering.py `
  tests/test_phase157_r20_repair47_injective_image_order_reason.py `
  tests/test_phase157_r20_repair45_relation_dependency_and_unique_step_dedup.py `
  tests/test_phase157_r20_repair43_dangling_connector_cleanup.py `
  tests/test_phase157_r20_repair42_repeated_reference_restatements.py `
  -x -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""

Write-Host "[4/5] Re-run residual display audit"
python ".\phase157_r20_repair51_residual_display_defect_audit\audit_phase157_r20_repair51.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""

Write-Host "[5/5] Render pi_8^5 and pi_15^8 excerpts"
@'
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay

for n, k, label in (
    (5, 3, "pi_8^5"),
    (8, 7, "pi_15^8"),
):
    report = build_standard_toda_report(n=n, k=k)
    group_result = report.candidates[0].source_candidate.group_result
    replay = build_toda_group_result_proof_replay(
        group_result,
        max_depth=2,
    )
    presentation = build_toda_group_proof_presentation(replay)
    rendered = render_toda_group_proof_narrative_markdown(
        presentation
    )

    print("=" * 72)
    print(label)
    print("=" * 72)
    print(rendered)
'@ | python -

Write-Host ""
Write-Host "Repository-wide pytest is intentionally not run."
