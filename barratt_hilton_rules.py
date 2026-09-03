from dataclasses import dataclass

from expression import (
  Composition,
  Expression,
  IteratedSuspension,
  Multiple,
  ScalarPower,
  ScalarProduct,
  ScalarSum,
  ScalarValue,
  SmashProduct,
)
from proof import (
  InferenceRule,
  LiteratureReference,
  PremisePattern,
  Relation,
  RelationType,
)


TODA_PROP_3_1_REFERENCE = LiteratureReference(
  label="Toda Prop.3.1",
  author="H. Toda",
  title=(
    "Composition Methods in "
    "Homotopy Groups of Spheres"
  ),
  year=1962,
  locator="Proposition 3.1",
)


@dataclass(frozen=True)
class HomotopyGroupMembershipStatement:
  element: Expression
  group_dimension: ScalarValue
  sphere_dimension: ScalarValue


def _barratt_hilton_scalar_sum(
  left,
  right,
):
  if (
    isinstance(
      left,
      int,
    )
    and isinstance(
      right,
      int,
    )
  ):
    return left + right

  return ScalarSum(
    left=left,
    right=right,
  )


def barratt_hilton_first_inference_rule(
  alpha,
  beta,
  p,
  q,
  k,
  h,
):
  p_plus_k = (
    _barratt_hilton_scalar_sum(
      p,
      k,
    )
  )

  q_plus_h = (
    _barratt_hilton_scalar_sum(
      q,
      h,
    )
  )

  expected_alpha_membership = (
    HomotopyGroupMembershipStatement(
      element=alpha,
      group_dimension=p_plus_k,
      sphere_dimension=p,
    )
  )

  expected_beta_membership = (
    HomotopyGroupMembershipStatement(
      element=beta,
      group_dimension=q_plus_h,
      sphere_dimension=q,
    )
  )

  def guard(
    premises,
    bindings,
  ):
    conclusions = tuple(
      premise.conclusion
      for premise in premises
    )

    return (
      expected_alpha_membership
      in conclusions
      and expected_beta_membership
      in conclusions
    )

  def conclusion_builder(
    premises,
  ):
    sign_exponent = ScalarProduct(
      left=p_plus_k,
      right=h,
    )

    sign = ScalarPower(
      base=-1,
      exponent=sign_exponent,
    )

    composition = Composition(
      left=IteratedSuspension(
        expression=alpha,
        exponent=q,
      ),
      right=IteratedSuspension(
        expression=beta,
        exponent=p_plus_k,
      ),
    )

    return Relation(
      lhs=SmashProduct(
        left=alpha,
        right=beta,
      ),
      rhs=Multiple(
        coefficient=sign,
        expression=composition,
      ),
      relation_type=RelationType.EQUALITY,
      source=TODA_PROP_3_1_REFERENCE,
      note=(
        "Toda Prop.3.1 "
        "Barratt-Hilton first formula."
      ),
    )

  return InferenceRule(
    name=(
      "Toda Prop.3.1 "
      "Barratt-Hilton first formula"
    ),
    description=(
      "If alpha is in pi_(p+k)(S^p) "
      "and beta is in pi_(q+h)(S^q), "
      "Toda Prop.3.1 gives the first "
      "Barratt-Hilton formula."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          HomotopyGroupMembershipStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          HomotopyGroupMembershipStatement
        ),
      ),
    ),
    conclusion_builder=conclusion_builder,
    match_guard=guard,
  )


def barratt_hilton_second_inference_rule(
  alpha,
  beta,
  p,
  q,
  k,
  h,
):
  p_plus_k = (
    _barratt_hilton_scalar_sum(
      p,
      k,
    )
  )

  q_plus_h = (
    _barratt_hilton_scalar_sum(
      q,
      h,
    )
  )

  expected_alpha_membership = (
    HomotopyGroupMembershipStatement(
      element=alpha,
      group_dimension=p_plus_k,
      sphere_dimension=p,
    )
  )

  expected_beta_membership = (
    HomotopyGroupMembershipStatement(
      element=beta,
      group_dimension=q_plus_h,
      sphere_dimension=q,
    )
  )

  def guard(
    premises,
    bindings,
  ):
    conclusions = tuple(
      premise.conclusion
      for premise in premises
    )

    return (
      expected_alpha_membership
      in conclusions
      and expected_beta_membership
      in conclusions
    )

  def conclusion_builder(
    premises,
  ):
    sign_exponent = ScalarProduct(
      left=p,
      right=h,
    )

    sign = ScalarPower(
      base=-1,
      exponent=sign_exponent,
    )

    composition = Composition(
      left=IteratedSuspension(
        expression=beta,
        exponent=p,
      ),
      right=IteratedSuspension(
        expression=alpha,
        exponent=q_plus_h,
      ),
    )

    return Relation(
      lhs=SmashProduct(
        left=alpha,
        right=beta,
      ),
      rhs=Multiple(
        coefficient=sign,
        expression=composition,
      ),
      relation_type=RelationType.EQUALITY,
      source=TODA_PROP_3_1_REFERENCE,
      note=(
        "Toda Prop.3.1 "
        "Barratt-Hilton second formula."
      ),
    )

  return InferenceRule(
    name=(
      "Toda Prop.3.1 "
      "Barratt-Hilton second formula"
    ),
    description=(
      "If alpha is in pi_(p+k)(S^p) "
      "and beta is in pi_(q+h)(S^q), "
      "Toda Prop.3.1 gives the second "
      "Barratt-Hilton formula."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          HomotopyGroupMembershipStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          HomotopyGroupMembershipStatement
        ),
      ),
    ),
    conclusion_builder=conclusion_builder,
    match_guard=guard,
  )



