import pytest

from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)

from test_phase143_12_purpose_subject import (
  _arguments,
)


def _source_indices(
  source,
  ordered,
):
  index_by_identity = {
    id(
      argument
    ): index
    for index, argument in enumerate(
      source
    )
  }

  return tuple(
    index_by_identity[
      id(
        argument
      )
    ]
    for argument in ordered
  )


def test_phase143_15_pi6_3_discourse_order():
  source = _arguments(
    3,
    3,
  )
  ordered = order_toda_group_proof_narrative_arguments(
    source
  )

  assert _source_indices(
    source,
    ordered,
  ) == (
    2,
    1,
    0,
  )


def test_phase143_15_pi8_5_root_chain_precedes_detached_order():
  source = _arguments(
    5,
    3,
  )
  ordered = order_toda_group_proof_narrative_arguments(
    source
  )

  assert _source_indices(
    source,
    ordered,
  ) == (
    2,
    1,
    0,
    3,
  )


def test_phase143_15_pi15_8_single_argument_is_unchanged():
  source = _arguments(
    8,
    7,
  )

  assert (
    order_toda_group_proof_narrative_arguments(
      source
    )
    == source
  )


def test_phase143_15_pi16_9_definition_precedes_group_structure():
  source = _arguments(
    9,
    7,
  )
  ordered = order_toda_group_proof_narrative_arguments(
    source
  )

  assert _source_indices(
    source,
    ordered,
  ) == (
    1,
    0,
  )


def test_phase143_15_rejects_non_tuple_arguments():
  with pytest.raises(
    TypeError,
    match="arguments must be a tuple",
  ):
    order_toda_group_proof_narrative_arguments(
      []
    )
