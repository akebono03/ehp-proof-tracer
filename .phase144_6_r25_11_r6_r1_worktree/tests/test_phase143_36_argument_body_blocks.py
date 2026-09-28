import pytest

from toda_group_proof_narrative_argument_body import (
  extract_toda_group_proof_narrative_argument_body_blocks,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
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


def _body_data(
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
  body_blocks = (
    extract_toda_group_proof_narrative_argument_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
      primary_component,
    )
  )

  return (
    presentation,
    blocks,
    sidecar,
    arguments,
    argument_index,
    argument,
    primary_component,
    body_blocks,
  )


def test_phase143_36_pi6_3_order_suppresses_primary_exactness_evidence():
  (
    _presentation,
    _blocks,
    _sidecar,
    _arguments,
    _argument_index,
    _argument,
    primary_component,
    body_blocks,
  ) = _body_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  assert primary_component is not None
  evidence_ids = {
    id(
      block
    )
    for block in primary_component.evidence_blocks
  }

  assert evidence_ids
  assert all(
    id(
      block
    ) not in evidence_ids
    for block in body_blocks
  )


def test_phase143_36_pi6_3_order_keeps_conclusion_last():
  (
    _presentation,
    _blocks,
    _sidecar,
    _arguments,
    _argument_index,
    argument,
    _primary_component,
    body_blocks,
  ) = _body_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  assert body_blocks
  assert (
    body_blocks[
      -1
    ]
    is argument.conclusion_block
  )


def test_phase143_36_pi6_3_group_structure_stops_at_child_argument_conclusion():
  (
    _presentation,
    _blocks,
    _sidecar,
    arguments,
    argument_index,
    argument,
    _primary_component,
    body_blocks,
  ) = _body_data(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  child_conclusion_ids = {
    id(
      arguments[
        child_index
      ].conclusion_block
    )
    for child_index in argument.child_argument_indices
  }

  assert child_conclusion_ids
  assert all(
    id(
      block
    ) not in child_conclusion_ids
    for block in body_blocks[
      :-1
    ]
  )
  assert (
    body_blocks[
      -1
    ]
    is arguments[
      argument_index
    ].conclusion_block
  )


def test_phase143_36_pi8_5_group_without_primary_keeps_exactness_blocks():
  (
    _presentation,
    _blocks,
    _sidecar,
    _arguments,
    _argument_index,
    _argument,
    primary_component,
    body_blocks,
  ) = _body_data(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
  )

  assert primary_component is None
  assert any(
    block.role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .EXACTNESS
    for block in body_blocks
  )


def test_phase143_36_pi8_5_detached_order_suppresses_only_selected_evidence():
  (
    _presentation,
    _blocks,
    _sidecar,
    _arguments,
    _argument_index,
    _argument,
    primary_component,
    body_blocks,
  ) = _body_data(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
    occurrence=1,
  )

  assert primary_component is not None
  evidence_ids = {
    id(
      block
    )
    for block in primary_component.evidence_blocks
  }

  assert all(
    id(
      block
    ) not in evidence_ids
    for block in body_blocks
  )


def test_phase143_36a_pi8_5_detached_order_keeps_conclusion_once_at_end():
  (
    _presentation,
    _blocks,
    _sidecar,
    _arguments,
    _argument_index,
    argument,
    _primary_component,
    body_blocks,
  ) = _body_data(
    5,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
    occurrence=1,
  )

  assert (
    body_blocks[
      -1
    ]
    is argument.conclusion_block
  )
  assert (
    sum(
      block is argument.conclusion_block
      for block in body_blocks
    )
    == 1
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
def test_phase143_36_four_targets_extract_body_blocks_safely(
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
    body_blocks = (
      extract_toda_group_proof_narrative_argument_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
        primary_component,
      )
    )

    assert body_blocks
    assert (
      body_blocks[
        -1
      ]
      is argument.conclusion_block
    )
    assert (
      sum(
        block is argument.conclusion_block
        for block in body_blocks
      )
      == 1
    )


def test_phase143_36_rejects_out_of_range_argument_index():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  with pytest.raises(
    ValueError,
    match="argument_index is out of range",
  ):
    extract_toda_group_proof_narrative_argument_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      len(
        arguments
      ),
      None,
    )


def test_phase143_36_rejects_non_component():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  with pytest.raises(
    TypeError,
    match=(
      "primary_component must be a "
      "TodaGroupProofNarrativeExactnessMethodComponent "
      "or None"
    ),
  ):
    extract_toda_group_proof_narrative_argument_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      0,
      object(),
    )
