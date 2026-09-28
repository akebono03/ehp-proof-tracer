from expression import (
  HomotopyElement,
  MapApplication,
  MapSymbol,
)
from map_property_rules import (
  InjectiveMapStatement,
  IsomorphismStatement,
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


def derive_representative_end_to_end_result():
  h = MapSymbol(
    name="H",
  )

  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  isomorphism_step = ProofStep(
    conclusion=IsomorphismStatement(
      map=h,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  mapped_equality_step = ProofStep(
    conclusion=Relation(
      lhs=MapApplication(
        map=h,
        expression=a,
      ),
      rhs=MapApplication(
        map=h,
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

  injective_statement = InjectiveMapStatement(
    map=h,
  )

  equality_statement = Relation(
    lhs=a,
    rhs=b,
    relation_type=RelationType.EQUALITY,
  )

  injective_step = next(
    (
      step
      for step in result.steps
      if step.conclusion == injective_statement
    ),
    None,
  )

  equality_step = next(
    (
      step
      for step in result.steps
      if step.conclusion == equality_statement
    ),
    None,
  )

  return (
    h,
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


def print_phase28_inputs():
  print_separator()
  print("Phase 28 representative map-theoretic inputs")
  print_separator()
  print()

  print("Goal:")
  print("  a = b")
  print()

  print("[1] GIVEN")
  print("  H is an isomorphism")
  print()

  print("[2] GIVEN")
  print("  H(a) = H(b)")


def print_injectivity_derivation(data):
  print()
  print_separator()
  print("Isomorphism to injectivity")
  print_separator()
  print()

  (
    h,
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

  print("[3] Derived")
  print("  H is injective")
  print()

  print("  rule:")
  print(
    "   ",
    injective_step.rule,
  )
  print()

  print("  inference rule:")
  print(
    "   ",
    injective_step.inference_rule.name,
  )
  print()

  if injective_step.premises == (
    isomorphism_step,
  ):
    print("  provenance:")
    print("    H is an isomorphism")
  else:
    print("  provenance:")
    print("    unexpected premise chain")


def print_equality_reflection_derivation(data):
  print()
  print_separator()
  print("Equality reflection under injectivity")
  print_separator()
  print()

  (
    h,
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
    reflection_rule.name,
  )
  print()

  print("Premises:")
  print("  1. H is injective")
  print("  2. H(a) = H(b)")
  print()

  if equality_step is None:
    print("[RESULT]")
    print("  a = b was not derived")
    return

  print("[4] Derived")
  print("  a = b")
  print()

  print("  rule:")
  print(
    "   ",
    equality_step.rule,
  )
  print()

  print("  inference rule:")
  print(
    "   ",
    equality_step.inference_rule.name,
  )
  print()

  if equality_step.premises == (
    injective_step,
    mapped_equality_step,
  ):
    print("  direct provenance:")
    print("    derived H injectivity")
    print("    +")
    print("    H(a) = H(b)")
  else:
    print("  direct provenance:")
    print("    unexpected premise chain")


def print_full_proof_trace(data):
  print()
  print_separator()
  print("Human-readable proof trace")
  print_separator()
  print()

  (
    h,
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


def print_phase28_boundary(data):
  print()
  print_separator()
  print("Phase 28 representative boundary")
  print_separator()
  print()

  print("Now demonstrated:")
  print("  Isomorphism(H)")
  print("  → Injective(H)")
  print("  + H(a) = H(b)")
  print("  → a = b")
  print()

  print("Important:")
  print(
    "  H is only a representative MapSymbol "
    "in this Phase"
  )
  print()

  print("Still outside Phase 28:")
  print("  actual Hopf map typing")
  print("  actual H isomorphism fact")
  print("  literature provenance for H")
  print("  Hopf invariant formulas")
  print("  smash-product calculations")
  print("  actual (2ι₂)η₂ = 4η₂ calculation")
  print()

  (
    h,
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
    and result.round_count == 2
  ):
    print("[CONCLUSION]")
    print(
      "  map-property equality reflection "
      "runs end-to-end"
    )
  else:
    print("[CONCLUSION]")
    print(
      "  representative end-to-end proof "
      "was not completed"
    )


def main():
  print()
  print("EHP Proof Tracer")
  print(
    "Phase 28 map-property "
    "capability demonstration"
  )
  print()

  print_phase28_inputs()

  data = derive_representative_end_to_end_result()

  print_injectivity_derivation(
    data
  )

  print_equality_reflection_derivation(
    data
  )

  print_full_proof_trace(
    data
  )

  print_phase28_boundary(
    data
  )

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()





