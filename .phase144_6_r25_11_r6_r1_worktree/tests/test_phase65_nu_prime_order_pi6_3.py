from functools import lru_cache

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from probes.probe_phase58_capabilities import (
  build_phase58_representative_result,
)
from test_phase59_n3_ehp_chain import (
  build_phase59_3_data,
)
from test_phase60_toda48_hopf_parity import (
  build_phase60_7_data,
)
from test_phase65_equation57_injectivity import (
  build_phase65_3_data,
)
from test_phase65_pi5_2_eta2_cube import (
  build_phase65_2_data,
)
from toda_rules import (
  TodaHopfInvariantSurjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
  toda_prop56_eta3_cube_order_two_inference_rule,
  toda_prop56_nu_prime_order_four_inference_rule,
  toda_prop56_pi6_3_finite_cyclic_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase65_4_data():
  phase58 = (
    build_phase58_representative_result()
  )

  phase59_3 = (
    build_phase59_3_data()
  )

  phase60_7 = (
    build_phase60_7_data()
  )

  phase65_2 = (
    build_phase65_2_data()
  )

  phase65_3 = (
    build_phase65_3_data()
  )

  pi5_2_step = (
    phase65_2[
      "final_step"
    ]
  )

  suspension_injective_step = (
    phase65_3[
      "suspension_injective_step"
    ]
  )

  double_step = (
    phase58[
      "final_double_step"
    ]
  )

  membership_step = (
    phase58[
      "membership_step"
    ]
  )

  pi6_5_step = (
    phase60_7[
      "pi6_5_step"
    ]
  )

  hopf_surjective_step = next(
    step
    for step in phase59_3[
      "result"
    ].steps
    if (
      step.conclusion
      == phase59_3[
        "expected_hopf_surjective"
      ]
    )
  )

  pi_5_2 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=2,
  )

  pi_6_3 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=3,
  )

  pi_6_5 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=5,
  )

  e_h_exactness = (
    TodaProp42ExactnessStatement(
      window=TodaEHPExactnessWindow(
        source_term=pi_5_2,
        middle_term=pi_6_3,
        target_term=pi_6_5,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
      ),
    )
  )

  e_h_exactness_step = ProofStep(
    conclusion=e_h_exactness,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  eta_4 = HomotopyElement(
    name="η₄",
    dimension=4,
    source=5,
    target=4,
    generator=GeneratorSymbol(
      family="η",
      index=4,
    ),
  )

  eta_5 = HomotopyElement(
    name="η₅",
    dimension=5,
    source=6,
    target=5,
    generator=GeneratorSymbol(
      family="η",
      index=5,
    ),
  )

  eta_3_cube = Composition(
    left=eta_3,
    right=Composition(
      left=eta_4,
      right=eta_5,
    ),
  )

  nu_prime = (
    phase58[
      "nu_prime"
    ]
  )

  expected_eta3_cube_order = Relation(
    lhs=eta_3_cube,
    rhs=2,
    relation_type=RelationType.ORDER,
  )

  expected_nu_prime_order = Relation(
    lhs=nu_prime,
    rhs=4,
    relation_type=RelationType.ORDER,
  )

  expected_pi6_3_relation = Relation(
    lhs=pi_6_3,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=nu_prime,
    ),
    relation_type=RelationType.EQUALITY,
  )

  eta3_cube_order_rule = (
    toda_prop56_eta3_cube_order_two_inference_rule()
  )

  nu_prime_order_rule = (
    toda_prop56_nu_prime_order_four_inference_rule()
  )

  pi6_3_rule = (
    toda_prop56_pi6_3_finite_cyclic_inference_rule()
  )

  rules = (
    eta3_cube_order_rule,
    nu_prime_order_rule,
    pi6_3_rule,
  )

  premise_steps = (
    pi5_2_step,
    suspension_injective_step,
    double_step,
    membership_step,
    e_h_exactness_step,
    hopf_surjective_step,
    pi6_5_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  eta3_cube_order_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_eta3_cube_order
    )
  )

  nu_prime_order_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_nu_prime_order
    )
  )

  pi6_3_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_pi6_3_relation
    )
  )

  return {
    "phase58": phase58,
    "phase59_3": phase59_3,
    "phase60_7": phase60_7,
    "phase65_2": phase65_2,
    "phase65_3": phase65_3,
    "pi5_2_step": pi5_2_step,
    "suspension_injective_step": (
      suspension_injective_step
    ),
    "double_step": double_step,
    "membership_step": membership_step,
    "hopf_surjective_step": (
      hopf_surjective_step
    ),
    "pi6_5_step": pi6_5_step,
    "e_h_exactness": e_h_exactness,
    "e_h_exactness_step": (
      e_h_exactness_step
    ),
    "eta_3": eta_3,
    "eta_4": eta_4,
    "eta_5": eta_5,
    "eta_3_cube": eta_3_cube,
    "nu_prime": nu_prime,
    "expected_eta3_cube_order": (
      expected_eta3_cube_order
    ),
    "expected_nu_prime_order": (
      expected_nu_prime_order
    ),
    "expected_pi6_3_relation": (
      expected_pi6_3_relation
    ),
    "eta3_cube_order_rule": (
      eta3_cube_order_rule
    ),
    "nu_prime_order_rule": (
      nu_prime_order_rule
    ),
    "pi6_3_rule": pi6_3_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "eta3_cube_order_step": (
      eta3_cube_order_step
    ),
    "nu_prime_order_step": (
      nu_prime_order_step
    ),
    "pi6_3_step": pi6_3_step,
  }


def test_phase65_4_reuses_phase65_2_pi5_2():
  data = build_phase65_4_data()

  assert (
    data[
      "pi5_2_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_4_reuses_phase65_3_injectivity():
  data = build_phase65_4_data()

  assert isinstance(
    data[
      "suspension_injective_step"
    ].conclusion,
    TodaSuspensionInjectiveStatement,
  )

  assert (
    data[
      "suspension_injective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_4_reuses_phase58_double_relation():
  data = build_phase65_4_data()

  assert (
    data[
      "double_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "double_step"
    ].conclusion
    == Relation(
      lhs=Multiple(
        coefficient=2,
        expression=data[
          "nu_prime"
        ],
      ),
      rhs=data[
        "eta_3_cube"
      ],
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase65_4_reuses_nu_prime_membership():
  data = build_phase65_4_data()

  assert isinstance(
    data[
      "membership_step"
    ].conclusion,
    HomotopyGroupMembershipStatement,
  )

  assert (
    data[
      "membership_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_4_reuses_hopf_surjectivity():
  data = build_phase65_4_data()

  assert isinstance(
    data[
      "hopf_surjective_step"
    ].conclusion,
    TodaHopfInvariantSurjectiveStatement,
  )

  assert (
    data[
      "hopf_surjective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_4_reuses_pi6_5_order_two():
  data = build_phase65_4_data()

  assert (
    data[
      "pi6_5_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi6_5_step"
    ].conclusion.rhs.order
    == 2
  )


def test_phase65_4_eta3_cube_rule_matches():
  data = build_phase65_4_data()

  assert find_inference_match(
    data[
      "eta3_cube_order_rule"
    ],
    (
      data[
        "pi5_2_step"
      ],
      data[
        "suspension_injective_step"
      ],
    ),
  ) is not None


def test_phase65_4_derives_eta3_cube_order_two():
  data = build_phase65_4_data()

  assert (
    data[
      "eta3_cube_order_step"
    ].conclusion
    == data[
      "expected_eta3_cube_order"
    ]
  )

  assert (
    data[
      "eta3_cube_order_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_4_nu_prime_order_rule_matches():
  data = build_phase65_4_data()

  assert find_inference_match(
    data[
      "nu_prime_order_rule"
    ],
    (
      data[
        "eta3_cube_order_step"
      ],
      data[
        "double_step"
      ],
    ),
  ) is not None


def test_phase65_4_derives_nu_prime_order_four():
  data = build_phase65_4_data()

  assert (
    data[
      "nu_prime_order_step"
    ].conclusion
    == data[
      "expected_nu_prime_order"
    ]
  )

  assert (
    data[
      "nu_prime_order_step"
    ].conclusion.relation_type
    == RelationType.ORDER
  )

  assert (
    data[
      "nu_prime_order_step"
    ].conclusion.rhs
    == 4
  )


def test_phase65_4_pi6_3_rule_matches_all_dependencies():
  data = build_phase65_4_data()

  assert find_inference_match(
    data[
      "pi6_3_rule"
    ],
    (
      data[
        "nu_prime_order_step"
      ],
      data[
        "membership_step"
      ],
      data[
        "pi5_2_step"
      ],
      data[
        "suspension_injective_step"
      ],
      data[
        "e_h_exactness_step"
      ],
      data[
        "hopf_surjective_step"
      ],
      data[
        "pi6_5_step"
      ],
    ),
  ) is not None


def test_phase65_4_derives_pi6_3_z4_nu_prime():
  data = build_phase65_4_data()

  assert (
    data[
      "pi6_3_step"
    ].conclusion
    == data[
      "expected_pi6_3_relation"
    ]
  )

  assert (
    data[
      "pi6_3_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_4_final_generator_is_nu_prime():
  data = build_phase65_4_data()

  group = (
    data[
      "pi6_3_step"
    ].conclusion.rhs
  )

  assert isinstance(
    group,
    FiniteCyclicGroup,
  )

  assert group.order == 4

  assert (
    group.generator
    == data[
      "nu_prime"
    ]
  )


def test_phase65_4_order_provenance():
  data = build_phase65_4_data()

  assert (
    data[
      "eta3_cube_order_step"
    ].premises
    == (
      data[
        "pi5_2_step"
      ],
      data[
        "suspension_injective_step"
      ],
    )
  )

  assert (
    data[
      "nu_prime_order_step"
    ].premises
    == (
      data[
        "eta3_cube_order_step"
      ],
      data[
        "double_step"
      ],
    )
  )


def test_phase65_4_final_provenance():
  data = build_phase65_4_data()

  assert (
    data[
      "pi6_3_step"
    ].premises
    == (
      data[
        "nu_prime_order_step"
      ],
      data[
        "membership_step"
      ],
      data[
        "pi5_2_step"
      ],
      data[
        "suspension_injective_step"
      ],
      data[
        "e_h_exactness_step"
      ],
      data[
        "hopf_surjective_step"
      ],
      data[
        "pi6_5_step"
      ],
    )
  )


def test_phase65_4_rejects_given_order_four():
  data = build_phase65_4_data()

  given_order_step = ProofStep(
    conclusion=(
      data[
        "nu_prime_order_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "pi6_3_rule"
    ],
    (
      given_order_step,
      data[
        "membership_step"
      ],
      data[
        "pi5_2_step"
      ],
      data[
        "suspension_injective_step"
      ],
      data[
        "e_h_exactness_step"
      ],
      data[
        "hopf_surjective_step"
      ],
      data[
        "pi6_5_step"
      ],
    ),
  ) is None


def test_phase65_4_final_result_is_not_given():
  data = build_phase65_4_data()

  assert (
    data[
      "pi6_3_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "expected_pi6_3_relation"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase65_4_reaches_fixed_point_in_three_rounds():
  data = build_phase65_4_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 3

  assert (
    data[
      "eta3_cube_order_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "nu_prime_order_step"
    ]
    in result.round_results[
      1
    ].new_steps
  )

  assert (
    data[
      "pi6_3_step"
    ]
    in result.round_results[
      2
    ].new_steps
  )


