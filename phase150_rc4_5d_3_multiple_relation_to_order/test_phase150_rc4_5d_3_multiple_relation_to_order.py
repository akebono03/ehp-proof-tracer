import inspect

from expression import Multiple
from proof import Relation, RelationType
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


def _pi6_reason_data():
  presentation, blocks, semantic_sidecar, arguments = _method_evidence_data(3, 3)
  reason_sidecar = build_toda_group_proof_narrative_reason_sidecar(
    presentation,
    semantic_sidecar,
  )
  return presentation, blocks, semantic_sidecar, arguments, reason_sidecar


def test_phase150_rc4_5d_3_builds_multiple_relation_to_order_from_typed_shape():
  presentation, blocks, semantic_sidecar, arguments, reason_sidecar = _pi6_reason_data()
  reasons = tuple(
    reason for reason in reason_sidecar.reasons
    if reason.kind is TodaGroupProofNarrativeReasonKind.MULTIPLE_RELATION_TO_ORDER
  )
  assert len(reasons) == 1
  reason = reasons[0]
  conclusion = reason.conclusion_step.conclusion
  order_statement = reason.premise_steps[0].conclusion
  equality_statement = reason.premise_steps[1].conclusion
  assert isinstance(conclusion, Relation)
  assert conclusion.relation_type is RelationType.ORDER
  assert conclusion.rhs == 4
  assert isinstance(order_statement, Relation)
  assert order_statement.relation_type is RelationType.ORDER
  assert order_statement.rhs == 2
  assert isinstance(equality_statement, Relation)
  assert equality_statement.relation_type is RelationType.EQUALITY
  assert isinstance(equality_statement.lhs, Multiple)
  assert equality_statement.lhs.coefficient == 2
  assert equality_statement.rhs == order_statement.lhs
  assert equality_statement.lhs.expression == conclusion.lhs


def test_phase150_rc4_5d_3_reason_is_visible_before_order_four_conclusion():
  presentation, blocks, semantic_sidecar, arguments, reason_sidecar = _pi6_reason_data()
  reason = next(
    reason for reason in reason_sidecar.reasons
    if reason.kind is TodaGroupProofNarrativeReasonKind.MULTIPLE_RELATION_TO_ORDER
  )
  sentence = render_toda_group_proof_narrative_reason_sentence(reason)
  rendered = render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )
  assert sentence is not None
  assert "operatorname{ord}" in sentence
  assert "\\neq0" in sentence
  assert rendered.count(sentence) == 1
  assert rendered.index(sentence) < rendered.index(
    "$\\operatorname{ord}(\\nu')=4$."
  )


def test_phase150_rc4_5d_3_classifier_has_no_target_or_rule_name_special_case():
  import toda_group_proof_narrative_reasons as module
  source = inspect.getsource(module._multiple_relation_to_order_reason)
  for fragment in (
    "(6, 3)", "pi6", "nu_prime", "ν′", "Proposition 5.6",
    "inference_rule", ".rule",
  ):
    assert fragment not in source


def test_phase150_rc4_5d_3_renderer_has_no_target_or_proposition_special_case():
  import toda_group_proof_narrative_reason_renderer as module
  source = inspect.getsource(
    module.render_toda_group_proof_narrative_reason_sentence
  )
  for fragment in (
    "(6, 3)", "pi6", "nu_prime", "ν′", "Proposition 5.6",
  ):
    assert fragment not in source
