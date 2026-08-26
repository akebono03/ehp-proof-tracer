from expression import (
  Composition,
  Zero,
)
from proof import (
  InferenceRule,
  PatternVariable,
  PremisePattern,
  Relation,
  RelationType,
  lookup_variable_binding,
)


def zero_composition_equality_implies_zero_inference_rule():
  zero_expression = PatternVariable(
    name="zero_expression",
  )

  equivalent_expression = PatternVariable(
    name="equivalent_expression",
  )

  def guard(
    premises,
    bindings,
  ):
    bound_zero_expression = (
      lookup_variable_binding(
        zero_expression,
        bindings,
      )
    )

    return isinstance(
      bound_zero_expression,
      Composition,
    )

  return InferenceRule(
    name=(
      "zero composition equality "
      "implies zero"
    ),
    description=(
      "If a composition is zero and "
      "another expression is equal to "
      "that composition, the other "
      "expression is also zero."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.ZERO,
        relation_pattern=Relation(
          lhs=zero_expression,
          rhs=Zero(),
          relation_type=RelationType.ZERO,
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.EQUALITY,
        relation_pattern=Relation(
          lhs=equivalent_expression,
          rhs=zero_expression,
          relation_type=RelationType.EQUALITY,
        ),
      ),
    ),
    conclusion_pattern=Relation(
      lhs=equivalent_expression,
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    match_guard=guard,
  )


def zero_composition_reverse_equality_implies_zero_inference_rule():
  zero_expression = PatternVariable(
    name="zero_expression",
  )

  equivalent_expression = PatternVariable(
    name="equivalent_expression",
  )

  def guard(
    premises,
    bindings,
  ):
    bound_zero_expression = (
      lookup_variable_binding(
        zero_expression,
        bindings,
      )
    )

    return isinstance(
      bound_zero_expression,
      Composition,
    )

  return InferenceRule(
    name=(
      "zero composition reverse equality "
      "implies zero"
    ),
    description=(
      "If a composition is zero and "
      "that composition is equal to "
      "another expression, the other "
      "expression is also zero."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.ZERO,
        relation_pattern=Relation(
          lhs=zero_expression,
          rhs=Zero(),
          relation_type=RelationType.ZERO,
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.EQUALITY,
        relation_pattern=Relation(
          lhs=zero_expression,
          rhs=equivalent_expression,
          relation_type=RelationType.EQUALITY,
        ),
      ),
    ),
    conclusion_pattern=Relation(
      lhs=equivalent_expression,
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    match_guard=guard,
  )






