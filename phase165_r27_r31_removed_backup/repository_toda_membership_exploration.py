from dataclasses import dataclass
from enum import Enum

from expression import GeneratorSymbol
from generator_occurrence_roles import (
  GeneratorOccurrenceRole,
)
from proof_repository import ProofRepository
from repository_theorem_pattern_exploration import (
  RepositoryTheoremPatternOccurrence,
  build_repository_theorem_pattern_occurrences,
)
from toda_rules import (
  TodaBracketMembershipStatement,
  TodaBracketMembershipTheoremStatement,
)


class TodaBracketMembershipKind(Enum):
  MEMBERSHIP = "membership"
  THEOREM = "theorem"


class TodaBracketPosition(Enum):
  FIRST = "first"
  SECOND = "second"
  THIRD = "third"


_POSITION_ROLE_PAIRS = (
  (
    TodaBracketPosition.FIRST,
    GeneratorOccurrenceRole.TODA_BRACKET_FIRST,
  ),
  (
    TodaBracketPosition.SECOND,
    GeneratorOccurrenceRole.TODA_BRACKET_SECOND,
  ),
  (
    TodaBracketPosition.THIRD,
    GeneratorOccurrenceRole.TODA_BRACKET_THIRD,
  ),
)


@dataclass(frozen=True)
class RepositoryTodaBracketMembershipOccurrence:
  source_pattern_occurrence: RepositoryTheoremPatternOccurrence
  statement: (
    TodaBracketMembershipStatement
    | TodaBracketMembershipTheoremStatement
  )
  kind: TodaBracketMembershipKind
  positions: tuple[
    TodaBracketPosition,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_pattern_occurrence,
      RepositoryTheoremPatternOccurrence,
    ):
      raise TypeError(
        "source_pattern_occurrence must be a "
        "RepositoryTheoremPatternOccurrence"
      )

    if (
      self.statement
      is not self.source_pattern_occurrence.statement
    ):
      raise ValueError(
        "statement must be the source pattern "
        "occurrence statement"
      )

    if not isinstance(
      self.statement,
      (
        TodaBracketMembershipStatement,
        TodaBracketMembershipTheoremStatement,
      ),
    ):
      raise TypeError(
        "statement must be a Toda bracket "
        "membership statement"
      )

    if not isinstance(
      self.kind,
      TodaBracketMembershipKind,
    ):
      raise TypeError(
        "kind must be a TodaBracketMembershipKind"
      )

    if not isinstance(
      self.positions,
      tuple,
    ):
      raise TypeError(
        "positions must be a tuple"
      )

    for position in self.positions:
      if not isinstance(
        position,
        TodaBracketPosition,
      ):
        raise TypeError(
          "positions must contain only "
          "TodaBracketPosition values"
        )

    if not self.positions:
      raise ValueError(
        "positions must not be empty"
      )

    expected_kind = _membership_kind(
      self.statement
    )

    if self.kind is not expected_kind:
      raise ValueError(
        "kind must match the statement type"
      )

    expected_positions = _bracket_positions(
      self.source_pattern_occurrence
    )

    if self.positions != expected_positions:
      raise ValueError(
        "positions must match the source "
        "occurrence Toda bracket roles"
      )


def _membership_kind(
  statement,
) -> TodaBracketMembershipKind:
  if isinstance(
    statement,
    TodaBracketMembershipTheoremStatement,
  ):
    return TodaBracketMembershipKind.THEOREM

  if isinstance(
    statement,
    TodaBracketMembershipStatement,
  ):
    return TodaBracketMembershipKind.MEMBERSHIP

  raise TypeError(
    "statement must be a Toda bracket "
    "membership statement"
  )


def _bracket_positions(
  pattern_occurrence: RepositoryTheoremPatternOccurrence,
) -> tuple[
  TodaBracketPosition,
  ...,
]:
  roles = (
    pattern_occurrence
    .source_occurrence
    .roles
  )

  return tuple(
    position
    for position, role in _POSITION_ROLE_PAIRS
    if role in roles
  )


def find_repository_toda_bracket_membership_occurrences(
  repository: ProofRepository,
  generator: GeneratorSymbol,
  position: TodaBracketPosition | None = None,
  kind: TodaBracketMembershipKind | None = None,
) -> tuple[
  RepositoryTodaBracketMembershipOccurrence,
  ...,
]:
  if not isinstance(
    repository,
    ProofRepository,
  ):
    raise TypeError(
      "repository must be a ProofRepository"
    )

  if not isinstance(
    generator,
    GeneratorSymbol,
  ):
    raise TypeError(
      "generator must be a GeneratorSymbol"
    )

  if (
    position is not None
    and not isinstance(
      position,
      TodaBracketPosition,
    )
  ):
    raise TypeError(
      "position must be a TodaBracketPosition "
      "or None"
    )

  if (
    kind is not None
    and not isinstance(
      kind,
      TodaBracketMembershipKind,
    )
  ):
    raise TypeError(
      "kind must be a TodaBracketMembershipKind "
      "or None"
    )

  pattern_occurrences = (
    build_repository_theorem_pattern_occurrences(
      repository,
      generator,
    )
  )

  results = []

  for pattern_occurrence in pattern_occurrences:
    statement = pattern_occurrence.statement

    if not isinstance(
      statement,
      (
        TodaBracketMembershipStatement,
        TodaBracketMembershipTheoremStatement,
      ),
    ):
      continue

    positions = _bracket_positions(
      pattern_occurrence
    )

    if not positions:
      continue

    occurrence_kind = _membership_kind(
      statement
    )

    if (
      position is not None
      and position not in positions
    ):
      continue

    if (
      kind is not None
      and occurrence_kind is not kind
    ):
      continue

    results.append(
      RepositoryTodaBracketMembershipOccurrence(
        source_pattern_occurrence=pattern_occurrence,
        statement=statement,
        kind=occurrence_kind,
        positions=positions,
      )
    )

  return tuple(
    results
  )
