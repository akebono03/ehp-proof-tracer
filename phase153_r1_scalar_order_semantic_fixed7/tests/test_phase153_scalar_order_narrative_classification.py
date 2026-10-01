from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_classifier import (
  TodaGroupProofNarrativeBlockRole,
  classify_toda_group_proof_narrative_step,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _presentation_with_scalar_statement():
  report = (
    build_standard_toda_report(
      n=3,
      k=3,
    )
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

  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  scalar_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      ScalarGreaterEqualStatement,
    )
  )

  if not scalar_steps:
    raise AssertionError(
      "ScalarGreaterEqualStatement not found"
    )

  return presentation, scalar_steps[0]


def test_phase153_scalar_greater_equal_statement_is_order_block():
  presentation, scalar_step = (
    _presentation_with_scalar_statement()
  )

  classification = (
    classify_toda_group_proof_narrative_step(
      presentation,
      scalar_step,
    )
  )

  assert (
    classification.block_role
    is TodaGroupProofNarrativeBlockRole.ORDER
  )
