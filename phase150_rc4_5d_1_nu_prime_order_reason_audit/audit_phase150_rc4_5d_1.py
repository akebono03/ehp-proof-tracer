from proof import (
  Relation,
  RelationType,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_proof_dependency import (
  extract_toda_recursive_proof_provenance,
)


def _is_order_four_relation(statement):
  return (
    isinstance(statement, Relation)
    and statement.relation_type is RelationType.ORDER
    and statement.rhs == 4
  )


def _rule_name(step):
  rule = step.inference_rule
  return None if rule is None else rule.name


def main():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  provenance = extract_toda_recursive_proof_provenance(
    presentation.source_replay.group_result
  )

  order_four_steps = tuple(
    node.proof_step
    for node in provenance.nodes
    if _is_order_four_relation(
      node.proof_step.conclusion
    )
  )

  print("=" * 78)
  print("Phase 150 / RC4-5D-1 ord(nu-prime)=4 reason-chain audit")
  print("=" * 78)
  print("presentation nodes:", len(presentation.nodes))
  print("provenance nodes:", len(provenance.nodes))
  print("order-four steps:", len(order_four_steps))

  if not order_four_steps:
    raise AssertionError("no order-four step found")

  presentation_step_ids = {
    id(node.proof_step)
    for node in presentation.nodes
  }

  for index, step in enumerate(order_four_steps, 1):
    print("-" * 78)
    print("order-four step", index)
    print("rule:", _rule_name(step))
    print("conclusion type:", type(step.conclusion).__name__)
    print("conclusion:", step.conclusion)
    print("direct premise count:", len(step.premises))
    print(
      "direct premise types:",
      tuple(
        type(premise.conclusion).__name__
        for premise in step.premises
      ),
    )
    print(
      "direct premises in presentation:",
      tuple(
        id(premise) in presentation_step_ids
        for premise in step.premises
      ),
    )

    for premise_index, premise in enumerate(step.premises):
      print(
        f"  premise[{premise_index}]",
        type(premise.conclusion).__name__,
        "| rule=",
        _rule_name(premise),
        "|",
        premise.conclusion,
      )
      print(
        "    nested premise types:",
        tuple(
          type(nested.conclusion).__name__
          for nested in premise.premises
        ),
      )

  target_steps = tuple(
    step
    for step in order_four_steps
    if "ν" in repr(step.conclusion)
    or "nu" in repr(step.conclusion).lower()
  )

  print("=" * 78)
  print("nu-like order-four steps:", len(target_steps))

  if len(target_steps) != 1:
    print("SAFE_TYPED_REASON=NO")
    print("AUDIT_RESULT=PASS")
    return 0

  target = target_steps[0]
  premise_types = tuple(
    type(premise.conclusion).__name__
    for premise in target.premises
  )
  premise_reprs = tuple(
    repr(premise.conclusion)
    for premise in target.premises
  )

  has_group_information = any(
    "FiniteCyclicGroup" in text
    or "TodaPrimaryGroup" in text
    for text in premise_reprs
  )
  has_map_property = any(
    "Injective" in name
    or "Isomorphism" in name
    for name in premise_types
  )
  has_relation = any(
    isinstance(premise.conclusion, Relation)
    for premise in target.premises
  )

  print("has group information:", has_group_information)
  print("has map property:", has_map_property)
  print("has relation premise:", has_relation)

  if len(target.premises) <= 2 and not (
    has_group_information or has_map_property
  ):
    print(
      "INSUFFICIENT_PATTERN="
      "possible multiple-relation + rhs-order only"
    )
    print("SAFE_TYPED_REASON=NO")
  else:
    print(
      "INSUFFICIENT_PATTERN="
      "not merely multiple-relation + rhs-order"
    )
    print("SAFE_TYPED_REASON=NEEDS_CLASSIFICATION")

  print("AUDIT_RESULT=PASS")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
