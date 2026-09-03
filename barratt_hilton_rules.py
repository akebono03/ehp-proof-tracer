from dataclasses import dataclass

from expression import (
  Composition,
  HomotopyElement,
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
  PremisePattern,
  Relation,
  RelationType,
)


@dataclass(frozen=True)
class HomotopyGroupMembershipStatement:
  element: HomotopyElement
  group_dimension: ScalarValue
  sphere_dimension: ScalarValue


def barratt_hilton_first_inference_rule(
  alpha,
  beta,
  p,
  q,
  k,
  h,
):
  expected_alpha_membership = (
    HomotopyGroupMembershipStatement(
      element=alpha,
      group_dimension=ScalarSum(
        left=p,
        right=k,
      ),
      sphere_dimension=p,
    )
  )

  expected_beta_membership = (
    HomotopyGroupMembershipStatement(
      element=beta,
      group_dimension=ScalarSum(
        left=q,
        right=h,
      ),
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
    p_plus_k = ScalarSum(
      left=p,
      right=k,
    )

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




