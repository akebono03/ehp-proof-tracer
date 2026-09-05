import pytest

from expression import (
  MapSymbol,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  PrimaryComponent,
  TodaEHPSequence,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  ExactnessStatement,
)


def build_phase45_2_symbolic_sequence():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  i_plus_one = ScalarSum(
    left=i,
    right=1,
  )

  i_minus_one = ScalarSum(
    left=i,
    right=-1,
  )

  n_plus_one = ScalarSum(
    left=n,
    right=1,
  )

  two_n_plus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=1,
  )

  terms = (
    TodaPrimaryGroup(
      group_dimension=i,
      sphere_dimension=n,
    ),
    TodaPrimaryGroup(
      group_dimension=i_plus_one,
      sphere_dimension=n_plus_one,
    ),
    TodaPrimaryGroup(
      group_dimension=i_plus_one,
      sphere_dimension=two_n_plus_one,
    ),
    TodaPrimaryGroup(
      group_dimension=i_minus_one,
      sphere_dimension=n,
    ),
    TodaPrimaryGroup(
      group_dimension=i,
      sphere_dimension=n_plus_one,
    ),
  )

  maps = (
    EHP_E_MAP,
    EHP_H_MAP,
    EHP_DELTA_MAP,
    EHP_E_MAP,
  )

  return TodaEHPSequence(
    terms=terms,
    maps=maps,
  )


def test_phase45_2_canonical_e_map_is_structural_map_symbol():
  assert isinstance(
    EHP_E_MAP,
    MapSymbol,
  )

  assert EHP_E_MAP == MapSymbol(
    name="E",
  )


def test_phase45_2_canonical_h_map_remains_existing_map_symbol():
  assert isinstance(
    EHP_H_MAP,
    MapSymbol,
  )

  assert EHP_H_MAP == MapSymbol(
    name="H",
  )


def test_phase45_2_canonical_delta_map_is_structural_map_symbol():
  assert isinstance(
    EHP_DELTA_MAP,
    MapSymbol,
  )

  assert EHP_DELTA_MAP == MapSymbol(
    name="Δ",
  )


def test_phase45_2_sequence_preserves_all_five_terms():
  sequence = (
    build_phase45_2_symbolic_sequence()
  )

  assert len(
    sequence.terms
  ) == 5


def test_phase45_2_sequence_preserves_e_h_delta_e_map_order():
  sequence = (
    build_phase45_2_symbolic_sequence()
  )

  assert sequence.maps == (
    EHP_E_MAP,
    EHP_H_MAP,
    EHP_DELTA_MAP,
    EHP_E_MAP,
  )


def test_phase45_2_sequence_first_term_is_pi_i_n():
  sequence = (
    build_phase45_2_symbolic_sequence()
  )

  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  assert sequence.terms[
    0
  ] == TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=n,
  )


def test_phase45_2_sequence_second_term_is_pi_i_plus_1_n_plus_1():
  sequence = (
    build_phase45_2_symbolic_sequence()
  )

  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  assert sequence.terms[
    1
  ] == TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=i,
      right=1,
    ),
    sphere_dimension=ScalarSum(
      left=n,
      right=1,
    ),
  )


def test_phase45_2_sequence_third_term_is_pi_i_plus_1_2n_plus_1():
  sequence = (
    build_phase45_2_symbolic_sequence()
  )

  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  assert sequence.terms[
    2
  ] == TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=i,
      right=1,
    ),
    sphere_dimension=ScalarSum(
      left=ScalarProduct(
        left=2,
        right=n,
      ),
      right=1,
    ),
  )


def test_phase45_2_sequence_fourth_term_is_pi_i_minus_1_n():
  sequence = (
    build_phase45_2_symbolic_sequence()
  )

  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  assert sequence.terms[
    3
  ] == TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=i,
      right=-1,
    ),
    sphere_dimension=n,
  )


def test_phase45_2_sequence_fifth_term_is_pi_i_n_plus_1():
  sequence = (
    build_phase45_2_symbolic_sequence()
  )

  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  assert sequence.terms[
    4
  ] == TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=ScalarSum(
      left=n,
      right=1,
    ),
  )


def test_phase45_2_sequence_reuses_same_canonical_e_map():
  sequence = (
    build_phase45_2_symbolic_sequence()
  )

  assert (
    sequence.maps[
      0
    ]
    is EHP_E_MAP
  )

  assert (
    sequence.maps[
      3
    ]
    is EHP_E_MAP
  )


def test_phase45_2_sequence_terms_remain_toda_primary_groups():
  sequence = (
    build_phase45_2_symbolic_sequence()
  )

  assert all(
    isinstance(
      term,
      TodaPrimaryGroup,
    )
    for term in sequence.terms
  )


def test_phase45_2_sequence_does_not_replace_terms_with_primary_components():
  sequence = (
    build_phase45_2_symbolic_sequence()
  )

  assert all(
    not isinstance(
      term,
      PrimaryComponent,
    )
    for term in sequence.terms
  )


def test_phase45_2_sequence_requires_one_more_term_than_maps():
  with pytest.raises(
    ValueError,
    match=(
      "TodaEHPSequence requires "
      "exactly one more term than maps"
    ),
  ):
    TodaEHPSequence(
      terms=(
        TodaPrimaryGroup(
          group_dimension=1,
          sphere_dimension=1,
        ),
        TodaPrimaryGroup(
          group_dimension=2,
          sphere_dimension=2,
        ),
      ),
      maps=(
        EHP_E_MAP,
        EHP_H_MAP,
      ),
    )


def test_phase45_2_sequence_has_structural_equality():
  left = (
    build_phase45_2_symbolic_sequence()
  )

  right = (
    build_phase45_2_symbolic_sequence()
  )

  assert left == right


def test_phase45_2_sequence_is_not_exactness_statement():
  sequence = (
    build_phase45_2_symbolic_sequence()
  )

  assert not isinstance(
    sequence,
    ExactnessStatement,
  )


def test_phase45_2_sequence_does_not_assert_exactness():
  sequence = (
    build_phase45_2_symbolic_sequence()
  )

  assert not hasattr(
    sequence,
    "is_exact",
  )

  assert not hasattr(
    sequence,
    "exact",
  )


def test_phase45_2_sequence_has_no_theorem_semantics():
  sequence = (
    build_phase45_2_symbolic_sequence()
  )

  assert not hasattr(
    sequence,
    "theorem",
  )

  assert not hasattr(
    sequence,
    "source",
  )

  assert not hasattr(
    sequence,
    "provenance",
  )


def test_phase45_2_sequence_does_not_encode_toda_prop42_itself():
  sequence = (
    build_phase45_2_symbolic_sequence()
  )

  assert not hasattr(
    sequence,
    "toda_prop_4_2",
  )

  assert not hasattr(
    sequence,
    "proposition",
  )


