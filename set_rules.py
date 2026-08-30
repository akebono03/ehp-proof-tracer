from dataclasses import dataclass

from algebra import Subgroup
from expression import Expression
from proof import (
  InferenceRule,
  PatternVariable,
  PremisePattern,
)


@dataclass(frozen=True)
class MembershipStatement:
  element: Expression
  subgroup: Subgroup


@dataclass(frozen=True)
class SubsetStatement:
  subset: Subgroup
  superset: Subgroup


def membership_subset_propagation_inference_rule():
  element = PatternVariable(
    name="element",
  )

  subset = PatternVariable(
    name="subset",
  )

  superset = PatternVariable(
    name="superset",
  )

  return InferenceRule(
    name="membership subset propagation",
    description=(
      "If an element belongs to a subgroup "
      "and that subgroup is contained in another "
      "subgroup, then the element belongs to the "
      "larger subgroup."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=MembershipStatement,
        statement_pattern=MembershipStatement(
          element=element,
          subgroup=subset,
        ),
      ),
      PremisePattern(
        statement_type=SubsetStatement,
        statement_pattern=SubsetStatement(
          subset=subset,
          superset=superset,
        ),
      ),
    ),
    conclusion_pattern=MembershipStatement(
      element=element,
      subgroup=superset,
    ),
  )









