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



