from dataclasses import dataclass

from proof import (
  InferenceRule,
  PremisePattern,
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








