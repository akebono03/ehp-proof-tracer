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
  toda_prop22_left_inference_rule,
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

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  rule = toda_prop22_left_inference_rule(
    alpha=a,
    gamma=c,
  )

  match = find_inference_match(
    rule,
    (),
  )

  if match is None:
    raise RuntimeError(
      "Toda Prop.2.2 left formula "
      "did not match"
    )

  theorem_step = apply_inference_match(
    match
  )

  return (
    a,
    c,
    theorem_step,
  )


def print_phase32_derivation():
  (
    a,
    c,
    theorem_step,
  ) = build_phase32_derivation()

  print_separator()
  print("Toda Prop.2.2 left formula")
  print_separator()
  print()

  print("Theorem:")
  print(
    "  H((Ec)∘a)=E(c∧c)∘H(a)"
  )
  print()

  print("Parameters:")
  print(
    "  a =",
    expression_text(a),
  )
  print(
    "  c =",
    expression_text(c),
  )
  print()

  print("[1] Apply Toda Prop.2.2")
  print(
    "  inference:",
    theorem_step.inference_rule.name,
  )
  print(
    "  premises: none"
  )
  print()

  print("[CONCLUSION]")
  print(
    " ",
    statement_text(
      theorem_step.conclusion
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
    theorem_step.conclusion.lhs
    == expected_lhs,
  )
  print(
    "  rhs correct =",
    theorem_step.conclusion.rhs
    == expected_rhs,
  )
  print(
    "  actual H map preserved =",
    theorem_step.conclusion.lhs.map
    is HOPF_MAP,
  )


def print_phase32_provenance():
  (
    _,
    _,
    theorem_step,
  ) = build_phase32_derivation()

  print()
  print_separator()
  print("Phase 32 theorem provenance")
  print_separator()
  print()

  print("Toda Prop.2.2:")
  print(
    " ",
    statement_text(
      theorem_step.conclusion
    ),
  )
  print()

  print("Proof object:")
  print(
    "  rule =",
    theorem_step.rule.value,
  )
  print(
    "  inference =",
    theorem_step.inference_rule.name,
  )
  print(
    "  premises =",
    theorem_step.premises,
  )
  print()

  print("Important:")
  print(
    "  H(a)=β is not required "
    "to state or apply Prop.2.2."
  )
  print(
    "  β-based reasoning is a "
    "separate specialization path."
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



