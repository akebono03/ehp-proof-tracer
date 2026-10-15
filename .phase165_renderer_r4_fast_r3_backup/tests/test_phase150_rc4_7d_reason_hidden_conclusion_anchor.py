from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_reason_renderer import (
  _toda_group_proof_narrative_reason_insertion_index,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)


def _data(n, k):
  presentation, blocks, sidecar, arguments = _method_evidence_data(n, k)
  reasons = build_toda_group_proof_narrative_reason_sidecar(
    presentation,
    sidecar,
  )
  markdown = render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
    presentation,
    blocks,
    sidecar,
    arguments,
  )
  return reasons, markdown


def test_phase150_rc4_7d_hidden_map_reason_uses_visible_downstream_anchor():
  reasons, markdown = _data(5, 7)
  map_reason = next(
    reason
    for reason in reasons.reasons
    if reason.kind is TodaGroupProofNarrativeReasonKind.MAP_STRUCTURE_DERIVATION
  )
  hidden_line = _render_generic_narrative_step(
    map_reason.conclusion_step
  )

  assert not hidden_line or hidden_line not in markdown
  assert (
    _toda_group_proof_narrative_reason_insertion_index(
      markdown,
      map_reason,
      reasons,
    )
    is not None
  )
  assert (
    "この完全性, 既知の群構造, および写像の像に関する"
    "結果を合わせると"
    in markdown
  )


def test_phase150_rc4_7d_visible_final_reason_is_preserved():
  reasons, markdown = _data(9, 7)
  final_reason = next(
    reason
    for reason in reasons.reasons
    if reason.kind is TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION
  )
  conclusion_line = _render_generic_narrative_step(
    final_reason.conclusion_step
  )

  assert conclusion_line
  assert conclusion_line in markdown
  assert (
    "以上で得た群構造, 生成元, および写像に関する結果を"
    "合わせると, "
    in markdown
  )
