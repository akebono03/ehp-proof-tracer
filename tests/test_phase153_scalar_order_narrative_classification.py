from expression import (
  ScalarSymbol,
)
from proof import (
  ProofRule,
  ProofStep,
)
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


def _supported_presentation():
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

  return (
    build_toda_group_proof_presentation(
      replay
    )
  )


def test_phase153_scalar_greater_equal_statement_is_order_block():
  presentation = (
    _supported_presentation()
  )

  scalar_step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=ScalarSymbol(
        name="n",
      ),
      right=6,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
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
