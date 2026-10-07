from expression import (
  IteratedSuspension,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  InferenceRule,
  PremisePattern,
  ProofRule,
  Relation,
  RelationType,
)
from toda_rules import (
  TodaSigmaFamilyDefinitionStatement,
)


def toda_sigma_transport_generator_normalization_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    transported_relation = (
      premises[
        0
      ].conclusion
    )
    first_definition = (
      premises[
        1
      ].conclusion
    )
    second_definition = (
      premises[
        2
      ].conclusion
    )

    definitions = (
      first_definition,
      second_definition,
    )

    sigma9_matches = tuple(
      statement
      for statement in definitions
      if statement.index == 9
    )

    symbolic_matches = tuple(
      statement
      for statement in definitions
      if isinstance(
        statement.index,
        ScalarSymbol,
      )
    )

    if len(sigma9_matches) != 1:
      return False

    if len(symbolic_matches) != 1:
      return False

    sigma9_definition = (
      sigma9_matches[
        0
      ]
    )
    sigma_family = (
      symbolic_matches[
        0
      ]
    )

    if (
      sigma9_definition.sigma8_statement
      != sigma_family.sigma8_statement
    ):
      return False

    if not isinstance(
      transported_relation.lhs,
      TodaPrimaryGroup,
    ):
      return False

    if not isinstance(
      transported_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    generator = (
      transported_relation
      .rhs
      .generator
    )

    if not isinstance(
      generator,
      IteratedSuspension,
    ):
      return False

    if (
      generator.expression
      != sigma9_definition.element
    ):
      return False

    n = sigma_family.index

    if (
      generator.exponent
      != ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=9,
        ),
      )
    ):
      return False

    if (
      transported_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=7,
        ),
        sphere_dimension=n,
      )
    ):
      return False

    if (
      sigma_family.element.source
      != ScalarSum(
        left=n,
        right=7,
      )
    ):
      return False

    return (
      sigma_family.element.target
      == n
    )

  def build_conclusion(
    premises,
  ):
    transported_relation = (
      premises[
        0
      ].conclusion
    )
    definitions = (
      premises[
        1
      ].conclusion,
      premises[
        2
      ].conclusion,
    )

    sigma_family = next(
      statement
      for statement in definitions
      if isinstance(
        statement.index,
        ScalarSymbol,
      )
    )

    return Relation(
      lhs=transported_relation.lhs,
      rhs=FiniteCyclicGroup(
        order=(
          transported_relation
          .rhs
          .order
        ),
        generator=sigma_family.element,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda sigma-family "
      "transported-generator normalization"
    ),
    description=(
      "Normalize the generator of a finite-cyclic "
      "group already transported from sigma_9 "
      "through E^(n-9) to the named sigma_n "
      "generator, using independently derived "
      "sigma-family definitions for sigma_9 "
      "and sigma_n. The cyclic order and target "
      "group are preserved. This rule performs "
      "generator normalization only and does not "
      "derive the group transport itself."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaSigmaFamilyDefinitionStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaSigmaFamilyDefinitionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )
