from typing import (
  get_type_hints,
)

from expression import (
  IteratedSuspension,
  MapSymbol,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  ScalarValue,
)
from homotopy_groups import (
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
)


def build_phase46_3_symbolic_map():
  n = ScalarSymbol(
    name="n",
  )

  k = ScalarSymbol(
    name="k",
  )

  m = ScalarSymbol(
    name="m",
  )

  exponent = ScalarSum(
    left=m,
    right=ScalarProduct(
      left=-1,
      right=n,
    ),
  )

  source_group = TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=n,
      right=k,
    ),
    sphere_dimension=n,
  )

  target_group = TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=m,
      right=k,
    ),
    sphere_dimension=m,
  )

  return TodaIteratedSuspensionMap(
    exponent=exponent,
    source_group=source_group,
    target_group=target_group,
  )


def test_phase46_3_map_exponent_uses_scalar_value():
  type_hints = get_type_hints(
    TodaIteratedSuspensionMap
  )

  assert type_hints[
    "exponent"
  ] == ScalarValue


def test_phase46_3_map_source_group_uses_toda_primary_group():
  type_hints = get_type_hints(
    TodaIteratedSuspensionMap
  )

  assert type_hints[
    "source_group"
  ] is TodaPrimaryGroup


def test_phase46_3_map_target_group_uses_toda_primary_group():
  type_hints = get_type_hints(
    TodaIteratedSuspensionMap
  )

  assert type_hints[
    "target_group"
  ] is TodaPrimaryGroup


def test_phase46_3_e_m_minus_n_exponent_is_losslessly_representable():
  suspension_map = (
    build_phase46_3_symbolic_map()
  )

  assert suspension_map.exponent == (
    ScalarSum(
      left=ScalarSymbol(
        name="m",
      ),
      right=ScalarProduct(
        left=-1,
        right=ScalarSymbol(
          name="n",
        ),
      ),
    )
  )


def test_phase46_3_source_is_pi_n_plus_k_n():
  suspension_map = (
    build_phase46_3_symbolic_map()
  )

  n = ScalarSymbol(
    name="n",
  )

  k = ScalarSymbol(
    name="k",
  )

  assert suspension_map.source_group == (
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=k,
      ),
      sphere_dimension=n,
    )
  )


def test_phase46_3_target_is_pi_m_plus_k_m():
  suspension_map = (
    build_phase46_3_symbolic_map()
  )

  m = ScalarSymbol(
    name="m",
  )

  k = ScalarSymbol(
    name="k",
  )

  assert suspension_map.target_group == (
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=m,
        right=k,
      ),
      sphere_dimension=m,
    )
  )


def test_phase46_3_same_map_instance_has_structural_equality():
  first = (
    build_phase46_3_symbolic_map()
  )

  second = (
    build_phase46_3_symbolic_map()
  )

  assert first == second


def test_phase46_3_different_exponents_are_structurally_distinct():
  suspension_map = (
    build_phase46_3_symbolic_map()
  )

  different = TodaIteratedSuspensionMap(
    exponent=ScalarSymbol(
      name="q",
    ),
    source_group=(
      suspension_map.source_group
    ),
    target_group=(
      suspension_map.target_group
    ),
  )

  assert suspension_map != different


def test_phase46_3_different_source_groups_are_structurally_distinct():
  suspension_map = (
    build_phase46_3_symbolic_map()
  )

  different = TodaIteratedSuspensionMap(
    exponent=suspension_map.exponent,
    source_group=TodaPrimaryGroup(
      group_dimension=1,
      sphere_dimension=1,
    ),
    target_group=(
      suspension_map.target_group
    ),
  )

  assert suspension_map != different


def test_phase46_3_different_target_groups_are_structurally_distinct():
  suspension_map = (
    build_phase46_3_symbolic_map()
  )

  different = TodaIteratedSuspensionMap(
    exponent=suspension_map.exponent,
    source_group=(
      suspension_map.source_group
    ),
    target_group=TodaPrimaryGroup(
      group_dimension=1,
      sphere_dimension=1,
    ),
  )

  assert suspension_map != different


def test_phase46_3_map_representation_is_distinct_from_map_symbol():
  suspension_map = (
    build_phase46_3_symbolic_map()
  )

  assert not isinstance(
    suspension_map,
    MapSymbol,
  )


def test_phase46_3_map_representation_is_distinct_from_element_suspension():
  suspension_map = (
    build_phase46_3_symbolic_map()
  )

  assert not isinstance(
    suspension_map,
    IteratedSuspension,
  )


def test_phase46_3_map_does_not_assert_isomorphism():
  suspension_map = (
    build_phase46_3_symbolic_map()
  )

  assert not hasattr(
    suspension_map,
    "is_isomorphism",
  )

  assert not hasattr(
    suspension_map,
    "isomorphic",
  )

  assert not hasattr(
    suspension_map,
    "isomorphism",
  )


def test_phase46_3_map_has_no_toda_45_theorem_semantics():
  suspension_map = (
    build_phase46_3_symbolic_map()
  )

  assert not hasattr(
    suspension_map,
    "toda_4_5",
  )

  assert not hasattr(
    suspension_map,
    "theorem",
  )

  assert not hasattr(
    suspension_map,
    "source",
  )


def test_phase46_3_map_constructor_does_not_solve_dimension_compatibility():
  suspension_map = TodaIteratedSuspensionMap(
    exponent=1,
    source_group=TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    ),
    target_group=TodaPrimaryGroup(
      group_dimension=100,
      sphere_dimension=200,
    ),
  )

  assert suspension_map.exponent == 1

  assert suspension_map.source_group == (
    TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    )
  )

  assert suspension_map.target_group == (
    TodaPrimaryGroup(
      group_dimension=100,
      sphere_dimension=200,
    )
  )
