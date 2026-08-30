from dataclasses import dataclass

from expression import ScalarSymbol
from proof import (
  InferenceRule,
  PremisePattern,
)


@dataclass(frozen=True)
class OddScalarStatement:
  scalar: ScalarSymbol


@dataclass(frozen=True)
class EvenScalarStatement:
  scalar: ScalarSymbol


@dataclass(frozen=True)
class ScalarCongruenceStatement:
  scalar: ScalarSymbol
  residue: int
  modulus: int


def odd_scalar_implies_mod_two_congruence_inference_rule():
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
      "An odd integer scalar is "
      "congruent to one modulo two."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=OddScalarStatement,
      ),
    ),
    conclusion_builder=build_conclusion,
  )


def even_scalar_implies_mod_two_congruence_inference_rule():
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
      "An even integer scalar is "
      "congruent to zero modulo two."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=EvenScalarStatement,
      ),
    ),
    conclusion_builder=build_conclusion,
  )




