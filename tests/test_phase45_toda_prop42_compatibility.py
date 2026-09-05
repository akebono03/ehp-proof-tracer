from typing import (
  get_type_hints,
)

import map_facts

from algebra import (
  GroupMap,
)
from ehp import (
  EHPSegment,
)
from expression import (
  MapSymbol,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  ScalarValue,
)
from homotopy_groups import (
  PreimageSubgroup,
  PrimaryComponent,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_H_MAP,
  MapTypingFact,
)
from models import (
  AbelianGroup,
)
from proof import (
  ExactnessStatement,
)


def test_phase45_1_primary_component_accepts_symbolic_dimensions():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  component = PrimaryComponent(
    group_dimension=i,
    sphere_dimension=n,
    prime=2,
  )

  assert component.group_dimension == i
  assert component.sphere_dimension == n
  assert component.prime == 2


def test_phase45_1_primary_component_accepts_symbolic_ehp_degree_expressions():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  i_minus_one = ScalarSum(
    left=i,
    right=-1,
  )

  two_n_plus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=1,
  )

  source = PrimaryComponent(
    group_dimension=i_minus_one,
    sphere_dimension=n,
    prime=2,
  )

  target = PrimaryComponent(
    group_dimension=i,
    sphere_dimension=two_n_plus_one,
    prime=2,
  )

  assert source.group_dimension == (
    i_minus_one
  )

  assert source.sphere_dimension == n

  assert target.group_dimension == i

  assert target.sphere_dimension == (
    two_n_plus_one
  )

  assert source.prime == 2
  assert target.prime == 2


def test_phase45_1_primary_component_dimensions_use_scalar_value():
  type_hints = get_type_hints(
    PrimaryComponent
  )

  assert type_hints[
    "group_dimension"
  ] == ScalarValue

  assert type_hints[
    "sphere_dimension"
  ] == ScalarValue


def test_phase45_1_toda_primary_group_accepts_symbolic_dimensions():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=n,
  )

  assert group.group_dimension == i
  assert group.sphere_dimension == n


def test_phase45_1_preimage_subgroup_accepts_primary_component():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  component = PrimaryComponent(
    group_dimension=i,
    sphere_dimension=n,
    prime=2,
  )

  preimage = PreimageSubgroup(
    map=MapSymbol(
      name="E",
    ),
    subgroup=component,
  )

  assert preimage.map == MapSymbol(
    name="E",
  )

  assert preimage.subgroup == component


def test_phase45_1_exactness_statement_accepts_symbolic_map_symbols():
  first_map = MapSymbol(
    name="E",
  )

  second_map = EHP_H_MAP

  statement = ExactnessStatement(
    first_map=first_map,
    second_map=second_map,
    is_exact=True,
  )

  assert statement.first_map == (
    first_map
  )

  assert statement.second_map is (
    EHP_H_MAP
  )

  assert statement.is_exact


def test_phase45_1_exactness_statement_does_not_store_sequence_terms():
  statement = ExactnessStatement(
    first_map=MapSymbol(
      name="E",
    ),
    second_map=EHP_H_MAP,
    is_exact=True,
  )

  assert not hasattr(
    statement,
    "source_group",
  )

  assert not hasattr(
    statement,
    "middle_group",
  )

  assert not hasattr(
    statement,
    "target_group",
  )

  assert not hasattr(
    statement,
    "terms",
  )


def test_phase45_1_ehp_segment_is_concrete_repository_backed():
  type_hints = get_type_hints(
    GroupMap
  )

  assert type_hints[
    "source"
  ] is AbelianGroup

  assert type_hints[
    "target"
  ] is AbelianGroup


def test_phase45_1_ehp_segment_has_concrete_e_h_p_maps():
  assert hasattr(
    EHPSegment,
    "exactness_at_sphere",
  )

  assert hasattr(
    EHPSegment,
    "exactness_at_hopf_target",
  )

  assert hasattr(
    EHPSegment,
    "exact_step_at_sphere",
  )

  assert hasattr(
    EHPSegment,
    "exact_step_at_hopf_target",
  )


def test_phase45_1_canonical_h_map_exists():
  assert isinstance(
    EHP_H_MAP,
    MapSymbol,
  )

  assert EHP_H_MAP.name == "H"


def test_phase45_1_canonical_symbolic_p_map_does_not_exist_yet():
  assert not hasattr(
    map_facts,
    "EHP_P_MAP",
  )


def test_phase45_1_map_typing_fact_is_concrete_dimension_only():
  type_hints = get_type_hints(
    MapTypingFact
  )

  assert type_hints[
    "source_group_dimension"
  ] is int

  assert type_hints[
    "source_sphere_dimension"
  ] is int

  assert type_hints[
    "target_group_dimension"
  ] is int

  assert type_hints[
    "target_sphere_dimension"
  ] is int


def test_phase45_1_primary_component_has_no_sequence_semantics():
  component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  assert not hasattr(
    component,
    "incoming_map",
  )

  assert not hasattr(
    component,
    "outgoing_map",
  )

  assert not hasattr(
    component,
    "previous_term",
  )

  assert not hasattr(
    component,
    "next_term",
  )

  assert not hasattr(
    component,
    "is_exact",
  )


def test_phase45_1_toda_primary_group_has_no_sequence_semantics():
  group = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=5,
  )

  assert not hasattr(
    group,
    "incoming_map",
  )

  assert not hasattr(
    group,
    "outgoing_map",
  )

  assert not hasattr(
    group,
    "is_exact",
  )


def test_phase45_1_preimage_subgroup_has_no_exactness_semantics():
  subgroup = PreimageSubgroup(
    map=MapSymbol(
      name="E",
    ),
    subgroup=PrimaryComponent(
      group_dimension=8,
      sphere_dimension=5,
      prime=2,
    ),
  )

  assert not hasattr(
    subgroup,
    "kernel",
  )

  assert not hasattr(
    subgroup,
    "image",
  )

  assert not hasattr(
    subgroup,
    "is_exact",
  )


def test_phase45_1_current_group_terms_have_no_toda_prop42_semantics():
  values = (
    PrimaryComponent(
      group_dimension=8,
      sphere_dimension=5,
      prime=2,
    ),
    TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    ),
    PreimageSubgroup(
      map=MapSymbol(
        name="E",
      ),
      subgroup=PrimaryComponent(
        group_dimension=8,
        sphere_dimension=5,
        prime=2,
      ),
    ),
  )

  for value in values:
    assert not hasattr(
      value,
      "toda_prop_4_2",
    )

    assert not hasattr(
      value,
      "theorem",
    )

    assert not hasattr(
      value,
      "source",
    )


def test_phase45_1_exactness_statement_is_distinct_from_concrete_ehp_segment():
  statement = ExactnessStatement(
    first_map=MapSymbol(
      name="E",
    ),
    second_map=EHP_H_MAP,
    is_exact=True,
  )

  assert not isinstance(
    statement,
    EHPSegment,
  )



