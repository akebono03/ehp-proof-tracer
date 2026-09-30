from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_rules import (
  TodaDeltaZeroStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
)


def _rule_name(step):
  rule = getattr(step, "inference_rule", None)
  if rule is None:
    return None
  return getattr(rule, "name", None)


def main():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(3, 3)

  injective_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaSuspensionInjectiveStatement,
    )
  )

  print("=" * 78)
  print("Phase 150 / RC4-5C-1 E-injective reason audit")
  print("=" * 78)
  print("presentation nodes:", len(presentation.nodes))
  print("suspension injective steps:", len(injective_steps))

  target_steps = []

  for index, step in enumerate(injective_steps, start=1):
    statement = step.conclusion
    group_map = statement.map
    source = group_map.source_group
    target = group_map.target_group

    print("-" * 78)
    print("injective step", index)
    print("rule:", _rule_name(step))
    print("source:", source)
    print("target:", target)
    print("premise count:", len(step.premises))

    premise_types = tuple(
      type(premise.conclusion).__name__
      for premise in step.premises
    )
    print("premise types:", premise_types)

    for premise_index, premise in enumerate(step.premises):
      print(
        f"  premise[{premise_index}]",
        type(premise.conclusion).__name__,
        "| rule=",
        _rule_name(premise),
        "|",
        repr(premise.conclusion),
      )

    if (
      getattr(source, "group_dimension", None) == 5
      and getattr(source, "sphere_dimension", None) == 2
      and getattr(target, "group_dimension", None) == 6
      and getattr(target, "sphere_dimension", None) == 3
    ):
      target_steps.append(step)

  print("=" * 78)
  print("target E: pi_5^2 -> pi_6^3 steps:", len(target_steps))

  if len(target_steps) != 1:
    print("TARGET_UNIQUENESS=FAIL")
    print("AUDIT_RESULT=FAIL")
    return 1

  target_step = target_steps[0]
  zero_premises = tuple(
    premise
    for premise in target_step.premises
    if isinstance(
      premise.conclusion,
      TodaDeltaZeroStatement,
    )
  )
  exactness_premises = tuple(
    premise
    for premise in target_step.premises
    if isinstance(
      premise.conclusion,
      TodaProp42ExactnessStatement,
    )
  )

  print("delta-zero direct premises:", len(zero_premises))
  print("exactness direct premises:", len(exactness_premises))

  compatible_exactness = []
  for premise in exactness_premises:
    window = premise.conclusion.window
    if (
      window.middle_term == target_step.conclusion.map.source_group
      and window.target_term == target_step.conclusion.map.target_group
      and getattr(window.first_map, "name", None) == "Delta"
      and getattr(window.second_map, "name", None) == "E"
    ):
      compatible_exactness.append(premise)

  compatible_zero = []
  for premise in zero_premises:
    delta_map = premise.conclusion.map
    for exactness in compatible_exactness:
      window = exactness.conclusion.window
      if (
        delta_map.source_group == window.source_term
        and delta_map.target_group == window.middle_term
      ):
        compatible_zero.append(premise)
        break

  print("compatible Delta-E exactness premises:", len(compatible_exactness))
  print("compatible Delta-zero premises:", len(compatible_zero))

  target_node_ids = {
    id(node.proof_step)
    for node in presentation.nodes
  }
  direct_premises_visible = all(
    id(premise) in target_node_ids
    for premise in (
      *compatible_exactness,
      *compatible_zero,
    )
  )
  print("compatible direct premises in presentation:", direct_premises_visible)

  print("-" * 78)

  if (
    len(compatible_exactness) == 1
    and len(compatible_zero) == 1
    and direct_premises_visible
  ):
    print("SAFE_TYPED_REASON=YES")
    print(
      "PROPOSED_REASON="
      "Delta zero + compatible Delta-E exactness -> E injective"
    )
    print(
      "PROPOSED_KIND=EXACTNESS_TO_MAP_PROPERTY"
    )
    print("AUDIT_RESULT=PASS")
    return 0

  print("SAFE_TYPED_REASON=NO")
  print(
    "Reason: the current presentation does not expose one unique "
    "compatible Delta-zero + Delta-E exactness pair as direct premises."
  )
  print("AUDIT_RESULT=PASS")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
