from expression import (
  Composition,
  HomotopyElement,
  Multiple,
  Sum,
  Suspension,
  Zero,
  eta,
  nu,
  sigma,
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





