from pathlib import Path

ROOT = Path.cwd()
REASONS = ROOT / "toda_group_proof_narrative_reasons.py"
RENDERER = ROOT / "toda_group_proof_narrative_reason_renderer.py"


def replace_once(text, old, new, label):
  count = text.count(old)
  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one replacement target, found {count}"
    )
  return text.replace(old, new, 1)


def patch_reasons():
  text = REASONS.read_text(encoding="utf-8")
  text = replace_once(
    text,
    "from proof import (\n  ProofStep,\n)\n",
    "from expression import (\n  Multiple,\n)\nfrom proof import (\n  ProofStep,\n  Relation,\n  RelationType,\n)\n",
    "reasons imports",
  )
  text = replace_once(
    text,
    '  EXACTNESS_TO_MAP_PROPERTY = (\n    "exactness_to_map_property"\n  )\n',
    '  EXACTNESS_TO_MAP_PROPERTY = (\n    "exactness_to_map_property"\n  )\n  MULTIPLE_RELATION_TO_ORDER = (\n    "multiple_relation_to_order"\n  )\n',
    "reason kind",
  )
  helper = '''def _multiple_relation_to_order_reason(
  proof_step: ProofStep,
) -> TodaGroupProofNarrativeReason | None:
  conclusion = proof_step.conclusion

  if (
    not isinstance(conclusion, Relation)
    or conclusion.relation_type is not RelationType.ORDER
    or conclusion.rhs != 4
  ):
    return None

  order_premises = tuple(
    premise
    for premise in proof_step.premises
    if (
      isinstance(premise.conclusion, Relation)
      and premise.conclusion.relation_type is RelationType.ORDER
      and premise.conclusion.rhs == 2
    )
  )
  equality_premises = tuple(
    premise
    for premise in proof_step.premises
    if (
      isinstance(premise.conclusion, Relation)
      and premise.conclusion.relation_type is RelationType.EQUALITY
      and isinstance(premise.conclusion.lhs, Multiple)
      and premise.conclusion.lhs.coefficient == 2
    )
  )

  compatible_pairs = []

  for order_premise in order_premises:
    ordered_expression = order_premise.conclusion.lhs

    for equality_premise in equality_premises:
      equality = equality_premise.conclusion
      multiple = equality.lhs

      if (
        equality.rhs != ordered_expression
        or multiple.expression != conclusion.lhs
      ):
        continue

      compatible_pairs.append((order_premise, equality_premise))

  if len(compatible_pairs) != 1:
    return None

  order_premise, equality_premise = compatible_pairs[0]

  return TodaGroupProofNarrativeReason(
    kind=(
      TodaGroupProofNarrativeReasonKind
      .MULTIPLE_RELATION_TO_ORDER
    ),
    premise_steps=(order_premise, equality_premise),
    conclusion_step=proof_step,
  )


'''
  text = replace_once(
    text,
    "def build_toda_group_proof_narrative_reason_sidecar(\n",
    helper + "def build_toda_group_proof_narrative_reason_sidecar(\n",
    "helper insertion",
  )
  old = '''  for node in presentation.nodes:
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
  new = '''  for node in presentation.nodes:
    exactness_reason = (
      _exactness_to_map_property_reason(
        node.proof_step
      )
    )

    if exactness_reason is not None:
      reasons.append(exactness_reason)

    multiple_order_reason = (
      _multiple_relation_to_order_reason(
        node.proof_step
      )
    )

    if multiple_order_reason is not None:
      reasons.append(multiple_order_reason)

  return (
'''
  text = replace_once(text, old, new, "builder loop")
  REASONS.write_text(text, encoding="utf-8")


def patch_renderer():
  text = RENDERER.read_text(encoding="utf-8")
  branch = r'''  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .MULTIPLE_RELATION_TO_ORDER
  ):
    if len(reason.premise_steps) != 2:
      return None

    order_statement = reason.premise_steps[0].conclusion
    equality_statement = reason.premise_steps[1].conclusion
    ordered_latex = render_toda_expression_latex(order_statement.lhs)
    target_latex = render_toda_expression_latex(
      equality_statement.lhs.expression
    )

    return (
      f"$\\operatorname{{ord}}({ordered_latex})=2$ "
      f"かつ $2{target_latex}={ordered_latex}$ より、"
      f"$4{target_latex}=0$ かつ "
      f"$2{target_latex}\\neq0$ である.\\n"
      "したがって、"
    )

  return None


def insert_toda_group_proof_narrative_reason_prose(
'''
  text = replace_once(
    text,
    "  return None\n\n\ndef insert_toda_group_proof_narrative_reason_prose(\n",
    branch,
    "renderer branch",
  )
  RENDERER.write_text(text, encoding="utf-8")


def main():
  patch_reasons()
  patch_renderer()
  print("RC4-5D-3 production patch applied.")


if __name__ == "__main__":
  main()
