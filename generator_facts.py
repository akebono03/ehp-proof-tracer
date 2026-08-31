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




