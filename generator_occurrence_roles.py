from enum import Enum

from expression import (
  Composition,
  GeneratorSymbol,
  MapApplication,
  TodaBracket,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  FreeCyclicGroup,
)
from proof import Relation


class GeneratorOccurrenceRole(Enum):
  RELATION_LHS = "relation_lhs"
  RELATION_RHS = "relation_rhs"
  GROUP_GENERATOR = "group_generator"
  COMPOSITION_LEFT = "composition_left"
  COMPOSITION_RIGHT = "composition_right"
  MAP_INPUT = "map_input"
  TODA_BRACKET_FIRST = "toda_bracket_first"
  TODA_BRACKET_SECOND = "toda_bracket_second"
  TODA_BRACKET_THIRD = "toda_bracket_third"


def _role_for_structural_edge(
  parent,
  segment: str,
) -> GeneratorOccurrenceRole | None:
  if isinstance(
    parent,
    Relation,
  ):
    if segment == "lhs":
      return (
        GeneratorOccurrenceRole.RELATION_LHS
      )

    if segment == "rhs":
      return (
        GeneratorOccurrenceRole.RELATION_RHS
      )

  if isinstance(
    parent,
    (
      FreeCyclicGroup,
      FiniteCyclicGroup,
    ),
  ):
    if segment == "generator":
      return (
        GeneratorOccurrenceRole.GROUP_GENERATOR
      )

  if isinstance(
    parent,
    Composition,
  ):
    if segment == "left":
      return (
        GeneratorOccurrenceRole.COMPOSITION_LEFT
      )

    if segment == "right":
      return (
        GeneratorOccurrenceRole.COMPOSITION_RIGHT
      )

  if isinstance(
    parent,
    MapApplication,
  ):
    if segment == "expression":
      return (
        GeneratorOccurrenceRole.MAP_INPUT
      )

  if isinstance(
    parent,
    TodaBracket,
  ):
    if segment == "first":
      return (
        GeneratorOccurrenceRole.TODA_BRACKET_FIRST
      )

    if segment == "second":
      return (
        GeneratorOccurrenceRole.TODA_BRACKET_SECOND
      )

    if segment == "third":
      return (
        GeneratorOccurrenceRole.TODA_BRACKET_THIRD
      )

  return None


def _descend_structural_path_segment(
  value,
  segment: str,
):
  if isinstance(
    value,
    tuple,
  ):
    try:
      index = int(
        segment
      )
    except ValueError as exc:
      raise ValueError(
        "tuple path segment must be an integer string"
      ) from exc

    try:
      return value[
        index
      ]
    except IndexError as exc:
      raise ValueError(
        "tuple path index is out of range"
      ) from exc

  if not hasattr(
    value,
    segment,
  ):
    raise ValueError(
      "path segment is not valid for value"
    )

  return getattr(
    value,
    segment,
  )


def classify_generator_occurrence_roles(
  value,
  path: tuple[
    str,
    ...,
  ],
) -> tuple[
  GeneratorOccurrenceRole,
  ...,
]:
  if not isinstance(
    path,
    tuple,
  ):
    raise TypeError(
      "path must be a tuple"
    )

  for segment in path:
    if not isinstance(
      segment,
      str,
    ):
      raise TypeError(
        "path must contain only str segments"
      )

  current = value
  roles = []

  for segment in path:
    role = (
      _role_for_structural_edge(
        current,
        segment,
      )
    )

    if role is not None:
      roles.append(
        role
      )

    current = (
      _descend_structural_path_segment(
        current,
        segment,
      )
    )

  if not isinstance(
    current,
    GeneratorSymbol,
  ):
    raise ValueError(
      "path must resolve to a GeneratorSymbol"
    )

  return tuple(
    roles
  )
