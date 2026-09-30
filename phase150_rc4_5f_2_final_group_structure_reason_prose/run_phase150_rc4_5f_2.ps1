$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-5F-2"
Write-Host "Final group-structure reason prose implementation"
Write-Host "=============================================================="

$repoRoot = (Get-Location).Path
$testsPath = Join-Path $repoRoot "tests"
$env:PYTHONPATH = "$repoRoot;$testsPath"
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Applying minimal implementation..."
  python `
    ".\phase150_rc4_5f_2_final_group_structure_reason_prose\apply_phase150_rc4_5f_2.py"

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\toda_group_proof_narrative_reasons.py" `
    ".\toda_group_proof_narrative_reason_renderer.py" `
    ".\tests\test_phase150_rc4_5f_2_final_group_structure_reason.py"

  Write-Host ""
  Write-Host "C. Focused RC4 reason regression..."
  python -m pytest -q `
    ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py" `
    ".\tests\test_phase150_rc4_5d_3_multiple_relation_to_order.py" `
    ".\tests\test_phase150_rc4_5e_2_short_exact_derivation_reason.py" `
    ".\tests\test_phase150_rc4_5f_2_final_group_structure_reason.py" `
    ".\tests\test_phase65_nu_prime_order_pi6_3.py" `
    ".\tests\test_phase149_rc3_4_cross_group_ordering.py"

  Write-Host ""
  Write-Host "D. Visible Narrative check..."
  @'
from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)

presentation, blocks, sidecar, arguments = _method_evidence_data(3, 3)
rendered = render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
  presentation,
  blocks,
  sidecar,
  arguments,
)
print(rendered)
print()
print(
  "VISIBLE_FINAL_GROUP_REASON=",
  (
    "この短完全列と両端の群の位数より" in rendered
    and "中央の群の位数は $2\\cdot2=4$" in rendered
    and "中央の群を生成する" in rendered
  ),
)
'@ | python -

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-5F-2 focused run completed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
