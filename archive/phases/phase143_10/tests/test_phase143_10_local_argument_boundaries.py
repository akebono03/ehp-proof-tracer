from dataclasses import replace

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
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


def _argument_data(
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
  return blocks, arguments


def test_phase143_10_pi6_3_uses_local_supports():
  blocks, arguments = _argument_data(
    3,
    3,
  )

  assert arguments

  for argument in arguments:
    assert len(
      argument.supporting_blocks
    ) < len(
      blocks
    ) - 1


def test_phase143_10_definition_keeps_semantic_precondition_local():
  _, arguments = _argument_data(
    3,
    3,
  )

  definition_argument = next(
    argument
    for argument in arguments
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_DEFINITION
    )
  )

  assert definition_argument.supporting_blocks


def test_phase143_10_four_audit_targets_build_local_arguments():
  for n, k in (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ):
    blocks, arguments = _argument_data(
      n,
      k,
    )

    assert arguments

    for argument in arguments:
      assert len(
        argument.supporting_blocks
      ) <= len(
        blocks
      )


def test_phase143_10_child_argument_indices_are_valid():
  for n, k in (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ):
    _, arguments = _argument_data(
      n,
      k,
    )

    for argument in arguments:
      for child_index in argument.child_argument_indices:
        assert 0 <= child_index < len(
          arguments
        )


def test_phase143_10_child_argument_indices_reject_duplicates():
  _, arguments = _argument_data(
    3,
    3,
  )

  argument = arguments[
    0
  ]

  try:
    replace(
      argument,
      child_argument_indices=(
        0,
        0,
      ),
    )
  except ValueError:
    pass
  else:
    raise AssertionError(
      "duplicate child argument indices "
      "must be rejected"
    )
