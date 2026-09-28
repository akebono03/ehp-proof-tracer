import pytest

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _method_evidence_data(
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
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=3,
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=sidecar,
    )
  )

  return (
    presentation,
    blocks,
    sidecar,
    arguments,
  )


def _method_evidence(
  n,
  k,
  role,
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

  argument_index = next(
    index
    for index, argument in enumerate(
      arguments
    )
    if argument.role is role
  )

  return (
    extract_toda_group_proof_narrative_argument_method_evidence(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )


def test_phase143_19_pi6_3_order_recovers_exactness_evidence():
  evidence = _method_evidence(
    3,
    3,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
  )

  assert evidence
  assert all(
    block.role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .EXACTNESS
    for block in evidence
  )


def test_phase143_19_pi6_3_method_evidence_is_not_direct_support_only():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  argument_index = next(
    index
    for index, argument in enumerate(
      arguments
    )
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_ORDER
    )
  )
  argument = arguments[
    argument_index
  ]

  assert all(
    block.role
    is not TodaGroupProofNarrativeMathematicalBlockRole
    .EXACTNESS
    for block in argument.supporting_blocks
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

  assert evidence


@pytest.mark.parametrize(
  "n,k",
  (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ),
)
def test_phase143_19_four_audit_targets_extract_safely(
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

  for argument_index in range(
    len(
      arguments
    )
  ):
    evidence = (
      extract_toda_group_proof_narrative_argument_method_evidence(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )

    assert isinstance(
      evidence,
      tuple,
    )
    assert all(
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
      for block in evidence
    )


def test_phase143_19_rejects_non_tuple_arguments():
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
    match="arguments must be a tuple",
  ):
    extract_toda_group_proof_narrative_argument_method_evidence(
      presentation,
      blocks,
      sidecar,
      list(
        arguments
      ),
      0,
    )


def test_phase143_19_rejects_out_of_range_argument_index():
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
    extract_toda_group_proof_narrative_argument_method_evidence(
      presentation,
      blocks,
      sidecar,
      arguments,
      len(
        arguments
      ),
    )
