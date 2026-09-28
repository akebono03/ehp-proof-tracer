from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)


_ROLE_PRIORITY = {
  TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION: 0,
  TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER: 1,
  TodaGroupProofNarrativeArgumentRole.ESTABLISH_GROUP_STRUCTURE: 2,
}


def _validate_toda_group_proof_narrative_arguments_for_discourse_order(
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> None:
  if not isinstance(
    arguments,
    tuple,
  ):
    raise TypeError(
      "arguments must be a tuple"
    )

  for argument in arguments:
    if not isinstance(
      argument,
      TodaGroupProofNarrativeArgument,
    ):
      raise TypeError(
        "arguments must contain only "
        "TodaGroupProofNarrativeArgument objects"
      )

    for child_index in argument.child_argument_indices:
      if child_index >= len(
        arguments
      ):
        raise ValueError(
          "child argument index is out of range"
        )


def _toda_group_proof_narrative_argument_discourse_key(
  argument_index: int,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> tuple[
  int,
  int,
]:
  argument = arguments[
    argument_index
  ]

  return (
    _ROLE_PRIORITY[
      argument.role
    ],
    argument_index,
  )


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


def order_toda_group_proof_narrative_arguments(
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> tuple[
  TodaGroupProofNarrativeArgument,
  ...,
]:
  _validate_toda_group_proof_narrative_arguments_for_discourse_order(
    arguments
  )

  ordered_indices = []
  visited = set()
  visiting = set()

  def visit(
    argument_index: int,
  ) -> None:
    if argument_index in visited:
      return

    if argument_index in visiting:
      raise ValueError(
        "NarrativeArgument child dependency cycle"
      )

    visiting.add(
      argument_index
    )

    argument = arguments[
      argument_index
    ]

    child_indices = tuple(
      sorted(
        argument.child_argument_indices,
        key=lambda child_index: (
          _toda_group_proof_narrative_argument_discourse_key(
            child_index,
            arguments,
          )
        ),
      )
    )

    for child_index in child_indices:
      visit(
        child_index
      )

    visiting.remove(
      argument_index
    )
    visited.add(
      argument_index
    )
    ordered_indices.append(
      argument_index
    )

  root_indices = tuple(
    sorted(
      _toda_group_proof_narrative_root_argument_indices(
        arguments
      ),
      key=lambda argument_index: (
        _toda_group_proof_narrative_argument_discourse_key(
          argument_index,
          arguments,
        )
      ),
    )
  )

  root_reachable = set()

  def collect_root_reachable(
    argument_index: int,
  ) -> None:
    if argument_index in root_reachable:
      return

    root_reachable.add(
      argument_index
    )

    for child_index in arguments[
      argument_index
    ].child_argument_indices:
      collect_root_reachable(
        child_index
      )

  for root_index in root_indices:
    collect_root_reachable(
      root_index
    )

  detached_definition_indices = tuple(
    index
    for index, argument in enumerate(
      arguments
    )
    if (
      index not in root_reachable
      and argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_DEFINITION
    )
  )

  for argument_index in detached_definition_indices:
    visit(
      argument_index
    )

  for root_index in root_indices:
    visit(
      root_index
    )

  remaining_indices = tuple(
    sorted(
      (
        index
        for index in range(
          len(
            arguments
          )
        )
        if index not in visited
      ),
      key=lambda argument_index: (
        _toda_group_proof_narrative_argument_discourse_key(
          argument_index,
          arguments,
        )
      ),
    )
  )

  for remaining_index in remaining_indices:
    visit(
      remaining_index
    )

  return tuple(
    arguments[
      index
    ]
    for index in ordered_indices
  )
