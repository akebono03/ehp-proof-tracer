from proof import (
  ProofStep,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  TodaGroupProofNarrativeArgumentRole,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)


def extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
  argument: TodaGroupProofNarrativeArgument,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> tuple[
  ProofStep,
  ...,
]:
  if not isinstance(
    argument,
    TodaGroupProofNarrativeArgument,
  ):
    raise TypeError(
      "argument must be a "
      "TodaGroupProofNarrativeArgument"
    )

  if not isinstance(
    arguments,
    tuple,
  ):
    raise TypeError(
      "arguments must be a tuple"
    )

  for candidate in arguments:
    if not isinstance(
      candidate,
      TodaGroupProofNarrativeArgument,
    ):
      raise TypeError(
        "arguments must contain only "
        "TodaGroupProofNarrativeArgument objects"
      )

  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )

  if conclusion_step is None:
    return ()

  definition_premise_step_ids = set()

  for child_argument_index in argument.child_argument_indices:
    if child_argument_index >= len(
      arguments
    ):
      raise ValueError(
        "child_argument_indices must refer to "
        "arguments"
      )

    child_argument = arguments[
      child_argument_index
    ]

    if (
      child_argument.role
      is not TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_DEFINITION
    ):
      continue

    child_conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        child_argument
      )
    )

    if child_conclusion_step is None:
      continue

    definition_premise_step_ids.add(
      id(
        child_conclusion_step
      )
    )

  return tuple(
    premise_step
    for premise_step in conclusion_step.premises
    if id(
      premise_step
    ) not in definition_premise_step_ids
  )
