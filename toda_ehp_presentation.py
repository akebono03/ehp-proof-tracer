from dataclasses import dataclass

from expression import MapSymbol
from proof import ProofStep
from toda_ehp_exactness_provenance import (
  TodaEHPExactnessUseProvenanceResult,
  TodaEHPExactnessUseResult,
)
from toda_ehp_result import (
  TodaEHPExactnessWindowResult,
  TodaEHPSequenceResult,
)
from toda_presentation import (
  TodaTargetPresentation,
  build_toda_target_presentation,
)


@dataclass(frozen=True)
class TodaEHPMapPresentation:
  source_map: MapSymbol

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_map,
      MapSymbol,
    ):
      raise TypeError(
        "source_map must be a MapSymbol"
      )

  @property
  def name(
    self,
  ) -> str:
    return self.source_map.name


@dataclass(frozen=True)
class TodaEHPExactnessWindowPresentation:
  source_window_result: TodaEHPExactnessWindowResult
  source_term: TodaTargetPresentation
  middle_term: TodaTargetPresentation
  target_term: TodaTargetPresentation
  first_map: TodaEHPMapPresentation
  second_map: TodaEHPMapPresentation

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_window_result,
      TodaEHPExactnessWindowResult,
    ):
      raise TypeError(
        "source_window_result must be "
        "a TodaEHPExactnessWindowResult"
      )

    for term in (
      self.source_term,
      self.middle_term,
      self.target_term,
    ):
      if not isinstance(
        term,
        TodaTargetPresentation,
      ):
        raise TypeError(
          "window terms must be "
          "TodaTargetPresentation objects"
        )

    for map_presentation in (
      self.first_map,
      self.second_map,
    ):
      if not isinstance(
        map_presentation,
        TodaEHPMapPresentation,
      ):
        raise TypeError(
          "window maps must be "
          "TodaEHPMapPresentation objects"
        )

    window = (
      self.source_window_result
      .window
    )

    if (
      self.source_term.source_target
      is not window.source_term
    ):
      raise ValueError(
        "source_term identity must match "
        "source window"
      )

    if (
      self.middle_term.source_target
      is not window.middle_term
    ):
      raise ValueError(
        "middle_term identity must match "
        "source window"
      )

    if (
      self.target_term.source_target
      is not window.target_term
    ):
      raise ValueError(
        "target_term identity must match "
        "source window"
      )

    if (
      self.first_map.source_map
      is not window.first_map
    ):
      raise ValueError(
        "first_map identity must match "
        "source window"
      )

    if (
      self.second_map.source_map
      is not window.second_map
    ):
      raise ValueError(
        "second_map identity must match "
        "source window"
      )


@dataclass(frozen=True)
class TodaEHPSequencePresentation:
  source_result: TodaEHPSequenceResult
  target: TodaTargetPresentation
  terms: tuple[
    TodaTargetPresentation,
    ...,
  ]
  maps: tuple[
    TodaEHPMapPresentation,
    ...,
  ]
  windows: tuple[
    TodaEHPExactnessWindowPresentation,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_result,
      TodaEHPSequenceResult,
    ):
      raise TypeError(
        "source_result must be "
        "a TodaEHPSequenceResult"
      )

    if not isinstance(
      self.target,
      TodaTargetPresentation,
    ):
      raise TypeError(
        "target must be a "
        "TodaTargetPresentation"
      )

    if (
      self.target.source_target
      is not self.source_result.target
    ):
      raise ValueError(
        "target identity must match "
        "source_result.target"
      )

    if not isinstance(
      self.terms,
      tuple,
    ):
      raise TypeError(
        "terms must be a tuple"
      )

    if not isinstance(
      self.maps,
      tuple,
    ):
      raise TypeError(
        "maps must be a tuple"
      )

    if not isinstance(
      self.windows,
      tuple,
    ):
      raise TypeError(
        "windows must be a tuple"
      )

    if (
      len(self.terms)
      != len(
        self.source_result
        .sequence
        .terms
      )
    ):
      raise ValueError(
        "terms must match source sequence"
      )

    if (
      len(self.maps)
      != len(
        self.source_result
        .sequence
        .maps
      )
    ):
      raise ValueError(
        "maps must match source sequence"
      )

    if (
      len(self.windows)
      != len(
        self.source_result.windows
      )
    ):
      raise ValueError(
        "windows must match source_result "
        "windows"
      )

    for (
      presented_term,
      source_term,
    ) in zip(
      self.terms,
      self.source_result.sequence.terms,
    ):
      if not isinstance(
        presented_term,
        TodaTargetPresentation,
      ):
        raise TypeError(
          "terms must contain only "
          "TodaTargetPresentation objects"
        )

      if (
        presented_term.source_target
        is not source_term
      ):
        raise ValueError(
          "term identity must match "
          "source sequence in order"
        )

    for (
      presented_map,
      source_map,
    ) in zip(
      self.maps,
      self.source_result.sequence.maps,
    ):
      if not isinstance(
        presented_map,
        TodaEHPMapPresentation,
      ):
        raise TypeError(
          "maps must contain only "
          "TodaEHPMapPresentation objects"
        )

      if (
        presented_map.source_map
        is not source_map
      ):
        raise ValueError(
          "map identity must match "
          "source sequence in order"
        )

    for (
      presented_window,
      source_window_result,
    ) in zip(
      self.windows,
      self.source_result.windows,
    ):
      if not isinstance(
        presented_window,
        TodaEHPExactnessWindowPresentation,
      ):
        raise TypeError(
          "windows must contain only "
          "TodaEHPExactnessWindowPresentation "
          "objects"
        )

      if (
        presented_window
        .source_window_result
        is not source_window_result
      ):
        raise ValueError(
          "window identity must match "
          "source_result in order"
        )


@dataclass(frozen=True)
class TodaEHPExactnessUsePresentation:
  source_use: TodaEHPExactnessUseResult
  window: TodaEHPExactnessWindowPresentation
  exactness_step: ProofStep
  consumer_steps: tuple[
    ProofStep,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_use,
      TodaEHPExactnessUseResult,
    ):
      raise TypeError(
        "source_use must be "
        "a TodaEHPExactnessUseResult"
      )

    if not isinstance(
      self.window,
      TodaEHPExactnessWindowPresentation,
    ):
      raise TypeError(
        "window must be a "
        "TodaEHPExactnessWindowPresentation"
      )

    if (
      self.window.source_window_result
      is not self.source_use.window_result
    ):
      raise ValueError(
        "window source identity must match "
        "source_use.window_result"
      )

    if not isinstance(
      self.exactness_step,
      ProofStep,
    ):
      raise TypeError(
        "exactness_step must be a ProofStep"
      )

    if (
      self.exactness_step
      is not self.source_use.exactness_step
    ):
      raise ValueError(
        "exactness_step identity must match "
        "source_use"
      )

    if not isinstance(
      self.consumer_steps,
      tuple,
    ):
      raise TypeError(
        "consumer_steps must be a tuple"
      )

    if (
      len(self.consumer_steps)
      != len(
        self.source_use.consumer_steps
      )
    ):
      raise ValueError(
        "consumer_steps must match "
        "source_use.consumer_steps"
      )

    for (
      presented_consumer,
      source_consumer,
    ) in zip(
      self.consumer_steps,
      self.source_use.consumer_steps,
    ):
      if not isinstance(
        presented_consumer,
        ProofStep,
      ):
        raise TypeError(
          "consumer_steps must contain "
          "only ProofStep objects"
        )

      if (
        presented_consumer
        is not source_consumer
      ):
        raise ValueError(
          "consumer step identity must match "
          "source_use in order"
        )


@dataclass(frozen=True)
class TodaEHPExactnessPresentation:
  source_provenance: TodaEHPExactnessUseProvenanceResult
  sequence: TodaEHPSequencePresentation
  uses: tuple[
    TodaEHPExactnessUsePresentation,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_provenance,
      TodaEHPExactnessUseProvenanceResult,
    ):
      raise TypeError(
        "source_provenance must be "
        "a TodaEHPExactnessUseProvenanceResult"
      )

    if not isinstance(
      self.sequence,
      TodaEHPSequencePresentation,
    ):
      raise TypeError(
        "sequence must be a "
        "TodaEHPSequencePresentation"
      )

    if (
      self.sequence.source_result
      is not self.source_provenance.ehp_result
    ):
      raise ValueError(
        "sequence source identity must match "
        "source_provenance.ehp_result"
      )

    if not isinstance(
      self.uses,
      tuple,
    ):
      raise TypeError(
        "uses must be a tuple"
      )

    if (
      len(self.uses)
      != len(
        self.source_provenance.uses
      )
    ):
      raise ValueError(
        "uses must match source_provenance"
      )

    for (
      presented_use,
      source_use,
    ) in zip(
      self.uses,
      self.source_provenance.uses,
    ):
      if not isinstance(
        presented_use,
        TodaEHPExactnessUsePresentation,
      ):
        raise TypeError(
          "uses must contain only "
          "TodaEHPExactnessUsePresentation "
          "objects"
        )

      if (
        presented_use.source_use
        is not source_use
      ):
        raise ValueError(
          "use identity must match "
          "source_provenance in order"
        )


def build_toda_ehp_map_presentation(
  map_symbol: MapSymbol,
) -> TodaEHPMapPresentation:
  if not isinstance(
    map_symbol,
    MapSymbol,
  ):
    raise TypeError(
      "map_symbol must be a MapSymbol"
    )

  return TodaEHPMapPresentation(
    source_map=map_symbol,
  )


def build_toda_ehp_exactness_window_presentation(
  window_result: TodaEHPExactnessWindowResult,
) -> TodaEHPExactnessWindowPresentation:
  if not isinstance(
    window_result,
    TodaEHPExactnessWindowResult,
  ):
    raise TypeError(
      "window_result must be "
      "a TodaEHPExactnessWindowResult"
    )

  window = window_result.window

  return TodaEHPExactnessWindowPresentation(
    source_window_result=window_result,
    source_term=(
      build_toda_target_presentation(
        window.source_term
      )
    ),
    middle_term=(
      build_toda_target_presentation(
        window.middle_term
      )
    ),
    target_term=(
      build_toda_target_presentation(
        window.target_term
      )
    ),
    first_map=(
      build_toda_ehp_map_presentation(
        window.first_map
      )
    ),
    second_map=(
      build_toda_ehp_map_presentation(
        window.second_map
      )
    ),
  )


def build_toda_ehp_sequence_presentation(
  ehp_result: TodaEHPSequenceResult,
) -> TodaEHPSequencePresentation:
  if not isinstance(
    ehp_result,
    TodaEHPSequenceResult,
  ):
    raise TypeError(
      "ehp_result must be "
      "a TodaEHPSequenceResult"
    )

  return TodaEHPSequencePresentation(
    source_result=ehp_result,
    target=(
      build_toda_target_presentation(
        ehp_result.target
      )
    ),
    terms=tuple(
      build_toda_target_presentation(
        term
      )
      for term in (
        ehp_result.sequence.terms
      )
    ),
    maps=tuple(
      build_toda_ehp_map_presentation(
        map_symbol
      )
      for map_symbol in (
        ehp_result.sequence.maps
      )
    ),
    windows=tuple(
      build_toda_ehp_exactness_window_presentation(
        window_result
      )
      for window_result in (
        ehp_result.windows
      )
    ),
  )


def build_toda_ehp_exactness_use_presentation(
  use: TodaEHPExactnessUseResult,
) -> TodaEHPExactnessUsePresentation:
  if not isinstance(
    use,
    TodaEHPExactnessUseResult,
  ):
    raise TypeError(
      "use must be "
      "a TodaEHPExactnessUseResult"
    )

  return TodaEHPExactnessUsePresentation(
    source_use=use,
    window=(
      build_toda_ehp_exactness_window_presentation(
        use.window_result
      )
    ),
    exactness_step=use.exactness_step,
    consumer_steps=use.consumer_steps,
  )


def build_toda_ehp_exactness_presentation(
  provenance: TodaEHPExactnessUseProvenanceResult,
) -> TodaEHPExactnessPresentation:
  if not isinstance(
    provenance,
    TodaEHPExactnessUseProvenanceResult,
  ):
    raise TypeError(
      "provenance must be "
      "a TodaEHPExactnessUseProvenanceResult"
    )

  return TodaEHPExactnessPresentation(
    source_provenance=provenance,
    sequence=(
      build_toda_ehp_sequence_presentation(
        provenance.ehp_result
      )
    ),
    uses=tuple(
      build_toda_ehp_exactness_use_presentation(
        use
      )
      for use in provenance.uses
    ),
  )
