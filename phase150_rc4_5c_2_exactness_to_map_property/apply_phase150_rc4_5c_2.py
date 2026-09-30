from pathlib import Path

ROOT = Path.cwd()
REASONS = ROOT / "toda_group_proof_narrative_reasons.py"
RENDERER = ROOT / "toda_group_proof_narrative_reason_renderer.py"
TEST = ROOT / "tests" / "test_phase150_rc4_5c_2_exactness_to_map_property.py"


def replace_once(text, old, new, path):
  count = text.count(old)
  if count != 1:
    raise RuntimeError(
      f"{path}: expected exactly one replacement target, found {count}"
    )
  return text.replace(old, new, 1)


def patch_reasons():
  path = REASONS
  text = path.read_text(encoding="utf-8")

  old_import = '''from proof import (
  ProofStep,
)
'''
  new_import = '''from proof import (
  ProofStep,
)
from toda_rules import (
  TodaDeltaZeroStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
)
'''
  text = replace_once(text, old_import, new_import, path)

  old_enum = '''  DEFINITION_APPLICABILITY = (
    "definition_applicability"
  )
'''
  new_enum = '''  DEFINITION_APPLICABILITY = (
    "definition_applicability"
  )
  EXACTNESS_TO_MAP_PROPERTY = (
    "exactness_to_map_property"
  )
'''
  text = replace_once(text, old_enum, new_enum, path)

  marker = '''def build_toda_group_proof_narrative_reason_sidecar(
'''
  helper = '''def _exactness_to_map_property_reason(
  proof_step: ProofStep,
) -> TodaGroupProofNarrativeReason | None:
  conclusion = proof_step.conclusion

  if not isinstance(
    conclusion,
    TodaSuspensionInjectiveStatement,
  ):
    return None

  zero_premises = tuple(
    premise
    for premise in proof_step.premises
    if isinstance(
      premise.conclusion,
      TodaDeltaZeroStatement,
    )
  )
  exactness_premises = tuple(
    premise
    for premise in proof_step.premises
    if isinstance(
      premise.conclusion,
      TodaProp42ExactnessStatement,
    )
  )

  compatible_pairs = []

  for zero_premise in zero_premises:
    zero_map = zero_premise.conclusion.map

    for exactness_premise in exactness_premises:
      window = exactness_premise.conclusion.window

      if (
        zero_map.source_group
        != window.source_term
        or zero_map.target_group
        != window.middle_term
        or window.middle_term
        != conclusion.map.source_group
        or window.target_term
        != conclusion.map.target_group
        or getattr(
          window.first_map,
          "name",
          None,
        )
        != "Δ"
        or getattr(
          window.second_map,
          "name",
          None,
        )
        != "E"
      ):
        continue

      compatible_pairs.append(
        (
          zero_premise,
          exactness_premise,
        )
      )

  if len(
    compatible_pairs
  ) != 1:
    return None

  zero_premise, exactness_premise = (
    compatible_pairs[0]
  )

  return TodaGroupProofNarrativeReason(
    kind=(
      TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
    ),
    premise_steps=(
      zero_premise,
      exactness_premise,
    ),
    conclusion_step=proof_step,
  )


'''
  text = replace_once(text, marker, helper + marker, path)

  old_tail = '''    reasons.append(
      TodaGroupProofNarrativeReason(
        kind=(
          TodaGroupProofNarrativeReasonKind
          .DEFINITION_APPLICABILITY
        ),
        premise_steps=(
          dependency.prerequisite_step,
        ),
        conclusion_step=(
          dependency.dependent_step
        ),
        reference_application=reference_application,
      )
    )

  return (
'''
  new_tail = '''    reasons.append(
      TodaGroupProofNarrativeReason(
        kind=(
          TodaGroupProofNarrativeReasonKind
          .DEFINITION_APPLICABILITY
        ),
        premise_steps=(
          dependency.prerequisite_step,
        ),
        conclusion_step=(
          dependency.dependent_step
        ),
        reference_application=reference_application,
      )
    )

  for node in presentation.nodes:
    reason = (
      _exactness_to_map_property_reason(
        node.proof_step
      )
    )

    if reason is not None:
      reasons.append(
        reason
      )

  return (
'''
  text = replace_once(text, old_tail, new_tail, path)

  path.write_text(text, encoding="utf-8")
  print("Patched:", path.name)


def patch_renderer():
  path = RENDERER
  text = path.read_text(encoding="utf-8")

  old = '''    return (
      "この前提条件を満たすので、"
      f"{reference_label} を適用できる.\\n"
      f"{reference_label} の "
      f"${formal_latex}$ を "
      f"${instantiated_latex}$ と定めると、"
    )

  return None
'''
  new = '''    return (
      "この前提条件を満たすので、"
      f"{reference_label} を適用できる.\\n"
      f"{reference_label} の "
      f"${formal_latex}$ を "
      f"${instantiated_latex}$ と定めると、"
    )

  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .EXACTNESS_TO_MAP_PROPERTY
  ):
    if len(reason.premise_steps) != 2:
      return None

    exactness_statement = (
      reason.premise_steps[1].conclusion
    )
    window = exactness_statement.window
    first_map_name = window.first_map.name
    second_map_name = window.second_map.name

    return (
      "この完全性と "
      f"${first_map_name}=0$ より、"
      f"$\\\\ker {second_map_name}"
      f"=\\\\operatorname{{Im}}{first_map_name}=0$ "
      "である.\\n"
      "したがって、"
    )

  return None
'''
  text = replace_once(text, old, new, path)
  path.write_text(text, encoding="utf-8")
  print("Patched:", path.name)


def write_test():
  TEST.write_text(r'''import inspect

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
    "$E:\\pi_{5}^{2} \\to \\pi_{6}^{3}$ "
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
''', encoding="utf-8")
  print("Wrote:", TEST.relative_to(ROOT))


def main():
  patch_reasons()
  patch_renderer()
  write_test()
  print("RC4-5C-2 minimal typed implementation applied.")


if __name__ == "__main__":
  main()
