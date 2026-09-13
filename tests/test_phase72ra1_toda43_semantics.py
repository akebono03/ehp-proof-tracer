from functools import lru_cache

from homotopy_groups import (
  FiniteCyclicGroup,
  FreeCyclicGroup,
  HomotopyGroup,
  TodaPrimaryGroup,
)
from test_phase70_pi11_6_delta_iota13 import (
  build_phase70_8_data,
)
from test_phase71_toda512_n6_delta_injective import (
  build_phase71_4_data,
)


@lru_cache(maxsize=1)
def build_phase72ra1_data():
  phase70 = build_phase70_8_data()
  phase71 = build_phase71_4_data()

  return {
    "phase70": phase70,
    "phase71": phase71,
  }


def test_phase72ra1_toda_group_is_not_uniformly_ordinary_group():
  toda_group = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=6,
  )

  ordinary_group = HomotopyGroup(
    group_dimension=11,
    sphere_dimension=6,
  )

  assert toda_group != ordinary_group


def test_phase72ra1_regular_branch_pi10_5_is_two_primary_in_current_calculation():
  data = build_phase72ra1_data()

  relation = data[
    "phase70"
  ][
    "pi10_5_step"
  ].conclusion

  assert relation.lhs == TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert relation.rhs.order == 2


def test_phase72ra1_exceptional_branch_pi11_6_can_have_free_part():
  data = build_phase72ra1_data()

  relation = data[
    "phase70"
  ][
    "final_step"
  ].conclusion

  assert relation.lhs == TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=6,
  )

  assert isinstance(
    relation.rhs,
    FreeCyclicGroup,
  )


def test_phase72ra1_diagonal_pi11_11_is_free_cyclic():
  data = build_phase72ra1_data()

  relation = data[
    "phase70"
  ][
    "pi11_11_step"
  ].conclusion

  assert relation.lhs == TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=11,
  )

  assert isinstance(
    relation.rhs,
    FreeCyclicGroup,
  )


def test_phase72ra1_diagonal_pi13_13_is_free_cyclic():
  data = build_phase72ra1_data()

  relation = data[
    "phase70"
  ][
    "pi13_13_step"
  ].conclusion

  assert relation.lhs == TodaPrimaryGroup(
    group_dimension=13,
    sphere_dimension=13,
  )

  assert isinstance(
    relation.rhs,
    FreeCyclicGroup,
  )


def test_phase72ra1_phase71_n6_reuses_diagonal_and_exceptional_toda_groups():
  data = build_phase72ra1_data()

  statement = data[
    "phase71"
  ][
    "final_step"
  ].conclusion

  assert statement.map.source_group == TodaPrimaryGroup(
    group_dimension=13,
    sphere_dimension=13,
  )

  assert statement.map.target_group == TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=6,
  )


def test_phase72ra1_ordinary_pi11_s6_remains_distinct_from_toda_pi11_6():
  ordinary_group = HomotopyGroup(
    group_dimension=11,
    sphere_dimension=6,
  )

  toda_group = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=6,
  )

  assert ordinary_group != toda_group
