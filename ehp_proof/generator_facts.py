from dataclasses import dataclass

from expression import GeneratorSymbol


@dataclass(frozen=True)
class GeneratorTypingFact:
  generator: GeneratorSymbol
  source: int
  target: int



