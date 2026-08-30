from expression import ScalarSymbol
from scalar_rules import (
  EvenScalarStatement,
  OddScalarStatement,
  ScalarCongruenceStatement,
)


def test_odd_scalar_statement():
  k = ScalarSymbol(
    name="k",
  )

  statement = OddScalarStatement(
    scalar=k,
  )

  assert statement.scalar == k


def test_odd_scalar_statement_has_structural_equality():
  first = OddScalarStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
  )

  second = OddScalarStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
  )

  assert first == second


def test_odd_scalar_statement_distinguishes_scalar():
  k_statement = OddScalarStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
  )

  ell_statement = OddScalarStatement(
    scalar=ScalarSymbol(
      name="l",
    ),
  )

  assert k_statement != ell_statement


def test_even_scalar_statement():
  k = ScalarSymbol(
    name="k",
  )

  statement = EvenScalarStatement(
    scalar=k,
  )

  assert statement.scalar == k


def test_even_scalar_statement_has_structural_equality():
  first = EvenScalarStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
  )

  second = EvenScalarStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
  )

  assert first == second


def test_scalar_congruence_statement():
  k = ScalarSymbol(
    name="k",
  )

  statement = ScalarCongruenceStatement(
    scalar=k,
    residue=1,
    modulus=2,
  )

  assert statement.scalar == k
  assert statement.residue == 1
  assert statement.modulus == 2


def test_scalar_congruence_statement_has_structural_equality():
  first = ScalarCongruenceStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
    residue=1,
    modulus=2,
  )

  second = ScalarCongruenceStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
    residue=1,
    modulus=2,
  )

  assert first == second


def test_scalar_congruence_statement_distinguishes_constraints():
  odd_congruence = ScalarCongruenceStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
    residue=1,
    modulus=2,
  )

  other_congruence = ScalarCongruenceStatement(
    scalar=ScalarSymbol(
      name="k",
    ),
    residue=0,
    modulus=2,
  )

  assert odd_congruence != other_congruence



