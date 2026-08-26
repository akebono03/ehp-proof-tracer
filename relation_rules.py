from expression import (
  Composition,
  Multiple,
  Suspension,
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


def order_implies_zero_multiple_inference_rule():
  element = PatternVariable(
    name="element",
  )

  order = PatternVariable(
    name="order",
  )

  def guard(
    premises,
    bindings,
  ):
    bound_order = (
      lookup_variable_binding(
        order,
        bindings,
      )
    )

    return (
      not isinstance(
        bound_order,
        bool,
      )
      and isinstance(
        bound_order,
        int,
      )
      and bound_order > 0
    )

  return InferenceRule(
    name="order implies zero multiple",
    description=(
      "If an element has exact additive "
      "order n, then n times that element "
      "is zero."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.ORDER,
        relation_pattern=Relation(
          lhs=element,
          rhs=order,
          relation_type=RelationType.ORDER,
        ),
      ),
    ),
    conclusion_pattern=Relation(
      lhs=Multiple(
        coefficient=order,
        expression=element,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    match_guard=guard,
  )


def zero_equality_implies_zero_inference_rule():
  zero_expression = PatternVariable(
    name="zero_expression",
  )

  equivalent_expression = PatternVariable(
    name="equivalent_expression",
  )

  return InferenceRule(
    name="zero equality implies zero",
    description=(
      "If an expression is zero and "
      "another expression is equal to "
      "that expression, the other "
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


def suspension_preserves_equality_inference_rule():
  left_expression = PatternVariable(
    name="left_expression",
  )

  right_expression = PatternVariable(
    name="right_expression",
  )

  return InferenceRule(
    name="suspension preserves equality",
    description=(
      "If two expressions are equal, "
      "their suspensions are also equal."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.EQUALITY,
        relation_pattern=Relation(
          lhs=left_expression,
          rhs=right_expression,
          relation_type=RelationType.EQUALITY,
        ),
      ),
    ),
    conclusion_pattern=Relation(
      lhs=Suspension(
        expression=left_expression,
      ),
      rhs=Suspension(
        expression=right_expression,
      ),
      relation_type=RelationType.EQUALITY,
    ),
  )


def equality_symmetry_inference_rule():
  left_expression = PatternVariable(
    name="left_expression",
  )

  right_expression = PatternVariable(
    name="right_expression",
  )

  return InferenceRule(
    name="equality symmetry",
    description=(
      "If one expression is equal to "
      "another expression, the reverse "
      "equality also holds."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.EQUALITY,
        relation_pattern=Relation(
          lhs=left_expression,
          rhs=right_expression,
          relation_type=RelationType.EQUALITY,
        ),
      ),
    ),
    conclusion_pattern=Relation(
      lhs=right_expression,
      rhs=left_expression,
      relation_type=RelationType.EQUALITY,
    ),
  )


def equality_transitivity_inference_rule():
  left_expression = PatternVariable(
    name="left_expression",
  )

  middle_expression = PatternVariable(
    name="middle_expression",
  )

  right_expression = PatternVariable(
    name="right_expression",
  )

  return InferenceRule(
    name="equality transitivity",
    description=(
      "If one expression is equal to "
      "a second expression and the "
      "second expression is equal to "
      "a third expression, the first "
      "expression is equal to the third."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.EQUALITY,
        relation_pattern=Relation(
          lhs=left_expression,
          rhs=middle_expression,
          relation_type=RelationType.EQUALITY,
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.EQUALITY,
        relation_pattern=Relation(
          lhs=middle_expression,
          rhs=right_expression,
          relation_type=RelationType.EQUALITY,
        ),
      ),
    ),
    conclusion_pattern=Relation(
      lhs=left_expression,
      rhs=right_expression,
      relation_type=RelationType.EQUALITY,
    ),
  )








