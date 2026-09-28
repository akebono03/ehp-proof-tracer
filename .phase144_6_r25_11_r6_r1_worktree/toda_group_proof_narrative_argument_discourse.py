from enum import Enum

from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)


class TodaGroupProofNarrativeArgumentDiscourseRole(
  Enum
):
  SINGLE = "single"
  FIRST = "first"
  MIDDLE = "middle"
  FINAL = "final"
  DETACHED = "detached"


def _toda_group_proof_narrative_root_argument_indices(
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> tuple[
  int,
  ...,
]:
  return tuple(
    index
    for index, argument in enumerate(
      arguments
    )
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_GROUP_STRUCTURE
      and argument.conclusion_block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .TARGET
    )
  )


def _toda_group_proof_narrative_root_reachable_indices(
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> frozenset[
  int
]:
  reachable = set()

  def visit(
    argument_index: int,
  ) -> None:
    if argument_index in reachable:
      return

    reachable.add(
      argument_index
    )

    for child_index in arguments[
      argument_index
    ].child_argument_indices:
      visit(
        child_index
      )

  for root_index in (
    _toda_group_proof_narrative_root_argument_indices(
      arguments
    )
  ):
    visit(
      root_index
    )

  return frozenset(
    reachable
  )


def classify_toda_group_proof_narrative_argument_discourse_roles(
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> tuple[
  TodaGroupProofNarrativeArgumentDiscourseRole,
  ...,
]:
  ordered = (
    order_toda_group_proof_narrative_arguments(
      arguments
    )
  )

  if not ordered:
    return ()

  source_index_by_identity = {
    id(
      argument
    ): index
    for index, argument in enumerate(
      arguments
    )
  }

  root_reachable = (
    _toda_group_proof_narrative_root_reachable_indices(
      arguments
    )
  )

  main_indices = {
    index
    for index, argument in enumerate(
      arguments
    )
    if (
      index in root_reachable
      or (
        index not in root_reachable
        and argument.role
        is TodaGroupProofNarrativeArgumentRole
        .ESTABLISH_DEFINITION
      )
    )
  }

  ordered_main_positions = tuple(
    position
    for position, argument in enumerate(
      ordered
    )
    if source_index_by_identity[
      id(
        argument
      )
    ] in main_indices
  )

  if len(
    ordered_main_positions
  ) == 1:
    single_position = ordered_main_positions[
      0
    ]
    return tuple(
      (
        TodaGroupProofNarrativeArgumentDiscourseRole
        .SINGLE
        if position == single_position
        else TodaGroupProofNarrativeArgumentDiscourseRole
        .DETACHED
      )
      for position in range(
        len(
          ordered
        )
      )
    )

  if not ordered_main_positions:
    return tuple(
      TodaGroupProofNarrativeArgumentDiscourseRole
      .DETACHED
      for _ in ordered
    )

  first_position = ordered_main_positions[
    0
  ]
  final_position = ordered_main_positions[
    -1
  ]

  roles = []

  for position, argument in enumerate(
    ordered
  ):
    source_index = source_index_by_identity[
      id(
        argument
      )
    ]

    if source_index not in main_indices:
      roles.append(
        TodaGroupProofNarrativeArgumentDiscourseRole
        .DETACHED
      )
      continue

    if position == first_position:
      roles.append(
        TodaGroupProofNarrativeArgumentDiscourseRole
        .FIRST
      )
      continue

    if position == final_position:
      roles.append(
        TodaGroupProofNarrativeArgumentDiscourseRole
        .FINAL
      )
      continue

    roles.append(
      TodaGroupProofNarrativeArgumentDiscourseRole
      .MIDDLE
    )

  return tuple(
    roles
  )


def render_toda_group_proof_narrative_argument_discourse_marker(
  role: TodaGroupProofNarrativeArgumentDiscourseRole,
) -> str:
  if not isinstance(
    role,
    TodaGroupProofNarrativeArgumentDiscourseRole,
  ):
    raise TypeError(
      "role must be a "
      "TodaGroupProofNarrativeArgumentDiscourseRole"
    )

  if (
    role
    is TodaGroupProofNarrativeArgumentDiscourseRole
    .FIRST
  ):
    return "まず、"

  if (
    role
    is TodaGroupProofNarrativeArgumentDiscourseRole
    .MIDDLE
  ):
    return "次に、"

  if (
    role
    is TodaGroupProofNarrativeArgumentDiscourseRole
    .FINAL
  ):
    return "最後に、"

  return ""
