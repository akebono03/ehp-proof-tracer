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






