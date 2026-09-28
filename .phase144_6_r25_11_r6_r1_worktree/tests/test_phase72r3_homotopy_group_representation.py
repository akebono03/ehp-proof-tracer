from expression import (
  ScalarSymbol,
)
from homotopy_groups import (
  HomotopyGroup,
  PrimaryComponent,
  TodaPrimaryGroup,
)


def test_phase72r3_ordinary_homotopy_group_concrete_dimensions():
  group = HomotopyGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  assert (
    group.group_dimension
    == 10
  )

  assert (
    group.sphere_dimension
    == 5
  )


def test_phase72r3_ordinary_homotopy_group_symbolic_dimensions():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  group = HomotopyGroup(
    group_dimension=i,
    sphere_dimension=n,
  )

  assert (
    group.group_dimension
    == i
  )

  assert (
    group.sphere_dimension
    == n
  )


def test_phase72r3_ordinary_homotopy_group_structural_equality():
  first = HomotopyGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  second = HomotopyGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  assert (
    first
    == second
  )


def test_phase72r3_ordinary_homotopy_group_distinguishes_group_dimension():
  first = HomotopyGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  second = HomotopyGroup(
    group_dimension=11,
    sphere_dimension=5,
  )

  assert (
    first
    != second
  )


def test_phase72r3_ordinary_homotopy_group_distinguishes_sphere_dimension():
  first = HomotopyGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  second = HomotopyGroup(
    group_dimension=10,
    sphere_dimension=6,
  )

  assert (
    first
    != second
  )


def test_phase72r3_ordinary_group_is_not_toda_primary_group():
  ordinary_group = HomotopyGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  toda_group = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  assert (
    ordinary_group
    != toda_group
  )


def test_phase72r3_ordinary_group_is_not_primary_component():
  ordinary_group = HomotopyGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  primary_component = PrimaryComponent(
    group_dimension=10,
    sphere_dimension=5,
    prime=2,
  )

  assert (
    ordinary_group
    != primary_component
  )


def test_phase72r3_toda_primary_group_and_primary_component_remain_distinct():
  toda_group = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  primary_component = PrimaryComponent(
    group_dimension=10,
    sphere_dimension=5,
    prime=2,
  )

  assert (
    toda_group
    != primary_component
  )


