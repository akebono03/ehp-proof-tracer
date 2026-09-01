from dataclasses import dataclass

from expression import MapSymbol
from map_property_rules import IsomorphismStatement
from proof import (
  ProofRule,
  ProofStep,
)


@dataclass(frozen=True)
class MapTypingFact:
  map: MapSymbol
  source_group_dimension: int
  source_sphere_dimension: int
  target_group_dimension: int
  target_sphere_dimension: int


@dataclass(frozen=True)
class MapIsomorphismFact:
  typing: MapTypingFact

  def to_proof_step(
    self,
  ) -> ProofStep:
    return ProofStep(
      conclusion=IsomorphismStatement(
        map=self.typing.map,
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    )


@dataclass(frozen=True)
class MapIsomorphismFactRepository:
  facts: tuple[
    MapIsomorphismFact,
    ...
  ] = ()

  def __post_init__(
    self,
  ) -> None:
    typings = [
      fact.typing
      for fact in self.facts
    ]

    for index, typing in enumerate(
      typings
    ):
      if typing in typings[:index]:
        raise ValueError(
          "duplicate map isomorphism fact"
        )

  def lookup(
    self,
    typing: MapTypingFact,
  ) -> MapIsomorphismFact | None:
    for fact in self.facts:
      if fact.typing == typing:
        return fact

    return None


HOPF_MAP = MapSymbol(
  name="H",
)


HOPF_MAP_TYPING_FACT = MapTypingFact(
  map=HOPF_MAP,
  source_group_dimension=3,
  source_sphere_dimension=2,
  target_group_dimension=3,
  target_sphere_dimension=3,
)


HOPF_MAP_ISOMORPHISM_FACT = (
  MapIsomorphismFact(
    typing=HOPF_MAP_TYPING_FACT,
  )
)


MAP_ISOMORPHISM_FACT_REPOSITORY = (
  MapIsomorphismFactRepository(
    facts=(
      HOPF_MAP_ISOMORPHISM_FACT,
    ),
  )
)




