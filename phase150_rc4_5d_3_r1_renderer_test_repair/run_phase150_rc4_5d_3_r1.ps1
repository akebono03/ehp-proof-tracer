$ErrorActionPreference = "Stop"
Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-5D-3-R1"
Write-Host "renderer newline + canonical test expectation repair"
Write-Host "=============================================================="
$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"
try {
  Write-Host "`nA. Applying minimal repair..."
  python ".\phase150_rc4_5d_3_r1_renderer_test_repair\apply_phase150_rc4_5d_3_r1.py"
  Write-Host "`nB. Syntax preflight..."
  python -m py_compile ".\toda_group_proof_narrative_reason_renderer.py" ".\tests\test_phase150_rc4_5d_3_multiple_relation_to_order.py"
  Write-Host "`nC. RC4-5D-3 focused regression..."
  python -m pytest -q ".\tests\test_phase150_rc4_5d_3_multiple_relation_to_order.py" ".\tests\test_phase150_rc4_4_reasons.py" ".\tests\test_phase150_rc4_5_visible_reasons.py" ".\tests\test_phase150_rc4_5b_3_reference_binding.py" ".\tests\test_phase150_rc4_5b_3_r1_beta_latex.py" ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py" ".\tests\test_phase65_nu_prime_order_pi6_3.py"
  Write-Host "`nD. Visible Narrative audit..."
  python -c "from tests.test_phase143_19_method_evidence import _method_evidence_data; from toda_group_proof_narrative_contribution_renderer import render_toda_group_proof_narrative_multi_argument_with_contributions_markdown as r; p,b,s,a=_method_evidence_data(3,3); m=r(p,b,s,a); print(m); print('VISIBLE_MULTIPLE_ORDER_REASON=PASS' if '\\neq0' in m and '\\operatorname{ord}' in m and '\\n' not in m else 'VISIBLE_MULTIPLE_ORDER_REASON=FAIL')"
  Write-Host "`n=============================================================="
  Write-Host "RC4-5D-3-R1 completed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
