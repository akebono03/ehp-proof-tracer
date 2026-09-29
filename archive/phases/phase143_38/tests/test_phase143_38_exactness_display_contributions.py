import pytest

from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_display_contributions import (
  TodaGroupProofNarrativeExactnessDisplayContribution,
  TodaGroupProofNarrativeExactnessDisplayContributionKind,
  extract_toda_group_proof_narrative_exactness_display_contributions,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _pi6_3_exactness_data():
  (
    presentation,
    blocks,
    _sidecar,
    _arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  exactness_blocks = tuple(
    block
    for block in blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    )
  )

  return (
    presentation,
    exactness_blocks,
  )


def test_phase143_38_pi6_3_exactness_blocks_have_window_contributions():
  presentation, exactness_blocks = (
    _pi6_3_exactness_data()
  )

  contributions = tuple(
    contribution
    for block in exactness_blocks
    for contribution in (
      extract_toda_group_proof_narrative_exactness_display_contributions(
        presentation,
        block,
      )
    )
  )

  assert contributions
  assert any(
    contribution.kind
    is TodaGroupProofNarrativeExactnessDisplayContributionKind
    .EXACTNESS_WINDOW
    for contribution in contributions
  )


def test_phase143_38_pi6_3_recovers_derived_short_exact_sequence():
  presentation, exactness_blocks = (
    _pi6_3_exactness_data()
  )

  short_exact_contributions = tuple(
    contribution
    for block in exactness_blocks
    for contribution in (
      extract_toda_group_proof_narrative_exactness_display_contributions(
        presentation,
        block,
      )
    )
    if (
      contribution.kind
      is TodaGroupProofNarrativeExactnessDisplayContributionKind
      .DERIVED_SHORT_EXACT_SEQUENCE
    )
  )

  assert any(
    contribution.latex
    == (
      r"0\longrightarrow \pi_{5}^{2}"
      r"\xrightarrow{E} \pi_{6}^{3}"
      r"\xrightarrow{H} \pi_{6}^{5}"
      r"\longrightarrow 0"
    )
    for contribution in short_exact_contributions
  )


def test_phase143_38_short_exact_contribution_keeps_source_exactness_step():
  presentation, exactness_blocks = (
    _pi6_3_exactness_data()
  )

  for block in exactness_blocks:
    contributions = (
      extract_toda_group_proof_narrative_exactness_display_contributions(
        presentation,
        block,
      )
    )

    for contribution in contributions:
      assert any(
        contribution.proof_step is proof_step
        for proof_step in block.steps
      )


def test_phase143_38_not_every_window_has_short_exact_contribution():
  presentation, exactness_blocks = (
    _pi6_3_exactness_data()
  )

  contribution_sets = tuple(
    extract_toda_group_proof_narrative_exactness_display_contributions(
      presentation,
      block,
    )
    for block in exactness_blocks
  )

  assert any(
    any(
      contribution.kind
      is TodaGroupProofNarrativeExactnessDisplayContributionKind
      .EXACTNESS_WINDOW
      for contribution in contributions
    )
    and not any(
      contribution.kind
      is TodaGroupProofNarrativeExactnessDisplayContributionKind
      .DERIVED_SHORT_EXACT_SEQUENCE
      for contribution in contributions
    )
    for contributions in contribution_sets
  )


@pytest.mark.parametrize(
  "n,k",
  (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ),
)
def test_phase143_38_four_targets_extract_exactness_contributions_safely(
  n,
  k,
):
  (
    presentation,
    blocks,
    _sidecar,
    _arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  for block in blocks:
    if (
      block.role
      is not TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    ):
      continue

    contributions = (
      extract_toda_group_proof_narrative_exactness_display_contributions(
        presentation,
        block,
      )
    )

    assert isinstance(
      contributions,
      tuple,
    )
    assert all(
      isinstance(
        contribution,
        TodaGroupProofNarrativeExactnessDisplayContribution,
      )
      for contribution in contributions
    )
    assert all(
      contribution.latex
      for contribution in contributions
    )


def test_phase143_38_rejects_non_exactness_block():
  (
    presentation,
    blocks,
    _sidecar,
    _arguments,
  ) = _method_evidence_data(
    3,
    3,
  )
  non_exactness_block = next(
    block
    for block in blocks
    if (
      block.role
      is not TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    )
  )

  with pytest.raises(
    ValueError,
    match="block must be an EXACTNESS block",
  ):
    extract_toda_group_proof_narrative_exactness_display_contributions(
      presentation,
      non_exactness_block,
    )


def test_phase143_38_contribution_rejects_empty_latex():
  presentation, exactness_blocks = (
    _pi6_3_exactness_data()
  )
  proof_step = exactness_blocks[
    0
  ].steps[
    0
  ]

  with pytest.raises(
    ValueError,
    match="latex must not be empty",
  ):
    TodaGroupProofNarrativeExactnessDisplayContribution(
      kind=(
        TodaGroupProofNarrativeExactnessDisplayContributionKind
        .EXACTNESS_WINDOW
      ),
      proof_step=proof_step,
      latex="",
    )
