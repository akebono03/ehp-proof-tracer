$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-5F-2-R1"
Write-Host "Final group-structure test/audit escaping repair"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$repoRoot = (Get-Location).Path
$testsPath = Join-Path $repoRoot "tests"
$env:PYTHONPATH = "$repoRoot;$testsPath"
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Repairing RC4-5F-2 test escaping..."
  python `
    ".\phase150_rc4_5f_2_r1_test_audit_escape_repair\apply_phase150_rc4_5f_2_r1.py"

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

reason_fragments = (
  "この短完全列と両端の群の位数より",
  r"中央の群の位数は $2\cdot2=4$",
  "中央の群を生成する",
)
conclusion = r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"

checks = {
  "reason_fragments": all(
    fragment in rendered
    for fragment in reason_fragments
  ),
  "conclusion": conclusion in rendered,
  "reason_before_conclusion": (
    reason_fragments[0] in rendered
    and conclusion in rendered
    and rendered.index(reason_fragments[0])
    < rendered.index(conclusion)
  ),
}

for name, value in checks.items():
  print(f"{name}={value}")

print(
  "VISIBLE_FINAL_GROUP_REASON=",
  all(checks.values()),
)
'@ | python -

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-5F-2-R1 completed."
  Write-Host "Production changes: none"
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
