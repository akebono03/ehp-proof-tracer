from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from homotopy_groups import (
  TodaPrimaryGroup,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)


def extract_toda_group_proof_narrative_argument_relevant_groups(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  argument: TodaGroupProofNarrativeArgument,
) -> tuple[
  TodaPrimaryGroup,
  ...,
]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    blocks,
    tuple,
  ):
    raise TypeError(
      "blocks must be a tuple"
    )

  selected_step_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }
  block_step_ids = set()

  for block in blocks:
    if not isinstance(
      block,
      TodaGroupProofNarrativeBlock,
    ):
      raise TypeError(
        "blocks must contain only "
        "TodaGroupProofNarrativeBlock objects"
      )

    for proof_step in block.steps:
      step_id = id(
        proof_step
      )

      if step_id not in selected_step_ids:
        raise ValueError(
          "block proof steps must appear "
          "in presentation nodes"
        )

      if step_id in block_step_ids:
        raise ValueError(
          "blocks must not contain duplicate "
          "ProofStep objects"
        )

      block_step_ids.add(
        step_id
      )

  if block_step_ids != selected_step_ids:
    raise ValueError(
      "blocks must cover presentation nodes "
      "exactly once"
    )

  if not isinstance(
    argument,
    TodaGroupProofNarrativeArgument,
  ):
    raise TypeError(
      "argument must be a "
      "TodaGroupProofNarrativeArgument"
    )

  block_ids = {
    id(
      block
    )
    for block in blocks
  }

  if id(
    argument.conclusion_block
  ) not in block_ids:
    raise ValueError(
      "argument conclusion_block must appear "
      "in blocks"
    )

  if any(
    id(
      block
    ) not in block_ids
    for block in argument.supporting_blocks
  ):
    raise ValueError(
      "argument supporting_blocks must appear "
      "in blocks"
    )

  subject = (
    extract_toda_group_proof_narrative_argument_purpose_subject(
      argument
    )
  )

  if subject is None:
    return ()

  if isinstance(
    subject,
    TodaPrimaryGroup,
  ):
    return (
      subject,
    )

  groups = []

  for block in blocks:
    for proof_step in block.steps:
      statement = proof_step.conclusion

      if not isinstance(
        statement,
        HomotopyGroupMembershipStatement,
      ):
        continue

      if statement.element != subject:
        continue

      group = TodaPrimaryGroup(
        group_dimension=statement.group_dimension,
        sphere_dimension=statement.sphere_dimension,
      )

      if group not in groups:
        groups.append(
          group
        )

  return tuple(
    groups
  )
