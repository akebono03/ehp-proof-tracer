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


@dataclass(frozen=True)
class GeneratorFactRepository:
  typing_facts: tuple[
    GeneratorTypingFact,
    ...
  ] = ()
  ambient_group_facts: tuple[
    GeneratorAmbientGroupFact,
    ...
  ] = ()

  def lookup_typing(
    self,
    generator: GeneratorSymbol,
  ) -> GeneratorTypingFact | None:
    for fact in self.typing_facts:
      if fact.matches_generator(
        generator
      ):
        return fact

    return None

  def lookup_ambient_group(
    self,
    generator: GeneratorSymbol,
  ) -> GeneratorAmbientGroupFact | None:
    for fact in self.ambient_group_facts:
      if fact.generator == generator:
        return fact

    return None


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


GENERATOR_FACT_REPOSITORY = GeneratorFactRepository(
  typing_facts=(
    ETA_3_TYPING_FACT,
  ),
  ambient_group_facts=(
    ETA_3_AMBIENT_GROUP_FACT,
  ),
)



