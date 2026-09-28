from dataclasses import dataclass

from homotopy_groups import (
  TodaEHPExactnessWindow,
  TodaEHPSequence,
  TodaPrimaryGroup,
)


@dataclass(frozen=True)
class TodaEHPExactnessWindowResult:
  window: TodaEHPExactnessWindow

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.window,
      TodaEHPExactnessWindow,
    ):
      raise TypeError(
        "window must be "
        "a TodaEHPExactnessWindow"
      )


@dataclass(frozen=True)
class TodaEHPSequenceResult:
  target: TodaPrimaryGroup
  sequence: TodaEHPSequence
  windows: tuple[
    TodaEHPExactnessWindowResult,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.target,
      TodaPrimaryGroup,
    ):
      raise TypeError(
        "target must be "
        "a TodaPrimaryGroup"
      )

    if not isinstance(
      self.sequence,
      TodaEHPSequence,
    ):
      raise TypeError(
        "sequence must be "
        "a TodaEHPSequence"
      )

    if not isinstance(
      self.windows,
      tuple,
    ):
      raise TypeError(
        "windows must be a tuple"
      )

    for window_result in self.windows:
      if not isinstance(
        window_result,
        TodaEHPExactnessWindowResult,
      ):
        raise TypeError(
          "windows must contain only "
          "TodaEHPExactnessWindowResult "
          "objects"
        )

    if (
      self.target
      not in self.sequence.terms
    ):
      raise ValueError(
        "target must occur in "
        "sequence.terms"
      )

    for window_result in self.windows:
      window = window_result.window

      matches_sequence = any(
        (
          self.sequence.terms[
            index
          ]
          == window.source_term
          and self.sequence.terms[
            index + 1
          ]
          == window.middle_term
          and self.sequence.terms[
            index + 2
          ]
          == window.target_term
          and self.sequence.maps[
            index
          ]
          == window.first_map
          and self.sequence.maps[
            index + 1
          ]
          == window.second_map
        )
        for index in range(
          len(
            self.sequence.terms
          )
          - 2
        )
      )

      if not matches_sequence:
        raise ValueError(
          "each window must be "
          "a contiguous window of sequence"
        )
