from expression import (
  IteratedSuspension,
  ScalarSum,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  InferenceRule,
  PremisePattern,
  Relation,
  RelationType,
)
from toda_rules import (
  Toda45IsomorphismStatement,
)


def _concrete_toda_group_matches_structural_group(
  concrete_group: TodaPrimaryGroup,
  structural_group: TodaPrimaryGroup,
) -> bool:
  if not isinstance(
    concrete_group,
    TodaPrimaryGroup,
  ):
    return False

  if not isinstance(
    structural_group,
    TodaPrimaryGroup,
  ):
    return False

  if not isinstance(
    concrete_group.group_dimension,
    int,
  ):
    return (
      concrete_group
      == structural_group
    )

  if not isinstance(
    concrete_group.sphere_dimension,
    int,
  ):
    return (
      concrete_group
      == structural_group
    )

  if (
    structural_group.sphere_dimension
    != concrete_group.sphere_dimension
  ):
    return False

  structural_dimension = (
    structural_group.group_dimension
  )

  if isinstance(
    structural_dimension,
    int,
  ):
    return (
      structural_dimension
      == concrete_group.group_dimension
    )

  if not isinstance(
    structural_dimension,
    ScalarSum,
  ):
    return False

  if not isinstance(
    structural_dimension.left,
    int,
  ):
    return False

  if not isinstance(
    structural_dimension.right,
    int,
  ):
    return False

  return (
    structural_dimension.left
    + structural_dimension.right
    == concrete_group.group_dimension
  )


def toda_45_generic_finite_cyclic_transport_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    source_relation = (
      premises[
        0
      ].conclusion
    )
    isomorphism = (
      premises[
        1
      ].conclusion
    )

    if not isinstance(
      source_relation.lhs,
      TodaPrimaryGroup,
    ):
      return False

    if not isinstance(
      source_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    transport_map = (
      isomorphism.map
    )

    return (
      _concrete_toda_group_matches_structural_group(
        source_relation.lhs,
        transport_map.source_group,
      )
    )

  def build_conclusion(
    premises,
  ):
    source_relation = (
      premises[
        0
      ].conclusion
    )
    isomorphism = (
      premises[
        1
      ].conclusion
    )
    transport_map = (
      isomorphism.map
    )

    return Relation(
      lhs=transport_map.target_group,
      rhs=FiniteCyclicGroup(
        order=source_relation.rhs.order,
        generator=IteratedSuspension(
          expression=(
            source_relation
            .rhs
            .generator
          ),
          exponent=(
            transport_map
            .exponent
          ),
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda 4.5 generic "
      "finite-cyclic transport"
    ),
    description=(
      "Transport a finite cyclic "
      "Toda primary group through "
      "a supplied Toda (4.5) "
      "iterated-suspension isomorphism. "
      "The group order is preserved, "
      "and the target generator is kept "
      "as the iterated suspension of "
      "the source generator. "
      "No generator-family "
      "normalization is performed."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        statement_type=(
          Toda45IsomorphismStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )
