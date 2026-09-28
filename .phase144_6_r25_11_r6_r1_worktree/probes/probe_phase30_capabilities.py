from expression import (
  Composition,
  HomotopyElement,
  MapApplication,
  Suspension,
)
from hopf_rules import (
  HopfInvariantStatement,
  hopf_composition_formula_inference_rule,
  hopf_composition_law_inference_rule,
  hopf_invariant_proof_step,
  hopf_invariant_statement_to_ehp_h_equality_inference_rule,
)
from map_facts import EHP_H_MAP
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from relation_rules import (
  equality_preserved_under_right_composition_inference_rule,
  equality_symmetry_inference_rule,
  equality_transitivity_inference_rule,
)


def print_separator():
  print("=" * 60)


def derive_phase30_right_formula():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  beta = HomotopyElement(
    name="beta",
    dimension=1,
  )

  suspended_b = Suspension(
    expression=b,
  )

  hopf_step = hopf_invariant_proof_step(
    HopfInvariantStatement(
      expression=a,
      value=beta,
    )
  )

  law_rule = (
    hopf_composition_law_inference_rule()
  )

  law_match = find_inference_match(
    law_rule,
    (
      hopf_step,
    ),
  )

  if law_match is None:
    return None

  law_step = apply_inference_match(
    law_match
  )

  b_step = ProofStep(
    conclusion=b,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  formula_rule = (
    hopf_composition_formula_inference_rule()
  )

  formula_match = find_inference_match(
    formula_rule,
    (
      law_step,
      b_step,
    ),
  )

  if formula_match is None:
    return None

  formula_step = apply_inference_match(
    formula_match
  )

  bridge_rule = (
    hopf_invariant_statement_to_ehp_h_equality_inference_rule()
  )

  formula_bridge_match = (
    find_inference_match(
      bridge_rule,
      (
        formula_step,
      ),
    )
  )

  if formula_bridge_match is None:
    return None

  composed_h_equality_step = (
    apply_inference_match(
      formula_bridge_match
    )
  )

  base_bridge_match = (
    find_inference_match(
      bridge_rule,
      (
        hopf_step,
      ),
    )
  )

  if base_bridge_match is None:
    return None

  base_h_equality_step = (
    apply_inference_match(
      base_bridge_match
    )
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  symmetry_match = find_inference_match(
    symmetry_rule,
    (
      base_h_equality_step,
    ),
  )

  if symmetry_match is None:
    return None

  reversed_base_step = (
    apply_inference_match(
      symmetry_match
    )
  )

  right_composition_rule = (
    equality_preserved_under_right_composition_inference_rule(
      suspended_b
    )
  )

  right_composition_match = (
    find_inference_match(
      right_composition_rule,
      (
        reversed_base_step,
      ),
    )
  )

  if right_composition_match is None:
    return None

  right_composition_step = (
    apply_inference_match(
      right_composition_match
    )
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  transitivity_match = (
    find_inference_match(
      transitivity_rule,
      (
        composed_h_equality_step,
        right_composition_step,
      ),
    )
  )

  if transitivity_match is None:
    return None

  final_step = apply_inference_match(
    transitivity_match
  )

  return (
    a,
    b,
    beta,
    suspended_b,
    hopf_step,
    law_rule,
    law_step,
    b_step,
    formula_rule,
    formula_step,
    bridge_rule,
    composed_h_equality_step,
    base_h_equality_step,
    symmetry_rule,
    reversed_base_step,
    right_composition_rule,
    right_composition_step,
    transitivity_rule,
    final_step,
  )


def print_target():
  print_separator()
  print("Phase 30-8 target")
  print_separator()
  print()

  print("[Toda] Proposition 2.2")
  print()

  print("Target:")
  print("  H(a ∘ Eb) = H(a) ∘ Eb")
  print()

  print("Current Phase 30 scope:")
  print(
    "  right suspended-composition "
    "formula only"
  )
  print()

  print("The probe uses:")
  print("  existing HopfInvariantStatement")
  print("  existing Hopf composition rule")
  print("  actual EHP H map bridge")
  print("  equality symmetry")
  print("  staged right composition")
  print("  equality transitivity")


def print_initial_hopf_fact(data):
  print()
  print_separator()
  print("Base Hopf-invariant fact")
  print_separator()
  print()

  if data is None:
    print("[ERROR]")
    print("  Phase 30 data is unavailable")
    return

  (
    a,
    b,
    beta,
    suspended_b,
    hopf_step,
    law_rule,
    law_step,
    b_step,
    formula_rule,
    formula_step,
    bridge_rule,
    composed_h_equality_step,
    base_h_equality_step,
    symmetry_rule,
    reversed_base_step,
    right_composition_rule,
    right_composition_step,
    transitivity_rule,
    final_step,
  ) = data

  print("GIVEN")
  print("  H(a) = beta")
  print()

  print("Internal representation:")
  print("  HopfInvariantStatement(")
  print("    expression=a,")
  print("    value=beta,")
  print("  )")
  print()

  print("Materialized actual-H equality:")
  print("  H(a) = beta")
  print()

  print("Map:")
  print(
    " ",
    base_h_equality_step
    .conclusion
    .lhs
    .map
    .name,
  )


def print_hopf_composition_formula(data):
  print()
  print_separator()
  print("Hopf composition formula")
  print_separator()
  print()

  if data is None:
    print("[ERROR]")
    print("  Phase 30 data is unavailable")
    return

  (
    a,
    b,
    beta,
    suspended_b,
    hopf_step,
    law_rule,
    law_step,
    b_step,
    formula_rule,
    formula_step,
    bridge_rule,
    composed_h_equality_step,
    base_h_equality_step,
    symmetry_rule,
    reversed_base_step,
    right_composition_rule,
    right_composition_step,
    transitivity_rule,
    final_step,
  ) = data

  print("INFERENCE")
  print(
    " ",
    law_rule.name,
  )
  print("  ↓")
  print(
    "  generalized Hopf composition "
    "law enabled"
  )
  print()

  print("GIVEN")
  print("  b")
  print()

  print("INFERENCE")
  print(
    " ",
    formula_rule.name,
  )
  print("  ↓")
  print("  H(a ∘ Eb) = beta ∘ Eb")
  print()

  print("Bridge to actual EHP H map:")
  print(
    " ",
    bridge_rule.name,
  )
  print("  ↓")
  print("  H(a ∘ Eb) = beta ∘ Eb")


def print_right_side_conversion(data):
  print()
  print_separator()
  print("Right-hand side conversion")
  print_separator()
  print()

  if data is None:
    print("[ERROR]")
    print("  Phase 30 data is unavailable")
    return

  (
    a,
    b,
    beta,
    suspended_b,
    hopf_step,
    law_rule,
    law_step,
    b_step,
    formula_rule,
    formula_step,
    bridge_rule,
    composed_h_equality_step,
    base_h_equality_step,
    symmetry_rule,
    reversed_base_step,
    right_composition_rule,
    right_composition_step,
    transitivity_rule,
    final_step,
  ) = data

  print("From:")
  print("  H(a) = beta")
  print()

  print("INFERENCE")
  print(
    " ",
    symmetry_rule.name,
  )
  print("  ↓")
  print("  beta = H(a)")
  print()

  print("INFERENCE")
  print(
    " ",
    right_composition_rule.name,
  )
  print("  ↓")
  print(
    "  beta ∘ Eb = H(a) ∘ Eb"
  )
  print()

  print("Important:")
  print(
    "  right composition is applied "
    "as one staged step"
  )


def print_final_closure(data):
  print()
  print_separator()
  print("Prop.2.2 right-formula closure")
  print_separator()
  print()

  if data is None:
    print("[ERROR]")
    print("  Phase 30 data is unavailable")
    return

  (
    a,
    b,
    beta,
    suspended_b,
    hopf_step,
    law_rule,
    law_step,
    b_step,
    formula_rule,
    formula_step,
    bridge_rule,
    composed_h_equality_step,
    base_h_equality_step,
    symmetry_rule,
    reversed_base_step,
    right_composition_rule,
    right_composition_step,
    transitivity_rule,
    final_step,
  ) = data

  print("We now have:")
  print("  H(a ∘ Eb) = beta ∘ Eb")
  print("  beta ∘ Eb = H(a) ∘ Eb")
  print()

  print("INFERENCE")
  print(
    " ",
    transitivity_rule.name,
  )
  print("  ↓")
  print()

  print("[RESULT]")
  print(
    "  H(a ∘ Eb) = H(a) ∘ Eb"
  )


def print_full_proof_trace(data):
  print()
  print_separator()
  print("Human-readable proof trace")
  print_separator()
  print()

  if data is None:
    print("[ERROR]")
    print(
      "  complete Phase 30 proof "
      "trace is unavailable"
    )
    return

  (
    a,
    b,
    beta,
    suspended_b,
    hopf_step,
    law_rule,
    law_step,
    b_step,
    formula_rule,
    formula_step,
    bridge_rule,
    composed_h_equality_step,
    base_h_equality_step,
    symmetry_rule,
    reversed_base_step,
    right_composition_rule,
    right_composition_step,
    transitivity_rule,
    final_step,
  ) = data

  print("GIVEN")
  print("  H(a) = beta")
  print()

  print("INFERENCE")
  print(
    " ",
    law_rule.name,
  )
  print("  ↓")
  print(
    "  Hopf composition law "
    "for a and beta"
  )
  print()

  print("GIVEN")
  print("  b")
  print()

  print("INFERENCE")
  print(
    " ",
    formula_rule.name,
  )
  print("  ↓")
  print(
    "  H(a ∘ Eb) = beta ∘ Eb"
  )
  print()

  print("INFERENCE")
  print(
    " ",
    bridge_rule.name,
  )
  print("  ↓")
  print(
    "  actual EHP H equality:"
  )
  print(
    "  H(a ∘ Eb) = beta ∘ Eb"
  )
  print()

  print("GIVEN")
  print("  H(a) = beta")
  print()

  print("INFERENCE")
  print(
    " ",
    bridge_rule.name,
  )
  print("  ↓")
  print(
    "  actual EHP H equality:"
  )
  print("  H(a) = beta")
  print()

  print("INFERENCE")
  print(
    " ",
    symmetry_rule.name,
  )
  print("  ↓")
  print("  beta = H(a)")
  print()

  print("INFERENCE")
  print(
    " ",
    right_composition_rule.name,
  )
  print("  ↓")
  print(
    "  beta ∘ Eb = H(a) ∘ Eb"
  )
  print()

  print("INFERENCE")
  print(
    " ",
    transitivity_rule.name,
  )
  print("  ↓")
  print()

  print("FINAL")
  print(
    "  H(a ∘ Eb) = H(a) ∘ Eb"
  )


def print_provenance(data):
  print()
  print_separator()
  print("Proof provenance")
  print_separator()
  print()

  if data is None:
    print("[ERROR]")
    print("  provenance is unavailable")
    return

  (
    a,
    b,
    beta,
    suspended_b,
    hopf_step,
    law_rule,
    law_step,
    b_step,
    formula_rule,
    formula_step,
    bridge_rule,
    composed_h_equality_step,
    base_h_equality_step,
    symmetry_rule,
    reversed_base_step,
    right_composition_rule,
    right_composition_step,
    transitivity_rule,
    final_step,
  ) = data

  print("Final equality premises:")
  print(
    "  H(a ∘ Eb) = beta ∘ Eb"
  )
  print("  +")
  print(
    "  beta ∘ Eb = H(a) ∘ Eb"
  )
  print()

  print("Left branch:")
  print(
    "  final transitivity premise"
  )
  print("  ↓")
  print(
    "  actual-H bridge"
  )
  print("  ↓")
  print(
    "  Hopf composition formula"
  )
  print("  ↓")
  print(
    "  Hopf composition law"
  )
  print("  ↓")
  print("  GIVEN H(a) = beta")
  print()

  print("Right branch:")
  print(
    "  final transitivity premise"
  )
  print("  ↓")
  print(
    "  staged right composition"
  )
  print("  ↓")
  print("  equality symmetry")
  print("  ↓")
  print(
    "  actual-H bridge"
  )
  print("  ↓")
  print("  GIVEN H(a) = beta")
  print()

  valid = (
    final_step.premises
    == (
      composed_h_equality_step,
      right_composition_step,
    )
    and composed_h_equality_step.premises
    == (
      formula_step,
    )
    and formula_step.premises
    == (
      law_step,
      b_step,
    )
    and law_step.premises
    == (
      hopf_step,
    )
    and right_composition_step.premises
    == (
      reversed_base_step,
    )
    and reversed_base_step.premises
    == (
      base_h_equality_step,
    )
    and base_h_equality_step.premises
    == (
      hopf_step,
    )
  )

  if valid:
    print("[PROVENANCE]")
    print(
      "  full proof chain is preserved"
    )
  else:
    print("[PROVENANCE]")
    print(
      "  unexpected proof chain"
    )


def print_phase30_boundary(data):
  print()
  print_separator()
  print("Phase 30-8 boundary")
  print_separator()
  print()

  print("Now demonstrated:")
  print(
    "  H(a ∘ Eb) = H(a) ∘ Eb"
  )
  print()

  print("Using:")
  print("  HopfInvariantStatement")
  print(
    "  Hopf composition formula"
  )
  print("  actual EHP H map bridge")
  print("  equality symmetry")
  print("  staged right composition")
  print("  equality transitivity")
  print()

  print("Still outside Phase 30-8:")
  print(
    "  H((Ec) ∘ a)"
    " = E(c ∧ c) ∘ H(a)"
  )
  print("  smash product c ∧ c")
  print("  Barratt-Hilton Prop.3.1")
  print(
    "  actual H((2ι₂)η₂) "
    "calculation"
  )
  print(
    "  H((2ι₂)η₂)=H(4η₂)"
  )
  print(
    "  (2ι₂)η₂=4η₂"
  )
  print()

  if data is None:
    print("[CONCLUSION]")
    print(
      "  Phase 30 right-formula "
      "proof was not completed"
    )
    return

  (
    a,
    b,
    beta,
    suspended_b,
    hopf_step,
    law_rule,
    law_step,
    b_step,
    formula_rule,
    formula_step,
    bridge_rule,
    composed_h_equality_step,
    base_h_equality_step,
    symmetry_rule,
    reversed_base_step,
    right_composition_rule,
    right_composition_step,
    transitivity_rule,
    final_step,
  ) = data

  expected = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=Composition(
        left=a,
        right=suspended_b,
      ),
    ),
    rhs=Composition(
      left=MapApplication(
        map=EHP_H_MAP,
        expression=a,
      ),
      right=suspended_b,
    ),
    relation_type=RelationType.EQUALITY,
  )

  if final_step.conclusion == expected:
    print("[CONCLUSION]")
    print(
      "  Toda Prop.2.2 right formula "
      "runs end-to-end"
    )
  else:
    print("[CONCLUSION]")
    print(
      "  expected right formula "
      "was not derived"
    )


def main():
  print()
  print("EHP Proof Tracer")
  print(
    "Phase 30 Toda Prop.2.2 "
    "right-formula capability "
    "demonstration"
  )
  print()

  print_target()

  data = (
    derive_phase30_right_formula()
  )

  print_initial_hopf_fact(
    data
  )

  print_hopf_composition_formula(
    data
  )

  print_right_side_conversion(
    data
  )

  print_final_closure(
    data
  )

  print_full_proof_trace(
    data
  )

  print_provenance(
    data
  )

  print_phase30_boundary(
    data
  )

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()



