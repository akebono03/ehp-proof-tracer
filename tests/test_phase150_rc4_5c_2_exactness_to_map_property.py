import inspect

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
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
from toda_rules import (
  TodaDeltaZeroStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
)


def _pi6_reason_data():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )
  return (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  )


def test_phase150_rc4_5c_2_builds_exactness_to_map_property_from_typed_direct_premises():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _pi6_reason_data()

  reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
    )
  )

  assert len(reasons) == 1
  reason = reasons[0]

  assert isinstance(
    reason.conclusion_step.conclusion,
    TodaSuspensionInjectiveStatement,
  )
  assert len(reason.premise_steps) == 2
  assert isinstance(
    reason.premise_steps[0].conclusion,
    TodaDeltaZeroStatement,
  )
  assert isinstance(
    reason.premise_steps[1].conclusion,
    TodaProp42ExactnessStatement,
  )

  zero_map = reason.premise_steps[0].conclusion.map
  window = reason.premise_steps[1].conclusion.window
  injective_map = reason.conclusion_step.conclusion.map

  assert zero_map.source_group == window.source_term
  assert zero_map.target_group == window.middle_term
  assert window.middle_term == injective_map.source_group
  assert window.target_term == injective_map.target_group
  assert window.first_map.name == "Δ"
  assert window.second_map.name == "E"


def test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _pi6_reason_data()

  reason = next(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
    )
  )
  sentence = (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
  )
  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  assert sentence == (
    "この完全性と $Δ=0$ より、"
    "$\\ker E=\\operatorname{Im}Δ=0$ である.\n"
    "したがって、"
  )
  assert rendered.count(sentence) == 1

  conclusion = (
    "$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ "
    "は単射である."
  )
  assert conclusion in rendered
  assert rendered.index(sentence) < rendered.index(
    conclusion
  )


def test_phase150_rc4_5c_2_reason_builder_has_no_pi6_or_rule_name_special_case():
  import toda_group_proof_narrative_reasons as module

  source = inspect.getsource(
    module._exactness_to_map_property_reason
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


def test_phase150_rc4_5c_2_renderer_has_no_pi6_or_proposition_special_case():
  import toda_group_proof_narrative_reason_renderer as module

  source = inspect.getsource(
    module.render_toda_group_proof_narrative_reason_sentence
  )

  forbidden_fragments = (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source
