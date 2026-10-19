from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupMembershipStatement,
  TodaPrimaryGroupZeroStatement,
  TodaProp44DecompositionMap,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
)
from map_facts import (
  EHP_H_MAP,
)
from expression import (
  MapApplication,
)
from toda_rules import (
  toda_prop44_isomorphism_inference_rule,
)


def build_phase56_1_data():
  i = ScalarSymbol(
    name="i",
  )

  i_minus_one = ScalarSum(
    left=i,
    right=-1,
  )

  two_times_two_minus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=2,
    ),
    right=-1,
  )

  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )

  iota_3 = HomotopyElement(
    name="ι_3",
    dimension=3,
    generator=GeneratorSymbol(
      family="ι",
      index=3,
    ),
  )

  beta = HomotopyElement(
    name="β",
    dimension=i_minus_one,
  )

  gamma = HomotopyElement(
    name="γ",
    dimension=i,
    source=i,
    target=3,
  )

  first_summand = TodaPrimaryGroup(
    group_dimension=i_minus_one,
    sphere_dimension=1,
  )

  second_summand = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=3,
  )

  source_group = DirectSumGroup(
    summands=(
      first_summand,
      second_summand,
    ),
  )

  target_group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=2,
  )

  composition = Composition(
    left=eta_2,
    right=gamma,
  )

  formula = Sum(
    left=Suspension(
      expression=beta,
    ),
    right=composition,
  )

  decomposition_map = TodaProp44DecompositionMap(
    source_group=source_group,
    target_group=target_group,
    alpha=eta_2,
    beta=beta,
    gamma=gamma,
    formula=formula,
  )

  zero_statement = TodaPrimaryGroupZeroStatement(
    group=first_summand,
  )

  concrete_membership = (
    TodaPrimaryGroupMembershipStatement(
      element=eta_2,
      group=TodaPrimaryGroup(
        group_dimension=3,
        sphere_dimension=2,
      ),
    )
  )

  concrete_hopf_relation = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=eta_2,
    ),
    rhs=iota_3,
    relation_type=RelationType.EQUALITY,
  )

  return {
    "i": i,
    "i_minus_one": i_minus_one,
    "two_times_two_minus_one": (
      two_times_two_minus_one
    ),
    "eta_2": eta_2,
    "iota_3": iota_3,
    "beta": beta,
    "gamma": gamma,
    "first_summand": first_summand,
    "second_summand": second_summand,
    "source_group": source_group,
    "target_group": target_group,
    "composition": composition,
    "formula": formula,
    "decomposition_map": (
      decomposition_map
    ),
    "zero_statement": zero_statement,
    "concrete_membership": (
      concrete_membership
    ),
    "concrete_hopf_relation": (
      concrete_hopf_relation
    ),
  }


def test_phase56_1_prop44_n2_direct_sum_shape_is_representable():
  data = build_phase56_1_data()

  assert (
    data[
      "decomposition_map"
    ].source_group
    == DirectSumGroup(
      summands=(
        TodaPrimaryGroup(
          group_dimension=(
            data[
              "i_minus_one"
            ]
          ),
          sphere_dimension=1,
        ),
        TodaPrimaryGroup(
          group_dimension=data[
            "i"
          ],
          sphere_dimension=3,
        ),
      ),
    )
  )

  assert (
    data[
      "decomposition_map"
    ].target_group
    == TodaPrimaryGroup(
      group_dimension=data[
        "i"
      ],
      sphere_dimension=2,
    )
  )


def test_phase56_1_prop44_n2_formula_preserves_eta2_composition():
  data = build_phase56_1_data()

  assert (
    data[
      "decomposition_map"
    ].formula
    == Sum(
      left=Suspension(
        expression=data[
          "beta"
        ],
      ),
      right=Composition(
        left=data[
          "eta_2"
        ],
        right=data[
          "gamma"
        ],
      ),
    )
  )


def test_phase56_1_eta2_gamma_composition_is_type_compatible():
  data = build_phase56_1_data()

  assert (
    data[
      "composition"
    ].is_type_compatible()
  )


def test_phase56_1_zero_first_summand_is_representable():
  data = build_phase56_1_data()

  assert (
    data[
      "zero_statement"
    ]
    == TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=data[
          "i_minus_one"
        ],
        sphere_dimension=1,
      ),
    )
  )


def test_phase56_1_concrete_three_is_not_structurally_two_times_two_minus_one():
  data = build_phase56_1_data()

  assert (
    data[
      "two_times_two_minus_one"
    ]
    != 3
  )


def test_phase56_1_existing_prop44_rule_does_not_directly_match_concrete_n2_data():
  data = build_phase56_1_data()

  steps = (
    ProofStep(
      conclusion=data[
        "concrete_membership"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "concrete_hopf_relation"
      ],
      premises=(),
      rule=ProofRule.INFERENCE,
    ),
    ProofStep(
      conclusion=data[
        "decomposition_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    steps,
  ) is None


