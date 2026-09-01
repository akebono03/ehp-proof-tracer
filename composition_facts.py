from dataclasses import dataclass

from expression import (
  Composition,
  Expression,
  HomotopyElement,
  Suspension,
  Zero,
)
from generator_facts import (
  ETA_3_GENERATOR,
  NU_6_GENERATOR,
  NU_7_GENERATOR,
  NU_PRIME_GENERATOR,
)
from proof import (
  Relation,
  RelationType,
)


def _homotopy_element_matches_ignoring_typing(
  actual: HomotopyElement,
  known: HomotopyElement,
) -> bool:
  return (
    actual.name == known.name
    and actual.dimension == known.dimension
    and actual.generator == known.generator
  )


def _expression_matches_ignoring_typing(
  actual: Expression,
  known: Expression,
) -> bool:
  if (
    isinstance(
      actual,
      HomotopyElement,
    )
    and isinstance(
      known,
      HomotopyElement,
    )
  ):
    return (
      _homotopy_element_matches_ignoring_typing(
        actual,
        known,
      )
    )

  if (
    isinstance(
      actual,
      Suspension,
    )
    and isinstance(
      known,
      Suspension,
    )
  ):
    if not isinstance(
      actual.expression,
      HomotopyElement,
    ):
      return False

    if not isinstance(
      known.expression,
      HomotopyElement,
    ):
      return False

    return (
      _homotopy_element_matches_ignoring_typing(
        actual.expression,
        known.expression,
      )
    )

  return actual == known


@dataclass(frozen=True)
class ZeroCompositionFactRepository:
  facts: tuple[
    Relation,
    ...
  ] = ()

  def __post_init__(
    self,
  ) -> None:
    compositions = [
      fact.lhs
      for fact in self.facts
    ]

    for fact in self.facts:
      if not isinstance(
        fact.lhs,
        Composition,
      ):
        raise ValueError(
          "invalid zero-composition fact"
        )

      if fact.rhs != Zero():
        raise ValueError(
          "invalid zero-composition fact"
        )

      if (
        fact.relation_type
        != RelationType.ZERO
      ):
        raise ValueError(
          "invalid zero-composition fact"
        )

    for index, composition in enumerate(
      compositions
    ):
      if composition in compositions[:index]:
        raise ValueError(
          "duplicate zero-composition fact"
        )

  def lookup(
    self,
    composition: Composition,
  ) -> Relation | None:
    for fact in self.facts:
      if fact.lhs == composition:
        return fact

    return None

  def lookup_by_untyped_structure(
    self,
    composition: Composition,
  ) -> Relation | None:
    for fact in self.facts:
      if not isinstance(
        fact.lhs,
        Composition,
      ):
        continue

      if not (
        _expression_matches_ignoring_typing(
          composition.left,
          fact.lhs.left,
        )
      ):
        continue

      if not (
        _expression_matches_ignoring_typing(
          composition.right,
          fact.lhs.right,
        )
      ):
        continue

      return fact

    return None


ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT = Relation(
  lhs=Composition(
    left=HomotopyElement(
      name="η₃",
      dimension=3,
      generator=ETA_3_GENERATOR,
    ),
    right=Suspension(
      expression=HomotopyElement(
        name="ν′",
        dimension=3,
        generator=NU_PRIME_GENERATOR,
      ),
    ),
  ),
  rhs=Zero(),
  relation_type=RelationType.ZERO,
)


NU_PRIME_NU_6_ZERO_COMPOSITION_FACT = Relation(
  lhs=Composition(
    left=HomotopyElement(
      name="ν′",
      dimension=3,
      generator=NU_PRIME_GENERATOR,
    ),
    right=HomotopyElement(
      name="ν₆",
      dimension=6,
      generator=NU_6_GENERATOR,
    ),
  ),
  rhs=Zero(),
  relation_type=RelationType.ZERO,
)


E_NU_6_EQUALS_NU_7_FACT = Relation(
  lhs=Suspension(
    expression=HomotopyElement(
      name="ν₆",
      dimension=6,
      generator=NU_6_GENERATOR,
    ),
  ),
  rhs=HomotopyElement(
    name="ν₇",
    dimension=7,
    generator=NU_7_GENERATOR,
  ),
  relation_type=RelationType.EQUALITY,
)


ZERO_COMPOSITION_FACT_REPOSITORY = (
  ZeroCompositionFactRepository(
    facts=(
      ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT,
      NU_PRIME_NU_6_ZERO_COMPOSITION_FACT,
    ),
  )
)
