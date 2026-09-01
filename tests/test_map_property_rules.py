from expression import (
  MapSymbol,
)
from map_property_rules import (
  InjectiveMapStatement,
  IsomorphismStatement,
)


def test_phase28_1_injective_map_statement_preserves_map():
  f = MapSymbol(
    name="f",
  )

  statement = InjectiveMapStatement(
    map=f,
  )

  assert statement.map == f


def test_phase28_1_injective_map_statement_has_structural_equality():
  f = MapSymbol(
    name="f",
  )

  first = InjectiveMapStatement(
    map=f,
  )

  second = InjectiveMapStatement(
    map=f,
  )

  assert first == second


def test_phase28_1_injective_map_statement_distinguishes_map():
  f = MapSymbol(
    name="f",
  )

  g = MapSymbol(
    name="g",
  )

  f_statement = InjectiveMapStatement(
    map=f,
  )

  g_statement = InjectiveMapStatement(
    map=g,
  )

  assert f_statement != g_statement


def test_phase28_1_map_symbol_does_not_imply_injectivity():
  f = MapSymbol(
    name="f",
  )

  statement = InjectiveMapStatement(
    map=f,
  )

  assert f != statement


def test_phase28_2_isomorphism_statement_preserves_map():
  f = MapSymbol(
    name="f",
  )

  statement = IsomorphismStatement(
    map=f,
  )

  assert statement.map == f


def test_phase28_2_isomorphism_statement_has_structural_equality():
  f = MapSymbol(
    name="f",
  )

  first = IsomorphismStatement(
    map=f,
  )

  second = IsomorphismStatement(
    map=f,
  )

  assert first == second


def test_phase28_2_isomorphism_statement_distinguishes_map():
  f = MapSymbol(
    name="f",
  )

  g = MapSymbol(
    name="g",
  )

  f_statement = IsomorphismStatement(
    map=f,
  )

  g_statement = IsomorphismStatement(
    map=g,
  )

  assert f_statement != g_statement


def test_phase28_2_isomorphism_and_injectivity_remain_distinct_statements():
  f = MapSymbol(
    name="f",
  )

  isomorphism = IsomorphismStatement(
    map=f,
  )

  injectivity = InjectiveMapStatement(
    map=f,
  )

  assert isomorphism != injectivity



