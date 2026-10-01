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
  for n, k in (
    (3, 3),
    (5, 3),
  ):
    presentation = _presentation(
      n,
      k,
    )

    for node in presentation.nodes:
      if isinstance(
        node.proof_step.conclusion,
        ScalarGreaterEqualStatement,
      ):
        return presentation, node.proof_step

  raise AssertionError(
    "ScalarGreaterEqualStatement not found "
    "in supported Phase 134-9 presentations"
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
