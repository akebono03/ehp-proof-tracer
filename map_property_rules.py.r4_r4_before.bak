from dataclasses import dataclass

from expression import (
  MapApplication,
  MapSymbol,
)
from proof import (
  InferenceRule,
  PremisePattern,
  Relation,
  RelationType,
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


def injective_map_reflects_equality_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    injective_statement = (
      premises[0].conclusion
    )

    equality_relation = (
      premises[1].conclusion
    )

    if not isinstance(
      equality_relation.lhs,
      MapApplication,
    ):
      return False

    if not isinstance(
      equality_relation.rhs,
      MapApplication,
    ):
      return False

    return (
      equality_relation.lhs.map
      == equality_relation.rhs.map
      and injective_statement.map
      == equality_relation.lhs.map
    )

  def build_conclusion(
    premises,
  ):
    equality_relation = (
      premises[1].conclusion
    )

    return Relation(
      lhs=equality_relation.lhs.expression,
      rhs=equality_relation.rhs.expression,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name="injective map reflects equality",
    description=(
      "If f is injective and "
      "f(a)=f(b), then a=b."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          InjectiveMapStatement
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
    match_guard=guard,
  )





