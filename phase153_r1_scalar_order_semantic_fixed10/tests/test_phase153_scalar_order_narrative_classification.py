from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from tests.test_phase134_9_group_proof_narrative_classifier import (
  _presentation,
)
from toda_group_proof_narrative_classifier import (
  TodaGroupProofNarrativeBlockRole,
  classify_toda_group_proof_narrative_step,
)


def _presentation_with_scalar_statement():
  presentation = _presentation(
    3,
    3,
  )

  for node in presentation.nodes:
    if isinstance(
      node.proof_step.conclusion,
      ScalarGreaterEqualStatement,
    ):
      return presentation, node.proof_step

  raise AssertionError(
    "ScalarGreaterEqualStatement not found"
  )


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
