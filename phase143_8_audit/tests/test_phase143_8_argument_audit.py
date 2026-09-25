from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
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


def test_phase143_8_audit_targets_are_constructible():
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

    assert blocks
    assert arguments


def test_phase143_8_arguments_never_include_their_conclusion_as_support():
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
      assert all(
        block is not argument.conclusion_block
        for block in argument.supporting_blocks
      )
