from generator_occurrence_roles import (
  GeneratorOccurrenceRole,
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
