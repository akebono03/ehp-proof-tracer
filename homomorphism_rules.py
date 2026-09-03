from dataclasses import dataclass

from expression import (
  MapApplication,
  MapSymbol,
  Multiple,
  Sum,
  Suspension,
  Zero,
)
from proof import (
  InferenceRule,
  PremisePattern,
  Relation,
  RelationType,
)


SUSPENSION_MAP = MapSymbol(
  name="E",
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


def suspension_is_homomorphism_inference_rule():
  return InferenceRule(
    name="suspension is homomorphism",
    description=(
      "The suspension map E is a homomorphism "
      "for the additive expressions considered "
      "in the current proof-expression layer."
    ),
    conclusion_pattern=HomomorphismStatement(
      map=SUSPENSION_MAP,
    ),
  )


def suspension_additivity_bridge_inference_rule(
  left,
  right,
):
  expected_generic_relation = Relation(
    lhs=MapApplication(
      map=SUSPENSION_MAP,
      expression=Sum(
        left=left,
        right=right,
      ),
    ),
    rhs=Sum(
      left=MapApplication(
        map=SUSPENSION_MAP,
        expression=left,
      ),
      right=MapApplication(
        map=SUSPENSION_MAP,
        expression=right,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  return InferenceRule(
    name="suspension additivity bridge",
    description=(
      "Translate the generic homomorphism "
      "additivity relation for E into the "
      "existing Suspension expression."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.EQUALITY,
        relation_pattern=(
          expected_generic_relation
        ),
      ),
    ),
    conclusion_pattern=Relation(
      lhs=Suspension(
        expression=Sum(
          left=left,
          right=right,
        ),
      ),
      rhs=Sum(
        left=Suspension(
          expression=left,
        ),
        right=Suspension(
          expression=right,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    ),
  )


def suspension_multiple_bridge_inference_rule(
  coefficient,
  expression,
):
  expected_generic_relation = Relation(
    lhs=MapApplication(
      map=SUSPENSION_MAP,
      expression=Multiple(
        coefficient=coefficient,
        expression=expression,
      ),
    ),
    rhs=Multiple(
      coefficient=coefficient,
      expression=MapApplication(
        map=SUSPENSION_MAP,
        expression=expression,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  return InferenceRule(
    name="suspension multiple bridge",
    description=(
      "Translate the generic homomorphism "
      "multiple relation for E into the "
      "existing Suspension expression."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.EQUALITY,
        relation_pattern=(
          expected_generic_relation
        ),
      ),
    ),
    conclusion_pattern=Relation(
      lhs=Suspension(
        expression=Multiple(
          coefficient=coefficient,
          expression=expression,
        ),
      ),
      rhs=Multiple(
        coefficient=coefficient,
        expression=Suspension(
          expression=expression,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    ),
  )


def homomorphism_preserves_known_zero_inference_rule(
  expression,
):
  zero_relation = Relation(
    lhs=expression,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

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
        expression=expression,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name="homomorphism preserves known zero",
    description=(
      "A homomorphism maps an expression "
      "known to be zero to zero."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          HomomorphismStatement
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.ZERO,
        relation_pattern=zero_relation,
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
  )








