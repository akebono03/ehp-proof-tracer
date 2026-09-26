import pytest

from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_contribution_ownership import (
  filter_toda_group_proof_narrative_exactness_body_contributions,
)
from toda_group_proof_narrative_exactness_display_contributions import (
  TodaGroupProofNarrativeExactnessDisplayContributionKind,
  extract_toda_group_proof_narrative_exactness_display_contributions,
)
from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_primary_exactness_component,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _argument_primary_data(
  n,
  k,
  role,
  occurrence=0,
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  matches = tuple(
    (
      argument_index,
      argument,
    )
    for argument_index, argument in enumerate(
      arguments
    )
    if argument.role is role
  )
  argument_index, argument = matches[
    occurrence
  ]

  relevant_groups = (
    extract_toda_group_proof_narrative_argument_relevant_groups(
      presentation,
      blocks,
      argument,
    )
  )
  evidence = (
    extract_toda_group_proof_narrative_argument_method_evidence(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )
  components = (
    build_toda_group_proof_narrative_exactness_method_components(
      evidence
    )
  )
  primary_component = (
    select_toda_group_proof_narrative_primary_exactness_component(
      relevant_groups,
      components,
    )
  )

  return (
    presentation,
    blocks,
    primary_component,
  )


def test_phase143_39_primary_pi6_3_group_suppresses_window_contributions():
  (
    presentation,
    _blocks,
    primary_component,
  ) = _argument_primary_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert primary_component is not None

  for block in primary_component.evidence_blocks:
    contributions = (
      extract_toda_group_proof_narrative_exactness_display_contributions(
        presentation,
        block,
      )
    )
    filtered = (
      filter_toda_group_proof_narrative_exactness_body_contributions(
        block,
        contributions,
        primary_component,
      )
    )

    assert all(
      contribution.kind
      is not TodaGroupProofNarrativeExactnessDisplayContributionKind
      .EXACTNESS_WINDOW
      for contribution in filtered
    )


def test_phase143_39_primary_pi6_3_group_keeps_derived_short_exact_sequence():
  (
    presentation,
    _blocks,
    primary_component,
  ) = _argument_primary_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert primary_component is not None

  filtered = tuple(
    contribution
    for block in primary_component.evidence_blocks
    for contribution in (
      filter_toda_group_proof_narrative_exactness_body_contributions(
        block,
        extract_toda_group_proof_narrative_exactness_display_contributions(
          presentation,
          block,
        ),
        primary_component,
      )
    )
  )

  assert any(
    contribution.kind
    is TodaGroupProofNarrativeExactnessDisplayContributionKind
    .DERIVED_SHORT_EXACT_SEQUENCE
    and contribution.latex
    == (
      r"0\longrightarrow \pi_{5}^{2}"
      r"\xrightarrow{E} \pi_{6}^{3}"
      r"\xrightarrow{H} \pi_{6}^{5}"
      r"\longrightarrow 0"
    )
    for contribution in filtered
  )


def test_phase143_39_none_primary_keeps_all_contributions():
  (
    presentation,
    blocks,
    primary_component,
  ) = _argument_primary_data(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert primary_component is None

  exactness_block = next(
    block
    for block in blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    )
  )
  contributions = (
    extract_toda_group_proof_narrative_exactness_display_contributions(
      presentation,
      exactness_block,
    )
  )

  assert (
    filter_toda_group_proof_narrative_exactness_body_contributions(
      exactness_block,
      contributions,
      primary_component,
    )
    == contributions
  )


def test_phase143_39_non_primary_evidence_block_keeps_all_contributions():
  (
    presentation,
    blocks,
    primary_component,
  ) = _argument_primary_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  assert primary_component is not None

  non_primary_block = next(
    block
    for block in blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
      and all(
        evidence_block is not block
        for evidence_block
        in primary_component.evidence_blocks
      )
    )
  )
  contributions = (
    extract_toda_group_proof_narrative_exactness_display_contributions(
      presentation,
      non_primary_block,
    )
  )

  assert (
    filter_toda_group_proof_narrative_exactness_body_contributions(
      non_primary_block,
      contributions,
      primary_component,
    )
    == contributions
  )


def test_phase143_39_primary_block_identity_not_structural_equality():
  (
    presentation,
    blocks,
    primary_component,
  ) = _argument_primary_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  assert primary_component is not None

  primary_block = primary_component.evidence_blocks[
    0
  ]
  matching_block = type(
    primary_block
  )(
    role=primary_block.role,
    steps=primary_block.steps,
  )
  contributions = (
    extract_toda_group_proof_narrative_exactness_display_contributions(
      presentation,
      primary_block,
    )
  )

  assert (
    filter_toda_group_proof_narrative_exactness_body_contributions(
      matching_block,
      contributions,
      primary_component,
    )
    == contributions
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
def test_phase143_39_four_targets_filter_safely(
  n,
  k,
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  for argument_index, argument in enumerate(
    arguments
  ):
    relevant_groups = (
      extract_toda_group_proof_narrative_argument_relevant_groups(
        presentation,
        blocks,
        argument,
      )
    )
    evidence = (
      extract_toda_group_proof_narrative_argument_method_evidence(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )
    components = (
      build_toda_group_proof_narrative_exactness_method_components(
        evidence
      )
    )
    primary_component = (
      select_toda_group_proof_narrative_primary_exactness_component(
        relevant_groups,
        components,
      )
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
      filtered = (
        filter_toda_group_proof_narrative_exactness_body_contributions(
          block,
          contributions,
          primary_component,
        )
      )

      assert isinstance(
        filtered,
        tuple,
      )
      assert all(
        contribution in contributions
        for contribution in filtered
      )


def test_phase143_39_rejects_non_tuple_contributions():
  (
    _presentation,
    blocks,
    _primary_component,
  ) = _argument_primary_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )
  exactness_block = next(
    block
    for block in blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    )
  )

  with pytest.raises(
    TypeError,
    match="contributions must be a tuple",
  ):
    filter_toda_group_proof_narrative_exactness_body_contributions(
      exactness_block,
      [],
      None,
    )
