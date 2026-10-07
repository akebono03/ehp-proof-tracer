import pytest

from expression import (
  ScalarSymbol,
)
from homotopy_groups import (
  TodaPrimaryGroup,
)
from stable_rules import (
  canonical_toda_stable_base,
  is_in_toda_stable_range,
  toda_primary_group_stem,
  toda_stable_transport_exponent,
)


def test_phase160_r2_pi4_3_is_canonical_stable_base_for_stem_1():
  target = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
  )

  assert toda_primary_group_stem(
    target
  ) == 1

  assert is_in_toda_stable_range(
    target
  )

  assert canonical_toda_stable_base(
    target
  ) == target

  assert toda_stable_transport_exponent(
    target
  ) == 0


def test_phase160_r2_pi5_4_uses_pi4_3_with_one_suspension():
  target = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=4,
  )

  assert canonical_toda_stable_base(
    target
  ) == TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
  )

  assert toda_stable_transport_exponent(
    target
  ) == 1


def test_phase160_r2_pi6_5_uses_pi4_3_with_two_suspensions():
  target = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=5,
  )

  assert canonical_toda_stable_base(
    target
  ) == TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
  )

  assert toda_stable_transport_exponent(
    target
  ) == 2


def test_phase160_r2_pi16_9_is_canonical_stable_base_for_stem_7():
  target = TodaPrimaryGroup(
    group_dimension=16,
    sphere_dimension=9,
  )

  assert toda_primary_group_stem(
    target
  ) == 7

  assert is_in_toda_stable_range(
    target
  )

  assert canonical_toda_stable_base(
    target
  ) == target

  assert toda_stable_transport_exponent(
    target
  ) == 0


def test_phase160_r2_higher_stem_7_target_uses_pi16_9():
  target = TodaPrimaryGroup(
    group_dimension=17,
    sphere_dimension=10,
  )

  assert canonical_toda_stable_base(
    target
  ) == TodaPrimaryGroup(
    group_dimension=16,
    sphere_dimension=9,
  )

  assert toda_stable_transport_exponent(
    target
  ) == 1


def test_phase160_r2_pi3_2_is_outside_stable_range():
  target = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  assert toda_primary_group_stem(
    target
  ) == 1

  assert not is_in_toda_stable_range(
    target
  )

  assert canonical_toda_stable_base(
    target
  ) == TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
  )


def test_phase160_r2_unstable_target_has_no_forward_stable_transport_exponent():
  target = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  with pytest.raises(
    ValueError,
    match=(
      "outside the Toda stable range"
    ),
  ):
    toda_stable_transport_exponent(
      target
    )


def test_phase160_r2_rejects_symbolic_target_dimensions():
  target = TodaPrimaryGroup(
    group_dimension=ScalarSymbol(
      name="n_plus_k",
    ),
    sphere_dimension=ScalarSymbol(
      name="n",
    ),
  )

  with pytest.raises(
    TypeError,
    match=(
      "dimensions must be concrete integers"
    ),
  ):
    is_in_toda_stable_range(
      target
    )


def test_phase160_r2_rejects_negative_stem_target():
  target = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=5,
  )

  with pytest.raises(
    ValueError,
    match="nonnegative stem",
  ):
    toda_primary_group_stem(
      target
    )
