from dataclasses import dataclass

from algebra import (
  GroupMap,
  Subgroup,
)
from expression import (
  Expression,
  MapApplication,
  MapSymbol,
  Zero,
)
from proof import (
  ExactnessStatement,
  InferenceRule,
  PatternVariable,
  PremisePattern,
  Relation,
  RelationType,
)


@dataclass(frozen=True)
class ImageSubgroupReference:
  group_map: GroupMap

  @property
  def subgroup(
    self,
  ) -> Subgroup:
    return self.group_map.image_subgroup()


@dataclass(frozen=True)
class KernelSubgroupReference:
  group_map: GroupMap

  @property
  def subgroup(
    self,
  ) -> Subgroup:
    return self.group_map.kernel_subgroup()


SubgroupTerm = (
  Subgroup
  | ImageSubgroupReference
  | KernelSubgroupReference
)


@dataclass(frozen=True)
class MembershipStatement:
  element: Expression
  subgroup: SubgroupTerm


@dataclass(frozen=True)
class SubsetStatement:
  subset: SubgroupTerm
  superset: SubgroupTerm


@dataclass(frozen=True)
class SubgroupEqualityStatement:
  left: SubgroupTerm
  right: SubgroupTerm


def kernel_membership_statement(
  element,
  group_map: GroupMap,
):
  return MembershipStatement(
    element=element,
    subgroup=KernelSubgroupReference(
      group_map=group_map,
    ),
  )


def image_membership_statement(
  element,
  group_map: GroupMap,
):
  return MembershipStatement(
    element=element,
    subgroup=ImageSubgroupReference(
      group_map=group_map,
    ),
  )


def kernel_membership_implies_mapped_zero_inference_rule(
  group_map: GroupMap,
  map_symbol: MapSymbol,
):
  element = PatternVariable(
    name="element",
  )

  def build_conclusion(
    premises,
  ):
    membership_statement = (
      premises[0].conclusion
    )

    return Relation(
      lhs=MapApplication(
        map=map_symbol,
        expression=membership_statement.element,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name="kernel membership implies mapped zero",
    description=(
      "An element in the kernel of a map "
      "is mapped to zero."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=MembershipStatement,
        statement_pattern=kernel_membership_statement(
          element=element,
          group_map=group_map,
        ),
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
  )


def mapped_zero_implies_kernel_membership_inference_rule(
  group_map: GroupMap,
  map_symbol: MapSymbol,
):
  def guard(
    premises,
    bindings,
  ):
    relation = premises[0].conclusion

    return (
      isinstance(
        relation.lhs,
        MapApplication,
      )
      and relation.lhs.map == map_symbol
      and relation.rhs == Zero()
    )

  def build_conclusion(
    premises,
  ):
    relation = premises[0].conclusion

    return kernel_membership_statement(
      element=relation.lhs.expression,
      group_map=group_map,
    )

  return InferenceRule(
    name="mapped zero implies kernel membership",
    description=(
      "If a map sends an element to zero, "
      "then the element belongs to the kernel "
      "of that map."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.ZERO,
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
    match_guard=guard,
  )


def exactness_implies_subgroup_equality_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    exactness_statement = (
      premises[0].conclusion
    )

    return (
      exactness_statement.is_exact
      is True
    )

  def build_conclusion(
    premises,
  ):
    exactness_statement = (
      premises[0].conclusion
    )

    return SubgroupEqualityStatement(
      left=ImageSubgroupReference(
        group_map=(
          exactness_statement.first_map
        ),
      ),
      right=KernelSubgroupReference(
        group_map=(
          exactness_statement.second_map
        ),
      ),
    )

  return InferenceRule(
    name="exactness implies subgroup equality",
    description=(
      "Exactness of consecutive maps means "
      "that the image of the first map equals "
      "the kernel of the second map."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=ExactnessStatement,
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
    match_guard=guard,
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


def subgroup_equality_symmetry_inference_rule():
  left = PatternVariable(
    name="left",
  )

  right = PatternVariable(
    name="right",
  )

  return InferenceRule(
    name="subgroup equality symmetry",
    description=(
      "Equality of subgroup terms is symmetric."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=SubgroupEqualityStatement,
        statement_pattern=SubgroupEqualityStatement(
          left=left,
          right=right,
        ),
      ),
    ),
    conclusion_pattern=SubgroupEqualityStatement(
      left=right,
      right=left,
    ),
  )


def subgroup_equality_transitivity_inference_rule():
  left = PatternVariable(
    name="left",
  )

  middle = PatternVariable(
    name="middle",
  )

  right = PatternVariable(
    name="right",
  )

  return InferenceRule(
    name="subgroup equality transitivity",
    description=(
      "Equality of subgroup terms is transitive."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=SubgroupEqualityStatement,
        statement_pattern=SubgroupEqualityStatement(
          left=left,
          right=middle,
        ),
      ),
      PremisePattern(
        statement_type=SubgroupEqualityStatement,
        statement_pattern=SubgroupEqualityStatement(
          left=middle,
          right=right,
        ),
      ),
    ),
    conclusion_pattern=SubgroupEqualityStatement(
      left=left,
      right=right,
    ),
  )


def subset_transitivity_inference_rule():
  subset = PatternVariable(
    name="subset",
  )

  middle = PatternVariable(
    name="middle",
  )

  superset = PatternVariable(
    name="superset",
  )

  return InferenceRule(
    name="subset transitivity",
    description=(
      "Containment of subgroup terms is transitive."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=SubsetStatement,
        statement_pattern=SubsetStatement(
          subset=subset,
          superset=middle,
        ),
      ),
      PremisePattern(
        statement_type=SubsetStatement,
        statement_pattern=SubsetStatement(
          subset=middle,
          superset=superset,
        ),
      ),
    ),
    conclusion_pattern=SubsetStatement(
      subset=subset,
      superset=superset,
    ),
  )





