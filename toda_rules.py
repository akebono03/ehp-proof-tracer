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
class TodaBracketMembershipTheoremStatement:
  element: Expression
  bracket: TodaBracket
  source: LiteratureReference | str | None = None
  note: str | None = None


def toda_bracket_membership_theorem_proof_step(
  statement,
):
  if not isinstance(
    statement,
    TodaBracketMembershipTheoremStatement,
  ):
    raise TypeError(
      "statement must be a "
      "TodaBracketMembershipTheoremStatement"
    )

  return ProofStep(
    conclusion=statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )


@dataclass(frozen=True)
class TodaBracketDefinedStatement:
  bracket: TodaBracket


def toda_bracket_membership_from_theorem_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    theorem_statement = premises[0].conclusion
    defined_statement = premises[1].conclusion

    return (
      theorem_statement.bracket
      == defined_statement.bracket
    )

  def conclusion_builder(
    premises,
  ):
    theorem_statement = premises[0].conclusion

    return TodaBracketMembershipStatement(
      element=theorem_statement.element,
      bracket=theorem_statement.bracket,
      source=theorem_statement.source,
      note=theorem_statement.note,
    )

  return InferenceRule(
    name=(
      "Toda bracket membership "
      "from theorem"
    ),
    description=(
      "If a literature-backed Toda "
      "membership theorem applies to "
      "a defined bracket, derive the "
      "corresponding bracket membership."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaBracketMembershipTheoremStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaBracketDefinedStatement
        ),
      ),
    ),
    conclusion_builder=conclusion_builder,
    match_guard=guard,
  )


def indexed_toda_bracket_membership_from_theorem_inference_rule(
  indexed_data,
):
  def guard(
    premises,
    bindings,
  ):
    theorem_statement = (
      premises[0].conclusion
    )

    defined_statement = (
      premises[1].conclusion
    )

    return (
      indexed_data.is_consistent()
      and indexed_data.bracket
      .are_defining_compositions_type_compatible()
      and theorem_statement.bracket
      == indexed_data.bracket
      and defined_statement.bracket
      == indexed_data.bracket
    )

  def build_conclusion(
    premises,
  ):
    theorem_statement = (
      premises[0].conclusion
    )

    return TodaBracketMembershipStatement(
      element=theorem_statement.element,
      bracket=theorem_statement.bracket,
      source=theorem_statement.source,
      note=theorem_statement.note,
    )

  return InferenceRule(
    name=(
      "Indexed Toda membership theorem "
      "bridge with structural and typing guards"
    ),
    description=(
      "A matching indexed Toda theorem fact "
      "and definedness derive membership only "
      "when the supplied indexed bracket data "
      "is structurally consistent and its "
      "displayed defining compositions are "
      "type-compatible."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaBracketMembershipTheoremStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaBracketDefinedStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


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




