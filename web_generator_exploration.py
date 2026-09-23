from dataclasses import dataclass

from repository_element_facade import (
  explore_standard_repository_generator_input,
)
from repository_element_presentation import (
  RepositoryGeneratorExplorationPresentation,
  RepositoryGeneratorOccurrencePresentation,
)
from repository_element_renderer import (
  render_generator_occurrence_role_label,
)
from toda_human_readable_renderer import (
  _render_generator_symbol_latex,
)


@dataclass(frozen=True)
class WebGeneratorExplorationOccurrenceView:
  conclusion_latex: str
  role_labels: tuple[
    str,
    ...,
  ]
  phase: str
  theorem: str

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.conclusion_latex,
      str,
    ):
      raise TypeError(
        "conclusion_latex must be a str"
      )

    if not self.conclusion_latex:
      raise ValueError(
        "conclusion_latex must not be empty"
      )

    if not isinstance(
      self.role_labels,
      tuple,
    ):
      raise TypeError(
        "role_labels must be a tuple"
      )

    for role_label in self.role_labels:
      if not isinstance(
        role_label,
        str,
      ):
        raise TypeError(
          "role_labels must contain only str values"
        )

      if not role_label:
        raise ValueError(
          "role_labels must not contain empty values"
        )

    if not isinstance(
      self.phase,
      str,
    ):
      raise TypeError(
        "phase must be a str"
      )

    if not self.phase:
      raise ValueError(
        "phase must not be empty"
      )

    if not isinstance(
      self.theorem,
      str,
    ):
      raise TypeError(
        "theorem must be a str"
      )

    if not self.theorem:
      raise ValueError(
        "theorem must not be empty"
      )


@dataclass(frozen=True)
class WebGeneratorExplorationView:
  generator_input: str
  generator_latex: str
  occurrence_count: int
  toda_bracket_occurrences: tuple[
    WebGeneratorExplorationOccurrenceView,
    ...,
  ]
  map_input_occurrences: tuple[
    WebGeneratorExplorationOccurrenceView,
    ...,
  ]
  group_generator_occurrences: tuple[
    WebGeneratorExplorationOccurrenceView,
    ...,
  ]
  composition_left_occurrences: tuple[
    WebGeneratorExplorationOccurrenceView,
    ...,
  ]
  composition_right_occurrences: tuple[
    WebGeneratorExplorationOccurrenceView,
    ...,
  ]
  other_occurrences: tuple[
    WebGeneratorExplorationOccurrenceView,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.generator_input,
      str,
    ):
      raise TypeError(
        "generator_input must be a str"
      )

    if not self.generator_input:
      raise ValueError(
        "generator_input must not be empty"
      )

    if not isinstance(
      self.generator_latex,
      str,
    ):
      raise TypeError(
        "generator_latex must be a str"
      )

    if not self.generator_latex:
      raise ValueError(
        "generator_latex must not be empty"
      )

    if (
      isinstance(
        self.occurrence_count,
        bool,
      )
      or not isinstance(
        self.occurrence_count,
        int,
      )
    ):
      raise TypeError(
        "occurrence_count must be an int"
      )

    if self.occurrence_count < 0:
      raise ValueError(
        "occurrence_count must be nonnegative"
      )

    groups = (
      self.toda_bracket_occurrences,
      self.map_input_occurrences,
      self.group_generator_occurrences,
      self.composition_left_occurrences,
      self.composition_right_occurrences,
      self.other_occurrences,
    )

    for group in groups:
      if not isinstance(
        group,
        tuple,
      ):
        raise TypeError(
          "occurrence groups must be tuples"
        )

      for occurrence in group:
        if not isinstance(
          occurrence,
          WebGeneratorExplorationOccurrenceView,
        ):
          raise TypeError(
            "occurrence groups must contain only "
            "WebGeneratorExplorationOccurrenceView values"
          )


def _build_web_occurrence_view(
  presentation: RepositoryGeneratorOccurrencePresentation,
) -> WebGeneratorExplorationOccurrenceView:
  if not isinstance(
    presentation,
    RepositoryGeneratorOccurrencePresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "RepositoryGeneratorOccurrencePresentation"
    )

  source_occurrence = (
    presentation.source_occurrence
  )
  entry = source_occurrence.entry

  role_labels = tuple(
    render_generator_occurrence_role_label(
      role
    )
    for role in source_occurrence.roles
  )

  phase = (
    entry.phase
    if entry.phase is not None
    else "unknown"
  )
  theorem = (
    entry.theorem
    if entry.theorem is not None
    else "unknown"
  )

  return WebGeneratorExplorationOccurrenceView(
    conclusion_latex=(
      presentation.conclusion_latex
    ),
    role_labels=role_labels,
    phase=phase,
    theorem=theorem,
  )


def _build_web_occurrence_views(
  presentations: tuple[
    RepositoryGeneratorOccurrencePresentation,
    ...,
  ],
) -> tuple[
  WebGeneratorExplorationOccurrenceView,
  ...,
]:
  return tuple(
    _build_web_occurrence_view(
      presentation
    )
    for presentation in presentations
  )


def _other_occurrence_presentations(
  presentation: RepositoryGeneratorExplorationPresentation,
) -> tuple[
  RepositoryGeneratorOccurrencePresentation,
  ...,
]:
  if not isinstance(
    presentation,
    RepositoryGeneratorExplorationPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "RepositoryGeneratorExplorationPresentation"
    )

  grouped_ids = {
    id(
      occurrence
    )
    for group in (
      presentation.toda_bracket_occurrences,
      presentation.map_input_occurrences,
      presentation.group_generator_occurrences,
      presentation.composition_left_occurrences,
      presentation.composition_right_occurrences,
    )
    for occurrence in group
  }

  return tuple(
    occurrence
    for occurrence in presentation.occurrences
    if id(
      occurrence
    ) not in grouped_ids
  )


def build_standard_web_generator_exploration_view(
  generator_input: str,
) -> WebGeneratorExplorationView:
  if not isinstance(
    generator_input,
    str,
  ):
    raise TypeError(
      "generator_input must be a str"
    )

  generator_input = (
    generator_input.strip()
  )

  if not generator_input:
    raise ValueError(
      "generator is required"
    )

  report = (
    explore_standard_repository_generator_input(
      generator_input
    )
  )

  presentation = report.presentation

  return WebGeneratorExplorationView(
    generator_input=generator_input,
    generator_latex=(
      _render_generator_symbol_latex(
        presentation.source_result.generator
      )
    ),
    occurrence_count=len(
      presentation.occurrences
    ),
    toda_bracket_occurrences=(
      _build_web_occurrence_views(
        presentation.toda_bracket_occurrences
      )
    ),
    map_input_occurrences=(
      _build_web_occurrence_views(
        presentation.map_input_occurrences
      )
    ),
    group_generator_occurrences=(
      _build_web_occurrence_views(
        presentation.group_generator_occurrences
      )
    ),
    composition_left_occurrences=(
      _build_web_occurrence_views(
        presentation.composition_left_occurrences
      )
    ),
    composition_right_occurrences=(
      _build_web_occurrence_views(
        presentation.composition_right_occurrences
      )
    ),
    other_occurrences=(
      _build_web_occurrence_views(
        _other_occurrence_presentations(
          presentation
        )
      )
    ),
  )
