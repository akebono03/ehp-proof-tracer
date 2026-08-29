from expression import MapSymbol
from homomorphism_rules import (
  HomomorphismStatement,
)


def test_homomorphism_statement():
  f = MapSymbol(
    name="f",
  )

  statement = HomomorphismStatement(
    map=f,
  )

  assert statement.map == f


def test_homomorphism_statement_has_structural_equality():
  f = MapSymbol(
    name="f",
  )

  first = HomomorphismStatement(
    map=f,
  )

  second = HomomorphismStatement(
    map=f,
  )

  assert first == second


def test_homomorphism_statement_distinguishes_map():
  f = MapSymbol(
    name="f",
  )

  g = MapSymbol(
    name="g",
  )

  f_statement = HomomorphismStatement(
    map=f,
  )

  g_statement = HomomorphismStatement(
    map=g,
  )

  assert f_statement != g_statement



