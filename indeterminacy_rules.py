from dataclasses import dataclass

from expression import (
  Expression,
  Multiple,
  Sum,
)
from proof import (
  InferenceRule,
  PatternVariable,
  PremisePattern,
  Relation,
  RelationType,
)
from scalar_rules import (
  OddScalarStatement,
)
from set_rules import (
  Coset,
  ModuloStatement,
)


@dataclass(frozen=True)
class CosetMembershipStatement:
  element: Expression
  coset: Coset


@dataclass(frozen=True)
class SignIndeterminacyStatement:
  value: Expression
  representative: Expression


@dataclass(frozen=True)
class CoefficientIndeterminacyStatement:
  value: Expression
  expression: Expression
  constraint: OddScalarStatement


def modulo_implies_coset_membership_inference_rule():
  left = PatternVariable(
    name="left",
  )

  right = PatternVariable(
    name="right",
  )

  modulus = PatternVariable(
    name="modulus",
  )

  return InferenceRule(
    name="modulo implies coset membership",
    description=(
      "If an element is congruent to a "
      "representative modulo a subgroup, then "
      "the element belongs to that representative's "
      "coset."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=ModuloStatement,
        statement_pattern=ModuloStatement(
          left=left,
          right=right,
          modulus=modulus,
        ),
      ),
    ),
    conclusion_pattern=CosetMembershipStatement(
      element=left,
      coset=Coset(
        representative=right,
        subgroup=modulus,
      ),
    ),
  )


def equality_implies_sign_indeterminacy_inference_rule():
  value = PatternVariable(
    name="value",
  )

  representative = PatternVariable(
    name="representative",
  )

  return InferenceRule(
    name="equality implies sign indeterminacy",
    description=(
      "If a value is exactly equal to a "
      "representative, then it is also "
      "determined up to sign by that "
      "representative."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.EQUALITY,
        relation_pattern=Relation(
          lhs=value,
          rhs=representative,
          relation_type=RelationType.EQUALITY,
        ),
      ),
    ),
    conclusion_pattern=SignIndeterminacyStatement(
      value=value,
      representative=representative,
    ),
  )


def coset_membership_implies_modulo_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    membership_statement = (
      premises[0].conclusion
    )

    return isinstance(
      membership_statement.coset,
      Coset,
    )

  def build_conclusion(
    premises,
  ):
    membership_statement = (
      premises[0].conclusion
    )

    return ModuloStatement(
      left=membership_statement.element,
      right=(
        membership_statement.coset.representative
      ),
      modulus=(
        membership_statement.coset.subgroup
      ),
    )

  return InferenceRule(
    name="coset membership implies modulo",
    description=(
      "If an element belongs to a "
      "representative's coset, then the "
      "element is congruent to the "
      "representative modulo the subgroup."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=CosetMembershipStatement,
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
    match_guard=guard,
  )


def symbolic_odd_equality_implies_coefficient_indeterminacy_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    equality_statement = premises[0].conclusion
    odd_statement = premises[1].conclusion

    if (
      equality_statement.relation_type
      != RelationType.EQUALITY
    ):
      return False

    expression = equality_statement.rhs

    if not isinstance(
      expression,
      Sum,
    ):
      return False

    if not isinstance(
      expression.left,
      Multiple,
    ):
      return False

    return (
      expression.left.coefficient
      == odd_statement.scalar
    )

  def build_conclusion(
    premises,
  ):
    equality_statement = premises[0].conclusion
    odd_statement = premises[1].conclusion

    return CoefficientIndeterminacyStatement(
      value=equality_statement.lhs,
      expression=equality_statement.rhs,
      constraint=odd_statement,
    )

  return InferenceRule(
    name=(
      "Symbolic odd equality implies "
      "coefficient indeterminacy"
    ),
    description=(
      "A symbolic additive equality whose "
      "coefficient is known to be odd "
      "defines a coefficient-indeterminate "
      "family without enumerating concrete "
      "coefficient values."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.EQUALITY,
      ),
      PremisePattern(
        statement_type=OddScalarStatement,
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )




