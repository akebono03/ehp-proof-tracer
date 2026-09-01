from dataclasses import dataclass

from expression import (
  Composition,
  HomotopyElement,
  Suspension,
  Zero,
)
from generator_facts import (
  ETA_3_GENERATOR,
  NU_7_GENERATOR,
  NU_PRIME_GENERATOR,
)
from proof import (
  Relation,
  RelationType,
)


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


E_NU_PRIME_NU_7_ZERO_COMPOSITION_FACT = Relation(
  lhs=Composition(
    left=Suspension(
      expression=HomotopyElement(
        name="ν′",
        dimension=3,
        generator=NU_PRIME_GENERATOR,
      ),
    ),
    right=HomotopyElement(
      name="ν₇",
      dimension=7,
      generator=NU_7_GENERATOR,
    ),
  ),
  rhs=Zero(),
  relation_type=RelationType.ZERO,
)


ZERO_COMPOSITION_FACT_REPOSITORY = (
  ZeroCompositionFactRepository(
    facts=(
      ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT,
      E_NU_PRIME_NU_7_ZERO_COMPOSITION_FACT,
    ),
  )
)





