from homotopy_groups import (
  TodaEHPExactnessWindow,
  TodaEHPSequence,
  TodaPrimaryGroup,
)
from proof import ProofStep
from toda_ehp_result import (
  TodaEHPExactnessWindowResult,
  TodaEHPSequenceResult,
)
from toda_group_result import TodaGroupResult
from toda_rules import (
  TodaProp42ExactnessStatement,
)


def _window_contains_target(
  window: TodaEHPExactnessWindow,
  target: TodaPrimaryGroup,
) -> bool:
  return target in (
    window.source_term,
    window.middle_term,
    window.target_term,
  )


def _collect_relevant_toda_ehp_windows(
  proof_step: ProofStep,
  target: TodaPrimaryGroup,
) -> tuple[
  TodaEHPExactnessWindow,
  ...,
]:
  if not isinstance(
    proof_step,
    ProofStep,
  ):
    raise TypeError(
      "proof_step must be a ProofStep"
    )

  if not isinstance(
    target,
    TodaPrimaryGroup,
  ):
    raise TypeError(
      "target must be a TodaPrimaryGroup"
    )

  windows: list[
    TodaEHPExactnessWindow
  ] = []

  visited_step_ids: set[int] = set()

  def visit(
    step: ProofStep,
  ) -> None:
    step_id = id(
      step
    )

    if (
      step_id
      in visited_step_ids
    ):
      return

    visited_step_ids.add(
      step_id
    )

    conclusion = (
      step.conclusion
    )

    if isinstance(
      conclusion,
      TodaProp42ExactnessStatement,
    ):
      window = (
        conclusion.window
      )

      if (
        _window_contains_target(
          window,
          target,
        )
        and not any(
          existing
          == window
          for existing in windows
        )
      ):
        windows.append(
          window
        )

    for premise in (
      step.premises
    ):
      if isinstance(
        premise,
        ProofStep,
      ):
        visit(
          premise
        )

  visit(
    proof_step
  )

  return tuple(
    windows
  )


def _order_contiguous_toda_ehp_windows(
  windows: tuple[
    TodaEHPExactnessWindow,
    ...,
  ],
) -> tuple[
  TodaEHPExactnessWindow,
  ...,
]:
  if not isinstance(
    windows,
    tuple,
  ):
    raise TypeError(
      "windows must be a tuple"
    )

  if not windows:
    return ()

  for window in windows:
    if not isinstance(
      window,
      TodaEHPExactnessWindow,
    ):
      raise TypeError(
        "windows must contain only "
        "TodaEHPExactnessWindow objects"
      )

  if len(
    windows
  ) == 1:
    return windows

  def precedes(
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

  starts = tuple(
    window
    for window in windows
    if not any(
      other
      != window
      and precedes(
        other,
        window,
      )
      for other in windows
    )
  )

  if len(
    starts
  ) != 1:
    raise ValueError(
      "relevant EHP windows must form "
      "one contiguous chain"
    )

  ordered = [
    starts[
      0
    ]
  ]

  while (
    len(
      ordered
    )
    < len(
      windows
    )
  ):
    current = (
      ordered[
        -1
      ]
    )

    followers = tuple(
      window
      for window in windows
      if (
        window
        not in ordered
        and precedes(
          current,
          window,
        )
      )
    )

    if len(
      followers
    ) != 1:
      raise ValueError(
        "relevant EHP windows must form "
        "one contiguous chain"
      )

    ordered.append(
      followers[
        0
      ]
    )

  return tuple(
    ordered
  )


def _build_toda_ehp_sequence(
  windows: tuple[
    TodaEHPExactnessWindow,
    ...,
  ],
) -> TodaEHPSequence:
  if not windows:
    raise ValueError(
      "at least one EHP window is required"
    )

  first = windows[
    0
  ]

  terms = [
    first.source_term,
    first.middle_term,
    first.target_term,
  ]

  maps = [
    first.first_map,
    first.second_map,
  ]

  for window in (
    windows[
      1:
    ]
  ):
    if (
      terms[
        -2
      ]
      != window.source_term
      or terms[
        -1
      ]
      != window.middle_term
      or maps[
        -1
      ]
      != window.first_map
    ):
      raise ValueError(
        "windows are not contiguous"
      )

    terms.append(
      window.target_term
    )

    maps.append(
      window.second_map
    )

  return TodaEHPSequence(
    terms=tuple(
      terms
    ),
    maps=tuple(
      maps
    ),
  )


def extract_toda_ehp_sequence_result(
  group_result: TodaGroupResult,
) -> TodaEHPSequenceResult | None:
  if not isinstance(
    group_result,
    TodaGroupResult,
  ):
    raise TypeError(
      "group_result must be "
      "a TodaGroupResult"
    )

  windows = (
    _collect_relevant_toda_ehp_windows(
      group_result.proof_step,
      group_result.target,
    )
  )

  if not windows:
    return None

  ordered_windows = (
    _order_contiguous_toda_ehp_windows(
      windows
    )
  )

  sequence = (
    _build_toda_ehp_sequence(
      ordered_windows
    )
  )

  return TodaEHPSequenceResult(
    target=group_result.target,
    sequence=sequence,
    windows=tuple(
      TodaEHPExactnessWindowResult(
        window=window,
      )
      for window in ordered_windows
    ),
  )
