import pytest

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_classifier import (
  classify_toda_group_proof_narrative_step,
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


def test_phase134_20_pi15_8_root_is_accepted_by_classifier(
):
  presentation = _presentation(
    8,
    7,
  )

  classification = (
    classify_toda_group_proof_narrative_step(
      presentation,
      presentation.root_step,
    )
  )

  assert classification is not None


def test_phase134_20_existing_pi6_3_root_remains_accepted(
):
  presentation = _presentation(
    3,
    3,
  )

  classification = (
    classify_toda_group_proof_narrative_step(
      presentation,
      presentation.root_step,
    )
  )

  assert classification is not None


def test_phase134_20_existing_pi8_5_root_remains_accepted(
):
  presentation = _presentation(
    5,
    3,
  )

  classification = (
    classify_toda_group_proof_narrative_step(
      presentation,
      presentation.root_step,
    )
  )

  assert classification is not None


def test_phase134_20_unrelated_root_is_still_rejected(
):
  presentation = _presentation(
    9,
    7,
  )

  with pytest.raises(
    ValueError,
  ):
    classify_toda_group_proof_narrative_step(
      presentation,
      presentation.root_step,
    )
