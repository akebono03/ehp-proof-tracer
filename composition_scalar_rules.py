from dataclasses import dataclass

from expression import (
  Composition,
  Expression,
  HomotopyElement,
  Multiple,
)
from proof import (
  InferenceRule,
  LiteratureReference,
  PremisePattern,
  Relation,
  RelationType,
)


TODA_2_1_REFERENCE = LiteratureReference(
  label="Toda (2.1)",
  author="H. Toda",
  title=(
    "Composition Methods in "
    "Homotopy Groups of Spheres"
  ),
  year=1962,
  locator="(2.1)",
)


@dataclass(frozen=True)
class IdentityMapStatement:
  element: HomotopyElement


def toda_2_1_right_multiple_inference_rule(
  left,
  right,
  coefficient,
):
  if (
    isinstance(
      coefficient,
      bool,
    )
    or not isinstance(
      coefficient,
      int,
    )
  ):
    raise TypeError(
      "Toda (2.1) right multiple "
      "requires an integer coefficient"
    )

  return InferenceRule(
    name="Toda (2.1) right multiple",
    description=(
      "Toda (2.1): "
      "a composed with k times b "
      "equals k times a composed with b."
    ),
    conclusion_pattern=Relation(
      lhs=Composition(
        left=left,
        right=Multiple(
          coefficient=coefficient,
          expression=right,
        ),
      ),
      rhs=Multiple(
        coefficient=coefficient,
        expression=Composition(
          left=left,
          right=right,
        ),
      ),
      relation_type=RelationType.EQUALITY,
      source=TODA_2_1_REFERENCE,
      note=(
        "Toda (2.1) integer scalar "
        "law on the right factor."
      ),
    ),
  )


def right_identity_composition_inference_rule(
  expression,
):
  def conclusion_builder(
    premises,
  ):
    identity_statement = (
      premises[0].conclusion
    )

    return Relation(
      lhs=Composition(
        left=expression,
        right=identity_statement.element,
      ),
      rhs=expression,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name="right identity composition",
    description=(
      "Composition on the right by an "
      "explicit identity-map fact leaves "
      "the expression unchanged."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=IdentityMapStatement,
      ),
    ),
    conclusion_builder=conclusion_builder,
  )


