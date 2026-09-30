from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REASONS = ROOT / "toda_group_proof_narrative_reasons.py"
RENDERER = ROOT / "toda_group_proof_narrative_reason_renderer.py"
TEST = ROOT / "tests" / "test_phase150_rc4_5f_2_final_group_structure_reason.py"


def replace_once(text, old, new, label):
  count = text.count(old)
  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one replacement target; found {count}"
    )
  return text.replace(old, new, 1)


def update_reasons():
  text = REASONS.read_text(encoding="utf-8")

  text = replace_once(
    text,
    """from dataclasses import dataclass
from enum import Enum

from expression import (
  Multiple,
)
""",
    """from dataclasses import dataclass
from enum import Enum

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  Multiple,
)
from homotopy_groups import (
  FiniteCyclicGroup,
)
""",
    "reason imports part 1",
  )

  text = replace_once(
    text,
    """from toda_rules import (
  TodaDeltaZeroStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
)
""",
    """from toda_rules import (
  TodaDeltaZeroStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
)
""",
    "reason imports part 2",
  )

  text = replace_once(
    text,
    """  MULTIPLE_RELATION_TO_ORDER = (
    "multiple_relation_to_order"
  )
""",
    """  MULTIPLE_RELATION_TO_ORDER = (
    "multiple_relation_to_order"
  )
  FINAL_GROUP_STRUCTURE = (
    "final_group_structure"
  )
""",
    "reason enum",
  )

  new_function = """def _final_group_structure_reason(
  proof_step: ProofStep,
) -> TodaGroupProofNarrativeReason | None:
  conclusion = proof_step.conclusion

  if (
    not isinstance(conclusion, Relation)
    or conclusion.relation_type is not RelationType.EQUALITY
    or not isinstance(conclusion.rhs, FiniteCyclicGroup)
  ):
    return None

  middle_group = conclusion.lhs
  target_group = conclusion.rhs
  target_order = target_group.order
  target_generator = target_group.generator

  order_premises = tuple(
    premise
    for premise in proof_step.premises
    if (
      isinstance(premise.conclusion, Relation)
      and premise.conclusion.relation_type is RelationType.ORDER
      and premise.conclusion.lhs == target_generator
      and premise.conclusion.rhs == target_order
    )
  )
  membership_premises = tuple(
    premise
    for premise in proof_step.premises
    if (
      isinstance(
        premise.conclusion,
        HomotopyGroupMembershipStatement,
      )
      and premise.conclusion.element == target_generator
      and premise.conclusion.group_dimension
      == getattr(middle_group, "group_dimension", None)
      and premise.conclusion.sphere_dimension
      == getattr(middle_group, "sphere_dimension", None)
    )
  )
  exactness_premises = tuple(
    premise
    for premise in proof_step.premises
    if (
      isinstance(
        premise.conclusion,
        TodaProp42ExactnessStatement,
      )
      and premise.conclusion.window.middle_term == middle_group
    )
  )

  compatible_structural_chains = []

  for exactness_premise in exactness_premises:
    window = exactness_premise.conclusion.window

    left_group_premises = tuple(
      premise
      for premise in proof_step.premises
      if (
        isinstance(premise.conclusion, Relation)
        and premise.conclusion.relation_type is RelationType.EQUALITY
        and premise.conclusion.lhs == window.source_term
        and isinstance(
          premise.conclusion.rhs,
          FiniteCyclicGroup,
        )
      )
    )
    right_group_premises = tuple(
      premise
      for premise in proof_step.premises
      if (
        isinstance(premise.conclusion, Relation)
        and premise.conclusion.relation_type is RelationType.EQUALITY
        and premise.conclusion.lhs == window.target_term
        and isinstance(
          premise.conclusion.rhs,
          FiniteCyclicGroup,
        )
      )
    )
    injective_premises = tuple(
      premise
      for premise in proof_step.premises
      if (
        isinstance(
          premise.conclusion,
          TodaSuspensionInjectiveStatement,
        )
        and premise.conclusion.map.source_group
        == window.source_term
        and premise.conclusion.map.target_group
        == window.middle_term
      )
    )
    surjective_premises = tuple(
      premise
      for premise in proof_step.premises
      if (
        isinstance(
          premise.conclusion,
          TodaHopfInvariantSurjectiveStatement,
        )
        and premise.conclusion.map.source_group
        == window.middle_term
        and premise.conclusion.map.target_group
        == window.target_term
      )
    )

    if (
      len(left_group_premises) != 1
      or len(right_group_premises) != 1
      or len(injective_premises) != 1
      or len(surjective_premises) != 1
    ):
      continue

    left_group_premise = left_group_premises[0]
    right_group_premise = right_group_premises[0]

    if (
      left_group_premise.conclusion.rhs.order
      * right_group_premise.conclusion.rhs.order
      != target_order
    ):
      continue

    compatible_structural_chains.append(
      (
        left_group_premise,
        injective_premises[0],
        exactness_premise,
        surjective_premises[0],
        right_group_premise,
      )
    )

  if (
    len(order_premises) != 1
    or len(membership_premises) != 1
    or len(compatible_structural_chains) != 1
  ):
    return None

  structural_chain = compatible_structural_chains[0]

  return TodaGroupProofNarrativeReason(
    kind=(
      TodaGroupProofNarrativeReasonKind
      .FINAL_GROUP_STRUCTURE
    ),
    premise_steps=(
      structural_chain
      + (
        order_premises[0],
        membership_premises[0],
      )
    ),
    conclusion_step=proof_step,
  )


"""

  anchor = "def build_toda_group_proof_narrative_reason_sidecar(\n"
  if anchor not in text:
    raise RuntimeError("reason function insertion anchor not found")
  text = text.replace(anchor, new_function + anchor, 1)

  text = replace_once(
    text,
    """    if multiple_order_reason is not None:
      reasons.append(multiple_order_reason)

  return (
""",
    """    if multiple_order_reason is not None:
      reasons.append(multiple_order_reason)

    final_group_structure_reason = (
      _final_group_structure_reason(
        node.proof_step
      )
    )

    if final_group_structure_reason is not None:
      reasons.append(
        final_group_structure_reason
      )

  return (
""",
    "reason builder loop",
  )

  REASONS.write_text(text, encoding="utf-8")


def update_renderer():
  text = RENDERER.read_text(encoding="utf-8")

  branch = """  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .FINAL_GROUP_STRUCTURE
  ):
    if len(reason.premise_steps) != 7:
      return None

    left_group_statement = reason.premise_steps[0].conclusion
    right_group_statement = reason.premise_steps[4].conclusion
    order_statement = reason.premise_steps[5].conclusion
    membership_statement = reason.premise_steps[6].conclusion

    left_order = left_group_statement.rhs.order
    right_order = right_group_statement.rhs.order
    middle_order = left_order * right_order
    generator_latex = render_toda_expression_latex(
      membership_statement.element
    )

    return (
      "この短完全列と両端の群の位数より、"
      f"中央の群の位数は ${left_order}\\cdot"
      f"{right_order}={middle_order}$ である.\\n"
      f"また、${generator_latex}$ は中央の群に属し、"
      f"$\\operatorname{{ord}}({generator_latex})"
      f"={order_statement.rhs}={middle_order}$ であるから、"
      f"${generator_latex}$ は中央の群を生成する.\\n"
      "したがって、"
    )

"""

  anchor = "  return None\n\n\ndef insert_toda_group_proof_narrative_reason_prose(\n"
  if anchor not in text:
    raise RuntimeError("reason renderer insertion anchor not found")
  text = text.replace(
    anchor,
    branch + anchor,
    1,
  )

  RENDERER.write_text(text, encoding="utf-8")


def write_test():
  TEST.write_text("""import inspect

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
  assert "中央の群の位数は $2\\cdot2=4$" in sentence
  assert "中央の群を生成する" in sentence
  assert rendered.count(sentence) == 1

  conclusion = "$\\pi_{6}^{3} = \\mathbb{Z}/4\\{\\nu'\\}$"
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
""", encoding="utf-8")


def main():
  update_reasons()
  update_renderer()
  write_test()
  print("RC4-5F-2 minimal implementation applied.")
  print("Changed production files:")
  print("  toda_group_proof_narrative_reasons.py")
  print("  toda_group_proof_narrative_reason_renderer.py")
  print("Added test:")
  print("  tests/test_phase150_rc4_5f_2_final_group_structure_reason.py")


if __name__ == "__main__":
  main()
