from expression import (
  Multiple,
)
from homotopy_groups import (
  FiniteCyclicGroup,
)
from proof import (
  Relation,
  RelationType,
  find_inference_match,
)
from tests.test_phase65_nu_prime_order_pi6_3 import (
  build_phase65_4_data,
)
from toda_rules import (
  TodaSuspensionInjectiveStatement,
)


def _rule_name(step):
  rule = step.inference_rule
  return None if rule is None else rule.name


def main():
  data = build_phase65_4_data()

  eta_order_step = data[
    "eta3_cube_order_step"
  ]
  nu_order_step = data[
    "nu_prime_order_step"
  ]
  pi5_2_step = data[
    "pi5_2_step"
  ]
  injective_step = data[
    "suspension_injective_step"
  ]
  double_step = data[
    "double_step"
  ]

  print("=" * 78)
  print("Phase 150 / RC4-5D-2 order-four semantic sufficiency audit")
  print("=" * 78)

  print("A. Repository ORDER semantics")
  print(
    "eta order relation type:",
    eta_order_step.conclusion.relation_type,
  )
  print(
    "eta order value:",
    eta_order_step.conclusion.rhs,
  )
  print(
    "nu order relation type:",
    nu_order_step.conclusion.relation_type,
  )
  print(
    "nu order value:",
    nu_order_step.conclusion.rhs,
  )

  assert (
    eta_order_step.conclusion.relation_type
    is RelationType.ORDER
  )
  assert (
    nu_order_step.conclusion.relation_type
    is RelationType.ORDER
  )

  print("ORDER_RELATION_EXACTNESS=SEMANTIC_CONTRACT")
  print(
    "NOTE=RelationType.ORDER is consumed as exact additive order "
    "by generic order rules."
  )

  print("-" * 78)
  print("B. eta_3^3 exact-order derivation")
  print("rule:", _rule_name(eta_order_step))
  print(
    "premise types:",
    tuple(
      type(premise.conclusion).__name__
      for premise in eta_order_step.premises
    ),
  )
  print(
    "premises equal expected:",
    eta_order_step.premises
    == (
      pi5_2_step,
      injective_step,
    ),
  )
  print("pi5_2:", pi5_2_step.conclusion)
  print("injectivity:", injective_step.conclusion)

  assert isinstance(
    pi5_2_step.conclusion,
    Relation,
  )
  assert isinstance(
    pi5_2_step.conclusion.rhs,
    FiniteCyclicGroup,
  )
  assert (
    pi5_2_step.conclusion.rhs.order
    == 2
  )
  assert isinstance(
    injective_step.conclusion,
    TodaSuspensionInjectiveStatement,
  )
  assert (
    eta_order_step.premises
    == (
      pi5_2_step,
      injective_step,
    )
  )

  eta_match = find_inference_match(
    data[
      "eta3_cube_order_rule"
    ],
    (
      pi5_2_step,
      injective_step,
    ),
  )
  print(
    "eta-order rule matches typed premises:",
    eta_match is not None,
  )
  assert eta_match is not None
  print("ETA_ORDER_TWO_SUFFICIENCY=PASS")

  print("-" * 78)
  print("C. nu-prime order-four derivation")
  print("rule:", _rule_name(nu_order_step))
  print(
    "premise types:",
    tuple(
      type(premise.conclusion).__name__
      for premise in nu_order_step.premises
    ),
  )
  print("order premise:", eta_order_step.conclusion)
  print("multiple relation:", double_step.conclusion)

  assert isinstance(
    double_step.conclusion,
    Relation,
  )
  assert (
    double_step.conclusion.relation_type
    is RelationType.EQUALITY
  )
  assert isinstance(
    double_step.conclusion.lhs,
    Multiple,
  )
  assert (
    double_step.conclusion.lhs.coefficient
    == 2
  )
  assert (
    double_step.conclusion.rhs
    == eta_order_step.conclusion.lhs
  )
  assert (
    eta_order_step.conclusion.rhs
    == 2
  )
  assert (
    nu_order_step.conclusion.lhs
    == double_step.conclusion.lhs.expression
  )
  assert (
    nu_order_step.conclusion.rhs
    == 4
  )
  assert (
    nu_order_step.premises
    == (
      eta_order_step,
      double_step,
    )
  )

  nu_match = find_inference_match(
    data[
      "nu_prime_order_rule"
    ],
    (
      eta_order_step,
      double_step,
    ),
  )
  print(
    "order-four rule matches typed premises:",
    nu_match is not None,
  )
  assert nu_match is not None

  print(
    "MATHEMATICAL_CHAIN="
    "ord(x)=2 exact + 2y=x -> ord(y)=4"
  )
  print(
    "NONZERO_WITNESS="
    "ord(x)=2 exact entails x != 0"
  )
  print(
    "UPPER_BOUND="
    "ord(x)=2 and 2y=x entail 4y=0"
  )
  print(
    "LOWER_BOUND="
    "x != 0 and 2y=x entail 2y!=0"
  )
  print("SAFE_GENERIC_REASON=YES")
  print("PROPOSED_KIND=MULTIPLE_RELATION_TO_ORDER")
  print("AUDIT_RESULT=PASS")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
