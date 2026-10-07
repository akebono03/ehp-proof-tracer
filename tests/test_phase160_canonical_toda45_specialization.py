import pytest

from expression import (
  ScalarProduct,
  ScalarSum,
)
from homotopy_groups import (
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_rules import (
  Toda45IsomorphismStatement,
)
from toda_stable_transport import (
  build_canonical_toda_45_isomorphism_step,
  build_canonical_toda_stable_transport_map,
)


def test_phase160_r3_pi4_3_transport_map_is_canonical_identity_specialization():
  target = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
  )

  transport_map = (
    build_canonical_toda_stable_transport_map(
      target
    )
  )

  assert transport_map == (
    TodaIteratedSuspensionMap(
      exponent=ScalarSum(
        left=3,
        right=ScalarProduct(
          left=-1,
          right=3,
        ),
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=3,
          right=1,
        ),
        sphere_dimension=3,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=3,
          right=1,
        ),
        sphere_dimension=3,
      ),
    )
  )


def test_phase160_r3_pi5_4_transport_map_uses_pi4_3():
  target = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=4,
  )

  transport_map = (
    build_canonical_toda_stable_transport_map(
      target
    )
  )

  assert transport_map.source_group == (
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=3,
        right=1,
      ),
      sphere_dimension=3,
    )
  )

  assert transport_map.target_group == (
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=4,
        right=1,
      ),
      sphere_dimension=4,
    )
  )

  assert transport_map.exponent == (
    ScalarSum(
      left=4,
      right=ScalarProduct(
        left=-1,
        right=3,
      ),
    )
  )


def test_phase160_r3_stem_7_transport_map_uses_pi16_9():
  target = TodaPrimaryGroup(
    group_dimension=17,
    sphere_dimension=10,
  )

  transport_map = (
    build_canonical_toda_stable_transport_map(
      target
    )
  )

  assert transport_map.source_group == (
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=9,
        right=7,
      ),
      sphere_dimension=9,
    )
  )

  assert transport_map.target_group == (
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=10,
        right=7,
      ),
      sphere_dimension=10,
    )
  )

  assert transport_map.exponent == (
    ScalarSum(
      left=10,
      right=ScalarProduct(
        left=-1,
        right=9,
      ),
    )
  )


def test_phase160_r3_pi5_4_derives_toda45_isomorphism():
  target = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=4,
  )

  step = (
    build_canonical_toda_45_isomorphism_step(
      target
    )
  )

  assert step.conclusion == (
    Toda45IsomorphismStatement(
      map=(
        build_canonical_toda_stable_transport_map(
          target
        )
      ),
    )
  )

  assert step.rule == ProofRule.INFERENCE

  assert step.inference_rule is not None


def test_phase160_r3_toda45_step_preserves_exact_three_specialization_premises():
  target = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=4,
  )

  step = (
    build_canonical_toda_45_isomorphism_step(
      target
    )
  )

  transport_map = (
    build_canonical_toda_stable_transport_map(
      target
    )
  )

  assert len(step.premises) == 3

  assert step.premises[
    0
  ].conclusion == (
    ScalarGreaterEqualStatement(
      left=3,
      right=ScalarSum(
        left=1,
        right=2,
      ),
    )
  )

  assert step.premises[
    1
  ].conclusion == (
    ScalarGreaterEqualStatement(
      left=4,
      right=3,
    )
  )

  assert step.premises[
    2
  ].conclusion == transport_map

  assert all(
    premise.rule == ProofRule.GIVEN
    for premise in step.premises
  )


def test_phase160_r3_stem_7_derives_toda45_from_canonical_base():
  target = TodaPrimaryGroup(
    group_dimension=17,
    sphere_dimension=10,
  )

  step = (
    build_canonical_toda_45_isomorphism_step(
      target
    )
  )

  assert step.conclusion.map.source_group == (
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=9,
        right=7,
      ),
      sphere_dimension=9,
    )
  )

  assert step.conclusion.map.target_group == (
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=10,
        right=7,
      ),
      sphere_dimension=10,
    )
  )


def test_phase160_r3_unstable_target_rejects_transport_map():
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
    build_canonical_toda_stable_transport_map(
      target
    )


def test_phase160_r3_unstable_target_rejects_toda45_specialization():
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
    build_canonical_toda_45_isomorphism_step(
      target
    )
