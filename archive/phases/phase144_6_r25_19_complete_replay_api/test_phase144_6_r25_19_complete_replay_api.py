import pytest

from tests.test_phase131_3_group_result_proof_replay import (
  build_phase131_3_fixture,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
  build_toda_group_result_proof_replay,
)


def test_phase144_6_r25_19_complete_replay_reaches_actual_leaf_depth():
  data = build_phase131_3_fixture()

  replay = (
    build_complete_toda_group_result_proof_replay(
      data[
        "group_result"
      ]
    )
  )

  assert replay.max_depth == 2
  assert tuple(
    step.proof_step
    for step in replay.steps
  ) == (
    data[
      "root_step"
    ],
    data[
      "middle_step"
    ],
    data[
      "sibling_step"
    ],
    data[
      "leaf_step"
    ],
  )


def test_phase144_6_r25_19_existing_default_depth_remains_one():
  data = build_phase131_3_fixture()

  replay = (
    build_toda_group_result_proof_replay(
      data[
        "group_result"
      ]
    )
  )

  assert replay.max_depth == 1
  assert all(
    step.depth <= 1
    for step in replay.steps
  )


def test_phase144_6_r25_19_complete_replay_rejects_invalid_group_result():
  with pytest.raises(
    TypeError,
    match="group_result must be a TodaGroupResult",
  ):
    build_complete_toda_group_result_proof_replay(
      "not-a-group-result"
    )
