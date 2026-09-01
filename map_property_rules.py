from dataclasses import dataclass

from expression import (
  MapSymbol,
)
from proof import (
  InferenceRule,
  PremisePattern,
)


@dataclass(frozen=True)
class InjectiveMapStatement:
  map: MapSymbol


@dataclass(frozen=True)
class IsomorphismStatement:
  map: MapSymbol


def isomorphism_implies_injective_inference_rule():
  def build_conclusion(
    premises,
  ):
    isomorphism_statement = (
      premises[0].conclusion
    )

    return InjectiveMapStatement(
      map=isomorphism_statement.map,
    )

  return InferenceRule(
    name="isomorphism implies injectivity",
    description=(
      "An isomorphism is injective."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          IsomorphismStatement
        ),
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
  )



