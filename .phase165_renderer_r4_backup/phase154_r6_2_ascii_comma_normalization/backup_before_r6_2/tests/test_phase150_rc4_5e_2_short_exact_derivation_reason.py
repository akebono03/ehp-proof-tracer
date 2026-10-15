import inspect

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _generic_short_exact_sequence_reason_prose,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
)


def _pi6_data():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )
  return (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )


def test_phase150_rc4_5e_2_builds_short_exact_reason_from_typed_contract():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _pi6_data()

  reason_proses = tuple(
    _generic_short_exact_sequence_reason_prose(
      presentation,
      node.proof_step,
    )
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaProp42ExactnessStatement,
    )
  )

  expected = (
    "この完全性と、左の写像が単射、"
    "右の写像が全射であることより、"
    "次の短完全列を得る."
  )

  assert expected in reason_proses
  assert None in reason_proses


def test_phase150_rc4_5e_2_reason_is_visible_before_short_exact_sequence():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _pi6_data()

  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  reason = (
    "この完全性と、左の写像が単射、"
    "右の写像が全射であることより、"
    "次の短完全列を得る."
  )
  sequence = (
    "$0\\longrightarrow \\pi_{5}^{2}"
    "\\xrightarrow{E} \\pi_{6}^{3}"
    "\\xrightarrow{H} \\pi_{6}^{5}"
    "\\longrightarrow 0$"
  )

  assert rendered.count(reason) == 1
  assert sequence in rendered
  assert rendered.index(reason) < rendered.index(sequence)
  assert "この完全性と両端の写像の性質より" not in rendered


def test_phase150_rc4_5e_2_helper_has_no_target_or_rule_name_special_case():
  import toda_group_proof_generic_narrative_renderer as module

  source = inspect.getsource(
    module._generic_short_exact_sequence_reason_prose
  )

  forbidden_fragments = (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
    "inference_rule",
    ".rule",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source
