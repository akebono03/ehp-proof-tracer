$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-5F-2-R2"
Write-Host "Final group-structure visible-test function repair"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$repoRoot = (Get-Location).Path
$testsPath = Join-Path $repoRoot "tests"
$env:PYTHONPATH = "$repoRoot;$testsPath"
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Repairing complete RC4-5F-2 visible test function..."
  python ".\phase150_rc4_5f_2_r2_test_function_repair\apply_phase150_rc4_5f_2_r2.py"

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
  Write-Host "D. Visible Narrative check using production renderer sentence..."
  @'
from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_reason_renderer import (
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)

presentation, blocks, sidecar, arguments = _method_evidence_data(3, 3)
reason_sidecar = build_toda_group_proof_narrative_reason_sidecar(
  presentation,
  sidecar,
)
reasons = tuple(
  reason
  for reason in reason_sidecar.reasons
  if reason.kind is TodaGroupProofNarrativeReasonKind.FINAL_GROUP_STRUCTURE
)
rendered = render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
  presentation,
  blocks,
  sidecar,
  arguments,
)
conclusion = r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"

reason_count_ok = len(reasons) == 1
sentence = (
  render_toda_group_proof_narrative_reason_sentence(reasons[0])
  if reason_count_ok
  else None
)
sentence_visible = sentence is not None and rendered.count(sentence) == 1
conclusion_visible = conclusion in rendered
ordering_ok = (
  sentence_visible
  and conclusion_visible
  and rendered.index(sentence) < rendered.index(conclusion)
)

print("reason_count_ok=", reason_count_ok)
print("sentence_visible=", sentence_visible)
print("conclusion_visible=", conclusion_visible)
print("reason_before_conclusion=", ordering_ok)
print(
  "VISIBLE_FINAL_GROUP_REASON=",
  reason_count_ok and sentence_visible and conclusion_visible and ordering_ok,
)
'@ | python -

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-5F-2-R2 completed."
  Write-Host "Production changes: none"
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
