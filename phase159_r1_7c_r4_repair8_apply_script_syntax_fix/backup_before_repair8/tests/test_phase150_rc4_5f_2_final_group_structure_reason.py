import inspect

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from homotopy_groups import (
  FiniteCyclicGroup,
)
from proof import (
  Relation,
  RelationType,
)
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
  TodaHopfInvariantSurjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
)


def _pi6_final_reason_data():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(3, 3)
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )
  reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .FINAL_GROUP_STRUCTURE
    )
  )
  return (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reasons,
  )


def test_phase150_rc4_5f_2_builds_final_group_structure_reason_from_typed_root_premises():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reasons,
  ) = _pi6_final_reason_data()

  assert len(reasons) == 1
  reason = reasons[0]
  assert reason.conclusion_step is presentation.root_step
  assert len(reason.premise_steps) == 7

  conclusion = reason.conclusion_step.conclusion
  assert isinstance(conclusion, Relation)
  assert conclusion.relation_type is RelationType.EQUALITY
  assert isinstance(conclusion.rhs, FiniteCyclicGroup)

  assert isinstance(
    reason.premise_steps[0].conclusion.rhs,
    FiniteCyclicGroup,
  )
  assert isinstance(
    reason.premise_steps[1].conclusion,
    TodaSuspensionInjectiveStatement,
  )
  assert isinstance(
    reason.premise_steps[2].conclusion,
    TodaProp42ExactnessStatement,
  )
  assert isinstance(
    reason.premise_steps[3].conclusion,
    TodaHopfInvariantSurjectiveStatement,
  )
  assert isinstance(
    reason.premise_steps[4].conclusion.rhs,
    FiniteCyclicGroup,
  )
  assert (
    reason.premise_steps[0].conclusion.rhs.order
    * reason.premise_steps[4].conclusion.rhs.order
    == conclusion.rhs.order
  )

  order_statement = reason.premise_steps[5].conclusion
  membership_statement = reason.premise_steps[6].conclusion
  assert isinstance(order_statement, Relation)
  assert order_statement.relation_type is RelationType.ORDER
  assert order_statement.lhs == conclusion.rhs.generator
  assert order_statement.rhs == conclusion.rhs.order
  assert isinstance(
    membership_statement,
    HomotopyGroupMembershipStatement,
  )
  assert membership_statement.element == conclusion.rhs.generator


def test_phase150_rc4_5f_2_final_reason_is_visible_before_final_group_conclusion():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reasons,
  ) = _pi6_final_reason_data()

  reason = reasons[0]
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

  assert sentence is not None
  assert "この短完全列と両端の群の位数より" in sentence
  assert r"中央の群の位数は $2\cdot2=4$" in sentence
  assert "中央の群を生成する" in sentence
  assert "である." not in sentence
  assert "であるから" not in sentence
  assert rendered.count(sentence) == 1

  conclusion = r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
  assert conclusion in rendered
  assert rendered.index(sentence) < rendered.index(conclusion)

def test_phase150_rc4_5f_2_classifier_has_no_target_or_rule_name_special_case():
  import toda_group_proof_narrative_reasons as module

  source = inspect.getsource(
    module._final_group_structure_reason
  )

  for fragment in (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
    "inference_rule",
    ".rule",
  ):
    assert fragment not in source


def test_phase150_rc4_5f_2_renderer_has_no_target_or_proposition_special_case():
  import toda_group_proof_narrative_reason_renderer as module

  source = inspect.getsource(
    module.render_toda_group_proof_narrative_reason_sentence
  )

  for fragment in (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
  ):
    assert fragment not in source
