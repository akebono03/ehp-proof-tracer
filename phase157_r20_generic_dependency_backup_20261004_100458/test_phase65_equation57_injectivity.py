from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
)
from homotopy_groups import (
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
  TodaSuspensionMap,
)
from map_facts import (
  EHP_DELTA_MAP,
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
from test_phase59_prop53_integration import (
  build_phase59_8_data,
)
from toda_rules import (
  TodaDeltaZeroStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
  toda_57_nu_prime_eta6_hopf_inference_rule,
  toda_eta_family_definition_statement,
  toda_prop56_pi5_2_suspension_injective_inference_rule,
  toda_prop56_pi7_3_hopf_surjective_inference_rule,
  toda_prop56_pi7_5_delta_zero_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase65_3_data():
  phase58 = (
    build_phase58_representative_result()
  )

  phase59 = (
    build_phase59_8_data()
  )

  hopf_nu_prime_step = (
    phase58[
      "final_hopf_step"
    ]
  )

  prop53_step = (
    phase59[
      "integration_step"
    ]
  )

  eta5_definition = (
    toda_eta_family_definition_statement(
      5
    )
  )

  eta6_definition = (
    toda_eta_family_definition_statement(
      6
    )
  )

  eta5_definition_step = ProofStep(
    conclusion=eta5_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta6_definition_step = ProofStep(
    conclusion=eta6_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pi_7_3 = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=3,
  )

  pi_7_5 = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=5,
  )

  pi_5_2 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=2,
  )

  pi_6_3 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=3,
  )

  h_delta_exactness = (
    TodaProp42ExactnessStatement(
      window=TodaEHPExactnessWindow(
        source_term=pi_7_3,
        middle_term=pi_7_5,
        target_term=pi_5_2,
        first_map=EHP_H_MAP,
        second_map=EHP_DELTA_MAP,
      ),
    )
  )

  delta_e_exactness = (
    TodaProp42ExactnessStatement(
      window=TodaEHPExactnessWindow(
        source_term=pi_7_5,
        middle_term=pi_5_2,
        target_term=pi_6_3,
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
      ),
    )
  )

  h_delta_exactness_step = ProofStep(
    conclusion=h_delta_exactness,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  delta_e_exactness_step = ProofStep(
    conclusion=delta_e_exactness,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
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

  eta_6 = HomotopyElement(
    name="η₆",
    dimension=6,
    source=7,
    target=6,
    generator=GeneratorSymbol(
      family="η",
      index=6,
    ),
  )

  eta_5_squared = Composition(
    left=eta_5,
    right=eta_6,
  )

  expected_equation57 = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=Composition(
        left=nu_prime,
        right=eta_6,
      ),
    ),
    rhs=eta_5_squared,
    relation_type=RelationType.EQUALITY,
  )

  expected_hopf_surjective = (
    TodaHopfInvariantSurjectiveStatement(
      map=TodaHopfInvariantMap(
        source_group=pi_7_3,
        target_group=pi_7_5,
      ),
    )
  )

  expected_delta_zero = (
    TodaDeltaZeroStatement(
      map=TodaDeltaMap(
        source_group=pi_7_5,
        target_group=pi_5_2,
      ),
    )
  )

  expected_suspension_injective = (
    TodaSuspensionInjectiveStatement(
      map=TodaSuspensionMap(
        source_group=pi_5_2,
        target_group=pi_6_3,
      ),
    )
  )

  equation57_rule = (
    toda_57_nu_prime_eta6_hopf_inference_rule()
  )

  hopf_surjective_rule = (
    toda_prop56_pi7_3_hopf_surjective_inference_rule()
  )

  delta_zero_rule = (
    toda_prop56_pi7_5_delta_zero_inference_rule()
  )

  suspension_injective_rule = (
    toda_prop56_pi5_2_suspension_injective_inference_rule()
  )

  rules = (
    equation57_rule,
    hopf_surjective_rule,
    delta_zero_rule,
    suspension_injective_rule,
  )

  premise_steps = (
    hopf_nu_prime_step,
    prop53_step,
    eta5_definition_step,
    eta6_definition_step,
    h_delta_exactness_step,
    delta_e_exactness_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  equation57_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_equation57
    )
  )

  hopf_surjective_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_hopf_surjective
    )
  )

  delta_zero_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_delta_zero
    )
  )

  suspension_injective_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_suspension_injective
    )
  )

  return {
    "phase58": phase58,
    "phase59": phase59,
    "hopf_nu_prime_step": (
      hopf_nu_prime_step
    ),
    "prop53_step": prop53_step,
    "eta5_definition": (
      eta5_definition
    ),
    "eta6_definition": (
      eta6_definition
    ),
    "eta5_definition_step": (
      eta5_definition_step
    ),
    "eta6_definition_step": (
      eta6_definition_step
    ),
    "pi_7_3": pi_7_3,
    "pi_7_5": pi_7_5,
    "pi_5_2": pi_5_2,
    "pi_6_3": pi_6_3,
    "h_delta_exactness": (
      h_delta_exactness
    ),
    "delta_e_exactness": (
      delta_e_exactness
    ),
    "h_delta_exactness_step": (
      h_delta_exactness_step
    ),
    "delta_e_exactness_step": (
      delta_e_exactness_step
    ),
    "nu_prime": nu_prime,
    "eta_5": eta_5,
    "eta_6": eta_6,
    "eta_5_squared": (
      eta_5_squared
    ),
    "expected_equation57": (
      expected_equation57
    ),
    "expected_hopf_surjective": (
      expected_hopf_surjective
    ),
    "expected_delta_zero": (
      expected_delta_zero
    ),
    "expected_suspension_injective": (
      expected_suspension_injective
    ),
    "equation57_rule": (
      equation57_rule
    ),
    "hopf_surjective_rule": (
      hopf_surjective_rule
    ),
    "delta_zero_rule": (
      delta_zero_rule
    ),
    "suspension_injective_rule": (
      suspension_injective_rule
    ),
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "equation57_step": (
      equation57_step
    ),
    "hopf_surjective_step": (
      hopf_surjective_step
    ),
    "delta_zero_step": (
      delta_zero_step
    ),
    "suspension_injective_step": (
      suspension_injective_step
    ),
  }


def test_phase65_3_reuses_derived_hopf_nu_prime():
  data = build_phase65_3_data()

  assert (
    data[
      "hopf_nu_prime_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "hopf_nu_prime_step"
    ].conclusion.rhs
    == data[
      "eta_5"
    ]
  )


def test_phase65_3_reuses_derived_prop53():
  data = build_phase65_3_data()

  assert (
    data[
      "prop53_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_3_eta_definitions_are_given():
  data = build_phase65_3_data()

  assert (
    data[
      "eta5_definition_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "eta6_definition_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase65_3_equation57_rule_matches_dependencies():
  data = build_phase65_3_data()

  assert find_inference_match(
    data[
      "equation57_rule"
    ],
    (
      data[
        "hopf_nu_prime_step"
      ],
      data[
        "eta5_definition_step"
      ],
      data[
        "eta6_definition_step"
      ],
    ),
  ) is not None


def test_phase65_3_derives_equation57():
  data = build_phase65_3_data()

  step = data[
    "equation57_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_equation57"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase65_3_equation57_is_h_nu_prime_eta6():
  data = build_phase65_3_data()

  lhs = (
    data[
      "equation57_step"
    ].conclusion.lhs
  )

  assert (
    lhs
    == MapApplication(
      map=EHP_H_MAP,
      expression=Composition(
        left=data[
          "nu_prime"
        ],
        right=data[
          "eta_6"
        ],
      ),
    )
  )


def test_phase65_3_equation57_value_is_eta5_squared():
  data = build_phase65_3_data()

  assert (
    data[
      "equation57_step"
    ].conclusion.rhs
    == Composition(
      left=data[
        "eta_5"
      ],
      right=data[
        "eta_6"
      ],
    )
  )


def test_phase65_3_equation57_provenance():
  data = build_phase65_3_data()

  assert (
    data[
      "equation57_step"
    ].premises
    == (
      data[
        "hopf_nu_prime_step"
      ],
      data[
        "eta5_definition_step"
      ],
      data[
        "eta6_definition_step"
      ],
    )
  )


def test_phase65_3_hopf_surjective_rule_matches():
  data = build_phase65_3_data()

  assert find_inference_match(
    data[
      "hopf_surjective_rule"
    ],
    (
      data[
        "equation57_step"
      ],
      data[
        "prop53_step"
      ],
    ),
  ) is not None


def test_phase65_3_derives_h_pi7_3_surjective():
  data = build_phase65_3_data()

  assert (
    data[
      "hopf_surjective_step"
    ].conclusion
    == data[
      "expected_hopf_surjective"
    ]
  )

  assert (
    data[
      "hopf_surjective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_3_delta_zero_rule_matches_exactness():
  data = build_phase65_3_data()

  assert find_inference_match(
    data[
      "delta_zero_rule"
    ],
    (
      data[
        "hopf_surjective_step"
      ],
      data[
        "h_delta_exactness_step"
      ],
    ),
  ) is not None


def test_phase65_3_derives_delta_pi7_5_zero():
  data = build_phase65_3_data()

  assert (
    data[
      "delta_zero_step"
    ].conclusion
    == data[
      "expected_delta_zero"
    ]
  )

  assert (
    data[
      "delta_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_3_suspension_injective_rule_matches():
  data = build_phase65_3_data()

  assert find_inference_match(
    data[
      "suspension_injective_rule"
    ],
    (
      data[
        "delta_zero_step"
      ],
      data[
        "delta_e_exactness_step"
      ],
    ),
  ) is not None


def test_phase65_3_derives_e_pi5_2_injective():
  data = build_phase65_3_data()

  step = data[
    "suspension_injective_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_suspension_injective"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert (
    step.conclusion.map.source_group
    == TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=2,
    )
  )

  assert (
    step.conclusion.map.target_group
    == TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=3,
    )
  )


def test_phase65_3_final_provenance_is_acyclic_chain():
  data = build_phase65_3_data()

  assert (
    data[
      "hopf_surjective_step"
    ].premises
    == (
      data[
        "equation57_step"
      ],
      data[
        "prop53_step"
      ],
    )
  )

  assert (
    data[
      "delta_zero_step"
    ].premises
    == (
      data[
        "hopf_surjective_step"
      ],
      data[
        "h_delta_exactness_step"
      ],
    )
  )

  assert (
    data[
      "suspension_injective_step"
    ].premises
    == (
      data[
        "delta_zero_step"
      ],
      data[
        "delta_e_exactness_step"
      ],
    )
  )


def test_phase65_3_rejects_given_equation57_for_surjectivity():
  data = build_phase65_3_data()

  given_equation57 = ProofStep(
    conclusion=(
      data[
        "equation57_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "hopf_surjective_rule"
    ],
    (
      given_equation57,
      data[
        "prop53_step"
      ],
    ),
  ) is None


def test_phase65_3_final_result_is_not_given():
  data = build_phase65_3_data()

  assert (
    data[
      "suspension_injective_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "expected_suspension_injective"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase65_3_reaches_fixed_point_in_four_rounds():
  data = build_phase65_3_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 4

  assert (
    data[
      "equation57_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "hopf_surjective_step"
    ]
    in result.round_results[
      1
    ].new_steps
  )

  assert (
    data[
      "delta_zero_step"
    ]
    in result.round_results[
      2
    ].new_steps
  )

  assert (
    data[
      "suspension_injective_step"
    ]
    in result.round_results[
      3
    ].new_steps
  )


