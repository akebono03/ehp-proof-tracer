from expression import (
  HomotopyElement,
  MapApplication,
)
from map_facts import (
  HOPF_MAP,
  HOPF_MAP_ISOMORPHISM_FACT,
  HOPF_MAP_TYPING_FACT,
  MAP_ISOMORPHISM_FACT_REPOSITORY,
)
from map_property_rules import (
  InjectiveMapStatement,
  injective_map_reflects_equality_inference_rule,
  isomorphism_implies_injective_inference_rule,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  run_inference_until_stable_with_history,
)


def print_separator():
  print("=" * 60)


def derive_actual_h_end_to_end_result():
  fact = (
    MAP_ISOMORPHISM_FACT_REPOSITORY
    .lookup(
      HOPF_MAP_TYPING_FACT
    )
  )

  if fact is None:
    return None

  isomorphism_step = (
    fact.to_proof_step()
  )

  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  mapped_equality_step = ProofStep(
    conclusion=Relation(
      lhs=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
      rhs=MapApplication(
        map=HOPF_MAP,
        expression=b,
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  isomorphism_rule = (
    isomorphism_implies_injective_inference_rule()
  )

  reflection_rule = (
    injective_map_reflects_equality_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      isomorphism_rule,
      reflection_rule,
    ),
    (
      isomorphism_step,
      mapped_equality_step,
    ),
  )

  injective_step = next(
    (
      step
      for step in result.steps
      if step.conclusion
      == InjectiveMapStatement(
        map=HOPF_MAP,
      )
    ),
    None,
  )

  equality_step = next(
    (
      step
      for step in result.steps
      if step.conclusion
      == Relation(
        lhs=a,
        rhs=b,
        relation_type=RelationType.EQUALITY,
      )
    ),
    None,
  )

  return (
    fact,
    a,
    b,
    isomorphism_step,
    mapped_equality_step,
    isomorphism_rule,
    reflection_rule,
    result,
    injective_step,
    equality_step,
  )


def print_actual_h_knowledge():
  print_separator()
  print("Phase 29 actual H mathematical knowledge")
  print_separator()
  print()

  print("[1] Production map identity")
  print("  HOPF_MAP")
  print("  → H")
  print()

  print("[2] Production map typing")
  print("  H : π₃(S²) → π₃(S³)")
  print()

  print("[3] Production map-property fact")
  print(
    "  H : π₃(S²) → π₃(S³) "
    "is an isomorphism"
  )
  print()

  print("[4] Repository lookup")
  fact = (
    MAP_ISOMORPHISM_FACT_REPOSITORY
    .lookup(
      HOPF_MAP_TYPING_FACT
    )
  )

  if fact is (
    HOPF_MAP_ISOMORPHISM_FACT
  ):
    print("  HOPF_MAP_ISOMORPHISM_FACT")
    print("  → found")
  else:
    print("  actual H isomorphism fact")
    print("  → not found")


def print_materialization_demo(data):
  print()
  print_separator()
  print("Actual H fact to proof-level statement")
  print_separator()
  print()

  if data is None:
    print("[ERROR]")
    print("  actual H data is unavailable")
    return

  (
    fact,
    a,
    b,
    isomorphism_step,
    mapped_equality_step,
    isomorphism_rule,
    reflection_rule,
    result,
    injective_step,
    equality_step,
  ) = data

  print("[5] to_proof_step()")
  print()
  print("GIVEN")
  print("  H is an isomorphism")
  print()
  print(
    "  source knowledge:"
  )
  print(
    "  H : π₃(S²) → π₃(S³) "
    "is an isomorphism"
  )


def print_injectivity_demo(data):
  print()
  print_separator()
  print("Actual H injectivity")
  print_separator()
  print()

  if data is None:
    print("[ERROR]")
    print("  actual H data is unavailable")
    return

  (
    fact,
    a,
    b,
    isomorphism_step,
    mapped_equality_step,
    isomorphism_rule,
    reflection_rule,
    result,
    injective_step,
    equality_step,
  ) = data

  print("Apply:")
  print(
    " ",
    isomorphism_rule.name,
  )
  print()

  if injective_step is None:
    print("[RESULT]")
    print("  H injectivity was not derived")
    return

  print("[6] Derived")
  print("  H is injective")


def print_equality_reflection_demo(data):
  print()
  print_separator()
  print("Actual H equality reflection")
  print_separator()
  print()

  if data is None:
    print("[ERROR]")
    print("  actual H data is unavailable")
    return

  (
    fact,
    a,
    b,
    isomorphism_step,
    mapped_equality_step,
    isomorphism_rule,
    reflection_rule,
    result,
    injective_step,
    equality_step,
  ) = data

  print("[7] GIVEN")
  print("  H(a) = H(b)")
  print()

  print("Apply:")
  print(
    " ",
    reflection_rule.name,
  )
  print()

  if equality_step is None:
    print("[RESULT]")
    print("  a = b was not derived")
    return

  print("[8] Derived")
  print("  a = b")


def print_full_proof_trace(data):
  print()
  print_separator()
  print("Human-readable actual H proof trace")
  print_separator()
  print()

  if data is None:
    print("[ERROR]")
    print("  actual H data is unavailable")
    return

  (
    fact,
    a,
    b,
    isomorphism_step,
    mapped_equality_step,
    isomorphism_rule,
    reflection_rule,
    result,
    injective_step,
    equality_step,
  ) = data

  if (
    injective_step is None
    or equality_step is None
  ):
    print("[ERROR]")
    print("  complete proof trace is unavailable")
    return

  print("PRODUCTION FACT")
  print(
    "  H : π₃(S²) → π₃(S³) "
    "is an isomorphism"
  )
  print()

  print("MATERIALIZE")
  print("  ↓")
  print()

  print("GIVEN")
  print("  H is an isomorphism")
  print()

  print("INFERENCE")
  print(
    " ",
    isomorphism_rule.name,
  )
  print("  ↓")
  print("  H is injective")
  print()

  print("GIVEN")
  print("  H(a) = H(b)")
  print()

  print("INFERENCE")
  print(
    " ",
    reflection_rule.name,
  )
  print("  ↓")
  print("  a = b")
  print()

  print("Inference engine:")
  print(
    "  rounds =",
    result.round_count,
  )
  print(
    "  termination =",
    result.termination_reason,
  )


def print_phase29_boundary(data):
  print()
  print_separator()
  print("Phase 29-8 boundary")
  print_separator()
  print()

  print("Now connected:")
  print(
    "  production H isomorphism fact"
  )
  print("  ↓")
  print("  proof-level Isomorphism(H)")
  print("  ↓")
  print("  Injective(H)")
  print("  +")
  print("  H(a) = H(b)")
  print("  ↓")
  print("  a = b")
  print()

  print("Still outside Phase 29-8:")
  print("  actual H((2ι₂)η₂) calculation")
  print("  Hopf formula")
  print("  smash product")
  print("  actual mapped equality")
  print(
    "  H((2ι₂)η₂)=H(4η₂)"
  )
  print()

  if data is None:
    return

  (
    fact,
    a,
    b,
    isomorphism_step,
    mapped_equality_step,
    isomorphism_rule,
    reflection_rule,
    result,
    injective_step,
    equality_step,
  ) = data

  if (
    injective_step is not None
    and equality_step is not None
  ):
    print("[CONCLUSION]")
    print(
      "  actual H fact-driven equality "
      "reflection runs end-to-end"
    )
  else:
    print("[CONCLUSION]")
    print(
      "  actual H end-to-end proof "
      "was not completed"
    )


def main():
  print()
  print("EHP Proof Tracer")
  print(
    "Phase 29 actual H map-property "
    "capability demonstration"
  )
  print()

  print_actual_h_knowledge()

  data = (
    derive_actual_h_end_to_end_result()
  )

  print_materialization_demo(
    data
  )

  print_injectivity_demo(
    data
  )

  print_equality_reflection_demo(
    data
  )

  print_full_proof_trace(
    data
  )

  print_phase29_boundary(
    data
  )

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()



