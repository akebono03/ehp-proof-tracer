from dataclasses import dataclass

from expression import (
  Multiple,
  ScalarPower,
  ScalarSymbol,
  ScalarValue,
)
from proof import (
  InferenceRule,
  PatternVariable,
  PremisePattern,
  Relation,
  RelationType,
)


@dataclass(frozen=True)
class OddScalarStatement:
  scalar: ScalarValue


@dataclass(frozen=True)
class EvenScalarStatement:
  scalar: ScalarValue


@dataclass(frozen=True)
class ScalarCongruenceStatement:
  scalar: ScalarSymbol
  residue: int
  modulus: int


@dataclass(frozen=True)
class ScalarSignEvaluationStatement:
  expression: ScalarPower
  value: int


def odd_scalar_implies_mod_two_congruence_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    statement = premises[0].conclusion

    return isinstance(
      statement.scalar,
      ScalarSymbol,
    )

  def build_conclusion(
    premises,
  ):
    statement = premises[0].conclusion

    return ScalarCongruenceStatement(
      scalar=statement.scalar,
      residue=1,
      modulus=2,
    )

  return InferenceRule(
    name=(
      "Odd scalar implies "
      "congruence to one modulo two"
    ),
    description=(
      "An odd integer scalar symbol is "
      "congruent to one modulo two."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=OddScalarStatement,
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def even_scalar_implies_mod_two_congruence_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    statement = premises[0].conclusion

    return isinstance(
      statement.scalar,
      ScalarSymbol,
    )

  def build_conclusion(
    premises,
  ):
    statement = premises[0].conclusion

    return ScalarCongruenceStatement(
      scalar=statement.scalar,
      residue=0,
      modulus=2,
    )

  return InferenceRule(
    name=(
      "Even scalar implies "
      "congruence to zero modulo two"
    ),
    description=(
      "An even integer scalar symbol is "
      "congruent to zero modulo two."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=EvenScalarStatement,
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def even_scalar_evaluates_minus_one_power_inference_rule():
  def build_conclusion(
    premises,
  ):
    statement = premises[0].conclusion

    return ScalarSignEvaluationStatement(
      expression=ScalarPower(
        base=-1,
        exponent=statement.scalar,
      ),
      value=1,
    )

  return InferenceRule(
    name=(
      "Even exponent evaluates "
      "minus-one power to one"
    ),
    description=(
      "If a scalar exponent is even, "
      "then minus one raised to that "
      "exponent equals one."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=EvenScalarStatement,
      ),
    ),
    conclusion_builder=build_conclusion,
  )


def odd_scalar_evaluates_minus_one_power_inference_rule():
  def build_conclusion(
    premises,
  ):
    statement = premises[0].conclusion

    return ScalarSignEvaluationStatement(
      expression=ScalarPower(
        base=-1,
        exponent=statement.scalar,
      ),
      value=-1,
    )

  return InferenceRule(
    name=(
      "Odd exponent evaluates "
      "minus-one power to minus one"
    ),
    description=(
      "If a scalar exponent is odd, "
      "then minus one raised to that "
      "exponent equals minus one."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=OddScalarStatement,
      ),
    ),
    conclusion_builder=build_conclusion,
  )


def mod_two_one_scalar_preserves_order_two_element_inference_rule():
  scalar = PatternVariable(
    "scalar",
  )

  element = PatternVariable(
    "element",
  )

  return InferenceRule(
    name=(
      "Scalar congruent to one modulo two "
      "preserves order-two element"
    ),
    description=(
      "If an element has exact order two "
      "and a scalar is congruent to one "
      "modulo two, then multiplying the "
      "element by that scalar gives the "
      "same element."
    ),
    premise_patterns=(
      PremisePattern(
        relation_pattern=Relation(
          lhs=element,
          rhs=2,
          relation_type=RelationType.ORDER,
        ),
      ),
      PremisePattern(
        statement_pattern=(
          ScalarCongruenceStatement(
            scalar=scalar,
            residue=1,
            modulus=2,
          )
        ),
      ),
    ),
    conclusion_pattern=Relation(
      lhs=Multiple(
        coefficient=scalar,
        expression=element,
      ),
      rhs=element,
      relation_type=RelationType.EQUALITY,
    ),
  )




