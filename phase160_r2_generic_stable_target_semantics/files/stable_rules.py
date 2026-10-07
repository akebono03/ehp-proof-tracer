from dataclasses import dataclass

from expression import (
  Expression,
  Zero,
)
from homotopy_groups import (
  TodaPrimaryGroup,
)
from proof import (
  InferenceRule,
  PremisePattern,
  Relation,
  RelationType,
)


@dataclass(frozen=True)
class SuspensionMapStatement:
  sphere_dimension: int
  stem: int


@dataclass(frozen=True)
class SuspensionIsomorphismStatement:
  suspension_map: SuspensionMapStatement


@dataclass(frozen=True)
class SuspensionEpimorphismStatement:
  suspension_map: SuspensionMapStatement


@dataclass(frozen=True)
class SuspensionInjectiveStatement:
  suspension_map: SuspensionMapStatement


@dataclass(frozen=True)
class SuspensionMapEqualityStatement:
  suspension_map: SuspensionMapStatement
  lhs: Expression
  rhs: Expression


@dataclass(frozen=True)
class SuspensionMapZeroStatement:
  suspension_map: SuspensionMapStatement
  expression: Expression


def _concrete_toda_primary_group_dimensions(
  target: TodaPrimaryGroup,
) -> tuple[int, int]:
  if not isinstance(
    target,
    TodaPrimaryGroup,
  ):
    raise TypeError(
      "target must be a TodaPrimaryGroup"
    )

  group_dimension = target.group_dimension
  sphere_dimension = target.sphere_dimension

  if (
    not isinstance(group_dimension, int)
    or isinstance(group_dimension, bool)
    or not isinstance(sphere_dimension, int)
    or isinstance(sphere_dimension, bool)
  ):
    raise TypeError(
      "target dimensions must be concrete integers"
    )

  if group_dimension < sphere_dimension:
    raise ValueError(
      "target must have nonnegative stem"
    )

  return (
    group_dimension,
    sphere_dimension,
  )


def toda_primary_group_stem(
  target: TodaPrimaryGroup,
) -> int:
  group_dimension, sphere_dimension = (
    _concrete_toda_primary_group_dimensions(
      target
    )
  )

  return (
    group_dimension
    - sphere_dimension
  )


def is_in_toda_stable_range(
  target: TodaPrimaryGroup,
) -> bool:
  _, sphere_dimension = (
    _concrete_toda_primary_group_dimensions(
      target
    )
  )
  stem = toda_primary_group_stem(
    target
  )

  return (
    sphere_dimension
    >= stem + 2
  )


def canonical_toda_stable_base(
  target: TodaPrimaryGroup,
) -> TodaPrimaryGroup:
  stem = toda_primary_group_stem(
    target
  )
  base_sphere_dimension = (
    stem + 2
  )

  return TodaPrimaryGroup(
    group_dimension=(
      base_sphere_dimension
      + stem
    ),
    sphere_dimension=(
      base_sphere_dimension
    ),
  )


def toda_stable_transport_exponent(
  target: TodaPrimaryGroup,
) -> int:
  if not is_in_toda_stable_range(
    target
  ):
    raise ValueError(
      "target is outside the Toda stable range"
    )

  base = canonical_toda_stable_base(
    target
  )

  return (
    target.sphere_dimension
    - base.sphere_dimension
  )


def is_freudenthal_stable_range(
  statement,
):
  return (
    statement.stem
    <= statement.sphere_dimension - 2
  )


def is_freudenthal_boundary_range(
  statement,
):
  return (
    statement.stem
    == statement.sphere_dimension - 1
  )


def freudenthal_stable_isomorphism_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    statement = premises[0].conclusion

    return is_freudenthal_stable_range(
      statement,
    )

  def build_conclusion(
    premises,
  ):
    return SuspensionIsomorphismStatement(
      suspension_map=(
        premises[0].conclusion
      ),
    )

  return InferenceRule(
    name=(
      "Freudenthal stable range "
      "implies suspension isomorphism"
    ),
    description=(
      "A suspension map in the "
      "Freudenthal stable range is "
      "an isomorphism."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          SuspensionMapStatement
        ),
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
    match_guard=guard,
  )


def freudenthal_boundary_epimorphism_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    statement = premises[0].conclusion

    return is_freudenthal_boundary_range(
      statement,
    )

  def build_conclusion(
    premises,
  ):
    return SuspensionEpimorphismStatement(
      suspension_map=(
        premises[0].conclusion
      ),
    )

  return InferenceRule(
    name=(
      "Freudenthal boundary range "
      "implies suspension epimorphism"
    ),
    description=(
      "A suspension map in the "
      "Freudenthal boundary range is "
      "an epimorphism."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          SuspensionMapStatement
        ),
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
    match_guard=guard,
  )


def suspension_isomorphism_implies_injective_inference_rule():
  def build_conclusion(
    premises,
  ):
    statement = premises[0].conclusion

    return SuspensionInjectiveStatement(
      suspension_map=(
        statement.suspension_map
      ),
    )

  return InferenceRule(
    name=(
      "Suspension isomorphism "
      "implies injectivity"
    ),
    description=(
      "An isomorphic suspension map "
      "is injective."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          SuspensionIsomorphismStatement
        ),
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
  )


def suspension_injectivity_reflects_equality_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    injective_statement = (
      premises[0].conclusion
    )

    equality_statement = (
      premises[1].conclusion
    )

    return (
      injective_statement.suspension_map
      == equality_statement.suspension_map
    )

  def build_conclusion(
    premises,
  ):
    equality_statement = (
      premises[1].conclusion
    )

    return Relation(
      lhs=equality_statement.lhs,
      rhs=equality_statement.rhs,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Suspension injectivity "
      "reflects equality"
    ),
    description=(
      "If an injective suspension map "
      "sends two elements to equal "
      "elements, then the original "
      "elements are equal."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          SuspensionInjectiveStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          SuspensionMapEqualityStatement
        ),
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
    match_guard=guard,
  )


def suspension_injectivity_reflects_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    injective_statement = (
      premises[0].conclusion
    )

    zero_statement = (
      premises[1].conclusion
    )

    return (
      injective_statement.suspension_map
      == zero_statement.suspension_map
    )

  def build_conclusion(
    premises,
  ):
    zero_statement = (
      premises[1].conclusion
    )

    return Relation(
      lhs=zero_statement.expression,
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Suspension injectivity "
      "reflects zero"
    ),
    description=(
      "If an injective suspension map "
      "sends an element to zero, then "
      "the original element is zero."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          SuspensionInjectiveStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          SuspensionMapZeroStatement
        ),
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
    match_guard=guard,
  )
