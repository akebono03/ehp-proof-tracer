from dataclasses import dataclass

from expression import (
  Composition,
  Expression,
  TodaBracket,
  Zero,
)
from proof import (
  InferenceRule,
  LiteratureReference,
  PremisePattern,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)


@dataclass(frozen=True)
class TodaBracketMembershipStatement:
  element: Expression
  bracket: TodaBracket
  source: LiteratureReference | str | None = None
  note: str | None = None


def toda_bracket_membership_proof_step(
  statement,
):
  if not isinstance(
    statement,
    TodaBracketMembershipStatement,
  ):
    raise TypeError(
      "statement must be a "
      "TodaBracketMembershipStatement"
    )

  return ProofStep(
    conclusion=statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )


@dataclass(frozen=True)
class TodaBracketDefinedStatement:
  bracket: TodaBracket


def toda_bracket_defined_by_zero_compositions_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    first_relation = premises[0].conclusion
    second_relation = premises[1].conclusion

    first_composition = first_relation.lhs
    second_composition = second_relation.lhs

    if not isinstance(
      first_composition,
      Composition,
    ):
      return False

    if not isinstance(
      second_composition,
      Composition,
    ):
      return False

    return (
      first_composition.right
      == second_composition.left
    )

  def conclusion_builder(
    premises,
  ):
    first_relation = premises[0].conclusion
    second_relation = premises[1].conclusion

    first_composition = first_relation.lhs
    second_composition = second_relation.lhs

    return TodaBracketDefinedStatement(
      bracket=TodaBracket(
        first=first_composition.left,
        second=first_composition.right,
        third=second_composition.right,
      ),
    )

  return InferenceRule(
    name=(
      "Toda bracket defined by "
      "zero compositions"
    ),
    description=(
      "If a∘b and b∘c are zero, "
      "the three-fold Toda bracket "
      "{a,b,c} is defined."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.ZERO,
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.ZERO,
      ),
    ),
    conclusion_builder=conclusion_builder,
    match_guard=guard,
  )




