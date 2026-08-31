from dataclasses import dataclass

from expression import GeneratorSymbol


@dataclass(frozen=True)
class GeneratorTypingFact:
  generator: GeneratorSymbol
  source: int
  target: int

  def matches_generator(
    self,
    generator: GeneratorSymbol,
  ) -> bool:
    return self.generator == generator


@dataclass(frozen=True)
class GeneratorAmbientGroupFact:
  generator: GeneratorSymbol
  group_dimension: int
  sphere_dimension: int


ETA_3_GENERATOR = GeneratorSymbol(
  family="η",
  index=3,
)


ETA_3_TYPING_FACT = GeneratorTypingFact(
  generator=ETA_3_GENERATOR,
  source=4,
  target=3,
)


ETA_3_AMBIENT_GROUP_FACT = GeneratorAmbientGroupFact(
  generator=ETA_3_GENERATOR,
  group_dimension=4,
  sphere_dimension=3,
)



