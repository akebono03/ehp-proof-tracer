from dataclasses import dataclass

from expression import (
  Expression,
)
from proof import (
  InferenceRule,
  PatternVariable,
  PremisePattern,
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



