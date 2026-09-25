from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)


def test_phase143_10_fix1_child_argument_indices_default_empty():
  block = TodaGroupProofNarrativeBlock(
    role=(
      TodaGroupProofNarrativeMathematicalBlockRole.TARGET
    ),
    steps=(),
  )

  argument = TodaGroupProofNarrativeArgument(
    role=(
      TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_GROUP_STRUCTURE
    ),
    supporting_blocks=(),
    conclusion_block=block,
  )

  assert argument.child_argument_indices == ()
