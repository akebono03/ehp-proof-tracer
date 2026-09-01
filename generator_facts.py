from dataclasses import (
  dataclass,
  replace,
)

from expression import (
  GeneratorSymbol,
  HomotopyElement,
)


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

  def __post_init__(
    self,
  ) -> None:
    typing_generators = [
      fact.generator
      for fact in self.typing_facts
    ]

    for index, generator in enumerate(
      typing_generators
    ):
      if generator in typing_generators[:index]:
        raise ValueError(
          "duplicate generator typing fact"
        )

    ambient_generators = [
      fact.generator
      for fact in self.ambient_group_facts
    ]

    for index, generator in enumerate(
      ambient_generators
    ):
      if generator in ambient_generators[:index]:
        raise ValueError(
          "duplicate generator ambient-group fact"
        )

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

  def materialize_typed_element(
    self,
    element: HomotopyElement,
  ) -> HomotopyElement | None:
    if element.generator is None:
      return None

    if (
      element.source is not None
      or element.target is not None
    ):
      return None

    typing_fact = self.lookup_typing(
      element.generator
    )

    if typing_fact is None:
      return None

    return replace(
      element,
      source=typing_fact.source,
      target=typing_fact.target,
    )


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


NU_PRIME_GENERATOR = GeneratorSymbol(
  family="ν",
  decoration="′",
)


NU_PRIME_TYPING_FACT = GeneratorTypingFact(
  generator=NU_PRIME_GENERATOR,
  source=6,
  target=3,
)


NU_PRIME_AMBIENT_GROUP_FACT = GeneratorAmbientGroupFact(
  generator=NU_PRIME_GENERATOR,
  group_dimension=6,
  sphere_dimension=3,
)


NU_7_GENERATOR = GeneratorSymbol(
  family="ν",
  index=7,
)


NU_7_TYPING_FACT = GeneratorTypingFact(
  generator=NU_7_GENERATOR,
  source=10,
  target=7,
)


NU_7_AMBIENT_GROUP_FACT = GeneratorAmbientGroupFact(
  generator=NU_7_GENERATOR,
  group_dimension=10,
  sphere_dimension=7,
)


GENERATOR_FACT_REPOSITORY = GeneratorFactRepository(
  typing_facts=(
    ETA_3_TYPING_FACT,
    NU_PRIME_TYPING_FACT,
    NU_7_TYPING_FACT,
  ),
  ambient_group_facts=(
    ETA_3_AMBIENT_GROUP_FACT,
    NU_PRIME_AMBIENT_GROUP_FACT,
    NU_7_AMBIENT_GROUP_FACT,
  ),
)




