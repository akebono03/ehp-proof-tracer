import pytest

from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _local_body_data(
  n,
  k,
):
  return _method_evidence_data(
    n,
    k,
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
def test_phase143_41_four_targets_keep_conclusion_once_and_last(
  n,
  k,
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _local_body_data(
    n,
    k,
  )

  for argument_index, argument in enumerate(
    arguments
  ):
    body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )

    assert body_blocks
    assert body_blocks[
      -1
    ] is argument.conclusion_block
    assert sum(
      block is argument.conclusion_block
      for block in body_blocks
    ) == 1


@pytest.mark.parametrize(
  "n,k",
  (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ),
)
def test_phase143_41_four_targets_stop_at_other_argument_conclusions(
  n,
  k,
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _local_body_data(
    n,
    k,
  )

  for argument_index, argument in enumerate(
    arguments
  ):
    body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )

    other_conclusions = tuple(
      other_argument.conclusion_block
      for other_index, other_argument in enumerate(
        arguments
      )
      if other_index != argument_index
    )

    assert all(
      all(
        block is not conclusion_block
        for conclusion_block in other_conclusions
      )
      for block in body_blocks
    )


def test_phase143_41_pi6_3_group_keeps_primary_exactness_blocks_in_local_body():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _local_body_data(
    3,
    3,
  )

  argument_index = next(
    index
    for index, argument in enumerate(
      arguments
    )
    if argument.role.value
    == "establish_group_structure"
  )

  body_blocks = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )

  exactness_blocks = tuple(
    block
    for block in body_blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    )
  )

  assert len(
    exactness_blocks
  ) == 3


def test_phase143_41_pi6_3_order_keeps_exactness_blocks_for_later_ownership():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _local_body_data(
    3,
    3,
  )

  argument_index = next(
    index
    for index, argument in enumerate(
      arguments
    )
    if argument.role.value
    == "establish_order"
  )

  body_blocks = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )

  assert any(
    block.role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .EXACTNESS
    for block in body_blocks
  )


def test_phase143_41_rejects_non_tuple_arguments():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _local_body_data(
    3,
    3,
  )

  with pytest.raises(
    TypeError,
    match="arguments must be a tuple",
  ):
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      list(
        arguments
      ),
      0,
    )


def test_phase143_41_rejects_boolean_argument_index():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _local_body_data(
    3,
    3,
  )

  with pytest.raises(
    TypeError,
    match="argument_index must be an integer",
  ):
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      True,
    )


def test_phase143_41_rejects_out_of_range_argument_index():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _local_body_data(
    3,
    3,
  )

  with pytest.raises(
    ValueError,
    match="argument_index is out of range",
  ):
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      len(
        arguments
      ),
    )
