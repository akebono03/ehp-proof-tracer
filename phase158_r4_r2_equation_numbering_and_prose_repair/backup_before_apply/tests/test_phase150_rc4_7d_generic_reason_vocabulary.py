from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_contribution_renderer import render_toda_group_proof_narrative_multi_argument_with_contributions_markdown
from toda_group_proof_narrative_reasons import TodaGroupProofNarrativeReasonKind, build_toda_group_proof_narrative_reason_sidecar

def _data(n,k):
 p,b,s,a=_method_evidence_data(n,k); r=build_toda_group_proof_narrative_reason_sidecar(p,s); m=render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(p,b,s,a); return r,m

def test_phase150_rc4_7d_pi10_final_reason():
 r,m=_data(4,6); assert any(x.kind is TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION for x in r.reasons); assert '以上で得た群構造, 生成元, および写像に関する結果を合わせると, ' in m

def test_phase150_rc4_7d_pi12_map_and_final_reasons():
 r,m=_data(5,7); k={x.kind for x in r.reasons}; assert TodaGroupProofNarrativeReasonKind.MAP_STRUCTURE_DERIVATION in k; assert TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION in k; assert 'この完全性, 既知の群構造, および写像の像に関する結果を合わせると' in m

def test_phase150_rc4_7d_pi16_order_and_final_reasons():
 r,m=_data(9,7); k={x.kind for x in r.reasons}; assert TodaGroupProofNarrativeReasonKind.GROUP_ORDER_DERIVATION in k; assert TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION in k; assert 'この群構造と写像による移送の結果を合わせると' in m

def test_phase150_rc4_7d_reason_kinds_are_generic():
 for kind in TodaGroupProofNarrativeReasonKind:
  assert not any(x in kind.name.upper() for x in ('PI10','PI12','PI15','PI16','NU4','SIGMA'))
