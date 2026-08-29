from dataclasses import dataclass

from expression import (
  MapApplication,
  MapSymbol,
  Multiple,
  Sum,
  Zero,
)
from proof import (
  InferenceRule,
  PremisePattern,
  Relation,
  RelationType,
)


@dataclass(frozen=True)
class HomomorphismStatement:
  map: MapSymbol


def homomorphism_preserves_addition_inference_rule(
  left,
  right,
):
  def build_conclusion(
    premises,
  ):
    homomorphism_statement = (
      premises[0].conclusion
    )

    map_symbol = (
      homomorphism_statement.map
    )

    return Relation(
      lhs=MapApplication(
        map=map_symbol,
        expression=Sum(
          left=left,
          right=right,
        ),
      ),
      rhs=Sum(
        left=MapApplication(
          map=map_symbol,
          expression=left,
        ),
        right=MapApplication(
          map=map_symbol,
          expression=right,
        ),
      ),
      relation_type=(
        RelationType.EQUALITY
      ),
    )

  return InferenceRule(
    name="homomorphism preserves addition",
    description=(
      "A homomorphism maps a sum to "
      "the sum of the images."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          HomomorphismStatement
        ),
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
  )


def homomorphism_preserves_zero_inference_rule():
  def build_conclusion(
    premises,
  ):
    homomorphism_statement = (
      premises[0].conclusion
    )

    map_symbol = (
      homomorphism_statement.map
    )

    return Relation(
      lhs=MapApplication(
        map=map_symbol,
        expression=Zero(),
      ),
      rhs=Zero(),
      relation_type=(
        RelationType.ZERO
      ),
    )

  return InferenceRule(
    name="homomorphism preserves zero",
    description=(
      "A homomorphism maps zero to zero."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          HomomorphismStatement
        ),
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
  )


def homomorphism_preserves_inverse_inference_rule(
  expression,
):
  def build_conclusion(
    premises,
  ):
    homomorphism_statement = (
      premises[0].conclusion
    )

    map_symbol = (
      homomorphism_statement.map
    )

    return Relation(
      lhs=MapApplication(
        map=map_symbol,
        expression=Multiple(
          coefficient=-1,
          expression=expression,
        ),
      ),
      rhs=Multiple(
        coefficient=-1,
        expression=MapApplication(
          map=map_symbol,
          expression=expression,
        ),
      ),
      relation_type=(
        RelationType.EQUALITY
      ),
    )

  return InferenceRule(
    name="homomorphism preserves inverse",
    description=(
      "A homomorphism maps an additive inverse "
      "to the additive inverse of the image."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          HomomorphismStatement
        ),
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
  )


def homomorphism_preserves_multiple_inference_rule(
  coefficient,
  expression,
):
  def build_conclusion(
    premises,
  ):
    homomorphism_statement = (
      premises[0].conclusion
    )

    map_symbol = (
      homomorphism_statement.map
    )

    return Relation(
      lhs=MapApplication(
        map=map_symbol,
        expression=Multiple(
          coefficient=coefficient,
          expression=expression,
        ),
      ),
      rhs=Multiple(
        coefficient=coefficient,
        expression=MapApplication(
          map=map_symbol,
          expression=expression,
        ),
      ),
      relation_type=(
        RelationType.EQUALITY
      ),
    )

  return InferenceRule(
    name="homomorphism preserves multiple",
    description=(
      "A homomorphism maps an integer multiple "
      "to the same integer multiple of the image."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          HomomorphismStatement
        ),
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
  )







