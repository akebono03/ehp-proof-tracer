from algebra import (
  Subgroup,
)
from expression import (
  ScalarSymbol,
)
from homotopy_groups import (
  PrimaryComponent,
)
from models import (
  AbelianGroup,
  GroupComponent,
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


def test_phase39_3_two_primary_component_differs_from_three_primary_component():
  two_primary = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  three_primary = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=3,
  )

  assert two_primary != three_primary


def test_phase39_3_primary_components_with_different_group_dimensions_are_distinct():
  first = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  second = PrimaryComponent(
    group_dimension=9,
    sphere_dimension=5,
    prime=2,
  )

  assert first != second


def test_phase39_3_primary_components_with_different_sphere_dimensions_are_distinct():
  first = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  second = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=6,
    prime=2,
  )

  assert first != second


def test_phase39_3_primary_component_is_not_an_abelian_group():
  primary_component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  abelian_group = AbelianGroup(
    n=5,
    k=3,
    components=[
      GroupComponent(
        id=0,
        order=2,
        generator="x",
        element=[],
        gen_coe=[],
      ),
    ],
  )

  assert not isinstance(
    primary_component,
    AbelianGroup,
  )

  assert primary_component != abelian_group


def test_phase39_3_primary_component_is_not_a_subgroup():
  primary_component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  ambient_group = AbelianGroup(
    n=5,
    k=3,
    components=[
      GroupComponent(
        id=0,
        order=2,
        generator="x",
        element=[],
        gen_coe=[],
      ),
    ],
  )

  subgroup = Subgroup(
    ambient_group=ambient_group,
    elements=frozenset(),
    generators=(),
  )

  assert not isinstance(
    primary_component,
    Subgroup,
  )

  assert primary_component != subgroup


def test_phase39_3_primary_component_has_no_known_decomposition_fields():
  component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  assert not hasattr(
    component,
    "components",
  )

  assert not hasattr(
    component,
    "orders",
  )

  assert not hasattr(
    component,
    "generators",
  )

  assert not hasattr(
    component,
    "elements",
  )


