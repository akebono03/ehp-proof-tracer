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
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from scalar_rules import (
  EvenScalarStatement,
  ScalarSignEvaluationStatement,
  even_scalar_evaluates_minus_one_power_inference_rule,
  scalar_sign_evaluation_applies_to_multiple_inference_rule,
)


def print_separator():
  print("=" * 60)


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
    ScalarSignEvaluationStatement,
  ):
    return (
      f"{scalar_text(statement.expression)}"
      "="
      f"{statement.value}"
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


def build_phase33_formulas():
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

  first_exponent = ScalarProduct(
    left=p_plus_k,
    right=h,
  )

  first_sign = ScalarPower(
    base=-1,
    exponent=first_exponent,
  )

  first_composition = Composition(
    left=IteratedSuspension(
      expression=a,
      exponent=q,
    ),
    right=IteratedSuspension(
      expression=b,
      exponent=p_plus_k,
    ),
  )

  first_formula = Relation(
    lhs=SmashProduct(
      left=a,
      right=b,
    ),
    rhs=Multiple(
      coefficient=first_sign,
      expression=first_composition,
    ),
    relation_type=RelationType.EQUALITY,
  )

  second_exponent = ScalarProduct(
    left=p,
    right=h,
  )

  second_sign = ScalarPower(
    base=-1,
    exponent=second_exponent,
  )

  second_composition = Composition(
    left=IteratedSuspension(
      expression=b,
      exponent=p,
    ),
    right=IteratedSuspension(
      expression=a,
      exponent=q_plus_h,
    ),
  )

  second_formula = Relation(
    lhs=SmashProduct(
      left=a,
      right=b,
    ),
    rhs=Multiple(
      coefficient=second_sign,
      expression=second_composition,
    ),
    relation_type=RelationType.EQUALITY,
  )

  return (
    a,
    b,
    p,
    q,
    k,
    h,
    first_exponent,
    first_sign,
    first_composition,
    first_formula,
    second_exponent,
    second_sign,
    second_composition,
    second_formula,
  )


def build_phase33_sign_reduction():
  (
    _,
    _,
    _,
    _,
    _,
    _,
    first_exponent,
    first_sign,
    first_composition,
    _,
    _,
    _,
    _,
    _,
  ) = build_phase33_formulas()

  parity_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=first_exponent,
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
      "Phase 33 symbolic sign "
      "evaluation did not match"
    )

  sign_step = apply_inference_match(
    sign_match
  )

  multiple_rule = (
    scalar_sign_evaluation_applies_to_multiple_inference_rule(
      sign=first_sign,
      expression=first_composition,
    )
  )

  multiple_match = find_inference_match(
    multiple_rule,
    (
      sign_step,
    ),
  )

  if multiple_match is None:
    raise RuntimeError(
      "Phase 33 symbolic sign "
      "Multiple bridge did not match"
    )

  multiple_step = apply_inference_match(
    multiple_match
  )

  return (
    parity_step,
    sign_step,
    multiple_step,
  )


def print_phase33_formula_representation():
  (
    a,
    b,
    p,
    q,
    k,
    h,
    first_exponent,
    first_sign,
    first_composition,
    first_formula,
    second_exponent,
    second_sign,
    second_composition,
    second_formula,
  ) = build_phase33_formulas()

  print_separator()
  print(
    "Barratt-Hilton minimum "
    "structural representation"
  )
  print_separator()
  print()

  print("Parameters:")
  print(
    "  a =",
    expression_text(a),
  )
  print(
    "  b =",
    expression_text(b),
  )
  print(
    "  p =",
    scalar_text(p),
  )
  print(
    "  q =",
    scalar_text(q),
  )
  print(
    "  k =",
    scalar_text(k),
  )
  print(
    "  h =",
    scalar_text(h),
  )
  print()

  print("Formula 1:")
  print(
    " ",
    statement_text(
      first_formula
    ),
  )
  print()

  print("Structural confirmation:")
  print(
    "  smash product preserved =",
    first_formula.lhs
    == SmashProduct(
      left=a,
      right=b,
    ),
  )
  print(
    "  p+k preserved =",
    first_composition.right.exponent
    == ScalarSum(
      left=p,
      right=k,
    ),
  )
  print(
    "  (p+k)h preserved =",
    first_exponent
    == ScalarProduct(
      left=ScalarSum(
        left=p,
        right=k,
      ),
      right=h,
    ),
  )
  print(
    "  symbolic sign preserved =",
    first_sign
    == ScalarPower(
      base=-1,
      exponent=first_exponent,
    ),
  )
  print(
    "  E^q a preserved =",
    first_composition.left
    == IteratedSuspension(
      expression=a,
      exponent=q,
    ),
  )
  print(
    "  E^(p+k)b preserved =",
    first_composition.right
    == IteratedSuspension(
      expression=b,
      exponent=ScalarSum(
        left=p,
        right=k,
      ),
    ),
  )
  print()

  print("Formula 2:")
  print(
    " ",
    statement_text(
      second_formula
    ),
  )
  print()

  print("Structural confirmation:")
  print(
    "  ph preserved =",
    second_exponent
    == ScalarProduct(
      left=p,
      right=h,
    ),
  )
  print(
    "  symbolic sign preserved =",
    second_sign
    == ScalarPower(
      base=-1,
      exponent=second_exponent,
    ),
  )
  print(
    "  E^p b preserved =",
    second_composition.left
    == IteratedSuspension(
      expression=b,
      exponent=p,
    ),
  )
  print(
    "  E^(q+h)a preserved =",
    second_composition.right
    == IteratedSuspension(
      expression=a,
      exponent=ScalarSum(
        left=q,
        right=h,
      ),
    ),
  )


def print_phase33_sign_reduction():
  (
    parity_step,
    sign_step,
    multiple_step,
  ) = build_phase33_sign_reduction()

  print()
  print_separator()
  print("Phase 33 symbolic sign reduction")
  print_separator()
  print()

  print("[1] Explicit parity fact")
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

  print("[2] Evaluate symbolic sign")
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
    "  premises:",
    statement_text(
      sign_step.premises[0].conclusion
    ),
  )
  print()

  print("[3] Apply evaluated sign to Multiple")
  print(
    " ",
    statement_text(
      multiple_step.conclusion
    ),
  )
  print(
    "  inference:",
    multiple_step.inference_rule.name,
  )
  print(
    "  premises:",
    statement_text(
      multiple_step.premises[0].conclusion
    ),
  )
  print()

  print("[RESULT]")
  print(
    " ",
    statement_text(
      multiple_step.conclusion
    ),
  )


def print_phase33_boundary():
  (
    _,
    _,
    _,
    _,
    _,
    _,
    first_exponent,
    first_sign,
    first_composition,
    first_formula,
    _,
    _,
    _,
    _,
  ) = build_phase33_formulas()

  print()
  print_separator()
  print("Phase 33 scope boundary")
  print_separator()
  print()

  print("Now available:")
  print(
    "  Barratt-Hilton formula syntax"
  )
  print(
    "  symbolic scalar sums/products/powers"
  )
  print(
    "  symbolic iterated suspension exponents"
  )
  print(
    "  explicit parity fact -> sign evaluation"
  )
  print(
    "  evaluated sign -> Multiple reduction"
  )
  print()

  print("Representation boundary:")
  print(
    "  formula is Relation:",
    isinstance(
      first_formula,
      Relation,
    ),
  )
  print(
    "  formula is ProofStep:",
    isinstance(
      first_formula,
      ProofStep,
    ),
  )
  print(
    "  symbolic exponent source =",
    first_composition.right.source,
  )
  print(
    "  symbolic exponent target =",
    first_composition.right.target,
  )
  print(
    "  symbolic sign remains structural =",
    first_sign
    == ScalarPower(
      base=-1,
      exponent=first_exponent,
    ),
  )
  print()

  print("Still outside Phase 33:")
  print(
    "  automatic compound parity inference"
  )
  print(
    "  general symbolic scalar algebra"
  )
  print(
    "  SmashProduct algebra / normalization"
  )
  print(
    "  SmashProduct typing"
  )
  print(
    "  Toda (2.1) composition formulas"
  )
  print(
    "  Barratt-Hilton theorem inference"
  )
  print(
    "  actual H((2ι₂)η₂) calculation"
  )


def main():
  print()
  print("EHP Proof Tracer")
  print("Phase 33 capability demonstration")
  print()

  print_phase33_formula_representation()
  print_phase33_sign_reduction()
  print_phase33_boundary()

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()





