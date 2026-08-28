from expression import (
  Composition,
  Multiple,
  Sum,
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


def additive_inverse_inference_rule(
  expression,
):
  return InferenceRule(
    name="additive inverse implies zero",
    description=(
      "An expression added to its "
      "additive inverse is zero."
    ),
    conclusion_pattern=Relation(
      lhs=Sum(
        left=expression,
        right=Multiple(
          coefficient=-1,
          expression=expression,
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
  )


def sum_commutativity_inference_rule(
  left,
  right,
):
  return InferenceRule(
    name="sum commutativity",
    description=(
      "The sum of two expressions is equal "
      "to the sum with operands reversed."
    ),
    conclusion_pattern=Relation(
      lhs=Sum(
        left=left,
        right=right,
      ),
      rhs=Sum(
        left=right,
        right=left,
      ),
      relation_type=RelationType.EQUALITY,
    ),
  )


def sum_associativity_inference_rule(
  left,
  middle,
  right,
):
  return InferenceRule(
    name="sum associativity",
    description=(
      "A nested sum is equal to the "
      "corresponding reassociated sum."
    ),
    conclusion_pattern=Relation(
      lhs=Sum(
        left=Sum(
          left=left,
          right=middle,
        ),
        right=right,
      ),
      rhs=Sum(
        left=left,
        right=Sum(
          left=middle,
          right=right,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    ),
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


def composition_equality_to_zero_inference_rule():
  composition = PatternVariable(
    name="composition",
  )

  def guard(
    premises,
    bindings,
  ):
    bound_composition = (
      lookup_variable_binding(
        composition,
        bindings,
      )
    )

    return isinstance(
      bound_composition,
      Composition,
    )

  return InferenceRule(
    name="composition equality to zero",
    description=(
      "If a composition is equal to zero, "
      "the composition is a generic zero "
      "relation."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.EQUALITY,
        relation_pattern=Relation(
          lhs=composition,
          rhs=Zero(),
          relation_type=RelationType.EQUALITY,
        ),
      ),
    ),
    conclusion_pattern=Relation(
      lhs=composition,
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    match_guard=guard,
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


def suspension_composition_functoriality_inference_rule():
  composition_expression = PatternVariable(
    name="composition_expression",
  )

  result_expression = PatternVariable(
    name="result_expression",
  )

  def guard(
    premises,
    bindings,
  ):
    bound_composition = (
      lookup_variable_binding(
        composition_expression,
        bindings,
      )
    )

    return isinstance(
      bound_composition,
      Composition,
    )

  def conclusion_builder(
    premises,
  ):
    premise_relation = (
      premises[0].conclusion
    )

    composition = premise_relation.lhs

    return Relation(
      lhs=Suspension(
        expression=composition,
      ),
      rhs=Composition(
        left=Suspension(
          expression=composition.left,
        ),
        right=Suspension(
          expression=composition.right,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "suspension composition "
      "functoriality"
    ),
    description=(
      "The suspension of a composition "
      "is equal to the composition of "
      "the suspended expressions."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.EQUALITY,
        relation_pattern=Relation(
          lhs=composition_expression,
          rhs=result_expression,
          relation_type=RelationType.EQUALITY,
        ),
      ),
    ),
    conclusion_builder=conclusion_builder,
    match_guard=guard,
  )


def suspension_preserves_zero_inference_rule():
  expression = PatternVariable(
    name="expression",
  )

  return InferenceRule(
    name="suspension preserves zero",
    description=(
      "If an expression is zero, "
      "its suspension is also zero."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.ZERO,
        relation_pattern=Relation(
          lhs=expression,
          rhs=Zero(),
          relation_type=RelationType.ZERO,
        ),
      ),
    ),
    conclusion_pattern=Relation(
      lhs=Suspension(
        expression=expression,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
  )


def suspension_preserves_zero_multiple_inference_rule():
  multiple_expression = PatternVariable(
    name="multiple_expression",
  )

  def guard(
    premises,
    bindings,
  ):
    bound_multiple_expression = (
      lookup_variable_binding(
        multiple_expression,
        bindings,
      )
    )

    return isinstance(
      bound_multiple_expression,
      Multiple,
    )

  def conclusion_builder(
    premises,
  ):
    premise_relation = (
      premises[0].conclusion
    )

    multiple = premise_relation.lhs

    return Relation(
      lhs=Multiple(
        coefficient=multiple.coefficient,
        expression=Suspension(
          expression=multiple.expression,
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name="suspension preserves zero multiple",
    description=(
      "If a multiple of an expression "
      "is zero, the same multiple of "
      "its suspension is also zero."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.ZERO,
        relation_pattern=Relation(
          lhs=multiple_expression,
          rhs=Zero(),
          relation_type=RelationType.ZERO,
        ),
      ),
    ),
    conclusion_builder=conclusion_builder,
    match_guard=guard,
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








