$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159-R1-7c R2 repair6 - semantic rendered equality chain"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$PhaseDir = Join-Path $RepoRoot "phase159_r1_7c_r2_repair6_semantic_rendered_equality_chain"
$env:PYTHONPATH = "$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host "Repository root: $RepoRoot"
  Write-Host ""

  Write-Host "[1/5] Apply repair6"
  python (Join-Path $PhaseDir "apply_phase159_r1_7c_r2_repair6.py")
  if ($LASTEXITCODE -ne 0) {
    throw "repair6 apply failed"
  }

  Write-Host ""
  Write-Host "[2/5] Syntax preflight"
  python -m py_compile `
    ".\toda_group_proof_narrative_renderer.py" `
    ".\tests\test_phase159_r1_7c_r2_repair6_semantic_rendered_equality_chain.py"
  if ($LASTEXITCODE -ne 0) {
    throw "syntax preflight failed"
  }

  Write-Host ""
  Write-Host "[3/5] Focused tests"
  python -m pytest -q `
    ".\tests\test_phase159_r1_7c_r2_repair6_semantic_rendered_equality_chain.py" `
    ".\tests\test_phase159_r1_7c_r2_repair3_projected_chain_match.py" `
    ".\tests\test_phase159_r1_7c_r2_repair2_restore_pipeline.py" `
    ".\tests\test_phase159_r1_7b_repair15_subsumed_exactness.py" `
    ".\tests\test_phase159_r1_7b_repair14_map_property_anchor.py" `
    ".\tests\test_phase159_r1_7b_exact_sequence_display_order.py" `
    ".\tests\test_phase157_r20_repair37_short_exact_after_map_support.py" `
    ".\tests\test_phase150_rc4_5e_2_short_exact_derivation_reason.py" `
    ".\tests\test_phase148_rc2_3_exactness_exposure.py" `
    ".\tests\test_phase148_rc2_3_repair_r1.py"
  if ($LASTEXITCODE -ne 0) {
    throw "focused tests failed"
  }

  Write-Host ""
  Write-Host "[4/5] Render pi_6^3 / pi_11^4 verification"
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

for label, n, k in (
    ("pi6_3", 3, 3),
    ("pi11_4", 4, 7),
):
    report = build_standard_toda_report(
        n=n,
        k=k,
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
    rendered = render_toda_group_proof_narrative_markdown(
        presentation
    )

    print("=" * 78)
    print(label)
    print("=" * 78)
    print(rendered)
'@ | python -
  if ($LASTEXITCODE -ne 0) {
    throw "render verification failed"
  }

  Write-Host ""
  Write-Host "[5/5] Completion"
  Write-Host "Phase 159-R1-7c R2 repair6 focused checks passed."
  Write-Host "Repository-wide pytest intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
