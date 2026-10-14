from expression import GeneratorSymbol
from generator_occurrence_roles import (
  GeneratorOccurrenceRole,
)
from repository_element_presentation import (
  RepositoryGeneratorExplorationPresentation,
  RepositoryGeneratorOccurrencePresentation,
)
from toda_human_readable_renderer import (
  _render_generator_symbol_latex,
)


_GENERATOR_OCCURRENCE_ROLE_LABELS = {
  GeneratorOccurrenceRole.RELATION_LHS: (
    "relation left-hand side"
  ),
  GeneratorOccurrenceRole.RELATION_RHS: (
    "relation right-hand side"
  ),
  GeneratorOccurrenceRole.GROUP_GENERATOR: (
    "group generator"
  ),
  GeneratorOccurrenceRole.COMPOSITION_LEFT: (
    "composition left factor"
  ),
  GeneratorOccurrenceRole.COMPOSITION_RIGHT: (
    "composition right factor"
  ),
  GeneratorOccurrenceRole.MAP_INPUT: (
    "map input"
  ),
  GeneratorOccurrenceRole.TODA_BRACKET_FIRST: (
    "Toda bracket first entry"
  ),
  GeneratorOccurrenceRole.TODA_BRACKET_SECOND: (
    "Toda bracket second entry"
  ),
  GeneratorOccurrenceRole.TODA_BRACKET_THIRD: (
    "Toda bracket third entry"
  ),
}


def render_generator_occurrence_role_label(
  role: GeneratorOccurrenceRole,
) -> str:
  if not isinstance(
    role,
    GeneratorOccurrenceRole,
  ):
    raise TypeError(
      "role must be a GeneratorOccurrenceRole"
    )

  return (
    _GENERATOR_OCCURRENCE_ROLE_LABELS[
      role
    ]
  )


def _render_occurrence_markdown_lines(
  presentation: RepositoryGeneratorOccurrencePresentation,
) -> tuple[
  str,
  ...,
]:
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

  roles_text = (
    ", ".join(
      role_labels
    )
    if role_labels
    else "none"
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

  return (
    (
      "- $"
      + presentation.conclusion_latex
      + "$"
    ),
    (
      "  - Roles: "
      + roles_text
    ),
    (
      "  - Phase: "
      + phase
    ),
    (
      "  - Theorem: "
      + theorem
    ),
  )


def _append_occurrence_section(
  lines: list[str],
  title: str,
  occurrences: tuple[
    RepositoryGeneratorOccurrencePresentation,
    ...,
  ],
) -> None:
  if not occurrences:
    return

  lines.extend(
    (
      "",
      "## " + title,
      "",
    )
  )

  for index, occurrence in enumerate(
    occurrences
  ):
    if index:
      lines.append(
        ""
      )

    lines.extend(
      _render_occurrence_markdown_lines(
        occurrence
      )
    )


def _other_occurrences(
  presentation: RepositoryGeneratorExplorationPresentation,
) -> tuple[
  RepositoryGeneratorOccurrencePresentation,
  ...,
]:
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


def render_repository_generator_exploration_markdown(
  presentation: RepositoryGeneratorExplorationPresentation,
) -> str:
  if not isinstance(
    presentation,
    RepositoryGeneratorExplorationPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "RepositoryGeneratorExplorationPresentation"
    )

  generator = (
    presentation
    .source_result
    .generator
  )

  if not isinstance(
    generator,
    GeneratorSymbol,
  ):
    raise TypeError(
      "presentation source generator must be "
      "a GeneratorSymbol"
    )

  lines = [
    (
      "# $"
      + _render_generator_symbol_latex(
        generator
      )
      + "$"
    ),
    "",
    (
      "Occurrences: "
      + str(
        len(
          presentation.occurrences
        )
      )
    ),
  ]

  _append_occurrence_section(
    lines,
    "Toda brackets",
    presentation.toda_bracket_occurrences,
  )
  _append_occurrence_section(
    lines,
    "Map inputs",
    presentation.map_input_occurrences,
  )
  _append_occurrence_section(
    lines,
    "Group generators",
    presentation.group_generator_occurrences,
  )
  _append_occurrence_section(
    lines,
    "Composition left",
    presentation.composition_left_occurrences,
  )
  _append_occurrence_section(
    lines,
    "Composition right",
    presentation.composition_right_occurrences,
  )
  _append_occurrence_section(
    lines,
    "Other occurrences",
    _other_occurrences(
      presentation
    ),
  )

  return "\n".join(
    lines
  ) + "\n"
