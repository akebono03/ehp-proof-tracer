from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_helpers import (
  is_completed_group_result_step,
  root_generator,
  root_target_group,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _presentation(
  n,
  k,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )

  return build_toda_group_proof_presentation(
    replay
  )


def test_phase134_14_pi6_3_root_is_completed_group_result(
):
  presentation = _presentation(
    3,
    3,
  )

  assert is_completed_group_result_step(
    presentation.root_step
  )


def test_phase134_14_pi8_5_root_is_completed_group_result(
):
  presentation = _presentation(
    5,
    3,
  )

  assert is_completed_group_result_step(
    presentation.root_step
  )


def test_phase134_14_root_generator_comes_from_group_result(
):
  for n, k in (
    (3, 3),
    (5, 3),
  ):
    presentation = _presentation(
      n,
      k,
    )

    assert root_generator(
      presentation
    ) == (
      presentation
      .source_replay
      .group_result
      .generators[
        0
      ]
    )


def test_phase134_14_root_target_group_comes_from_group_result(
):
  for n, k in (
    (3, 3),
    (5, 3),
  ):
    presentation = _presentation(
      n,
      k,
    )

    assert root_target_group(
      presentation
    ) == (
      presentation
      .source_replay
      .group_result
      .target
    )
