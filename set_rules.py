from dataclasses import dataclass

from algebra import (
  GroupMap,
  Subgroup,
)
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


@dataclass(frozen=True)
class SubgroupEqualityStatement:
  left: Subgroup
  right: Subgroup


def kernel_membership_statement(
  element,
  group_map: GroupMap,
):
  return MembershipStatement(
    element=element,
    subgroup=group_map.kernel_subgroup(),
  )


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


def subgroup_equality_membership_propagation_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    membership_statement = (
      premises[0].conclusion
    )

    equality_statement = (
      premises[1].conclusion
    )

    return (
      membership_statement.subgroup
      == equality_statement.left
      or membership_statement.subgroup
      == equality_statement.right
    )

  def build_conclusion(
    premises,
  ):
    membership_statement = (
      premises[0].conclusion
    )

    equality_statement = (
      premises[1].conclusion
    )

    if (
      membership_statement.subgroup
      == equality_statement.left
    ):
      target_subgroup = (
        equality_statement.right
      )
    else:
      target_subgroup = (
        equality_statement.left
      )

    return MembershipStatement(
      element=membership_statement.element,
      subgroup=target_subgroup,
    )

  return InferenceRule(
    name="subgroup equality membership propagation",
    description=(
      "Membership transfers across an equality "
      "of subgroups."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=MembershipStatement,
      ),
      PremisePattern(
        statement_type=SubgroupEqualityStatement,
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
    match_guard=guard,
  )










