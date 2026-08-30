from expression import (
  Composition,
  Expression,
  HomotopyElement,
  MapApplication,
  MapSymbol,
  Multiple,
  ScalarSymbol,
  Sum,
  Suspension,
  Zero,
  eta,
  nu,
  sigma,
)


def test_scalar_symbol():
  scalar = ScalarSymbol(
    name="k",
  )

  assert scalar.name == "k"


def test_scalar_symbol_has_structural_equality():
  k = ScalarSymbol(
    name="k",
  )

  same_k = ScalarSymbol(
    name="k",
  )

  ell = ScalarSymbol(
    name="l",
  )

  assert k == same_k
  assert k != ell


def test_scalar_symbol_is_not_expression():
  scalar = ScalarSymbol(
    name="k",
  )

  assert not isinstance(
    scalar,
    Expression,
  )


def test_homotopy_element():
  element = HomotopyElement(
    name="η",
    dimension=3,
  )

  assert element.name == "η"
  assert element.dimension == 3


def test_eta():
  assert eta(3) == HomotopyElement("η", 3)


def test_nu():
  assert nu(4) == HomotopyElement("ν", 4)


def test_sigma():
  assert sigma(8) == HomotopyElement("σ", 8)


def test_zero():
  assert Zero() == Zero()


def test_multiple():
  expression = Multiple(
    2,
    eta(3),
  )

  assert expression.coefficient == 2
  assert expression.expression == eta(3)


def test_inverse_is_represented_by_negative_one_multiple():
  alpha = eta(3)

  inverse = Multiple(
    -1,
    alpha,
  )

  assert inverse.coefficient == -1
  assert inverse.expression == alpha
  assert inverse == Multiple(
    -1,
    alpha,
  )


def test_multiple_remains_distinct_from_repeated_sum():
  alpha = eta(3)

  multiple = Multiple(
    2,
    alpha,
  )

  repeated_sum = Sum(
    alpha,
    alpha,
  )

  assert multiple != repeated_sum
  assert multiple.coefficient == 2
  assert multiple.expression == alpha


def test_zero_remains_distinct_from_zero_multiple():
  alpha = eta(3)

  zero = Zero()

  zero_multiple = Multiple(
    0,
    alpha,
  )

  assert zero_multiple != zero
  assert zero_multiple.coefficient == 0
  assert zero_multiple.expression == alpha


def test_sum():
  expression = Sum(
    eta(3),
    nu(4),
  )

  assert expression.left == eta(3)
  assert expression.right == nu(4)


def test_sum_with_zero_preserves_right_zero_structure():
  alpha = eta(3)

  expression = Sum(
    alpha,
    Zero(),
  )

  assert expression.left == alpha
  assert expression.right == Zero()
  assert expression != alpha


def test_sum_with_zero_preserves_left_zero_structure():
  alpha = eta(3)

  expression = Sum(
    Zero(),
    alpha,
  )

  assert expression.left == Zero()
  assert expression.right == alpha
  assert expression != alpha


def test_composition():
  expression = Composition(
    eta(3),
    eta(4),
  )

  assert expression.left == eta(3)
  assert expression.right == eta(4)


def test_suspension():
  expression = Suspension(
    eta(3),
  )

  assert expression.expression == eta(3)


def test_nested_suspension():
  expression = Suspension(
    Suspension(
      eta(3),
    )
  )

  assert expression == Suspension(
    Suspension(
      eta(3),
    )
  )

  assert expression.expression == Suspension(
    eta(3),
  )


def test_sum_has_structural_equality():
  expression = Sum(
    eta(3),
    nu(4),
  )

  assert expression == Sum(
    eta(3),
    nu(4),
  )


def test_sum_distinguishes_operand_order():
  left_right = Sum(
    eta(3),
    nu(4),
  )

  right_left = Sum(
    nu(4),
    eta(3),
  )

  assert left_right != right_left


def test_nested_sum_preserves_structure():
  alpha = eta(3)
  beta = nu(4)
  gamma = sigma(8)

  left_nested = Sum(
    Sum(
      alpha,
      beta,
    ),
    gamma,
  )

  right_nested = Sum(
    alpha,
    Sum(
      beta,
      gamma,
    ),
  )

  assert left_nested.left == Sum(
    alpha,
    beta,
  )
  assert left_nested.right == gamma

  assert right_nested.left == alpha
  assert right_nested.right == Sum(
    beta,
    gamma,
  )

  assert left_nested != right_nested


def test_map_symbol():
  map_symbol = MapSymbol(
    name="f",
  )

  assert map_symbol.name == "f"


def test_map_symbol_has_structural_equality():
  first = MapSymbol(
    name="f",
  )

  second = MapSymbol(
    name="f",
  )

  assert first == second


def test_map_symbol_distinguishes_name():
  f = MapSymbol(
    name="f",
  )

  g = MapSymbol(
    name="g",
  )

  assert f != g


def test_map_application():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  application = MapApplication(
    map=f,
    expression=alpha,
  )

  assert application.map == f
  assert application.expression == alpha


def test_map_application_has_structural_equality():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  first = MapApplication(
    map=f,
    expression=alpha,
  )

  second = MapApplication(
    map=f,
    expression=alpha,
  )

  assert first == second


def test_map_application_distinguishes_map():
  f = MapSymbol(
    name="f",
  )

  g = MapSymbol(
    name="g",
  )

  alpha = eta(3)

  f_alpha = MapApplication(
    map=f,
    expression=alpha,
  )

  g_alpha = MapApplication(
    map=g,
    expression=alpha,
  )

  assert f_alpha != g_alpha


def test_map_application_distinguishes_expression():
  f = MapSymbol(
    name="f",
  )

  f_alpha = MapApplication(
    map=f,
    expression=eta(3),
  )

  f_beta = MapApplication(
    map=f,
    expression=nu(4),
  )

  assert f_alpha != f_beta


def test_map_application_preserves_structured_argument():
  f = MapSymbol(
    name="f",
  )

  alpha = eta(3)
  beta = nu(4)

  argument = Sum(
    alpha,
    beta,
  )

  application = MapApplication(
    map=f,
    expression=argument,
  )

  assert application.expression == Sum(
    alpha,
    beta,
  )

  assert application != Sum(
    MapApplication(
      map=f,
      expression=alpha,
    ),
    MapApplication(
      map=f,
      expression=beta,
    ),
  )







