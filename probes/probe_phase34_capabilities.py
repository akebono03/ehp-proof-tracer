from barratt_hilton_rules import (
  TODA_PROP_3_1_REFERENCE,
  HomotopyGroupMembershipStatement,
  barratt_hilton_first_inference_rule,
  barratt_hilton_second_inference_rule,
)
from expression import (
  Composition,
  HomotopyElement,
  IteratedSuspension,
  Multiple,
  ScalarPower,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  SmashProduct,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  apply_inference_match,
  find_inference_match,
)
from relation_rules import (
  equality_transitivity_inference_rule,
)
from scalar_rules import (
  EvenScalarStatement,
  ScalarSignEvaluationStatement,
  even_scalar_evaluates_minus_one_power_inference_rule,
  scalar_sign_evaluation_applies_to_multiple_inference_rule,
)


def print_separator():
  print("=" * 72)


def scalar_text(
  scalar,
):
  if isinstance(
    scalar,
    int,
  ):
    return str(
      scalar
    )

  if isinstance(
    scalar,
    ScalarSymbol,
  ):
    return scalar.name

  if isinstance(
    scalar,
    ScalarSum,
  ):
    return (
      "("
      f"{scalar_text(scalar.left)}"
      "+"
      f"{scalar_text(scalar.right)}"
      ")"
    )

  if isinstance(
    scalar,
    ScalarProduct,
  ):
    return (
      "("
      f"{scalar_text(scalar.left)}"
      f"{scalar_text(scalar.right)}"
      ")"
    )

  if isinstance(
    scalar,
    ScalarPower,
  ):
    return (
      "("
      f"{scalar_text(scalar.base)}"
      "^"
      f"{scalar_text(scalar.exponent)}"
      ")"
    )

  return str(
    scalar
  )


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
      "("
      f"{expression_text(expression.left)}"
      "∧"
      f"{expression_text(expression.right)}"
      ")"
    )

  if isinstance(
    expression,
    IteratedSuspension,
  ):
    return (
      "E^"
      f"{scalar_text(expression.exponent)}"
      "("
      f"{expression_text(expression.expression)}"
      ")"
    )

  if isinstance(
    expression,
    Composition,
  ):
    return (
      "("
      f"{expression_text(expression.left)}"
      "∘"
      f"{expression_text(expression.right)}"
      ")"
    )

  if isinstance(
    expression,
    Multiple,
  ):
    return (
      f"{scalar_text(expression.coefficient)}"
      "("
      f"{expression_text(expression.expression)}"
      ")"
    )

  return str(
    expression
  )


def statement_text(
  statement,
):
  if isinstance(
    statement,
    HomotopyGroupMembershipStatement,
  ):
    return (
      f"{expression_text(statement.element)}"
      " ∈ "
      "π_"
      f"{scalar_text(statement.group_dimension)}"
      "("
      "S^"
      f"{scalar_text(statement.sphere_dimension)}"
      ")"
    )

  if isinstance(
    statement,
    EvenScalarStatement,
  ):
    return (
      f"{scalar_text(statement.scalar)}"
      " is even"
    )

  if isinstance(
    statement,
    ScalarSignEvaluationStatement,
  ):
    return (
      f"{scalar_text(statement.expression)}"
      "="
      f"{statement.value}"
    )

  if isinstance(
    statement,
    Relation,
  ):
    return (
      f"{expression_text(statement.lhs)}"
      "="
      f"{expression_text(statement.rhs)}"
    )

  return str(
    statement
  )


def build_phase34_first_chain():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  p_plus_k = ScalarSum(
    left=p,
    right=k,
  )

  q_plus_h = ScalarSum(
    left=q,
    right=h,
  )

  exponent = ScalarProduct(
    left=p_plus_k,
    right=h,
  )

  sign = ScalarPower(
    base=-1,
    exponent=exponent,
  )

  composition = Composition(
    left=IteratedSuspension(
      expression=a,
      exponent=q,
    ),
    right=IteratedSuspension(
      expression=b,
      exponent=p_plus_k,
    ),
  )

  a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=p_plus_k,
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=q_plus_h,
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  theorem_rule = (
    barratt_hilton_first_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  theorem_match = find_inference_match(
    theorem_rule,
    (
      a_membership_step,
      b_membership_step,
    ),
  )

  if theorem_match is None:
    raise RuntimeError(
      "Phase 34 Barratt-Hilton "
      "first theorem rule did not match"
    )

  theorem_step = apply_inference_match(
    theorem_match
  )

  parity_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=exponent,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  sign_rule = (
    even_scalar_evaluates_minus_one_power_inference_rule()
  )

  sign_match = find_inference_match(
    sign_rule,
    (
      parity_step,
    ),
  )

  if sign_match is None:
    raise RuntimeError(
      "Phase 34 symbolic sign "
      "evaluation did not match"
    )

  sign_step = apply_inference_match(
    sign_match
  )

  reduction_rule = (
    scalar_sign_evaluation_applies_to_multiple_inference_rule(
      sign=sign,
      expression=composition,
    )
  )

  reduction_match = find_inference_match(
    reduction_rule,
    (
      sign_step,
    ),
  )

  if reduction_match is None:
    raise RuntimeError(
      "Phase 34 sign-to-Multiple "
      "reduction did not match"
    )

  reduction_step = apply_inference_match(
    reduction_match
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  transitivity_match = find_inference_match(
    transitivity_rule,
    (
      theorem_step,
      reduction_step,
    ),
  )

  if transitivity_match is None:
    raise RuntimeError(
      "Phase 34 equality "
      "transitivity did not match"
    )

  final_step = apply_inference_match(
    transitivity_match
  )

  return (
    a,
    b,
    p,
    q,
    k,
    h,
    exponent,
    sign,
    composition,
    a_membership_step,
    b_membership_step,
    theorem_step,
    parity_step,
    sign_step,
    reduction_step,
    final_step,
  )


def build_phase34_second_theorem_step():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=ScalarSum(
          left=p,
          right=k,
        ),
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=h,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_second_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  match = find_inference_match(
    rule,
    (
      a_membership_step,
      b_membership_step,
    ),
  )

  if match is None:
    raise RuntimeError(
      "Phase 34 Barratt-Hilton "
      "second theorem rule did not match"
    )

  return apply_inference_match(
    match
  )


def print_phase34_theorem_chain():
  (
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    a_membership_step,
    b_membership_step,
    theorem_step,
    parity_step,
    sign_step,
    reduction_step,
    final_step,
  ) = build_phase34_first_chain()

  print_separator()
  print(
    "Toda Prop.3.1 "
    "Barratt-Hilton representative proof"
  )
  print_separator()
  print()

  print("[1] Typing premise")
  print(
    " ",
    statement_text(
      a_membership_step.conclusion
    ),
  )
  print(
    "  rule:",
    a_membership_step.rule.value,
  )
  print()

  print("[2] Typing premise")
  print(
    " ",
    statement_text(
      b_membership_step.conclusion
    ),
  )
  print(
    "  rule:",
    b_membership_step.rule.value,
  )
  print()

  print("[3] Apply Toda Prop.3.1")
  print(
    " ",
    statement_text(
      theorem_step.conclusion
    ),
  )
  print(
    "  inference:",
    theorem_step.inference_rule.name,
  )
  print(
    "  source:",
    theorem_step.conclusion.source.label,
  )
  print(
    "  locator:",
    theorem_step.conclusion.source.locator,
  )
  print(
    "  premises:"
  )
  for premise in theorem_step.premises:
    print(
      "   -",
      statement_text(
        premise.conclusion
      ),
    )
  print()

  print("[4] Explicit parity fact")
  print(
    " ",
    statement_text(
      parity_step.conclusion
    ),
  )
  print(
    "  rule:",
    parity_step.rule.value,
  )
  print()

  print("[5] Evaluate symbolic sign")
  print(
    " ",
    statement_text(
      sign_step.conclusion
    ),
  )
  print(
    "  inference:",
    sign_step.inference_rule.name,
  )
  print(
    "  premise:",
    statement_text(
      sign_step.premises[0].conclusion
    ),
  )
  print()

  print("[6] Reduce signed Multiple")
  print(
    " ",
    statement_text(
      reduction_step.conclusion
    ),
  )
  print(
    "  inference:",
    reduction_step.inference_rule.name,
  )
  print(
    "  premise:",
    statement_text(
      reduction_step.premises[0].conclusion
    ),
  )
  print()

  print("[7] Equality transitivity")
  print(
    " ",
    statement_text(
      final_step.conclusion
    ),
  )
  print(
    "  inference:",
    final_step.inference_rule.name,
  )
  print(
    "  premises:"
  )
  for premise in final_step.premises:
    print(
      "   -",
      statement_text(
        premise.conclusion
      ),
    )
  print()

  print("[RESULT]")
  print(
    " ",
    statement_text(
      final_step.conclusion
    ),
  )


def print_phase34_second_formula():
  second_step = (
    build_phase34_second_theorem_step()
  )

  print()
  print_separator()
  print(
    "Toda Prop.3.1 "
    "second Barratt-Hilton formula"
  )
  print_separator()
  print()

  print(
    " ",
    statement_text(
      second_step.conclusion
    ),
  )
  print()

  print(
    "  inference:",
    second_step.inference_rule.name,
  )
  print(
    "  source:",
    second_step.conclusion.source.label,
  )
  print(
    "  locator:",
    second_step.conclusion.source.locator,
  )


def print_phase34_provenance():
  (
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    a_membership_step,
    b_membership_step,
    theorem_step,
    parity_step,
    sign_step,
    reduction_step,
    final_step,
  ) = build_phase34_first_chain()

  print()
  print_separator()
  print("Phase 34 provenance")
  print_separator()
  print()

  print("Final step:")
  print(
    " ",
    statement_text(
      final_step.conclusion
    ),
  )
  print()

  print("Proof dependency:")
  print(
    "  final equality"
  )
  print(
    "  |-",
    final_step.inference_rule.name,
  )
  print(
    "  |  |- theorem branch"
  )
  print(
    "  |  |  |-",
    theorem_step.inference_rule.name,
  )
  print(
    "  |  |  |- source:",
    theorem_step.conclusion.source.label,
  )
  print(
    "  |  |  |-",
    statement_text(
      a_membership_step.conclusion
    ),
  )
  print(
    "  |  |  `-",
    statement_text(
      b_membership_step.conclusion
    ),
  )
  print(
    "  |"
  )
  print(
    "  `- sign branch"
  )
  print(
    "     |-",
    reduction_step.inference_rule.name,
  )
  print(
    "     |-",
    sign_step.inference_rule.name,
  )
  print(
    "     `-",
    statement_text(
      parity_step.conclusion
    ),
  )


def print_phase34_boundary():
  (
    _,
    _,
    _,
    _,
    _,
    _,
    exponent,
    sign,
    composition,
    _,
    _,
    theorem_step,
    _,
    _,
    _,
    final_step,
  ) = build_phase34_first_chain()

  print()
  print_separator()
  print("Phase 34 scope boundary")
  print_separator()
  print()

  print("Now available:")
  print(
    "  symbolic homotopy-group membership"
  )
  print(
    "  Toda Prop.3.1 first theorem rule"
  )
  print(
    "  Toda Prop.3.1 second theorem rule"
  )
  print(
    "  literature-backed provenance"
  )
  print(
    "  theorem RHS -> existing sign reduction"
  )
  print(
    "  theorem equality -> reduced equality"
  )
  print()

  print("Proof confirmation:")
  print(
    "  theorem result is ProofStep:",
    isinstance(
      theorem_step,
      ProofStep,
    ),
  )
  print(
    "  final result is ProofStep:",
    isinstance(
      final_step,
      ProofStep,
    ),
  )
  print(
    "  theorem source is Toda Prop.3.1:",
    (
      theorem_step.conclusion.source
      == TODA_PROP_3_1_REFERENCE
    ),
  )
  print(
    "  symbolic sign preserved before parity =",
    theorem_step.conclusion.rhs.coefficient
    == sign,
  )
  print(
    "  sign exponent =",
    scalar_text(
      exponent
    ),
  )
  print(
    "  symbolic left suspension source =",
    composition.left.source,
  )
  print(
    "  symbolic left suspension target =",
    composition.left.target,
  )
  print(
    "  symbolic right suspension source =",
    composition.right.source,
  )
  print(
    "  symbolic right suspension target =",
    composition.right.target,
  )
  print()

  print("Still outside Phase 34:")
  print(
    "  automatic compound parity inference"
  )
  print(
    "  general symbolic scalar algebra"
  )
  print(
    "  general SmashProduct normalization"
  )
  print(
    "  symbolic suspension typing solver"
  )
  print(
    "  Toda (2.1) composition formulas"
  )
  print(
    "  actual H((2ι₂)η₂) calculation"
  )
  print(
    "  H((2ι₂)η₂)=H(4η₂)"
  )
  print(
    "  (2ι₂)η₂=4η₂"
  )


def main():
  print()
  print("EHP Proof Tracer")
  print("Phase 34 capability demonstration")
  print()

  print_phase34_theorem_chain()
  print_phase34_second_formula()
  print_phase34_provenance()
  print_phase34_boundary()

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()



