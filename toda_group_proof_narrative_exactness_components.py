from dataclasses import dataclass

from homotopy_groups import (
  TodaEHPExactnessWindow,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
)


@dataclass(frozen=True)
class TodaGroupProofNarrativeExactnessMethodComponent:
  windows: tuple[
    TodaEHPExactnessWindow,
    ...,
  ]
  evidence_blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.windows,
      tuple,
    ):
      raise TypeError(
        "windows must be a tuple"
      )

    if not self.windows:
      raise ValueError(
        "windows must not be empty"
      )

    for window in self.windows:
      if not isinstance(
        window,
        TodaEHPExactnessWindow,
      ):
        raise TypeError(
          "windows must contain only "
          "TodaEHPExactnessWindow objects"
        )

    if not isinstance(
      self.evidence_blocks,
      tuple,
    ):
      raise TypeError(
        "evidence_blocks must be a tuple"
      )

    if not self.evidence_blocks:
      raise ValueError(
        "evidence_blocks must not be empty"
      )

    for block in self.evidence_blocks:
      if not isinstance(
        block,
        TodaGroupProofNarrativeBlock,
      ):
        raise TypeError(
          "evidence_blocks must contain only "
          "TodaGroupProofNarrativeBlock objects"
        )

      if (
        block.role
        is not TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      ):
        raise ValueError(
          "evidence_blocks must be EXACTNESS blocks"
        )


def _exactness_windows_for_evidence_block(
  block: TodaGroupProofNarrativeBlock,
) -> tuple[
  TodaEHPExactnessWindow,
  ...,
]:
  if not isinstance(
    block,
    TodaGroupProofNarrativeBlock,
  ):
    raise TypeError(
      "block must be a "
      "TodaGroupProofNarrativeBlock"
    )

  if (
    block.role
    is not TodaGroupProofNarrativeMathematicalBlockRole
    .EXACTNESS
  ):
    raise ValueError(
      "block must be an EXACTNESS block"
    )

  windows = []

  for proof_step in block.steps:
    statement = proof_step.conclusion

    if not isinstance(
      statement,
      TodaProp42ExactnessStatement,
    ):
      continue

    if statement.window not in windows:
      windows.append(
        statement.window
      )

  return tuple(
    windows
  )


def _windows_overlap_forward(
  left: TodaEHPExactnessWindow,
  right: TodaEHPExactnessWindow,
) -> bool:
  return (
    left.middle_term
    == right.source_term
    and left.target_term
    == right.middle_term
    and left.second_map
    == right.first_map
  )


def _windows_are_adjacent(
  left: TodaEHPExactnessWindow,
  right: TodaEHPExactnessWindow,
) -> bool:
  return (
    _windows_overlap_forward(
      left,
      right,
    )
    or _windows_overlap_forward(
      right,
      left,
    )
  )


def _ordered_component_windows(
  windows: tuple[
    TodaEHPExactnessWindow,
    ...,
  ],
) -> tuple[
  TodaEHPExactnessWindow,
  ...,
]:
  if len(
    windows
  ) <= 1:
    return windows

  predecessors = {
    window: tuple(
      candidate
      for candidate in windows
      if (
        candidate != window
        and _windows_overlap_forward(
          candidate,
          window,
        )
      )
    )
    for window in windows
  }

  starts = tuple(
    window
    for window in windows
    if not predecessors[
      window
    ]
  )

  if len(
    starts
  ) != 1:
    return windows

  ordered = []
  current = starts[
    0
  ]

  while current not in ordered:
    ordered.append(
      current
    )

    successors = tuple(
      candidate
      for candidate in windows
      if (
        candidate not in ordered
        and _windows_overlap_forward(
          current,
          candidate,
        )
      )
    )

    if len(
      successors
    ) != 1:
      break

    current = successors[
      0
    ]

  if len(
    ordered
  ) != len(
    windows
  ):
    return windows

  return tuple(
    ordered
  )


def build_toda_group_proof_narrative_exactness_method_components(
  evidence_blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
) -> tuple[
  TodaGroupProofNarrativeExactnessMethodComponent,
  ...,
]:
  if not isinstance(
    evidence_blocks,
    tuple,
  ):
    raise TypeError(
      "evidence_blocks must be a tuple"
    )

  for block in evidence_blocks:
    if not isinstance(
      block,
      TodaGroupProofNarrativeBlock,
    ):
      raise TypeError(
        "evidence_blocks must contain only "
        "TodaGroupProofNarrativeBlock objects"
      )

    if (
      block.role
      is not TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    ):
      raise ValueError(
        "evidence_blocks must be EXACTNESS blocks"
      )

  window_records = []

  for block in evidence_blocks:
    for window in (
      _exactness_windows_for_evidence_block(
        block
      )
    ):
      existing_index = next(
        (
          index
          for index, (
            existing_window,
            _,
          ) in enumerate(
            window_records
          )
          if existing_window == window
        ),
        None,
      )

      if existing_index is None:
        window_records.append(
          (
            window,
            [
              block
            ],
          )
        )
        continue

      existing_window, blocks = (
        window_records[
          existing_index
        ]
      )

      if block not in blocks:
        blocks.append(
          block
        )

      window_records[
        existing_index
      ] = (
        existing_window,
        blocks,
      )

  if not window_records:
    return ()

  neighbors = [
    set()
    for _ in window_records
  ]

  for left_index in range(
    len(
      window_records
    )
  ):
    for right_index in range(
      left_index + 1,
      len(
        window_records
      ),
    ):
      if not _windows_are_adjacent(
        window_records[
          left_index
        ][
          0
        ],
        window_records[
          right_index
        ][
          0
        ],
      ):
        continue

      neighbors[
        left_index
      ].add(
        right_index
      )
      neighbors[
        right_index
      ].add(
        left_index
      )

  components = []
  visited = set()

  for start_index in range(
    len(
      window_records
    )
  ):
    if start_index in visited:
      continue

    pending = [
      start_index
    ]
    component_indices = []

    while pending:
      current_index = pending.pop()

      if current_index in visited:
        continue

      visited.add(
        current_index
      )
      component_indices.append(
        current_index
      )
      pending.extend(
        neighbor_index
        for neighbor_index in neighbors[
          current_index
        ]
        if neighbor_index not in visited
      )

    component_indices.sort()

    component_windows = tuple(
      window_records[
        index
      ][
        0
      ]
      for index in component_indices
    )

    evidence = []

    for index in component_indices:
      for block in window_records[
        index
      ][
        1
      ]:
        if block not in evidence:
          evidence.append(
            block
          )

    components.append(
      TodaGroupProofNarrativeExactnessMethodComponent(
        windows=_ordered_component_windows(
          component_windows
        ),
        evidence_blocks=tuple(
          evidence
        ),
      )
    )

  return tuple(
    components
  )
