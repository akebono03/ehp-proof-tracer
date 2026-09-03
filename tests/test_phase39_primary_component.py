from expression import (
  ScalarSymbol,
)
from homotopy_groups import (
  PrimaryComponent,
)


def test_phase39_2_primary_component_represents_concrete_two_primary_group():
  component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  assert component.group_dimension == 8
  assert component.sphere_dimension == 5
  assert component.prime == 2


def test_phase39_2_primary_component_supports_arbitrary_prime_structurally():
  component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=3,
  )

  assert component.group_dimension == 8
  assert component.sphere_dimension == 5
  assert component.prime == 3


def test_phase39_2_primary_component_supports_symbolic_group_dimension():
  i = ScalarSymbol(
    name="i",
  )

  component = PrimaryComponent(
    group_dimension=i,
    sphere_dimension=5,
    prime=2,
  )

  assert component.group_dimension == i
  assert component.sphere_dimension == 5
  assert component.prime == 2


def test_phase39_2_primary_component_supports_symbolic_sphere_dimension():
  n = ScalarSymbol(
    name="n",
  )

  component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=n,
    prime=2,
  )

  assert component.group_dimension == 8
  assert component.sphere_dimension == n
  assert component.prime == 2


def test_phase39_2_primary_component_structural_equality_uses_all_fields():
  first = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  same = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  different_prime = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=3,
  )

  different_group_dimension = PrimaryComponent(
    group_dimension=9,
    sphere_dimension=5,
    prime=2,
  )

  different_sphere_dimension = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=6,
    prime=2,
  )

  assert first == same
  assert first != different_prime
  assert first != different_group_dimension
  assert first != different_sphere_dimension



