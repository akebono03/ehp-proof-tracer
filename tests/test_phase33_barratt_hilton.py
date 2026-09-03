from expression import (
  Composition,
  HomotopyElement,
  IteratedSuspension,
  Multiple,
  ScalarExpression,
  ScalarPower,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  SmashProduct,
  Sum,
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
  OddScalarStatement,
  ScalarSignEvaluationStatement,
  even_scalar_evaluates_minus_one_power_inference_rule,
  even_scalar_implies_mod_two_congruence_inference_rule,
  odd_scalar_evaluates_minus_one_power_inference_rule,
  odd_scalar_implies_mod_two_congruence_inference_rule,
  scalar_sign_evaluation_applies_to_multiple_inference_rule,
)


def test_phase33_1_single_symbol_iterated_suspensions_are_representable():
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

  assert IteratedSuspension(
    expression=a,
    exponent=q,
  ) == IteratedSuspension(
    expression=a,
    exponent=ScalarSymbol(
      name="q",
    ),
  )

  assert IteratedSuspension(
    expression=b,
    exponent=p,
  ) == IteratedSuspension(
    expression=b,
    exponent=ScalarSymbol(
      name="p",
    ),
  )


def test_phase33_1_existing_expression_nodes_compose_without_new_semantics():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  q = ScalarSymbol(
    name="q",
  )

  left = Composition(
    left=IteratedSuspension(
      expression=a,
      exponent=q,
    ),
    right=b,
  )

  right = Sum(
    left=Multiple(
      coefficient=2,
      expression=a,
    ),
    right=SmashProduct(
      left=a,
      right=b,
    ),
  )

  assert left.left == IteratedSuspension(
    expression=a,
    exponent=q,
  )

  assert left.right == b

  assert right.left == Multiple(
    coefficient=2,
    expression=a,
  )

  assert right.right == SmashProduct(
    left=a,
    right=b,
  )


def test_phase33_2_scalar_symbol_is_scalar_expression():
  p = ScalarSymbol(
    name="p",
  )

  assert isinstance(
    p,
    ScalarExpression,
  )


def test_phase33_2_scalar_sum_preserves_operands_structurally():
  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  scalar_sum = ScalarSum(
    left=p,
    right=k,
  )

  assert scalar_sum.left == p
  assert scalar_sum.right == k

  assert scalar_sum == ScalarSum(
    left=p,
    right=k,
  )


def test_phase33_2_scalar_product_preserves_operands_structurally():
  p = ScalarSymbol(
    name="p",
  )

  h = ScalarSymbol(
    name="h",
  )

  scalar_product = ScalarProduct(
    left=p,
    right=h,
  )

  assert scalar_product.left == p
  assert scalar_product.right == h

  assert scalar_product == ScalarProduct(
    left=p,
    right=h,
  )


def test_phase33_2_scalar_power_preserves_base_and_exponent_structurally():
  n = ScalarSymbol(
    name="n",
  )

  sign = ScalarPower(
    base=-1,
    exponent=n,
  )

  assert sign.base == -1
  assert sign.exponent == n

  assert sign == ScalarPower(
    base=-1,
    exponent=n,
  )


def test_phase33_2_p_plus_k_is_lossless_scalar_structure():
  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  p_plus_k = ScalarSum(
    left=p,
    right=k,
  )

  opaque = ScalarSymbol(
    name="p+k",
  )

  assert p_plus_k == ScalarSum(
    left=ScalarSymbol(
      name="p",
    ),
    right=ScalarSymbol(
      name="k",
    ),
  )

  assert p_plus_k != opaque


def test_phase33_2_p_plus_k_times_h_is_lossless_scalar_structure():
  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  exponent = ScalarProduct(
    left=ScalarSum(
      left=p,
      right=k,
    ),
    right=h,
  )

  assert exponent.left == ScalarSum(
    left=p,
    right=k,
  )

  assert exponent.right == h


def test_phase33_2_barratt_hilton_sign_with_sum_product_exponent_is_representable():
  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  sign = ScalarPower(
    base=-1,
    exponent=ScalarProduct(
      left=ScalarSum(
        left=p,
        right=k,
      ),
      right=h,
    ),
  )

  expected = ScalarPower(
    base=-1,
    exponent=ScalarProduct(
      left=ScalarSum(
        left=ScalarSymbol(
          name="p",
        ),
        right=ScalarSymbol(
          name="k",
        ),
      ),
      right=ScalarSymbol(
        name="h",
      ),
    ),
  )

  assert sign == expected


def test_phase33_2_barratt_hilton_ph_sign_is_representable():
  p = ScalarSymbol(
    name="p",
  )

  h = ScalarSymbol(
    name="h",
  )

  sign = ScalarPower(
    base=-1,
    exponent=ScalarProduct(
      left=p,
      right=h,
    ),
  )

  assert sign == ScalarPower(
    base=-1,
    exponent=ScalarProduct(
      left=p,
      right=h,
    ),
  )


def test_phase33_2_iterated_suspension_accepts_p_plus_k_structure():
  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  exponent = ScalarSum(
    left=p,
    right=k,
  )

  suspension = IteratedSuspension(
    expression=b,
    exponent=exponent,
  )

  assert suspension.expression == b
  assert suspension.exponent == exponent

  assert suspension == IteratedSuspension(
    expression=b,
    exponent=ScalarSum(
      left=p,
      right=k,
    ),
  )


def test_phase33_2_iterated_suspension_accepts_q_plus_h_structure():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  q = ScalarSymbol(
    name="q",
  )

  h = ScalarSymbol(
    name="h",
  )

  exponent = ScalarSum(
    left=q,
    right=h,
  )

  suspension = IteratedSuspension(
    expression=a,
    exponent=exponent,
  )

  assert suspension.expression == a
  assert suspension.exponent == exponent


def test_phase33_2_symbolic_scalar_sum_does_not_gain_concrete_typing():
  b = HomotopyElement(
    name="b",
    dimension=1,
    source=8,
    target=4,
  )

  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  suspension = IteratedSuspension(
    expression=b,
    exponent=ScalarSum(
      left=p,
      right=k,
    ),
  )

  assert suspension.source is None
  assert suspension.target is None


def test_phase33_2_scalar_sum_is_not_implicitly_commutative():
  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  assert ScalarSum(
    left=p,
    right=k,
  ) != ScalarSum(
    left=k,
    right=p,
  )


def test_phase33_2_scalar_product_is_not_implicitly_commutative():
  p = ScalarSymbol(
    name="p",
  )

  h = ScalarSymbol(
    name="h",
  )

  assert ScalarProduct(
    left=p,
    right=h,
  ) != ScalarProduct(
    left=h,
    right=p,
  )


def test_phase33_2_scalar_product_does_not_distribute_automatically():
  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  factored = ScalarProduct(
    left=ScalarSum(
      left=p,
      right=k,
    ),
    right=h,
  )

  expanded = ScalarSum(
    left=ScalarProduct(
      left=p,
      right=h,
    ),
    right=ScalarProduct(
      left=k,
      right=h,
    ),
  )

  assert factored != expanded


def test_phase33_2_scalar_power_is_not_evaluated_automatically():
  assert ScalarPower(
    base=-1,
    exponent=2,
  ) != 1

  assert ScalarPower(
    base=-1,
    exponent=3,
  ) != -1


def test_phase33_2_symbolic_sign_is_not_yet_connected_to_multiple():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  n = ScalarSymbol(
    name="n",
  )

  sign = ScalarPower(
    base=-1,
    exponent=n,
  )

  current_multiple = Multiple(
    coefficient=ScalarSymbol(
      name="k",
    ),
    expression=a,
  )

  assert sign != current_multiple.coefficient

  assert current_multiple == Multiple(
    coefficient=ScalarSymbol(
      name="k",
    ),
    expression=a,
  )


def test_phase33_3_even_scalar_fact_accepts_compound_scalar_expression():
  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  exponent = ScalarProduct(
    left=ScalarSum(
      left=p,
      right=k,
    ),
    right=h,
  )

  statement = EvenScalarStatement(
    scalar=exponent,
  )

  assert statement.scalar == exponent


def test_phase33_3_odd_scalar_fact_accepts_compound_scalar_expression():
  p = ScalarSymbol(
    name="p",
  )

  h = ScalarSymbol(
    name="h",
  )

  exponent = ScalarProduct(
    left=p,
    right=h,
  )

  statement = OddScalarStatement(
    scalar=exponent,
  )

  assert statement.scalar == exponent


def test_phase33_3_even_exponent_evaluates_symbolic_sign_to_one():
  n = ScalarSymbol(
    name="n",
  )

  even_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    even_scalar_evaluates_minus_one_power_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == (
    ScalarSignEvaluationStatement(
      expression=ScalarPower(
        base=-1,
        exponent=n,
      ),
      value=1,
    )
  )

  assert step.rule == ProofRule.INFERENCE
  assert step.inference_rule == rule
  assert step.premises == (
    even_step,
  )


def test_phase33_3_odd_exponent_evaluates_symbolic_sign_to_minus_one():
  n = ScalarSymbol(
    name="n",
  )

  odd_step = ProofStep(
    conclusion=OddScalarStatement(
      scalar=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    odd_scalar_evaluates_minus_one_power_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      odd_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == (
    ScalarSignEvaluationStatement(
      expression=ScalarPower(
        base=-1,
        exponent=n,
      ),
      value=-1,
    )
  )

  assert step.rule == ProofRule.INFERENCE
  assert step.inference_rule == rule
  assert step.premises == (
    odd_step,
  )


def test_phase33_3_even_compound_exponent_evaluates_barratt_hilton_sign():
  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  exponent = ScalarProduct(
    left=ScalarSum(
      left=p,
      right=k,
    ),
    right=h,
  )

  even_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=exponent,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    even_scalar_evaluates_minus_one_power_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == (
    ScalarSignEvaluationStatement(
      expression=ScalarPower(
        base=-1,
        exponent=ScalarProduct(
          left=ScalarSum(
            left=p,
            right=k,
          ),
          right=h,
        ),
      ),
      value=1,
    )
  )


def test_phase33_3_odd_compound_exponent_evaluates_barratt_hilton_sign():
  p = ScalarSymbol(
    name="p",
  )

  h = ScalarSymbol(
    name="h",
  )

  exponent = ScalarProduct(
    left=p,
    right=h,
  )

  odd_step = ProofStep(
    conclusion=OddScalarStatement(
      scalar=exponent,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    odd_scalar_evaluates_minus_one_power_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      odd_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == (
    ScalarSignEvaluationStatement(
      expression=ScalarPower(
        base=-1,
        exponent=ScalarProduct(
          left=p,
          right=h,
        ),
      ),
      value=-1,
    )
  )


def test_phase33_3_even_sign_rule_rejects_odd_fact():
  n = ScalarSymbol(
    name="n",
  )

  odd_step = ProofStep(
    conclusion=OddScalarStatement(
      scalar=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    even_scalar_evaluates_minus_one_power_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      odd_step,
    ),
  )

  assert match is None


def test_phase33_3_odd_sign_rule_rejects_even_fact():
  n = ScalarSymbol(
    name="n",
  )

  even_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    odd_scalar_evaluates_minus_one_power_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
    ),
  )

  assert match is None


def test_phase33_3_compound_parity_does_not_enter_phase16_mod_two_bridge():
  p = ScalarSymbol(
    name="p",
  )

  h = ScalarSymbol(
    name="h",
  )

  exponent = ScalarProduct(
    left=p,
    right=h,
  )

  odd_step = ProofStep(
    conclusion=OddScalarStatement(
      scalar=exponent,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    odd_scalar_implies_mod_two_congruence_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      odd_step,
    ),
  )

  assert match is None


def test_phase33_3_compound_even_parity_does_not_enter_phase16_mod_two_bridge():
  p = ScalarSymbol(
    name="p",
  )

  h = ScalarSymbol(
    name="h",
  )

  exponent = ScalarProduct(
    left=p,
    right=h,
  )

  even_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=exponent,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    even_scalar_implies_mod_two_congruence_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
    ),
  )

  assert match is None


def test_phase33_3_parity_is_not_inferred_from_scalar_structure_alone():
  p = ScalarSymbol(
    name="p",
  )

  h = ScalarSymbol(
    name="h",
  )

  exponent = ScalarProduct(
    left=p,
    right=h,
  )

  sign = ScalarPower(
    base=-1,
    exponent=exponent,
  )

  even_rule = (
    even_scalar_evaluates_minus_one_power_inference_rule()
  )

  odd_rule = (
    odd_scalar_evaluates_minus_one_power_inference_rule()
  )

  assert find_inference_match(
    even_rule,
    (),
  ) is None

  assert find_inference_match(
    odd_rule,
    (),
  ) is None

  assert sign == ScalarPower(
    base=-1,
    exponent=exponent,
  )


def test_phase33_3_sign_evaluation_does_not_connect_to_multiple_yet():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  n = ScalarSymbol(
    name="n",
  )

  evaluation = ScalarSignEvaluationStatement(
    expression=ScalarPower(
      base=-1,
      exponent=n,
    ),
    value=-1,
  )

  existing_multiple = Multiple(
    coefficient=-1,
    expression=a,
  )

  assert evaluation.value == -1

  assert evaluation != existing_multiple


def test_phase33_4_multiple_accepts_symbolic_sign_coefficient():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  n = ScalarSymbol(
    name="n",
  )

  sign = ScalarPower(
    base=-1,
    exponent=n,
  )

  multiple = Multiple(
    coefficient=sign,
    expression=a,
  )

  assert multiple.coefficient == sign
  assert multiple.expression == a


def test_phase33_4_symbolic_sign_multiple_preserves_structure():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  n = ScalarSymbol(
    name="n",
  )

  symbolic_multiple = Multiple(
    coefficient=ScalarPower(
      base=-1,
      exponent=n,
    ),
    expression=a,
  )

  assert symbolic_multiple == Multiple(
    coefficient=ScalarPower(
      base=-1,
      exponent=ScalarSymbol(
        name="n",
      ),
    ),
    expression=a,
  )

  assert symbolic_multiple != Multiple(
    coefficient=-1,
    expression=a,
  )

  assert symbolic_multiple != a


def test_phase33_4_positive_sign_evaluation_reduces_symbolic_multiple_to_expression():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  n = ScalarSymbol(
    name="n",
  )

  sign = ScalarPower(
    base=-1,
    exponent=n,
  )

  evaluation_step = ProofStep(
    conclusion=ScalarSignEvaluationStatement(
      expression=sign,
      value=1,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    scalar_sign_evaluation_applies_to_multiple_inference_rule(
      sign=sign,
      expression=a,
    )
  )

  match = find_inference_match(
    rule,
    (
      evaluation_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == Relation(
    lhs=Multiple(
      coefficient=sign,
      expression=a,
    ),
    rhs=a,
    relation_type=RelationType.EQUALITY,
  )

  assert step.rule == ProofRule.INFERENCE
  assert step.inference_rule == rule
  assert step.premises == (
    evaluation_step,
  )


def test_phase33_4_negative_sign_evaluation_reduces_symbolic_multiple_to_inverse():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  n = ScalarSymbol(
    name="n",
  )

  sign = ScalarPower(
    base=-1,
    exponent=n,
  )

  evaluation_step = ProofStep(
    conclusion=ScalarSignEvaluationStatement(
      expression=sign,
      value=-1,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    scalar_sign_evaluation_applies_to_multiple_inference_rule(
      sign=sign,
      expression=a,
    )
  )

  match = find_inference_match(
    rule,
    (
      evaluation_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == Relation(
    lhs=Multiple(
      coefficient=sign,
      expression=a,
    ),
    rhs=Multiple(
      coefficient=-1,
      expression=a,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert step.rule == ProofRule.INFERENCE
  assert step.inference_rule == rule
  assert step.premises == (
    evaluation_step,
  )


def test_phase33_4_sign_bridge_rejects_different_symbolic_sign():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  n = ScalarSymbol(
    name="n",
  )

  m = ScalarSymbol(
    name="m",
  )

  expected_sign = ScalarPower(
    base=-1,
    exponent=n,
  )

  different_sign = ScalarPower(
    base=-1,
    exponent=m,
  )

  evaluation_step = ProofStep(
    conclusion=ScalarSignEvaluationStatement(
      expression=different_sign,
      value=1,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    scalar_sign_evaluation_applies_to_multiple_inference_rule(
      sign=expected_sign,
      expression=a,
    )
  )

  match = find_inference_match(
    rule,
    (
      evaluation_step,
    ),
  )

  assert match is None


def test_phase33_4_sign_bridge_rejects_non_sign_value():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  n = ScalarSymbol(
    name="n",
  )

  sign = ScalarPower(
    base=-1,
    exponent=n,
  )

  invalid_evaluation_step = ProofStep(
    conclusion=ScalarSignEvaluationStatement(
      expression=sign,
      value=2,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    scalar_sign_evaluation_applies_to_multiple_inference_rule(
      sign=sign,
      expression=a,
    )
  )

  match = find_inference_match(
    rule,
    (
      invalid_evaluation_step,
    ),
  )

  assert match is None


def test_phase33_4_barratt_hilton_symbolic_signed_terms_fit_inside_sum():
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

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  first_sign = ScalarPower(
    base=-1,
    exponent=ScalarProduct(
      left=ScalarSum(
        left=p,
        right=k,
      ),
      right=h,
    ),
  )

  second_sign = ScalarPower(
    base=-1,
    exponent=ScalarProduct(
      left=p,
      right=h,
    ),
  )

  expression = Sum(
    left=Multiple(
      coefficient=first_sign,
      expression=a,
    ),
    right=Multiple(
      coefficient=second_sign,
      expression=b,
    ),
  )

  assert expression.left == Multiple(
    coefficient=first_sign,
    expression=a,
  )

  assert expression.right == Multiple(
    coefficient=second_sign,
    expression=b,
  )


def test_phase33_4_negative_sign_result_matches_existing_inverse_representation():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  n = ScalarSymbol(
    name="n",
  )

  sign = ScalarPower(
    base=-1,
    exponent=n,
  )

  evaluation_step = ProofStep(
    conclusion=ScalarSignEvaluationStatement(
      expression=sign,
      value=-1,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    scalar_sign_evaluation_applies_to_multiple_inference_rule(
      sign=sign,
      expression=a,
    )
  )

  match = find_inference_match(
    rule,
    (
      evaluation_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  additive_inverse = Multiple(
    coefficient=-1,
    expression=a,
  )

  assert step.conclusion.rhs == additive_inverse


def test_phase33_4_negative_sign_result_connects_to_existing_sum_structure():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  negative_a = Multiple(
    coefficient=-1,
    expression=a,
  )

  additive_inverse_sum = Sum(
    left=a,
    right=negative_a,
  )

  assert additive_inverse_sum == Sum(
    left=a,
    right=Multiple(
      coefficient=-1,
      expression=a,
    ),
  )


def test_phase33_4_symbolic_signed_sum_is_not_simplified_automatically():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  n = ScalarSymbol(
    name="n",
  )

  sign = ScalarPower(
    base=-1,
    exponent=n,
  )

  symbolic_sum = Sum(
    left=a,
    right=Multiple(
      coefficient=sign,
      expression=a,
    ),
  )

  additive_inverse_sum = Sum(
    left=a,
    right=Multiple(
      coefficient=-1,
      expression=a,
    ),
  )

  assert symbolic_sum != additive_inverse_sum


def test_phase33_5_e_q_a_is_structurally_representable():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  q = ScalarSymbol(
    name="q",
  )

  suspension = IteratedSuspension(
    expression=a,
    exponent=q,
  )

  assert suspension.expression == a
  assert suspension.exponent == q

  assert suspension == IteratedSuspension(
    expression=a,
    exponent=ScalarSymbol(
      name="q",
    ),
  )


def test_phase33_5_e_p_plus_k_b_is_structurally_representable():
  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  p_plus_k = ScalarSum(
    left=p,
    right=k,
  )

  suspension = IteratedSuspension(
    expression=b,
    exponent=p_plus_k,
  )

  assert suspension.expression == b

  assert suspension.exponent == ScalarSum(
    left=p,
    right=k,
  )

  assert suspension != IteratedSuspension(
    expression=b,
    exponent=ScalarSymbol(
      name="p+k",
    ),
  )


def test_phase33_5_e_p_b_is_structurally_representable():
  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  suspension = IteratedSuspension(
    expression=b,
    exponent=p,
  )

  assert suspension.expression == b
  assert suspension.exponent == p

  assert suspension == IteratedSuspension(
    expression=b,
    exponent=ScalarSymbol(
      name="p",
    ),
  )


def test_phase33_5_e_q_plus_h_a_is_structurally_representable():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  q = ScalarSymbol(
    name="q",
  )

  h = ScalarSymbol(
    name="h",
  )

  q_plus_h = ScalarSum(
    left=q,
    right=h,
  )

  suspension = IteratedSuspension(
    expression=a,
    exponent=q_plus_h,
  )

  assert suspension.expression == a

  assert suspension.exponent == ScalarSum(
    left=q,
    right=h,
  )

  assert suspension != IteratedSuspension(
    expression=a,
    exponent=ScalarSymbol(
      name="q+h",
    ),
  )


def test_phase33_5_first_barratt_hilton_composition_is_structurally_representable():
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

  composition = Composition(
    left=IteratedSuspension(
      expression=a,
      exponent=q,
    ),
    right=IteratedSuspension(
      expression=b,
      exponent=ScalarSum(
        left=p,
        right=k,
      ),
    ),
  )

  assert composition.left == IteratedSuspension(
    expression=a,
    exponent=q,
  )

  assert composition.right == IteratedSuspension(
    expression=b,
    exponent=ScalarSum(
      left=p,
      right=k,
    ),
  )


def test_phase33_5_second_barratt_hilton_composition_is_structurally_representable():
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

  h = ScalarSymbol(
    name="h",
  )

  composition = Composition(
    left=IteratedSuspension(
      expression=b,
      exponent=p,
    ),
    right=IteratedSuspension(
      expression=a,
      exponent=ScalarSum(
        left=q,
        right=h,
      ),
    ),
  )

  assert composition.left == IteratedSuspension(
    expression=b,
    exponent=p,
  )

  assert composition.right == IteratedSuspension(
    expression=a,
    exponent=ScalarSum(
      left=q,
      right=h,
    ),
  )


def test_phase33_5_symbolic_iterated_suspension_preserves_typing_boundary():
  a = HomotopyElement(
    name="a",
    dimension=1,
    source=7,
    target=3,
  )

  q = ScalarSymbol(
    name="q",
  )

  symbolic_suspension = IteratedSuspension(
    expression=a,
    exponent=q,
  )

  compound_suspension = IteratedSuspension(
    expression=a,
    exponent=ScalarSum(
      left=q,
      right=ScalarSymbol(
        name="h",
      ),
    ),
  )

  assert symbolic_suspension.source is None
  assert symbolic_suspension.target is None

  assert compound_suspension.source is None
  assert compound_suspension.target is None


def test_phase33_5_concrete_iterated_suspension_typing_regression_is_preserved():
  a = HomotopyElement(
    name="a",
    dimension=1,
    source=7,
    target=3,
  )

  suspension = IteratedSuspension(
    expression=a,
    exponent=2,
  )

  assert suspension.source == 9
  assert suspension.target == 5


def test_phase33_6_first_barratt_hilton_formula_is_structurally_representable():
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

  sign = ScalarPower(
    base=-1,
    exponent=ScalarProduct(
      left=ScalarSum(
        left=p,
        right=k,
      ),
      right=h,
    ),
  )

  composition = Composition(
    left=IteratedSuspension(
      expression=a,
      exponent=q,
    ),
    right=IteratedSuspension(
      expression=b,
      exponent=ScalarSum(
        left=p,
        right=k,
      ),
    ),
  )

  formula = Relation(
    lhs=SmashProduct(
      left=a,
      right=b,
    ),
    rhs=Multiple(
      coefficient=sign,
      expression=composition,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert formula.lhs == SmashProduct(
    left=a,
    right=b,
  )

  assert formula.rhs == Multiple(
    coefficient=sign,
    expression=composition,
  )

  assert formula.relation_type == (
    RelationType.EQUALITY
  )


def test_phase33_6_second_barratt_hilton_formula_is_structurally_representable():
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

  h = ScalarSymbol(
    name="h",
  )

  sign = ScalarPower(
    base=-1,
    exponent=ScalarProduct(
      left=p,
      right=h,
    ),
  )

  composition = Composition(
    left=IteratedSuspension(
      expression=b,
      exponent=p,
    ),
    right=IteratedSuspension(
      expression=a,
      exponent=ScalarSum(
        left=q,
        right=h,
      ),
    ),
  )

  formula = Relation(
    lhs=SmashProduct(
      left=a,
      right=b,
    ),
    rhs=Multiple(
      coefficient=sign,
      expression=composition,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert formula.lhs == SmashProduct(
    left=a,
    right=b,
  )

  assert formula.rhs == Multiple(
    coefficient=sign,
    expression=composition,
  )

  assert formula.relation_type == (
    RelationType.EQUALITY
  )


def test_phase33_6_first_formula_preserves_full_symbolic_sign_structure():
  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  sign = ScalarPower(
    base=-1,
    exponent=ScalarProduct(
      left=ScalarSum(
        left=p,
        right=k,
      ),
      right=h,
    ),
  )

  assert sign.base == -1

  assert sign.exponent == ScalarProduct(
    left=ScalarSum(
      left=p,
      right=k,
    ),
    right=h,
  )

  assert sign.exponent.left == ScalarSum(
    left=p,
    right=k,
  )

  assert sign.exponent.right == h


def test_phase33_6_second_formula_preserves_full_symbolic_sign_structure():
  p = ScalarSymbol(
    name="p",
  )

  h = ScalarSymbol(
    name="h",
  )

  sign = ScalarPower(
    base=-1,
    exponent=ScalarProduct(
      left=p,
      right=h,
    ),
  )

  assert sign.base == -1

  assert sign.exponent == ScalarProduct(
    left=p,
    right=h,
  )


def test_phase33_6_first_formula_preserves_full_suspension_structure():
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

  composition = Composition(
    left=IteratedSuspension(
      expression=a,
      exponent=q,
    ),
    right=IteratedSuspension(
      expression=b,
      exponent=ScalarSum(
        left=p,
        right=k,
      ),
    ),
  )

  assert composition.left == IteratedSuspension(
    expression=a,
    exponent=q,
  )

  assert composition.right == IteratedSuspension(
    expression=b,
    exponent=ScalarSum(
      left=p,
      right=k,
    ),
  )


def test_phase33_6_second_formula_preserves_full_suspension_structure():
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

  h = ScalarSymbol(
    name="h",
  )

  composition = Composition(
    left=IteratedSuspension(
      expression=b,
      exponent=p,
    ),
    right=IteratedSuspension(
      expression=a,
      exponent=ScalarSum(
        left=q,
        right=h,
      ),
    ),
  )

  assert composition.left == IteratedSuspension(
    expression=b,
    exponent=p,
  )

  assert composition.right == IteratedSuspension(
    expression=a,
    exponent=ScalarSum(
      left=q,
      right=h,
    ),
  )


def test_phase33_6_two_barratt_hilton_formula_shapes_remain_structurally_distinct():
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

  first = Relation(
    lhs=SmashProduct(
      left=a,
      right=b,
    ),
    rhs=Multiple(
      coefficient=ScalarPower(
        base=-1,
        exponent=ScalarProduct(
          left=ScalarSum(
            left=p,
            right=k,
          ),
          right=h,
        ),
      ),
      expression=Composition(
        left=IteratedSuspension(
          expression=a,
          exponent=q,
        ),
        right=IteratedSuspension(
          expression=b,
          exponent=ScalarSum(
            left=p,
            right=k,
          ),
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  second = Relation(
    lhs=SmashProduct(
      left=a,
      right=b,
    ),
    rhs=Multiple(
      coefficient=ScalarPower(
        base=-1,
        exponent=ScalarProduct(
          left=p,
          right=h,
        ),
      ),
      expression=Composition(
        left=IteratedSuspension(
          expression=b,
          exponent=p,
        ),
        right=IteratedSuspension(
          expression=a,
          exponent=ScalarSum(
            left=q,
            right=h,
          ),
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert first != second

  assert first.lhs == second.lhs
  assert first.rhs != second.rhs


def test_phase33_6_opaque_scalar_names_do_not_match_structural_formula():
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

  structural = Relation(
    lhs=SmashProduct(
      left=a,
      right=b,
    ),
    rhs=Multiple(
      coefficient=ScalarPower(
        base=-1,
        exponent=ScalarProduct(
          left=ScalarSum(
            left=p,
            right=k,
          ),
          right=h,
        ),
      ),
      expression=Composition(
        left=IteratedSuspension(
          expression=a,
          exponent=q,
        ),
        right=IteratedSuspension(
          expression=b,
          exponent=ScalarSum(
            left=p,
            right=k,
          ),
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  opaque = Relation(
    lhs=SmashProduct(
      left=a,
      right=b,
    ),
    rhs=Multiple(
      coefficient=ScalarSymbol(
        name="(-1)^((p+k)h)",
      ),
      expression=Composition(
        left=IteratedSuspension(
          expression=a,
          exponent=q,
        ),
        right=IteratedSuspension(
          expression=b,
          exponent=ScalarSymbol(
            name="p+k",
          ),
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert structural != opaque


def test_phase33_6_formula_representation_does_not_add_smash_product_typing():
  a = HomotopyElement(
    name="a",
    dimension=1,
    source=6,
    target=3,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
    source=7,
    target=4,
  )

  smash = SmashProduct(
    left=a,
    right=b,
  )

  assert not hasattr(
    smash,
    "source",
  )

  assert not hasattr(
    smash,
    "target",
  )


def test_phase33_6_formula_is_structural_statement_not_barratt_hilton_inference():
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

  formula = Relation(
    lhs=SmashProduct(
      left=a,
      right=b,
    ),
    rhs=Multiple(
      coefficient=ScalarPower(
        base=-1,
        exponent=ScalarProduct(
          left=ScalarSum(
            left=p,
            right=k,
          ),
          right=h,
        ),
      ),
      expression=Composition(
        left=IteratedSuspension(
          expression=a,
          exponent=q,
        ),
        right=IteratedSuspension(
          expression=b,
          exponent=ScalarSum(
            left=p,
            right=k,
          ),
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert isinstance(
    formula,
    Relation,
  )

  assert formula.relation_type == (
    RelationType.EQUALITY
  )


def test_phase33_7_scalar_sum_is_not_implicitly_commutative():
  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  assert ScalarSum(
    left=p,
    right=k,
  ) != ScalarSum(
    left=k,
    right=p,
  )


def test_phase33_7_scalar_product_is_not_implicitly_commutative():
  p = ScalarSymbol(
    name="p",
  )

  h = ScalarSymbol(
    name="h",
  )

  assert ScalarProduct(
    left=p,
    right=h,
  ) != ScalarProduct(
    left=h,
    right=p,
  )


def test_phase33_7_scalar_product_does_not_distribute_over_sum_automatically():
  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  factored = ScalarProduct(
    left=ScalarSum(
      left=p,
      right=k,
    ),
    right=h,
  )

  expanded = ScalarSum(
    left=ScalarProduct(
      left=p,
      right=h,
    ),
    right=ScalarProduct(
      left=k,
      right=h,
    ),
  )

  assert factored != expanded


def test_phase33_7_scalar_power_is_not_constant_folded_automatically():
  assert ScalarPower(
    base=-1,
    exponent=2,
  ) != 1

  assert ScalarPower(
    base=-1,
    exponent=3,
  ) != -1


def test_phase33_7_scalar_structure_does_not_imply_parity_fact():
  p = ScalarSymbol(
    name="p",
  )

  h = ScalarSymbol(
    name="h",
  )

  product = ScalarProduct(
    left=p,
    right=h,
  )

  even_statement = EvenScalarStatement(
    scalar=product,
  )

  odd_statement = OddScalarStatement(
    scalar=product,
  )

  assert product != even_statement
  assert product != odd_statement


def test_phase33_7_smash_product_is_not_implicitly_commutative():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  assert SmashProduct(
    left=a,
    right=b,
  ) != SmashProduct(
    left=b,
    right=a,
  )


def test_phase33_7_smash_product_has_no_automatic_typing():
  a = HomotopyElement(
    name="a",
    dimension=1,
    source=6,
    target=3,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
    source=7,
    target=4,
  )

  smash = SmashProduct(
    left=a,
    right=b,
  )

  assert not hasattr(
    smash,
    "source",
  )

  assert not hasattr(
    smash,
    "target",
  )


def test_phase33_7_smash_product_does_not_equal_barratt_hilton_composition_automatically():
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

  smash = SmashProduct(
    left=a,
    right=b,
  )

  barratt_hilton_rhs = Multiple(
    coefficient=ScalarPower(
      base=-1,
      exponent=ScalarProduct(
        left=ScalarSum(
          left=p,
          right=k,
        ),
        right=h,
      ),
    ),
    expression=Composition(
      left=IteratedSuspension(
        expression=a,
        exponent=q,
      ),
      right=IteratedSuspension(
        expression=b,
        exponent=ScalarSum(
          left=p,
          right=k,
        ),
      ),
    ),
  )

  assert smash != barratt_hilton_rhs


def test_phase33_7_barratt_hilton_formula_requires_explicit_relation():
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

  smash = SmashProduct(
    left=a,
    right=b,
  )

  rhs = Multiple(
    coefficient=ScalarPower(
      base=-1,
      exponent=ScalarProduct(
        left=ScalarSum(
          left=p,
          right=k,
        ),
        right=h,
      ),
    ),
    expression=Composition(
      left=IteratedSuspension(
        expression=a,
        exponent=q,
      ),
      right=IteratedSuspension(
        expression=b,
        exponent=ScalarSum(
          left=p,
          right=k,
        ),
      ),
    ),
  )

  formula = Relation(
    lhs=smash,
    rhs=rhs,
    relation_type=RelationType.EQUALITY,
  )

  assert smash != rhs
  assert formula.lhs == smash
  assert formula.rhs == rhs


def test_phase33_7_symbolic_sign_is_not_evaluated_without_parity_fact():
  p = ScalarSymbol(
    name="p",
  )

  h = ScalarSymbol(
    name="h",
  )

  sign = ScalarPower(
    base=-1,
    exponent=ScalarProduct(
      left=p,
      right=h,
    ),
  )

  assert sign != 1
  assert sign != -1


def test_phase33_7_symbolic_signed_multiple_is_not_simplified_without_sign_evaluation():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  h = ScalarSymbol(
    name="h",
  )

  sign = ScalarPower(
    base=-1,
    exponent=ScalarProduct(
      left=p,
      right=h,
    ),
  )

  symbolic = Multiple(
    coefficient=sign,
    expression=a,
  )

  assert symbolic != a

  assert symbolic != Multiple(
    coefficient=-1,
    expression=a,
  )


def test_phase33_7_signed_sum_is_not_simplified_automatically():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  n = ScalarSymbol(
    name="n",
  )

  sign = ScalarPower(
    base=-1,
    exponent=n,
  )

  symbolic_sum = Sum(
    left=a,
    right=Multiple(
      coefficient=sign,
      expression=a,
    ),
  )

  assert symbolic_sum != a

  assert symbolic_sum != Multiple(
    coefficient=2,
    expression=a,
  )


def test_phase33_7_symbolic_iterated_suspension_does_not_gain_typing_from_notation():
  a = HomotopyElement(
    name="a",
    dimension=1,
    source=8,
    target=4,
  )

  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  suspension = IteratedSuspension(
    expression=a,
    exponent=ScalarSum(
      left=p,
      right=k,
    ),
  )

  assert suspension.source is None
  assert suspension.target is None


def test_phase33_7_formula_representation_is_not_a_proof_step_by_itself():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  formula = Relation(
    lhs=SmashProduct(
      left=a,
      right=b,
    ),
    rhs=Composition(
      left=a,
      right=b,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert isinstance(
    formula,
    Relation,
  )

  assert not isinstance(
    formula,
    ProofStep,
  )





