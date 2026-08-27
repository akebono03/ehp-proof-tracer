from expression import (
  eta,
  nu,
)
from hopf_rules import (
  HopfInvariantStatement,
)


def test_hopf_invariant_statement():
  statement = HopfInvariantStatement(
    expression=eta(2),
    value=1,
  )

  assert statement.expression == eta(2)
  assert statement.value == 1


def test_hopf_invariant_statement_has_structural_equality():
  first = HopfInvariantStatement(
    expression=eta(2),
    value=1,
  )

  second = HopfInvariantStatement(
    expression=eta(2),
    value=1,
  )

  assert first == second


def test_hopf_invariant_statement_distinguishes_expression():
  first = HopfInvariantStatement(
    expression=eta(2),
    value=1,
  )

  different_expression = (
    HopfInvariantStatement(
      expression=nu(4),
      value=1,
    )
  )

  assert first != different_expression


def test_hopf_invariant_statement_distinguishes_value():
  first = HopfInvariantStatement(
    expression=eta(2),
    value=1,
  )

  different_value = (
    HopfInvariantStatement(
      expression=eta(2),
      value=0,
    )
  )

  assert first != different_value






