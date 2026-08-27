from stable_rules import (
  SuspensionMapStatement,
)


def test_suspension_map_statement():
  statement = SuspensionMapStatement(
    sphere_dimension=5,
    stem=2,
  )

  assert statement.sphere_dimension == 5
  assert statement.stem == 2


def test_suspension_map_statement_has_structural_equality():
  first = SuspensionMapStatement(
    sphere_dimension=5,
    stem=2,
  )

  second = SuspensionMapStatement(
    sphere_dimension=5,
    stem=2,
  )

  assert first == second


def test_suspension_map_statement_distinguishes_source_groups():
  first = SuspensionMapStatement(
    sphere_dimension=5,
    stem=2,
  )

  different_sphere = SuspensionMapStatement(
    sphere_dimension=6,
    stem=2,
  )

  different_stem = SuspensionMapStatement(
    sphere_dimension=5,
    stem=3,
  )

  assert first != different_sphere
  assert first != different_stem










