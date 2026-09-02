from expression import (
  Composition,
  HomotopyElement,
  MapApplication,
  SmashProduct,
  Suspension,
)
from hopf_rules import (
  HopfInvariantStatement,
  hopf_invariant_proof_step,
  hopf_invariant_statement_to_ehp_h_equality_inference_rule,
  hopf_left_composition_formula_inference_rule,
  hopf_left_composition_law_inference_rule,
)
from map_facts import (
  HOPF_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  apply_inference_match,
  find_inference_match,
)
from relation_rules import (
  equality_preserved_under_left_composition_inference_rule,
  equality_symmetry_inference_rule,
  equality_transitivity_inference_rule,
)


def print_separator():
  print("=" * 60)


def expression_text(
  expression,
):
  if isinstance(
    expression,
    HomotopyElement,
  ):
    return expression.name

  if isinstance(
    expression,
    SmashProduct,
  ):
    return (
      f"({expression_text(expression.left)}"
      f"∧"
      f"{expression_text(expression.right)})"
    )

  if isinstance(
    expression,
    Suspension,
  ):
    return (
      f"E({expression_text(expression.expression)})"
    )

  if isinstance(
    expression,
    Composition,
  ):
    return (
      f"{expression_text(expression.left)}"
      f"∘"
      f"{expression_text(expression.right)}"
    )

  if isinstance(
    expression,
    MapApplication,
  ):
    return (
      f"{expression.map.name}"
      f"({expression_text(expression.expression)})"
    )

  return str(
    expression
  )


def statement_text(
  statement,
):
  if isinstance(
    statement,
    HopfInvariantStatement,
  ):
    return (
      f"H({expression_text(statement.expression)})"
      f"="
      f"{expression_text(statement.value)}"
    )

  if isinstance(
    statement,
    Relation,
  ):
    return (
      f"{expression_text(statement.lhs)}"
      f"="
      f"{expression_text(statement.rhs)}"
    )

  return str(
    statement
  )


def print_step(
  number,
  step,
):
  print(
    f"[{number}]",
    statement_text(
      step.conclusion
    ),
  )

  print(
    "  rule:",
    step.rule.value,
  )

  if step.inference_rule is not None:
    print(
      "  inference:",
      step.inference_rule.name,
    )

  if step.premises:
    print(
      "  premises:",
      ", ".join(
        statement_text(
          premise.conclusion
        )
        for premise in step.premises
      ),
    )

  print()


def build_phase32_derivation():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  hopf_step = hopf_invariant_proof_step(
    HopfInvariantStatement(
      expression=a,
      value=beta,
    )
  )

  c_step = ProofStep(
    conclusion=c,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  law_rule = (
    hopf_left_composition_law_inference_rule()
  )

  law_match = find_inference_match(
    law_rule,
    (
      hopf_step,
      c_step,
    ),
  )

  if law_match is None:
    raise RuntimeError(
      "left composition law did not match"
    )

  law_step = apply_inference_match(
    law_match
  )

  formula_rule = (
    hopf_left_composition_formula_inference_rule()
  )

  formula_match = find_inference_match(
    formula_rule,
    law_step,
  )

  if formula_match is None:
    raise RuntimeError(
      "left composition formula did not match"
    )

  formula_step = apply_inference_match(
    formula_match
  )

  bridge_rule = (
    hopf_invariant_statement_to_ehp_h_equality_inference_rule()
  )

  formula_bridge_match = find_inference_match(
    bridge_rule,
    formula_step,
  )

  if formula_bridge_match is None:
    raise RuntimeError(
      "formula actual-H bridge did not match"
    )

  formula_actual_h_step = apply_inference_match(
    formula_bridge_match
  )

  base_bridge_match = find_inference_match(
    bridge_rule,
    hopf_step,
  )

  if base_bridge_match is None:
    raise RuntimeError(
      "base actual-H bridge did not match"
    )

  base_actual_h_step = apply_inference_match(
    base_bridge_match
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  symmetry_match = find_inference_match(
    symmetry_rule,
    base_actual_h_step,
  )

  if symmetry_match is None:
    raise RuntimeError(
      "equality symmetry did not match"
    )

  reversed_step = apply_inference_match(
    symmetry_match
  )

  suspended_smash = Suspension(
    expression=SmashProduct(
      left=c,
      right=c,
    ),
  )

  left_composition_rule = (
    equality_preserved_under_left_composition_inference_rule(
      suspended_smash,
    )
  )

  left_composition_match = find_inference_match(
    left_composition_rule,
    reversed_step,
  )

  if left_composition_match is None:
    raise RuntimeError(
      "left-composition equality did not match"
    )

  composed_step = apply_inference_match(
    left_composition_match
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  transitivity_match = find_inference_match(
    transitivity_rule,
    (
      formula_actual_h_step,
      composed_step,
    ),
  )

  if transitivity_match is None:
    raise RuntimeError(
      "final equality transitivity did not match"
    )

  final_step = apply_inference_match(
    transitivity_match
  )

  return (
    a,
    beta,
    c,
    hopf_step,
    c_step,
    law_step,
    formula_step,
    formula_actual_h_step,
    base_actual_h_step,
    reversed_step,
    composed_step,
    final_step,
  )


def print_phase32_derivation():
  (
    a,
    beta,
    c,
    hopf_step,
    c_step,
    law_step,
    formula_step,
    formula_actual_h_step,
    base_actual_h_step,
    reversed_step,
    composed_step,
    final_step,
  ) = build_phase32_derivation()

  print_separator()
  print("Toda Prop.2.2 left formula")
  print_separator()
  print()

  print("Goal:")
  print(
    "  H((Ec)∘a)=E(c∧c)∘H(a)"
  )
  print()

  print("Inputs:")
  print(
    "  H(a)=β"
  )
  print(
    "  c"
  )
  print()

  print_separator()
  print("Left theorem branch")
  print_separator()
  print()

  print_step(
    1,
    hopf_step,
  )

  print_step(
    2,
    c_step,
  )

  print("[3] HopfLeftCompositionLawStatement")
  print(
    "  alpha:",
    expression_text(
      law_step.conclusion.alpha
    ),
  )
  print(
    "  beta:",
    expression_text(
      law_step.conclusion.beta
    ),
  )
  print(
    "  gamma:",
    expression_text(
      law_step.conclusion.gamma
    ),
  )
  print(
    "  inference:",
    law_step.inference_rule.name,
  )
  print(
    "  premises:",
    "H(a)=β, c",
  )
  print()

  print_step(
    4,
    formula_step,
  )

  print_step(
    5,
    formula_actual_h_step,
  )

  print_separator()
  print("Actual-H replacement branch")
  print_separator()
  print()

  print_step(
    6,
    base_actual_h_step,
  )

  print_step(
    7,
    reversed_step,
  )

  print_step(
    8,
    composed_step,
  )

  print_separator()
  print("Equality transitivity closure")
  print_separator()
  print()

  print_step(
    9,
    final_step,
  )

  print("[CONCLUSION]")
  print(
    " ",
    statement_text(
      final_step.conclusion
    ),
  )
  print()

  expected_lhs = MapApplication(
    map=HOPF_MAP,
    expression=Composition(
      left=Suspension(
        expression=c,
      ),
      right=a,
    ),
  )

  expected_rhs = Composition(
    left=Suspension(
      expression=SmashProduct(
        left=c,
        right=c,
      ),
    ),
    right=MapApplication(
      map=HOPF_MAP,
      expression=a,
    ),
  )

  print("Structural confirmation:")
  print(
    "  lhs correct =",
    final_step.conclusion.lhs
    == expected_lhs,
  )
  print(
    "  rhs correct =",
    final_step.conclusion.rhs
    == expected_rhs,
  )
  print(
    "  actual H map preserved =",
    final_step.conclusion.lhs.map
    is HOPF_MAP,
  )
  print()

  print("Base symbols:")
  print(
    "  a =",
    expression_text(a),
  )
  print(
    "  β =",
    expression_text(beta),
  )
  print(
    "  c =",
    expression_text(c),
  )


def print_phase32_provenance():
  (
    _,
    _,
    _,
    hopf_step,
    c_step,
    law_step,
    formula_step,
    formula_actual_h_step,
    base_actual_h_step,
    reversed_step,
    composed_step,
    final_step,
  ) = build_phase32_derivation()

  print()
  print_separator()
  print("Phase 32 provenance")
  print_separator()
  print()

  print("Final:")
  print(
    " ",
    statement_text(
      final_step.conclusion
    ),
  )
  print()

  print("Left branch:")
  print(
    "  final transitivity premise"
  )
  print(
    "  ↓"
  )
  print(
    " ",
    statement_text(
      formula_actual_h_step.conclusion
    ),
  )
  print(
    "  ↓ actual-H bridge"
  )
  print(
    " ",
    statement_text(
      formula_step.conclusion
    ),
  )
  print(
    "  ↓ left composition formula"
  )
  print(
    "  HopfLeftCompositionLawStatement"
  )
  print(
    "  ↓ left composition law"
  )
  print(
    " ",
    statement_text(
      hopf_step.conclusion
    ),
  )
  print(
    "  +",
  )
  print(
    " ",
    statement_text(
      c_step.conclusion
    ),
  )
  print()

  print("Right branch:")
  print(
    "  final transitivity premise"
  )
  print(
    "  ↓"
  )
  print(
    " ",
    statement_text(
      composed_step.conclusion
    ),
  )
  print(
    "  ↓ staged left composition"
  )
  print(
    " ",
    statement_text(
      reversed_step.conclusion
    ),
  )
  print(
    "  ↓ equality symmetry"
  )
  print(
    " ",
    statement_text(
      base_actual_h_step.conclusion
    ),
  )
  print(
    "  ↓ actual-H bridge"
  )
  print(
    " ",
    statement_text(
      hopf_step.conclusion
    ),
  )
  print()

  print("Proof object checks:")
  print(
    "  final premises preserved =",
    final_step.premises
    == (
      formula_actual_h_step,
      composed_step,
    ),
  )
  print(
    "  formula provenance preserved =",
    formula_actual_h_step.premises
    == (
      formula_step,
    ),
  )
  print(
    "  law provenance preserved =",
    law_step.premises
    == (
      hopf_step,
      c_step,
    ),
  )
  print(
    "  right branch provenance preserved =",
    composed_step.premises
    == (
      reversed_step,
    ),
  )


def print_phase32_boundary():
  c = HomotopyElement(
    name="c",
    dimension=3,
    source=6,
    target=3,
  )

  smash = SmashProduct(
    left=c,
    right=c,
  )

  suspended_smash = Suspension(
    expression=smash,
  )

  print()
  print_separator()
  print("Phase 32 completion boundary")
  print_separator()
  print()

  print("Now available:")
  print(
    "  H((Ec)∘a)=E(c∧c)∘H(a)"
  )
  print(
    "  as an actual proof-level H equality"
  )
  print()

  print("Typing boundary:")
  print(
    "  SmashProduct has source:",
    hasattr(
      smash,
      "source",
    ),
  )
  print(
    "  SmashProduct has target:",
    hasattr(
      smash,
      "target",
    ),
  )
  print(
    "  E(c∧c).source =",
    suspended_smash.source,
  )
  print(
    "  E(c∧c).target =",
    suspended_smash.target,
  )
  print()

  print("Scope boundary:")
  print(
    "  left-composition equality is staged"
  )
  print(
    "  no unrestricted fixed-point use"
  )
  print()

  print("Still outside Phase 32:")
  print(
    "  SmashProduct typing"
  )
  print(
    "  SmashProduct algebra / normalization"
  )
  print(
    "  Barratt-Hilton Prop.3.1"
  )
  print(
    "  Toda (2.1) additive composition formulas"
  )
  print(
    "  symbolic (-1)^n algebra"
  )
  print(
    "  actual H((2ι₂)η₂) calculation"
  )


def main():
  print()
  print("EHP Proof Tracer")
  print("Phase 32 capability demonstration")
  print()

  print_phase32_derivation()
  print_phase32_provenance()
  print_phase32_boundary()

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()



