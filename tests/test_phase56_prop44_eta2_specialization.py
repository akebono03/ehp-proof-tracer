from expression import (
  Composition,
  HomotopyElement,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaPrimaryGroup,
  TodaProp44DecompositionMap,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from probes.probe_phase49_capabilities import (
  build_phase49_representative_result,
)
from toda_rules import (
  TodaProp44IsomorphismStatement,
  toda_prop44_eta2_n2_isomorphism_inference_rule,
)


def build_phase56_3_data():
  phase49 = (
    build_phase49_representative_result()
  )

  eta_2_definition_step = (
    phase49[
      "eta_2_definition_steps"
    ][
      0
    ]
  )

  hopf_relation_step = (
    phase49[
      "hopf_relation_steps"
    ][
      0
    ]
  )

  eta_2 = (
    eta_2_definition_step
    .conclusion
    .element
  )

  i = ScalarSymbol(
    name="i",
  )

  i_minus_one = ScalarSum(
    left=i,
    right=-1,
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

  formula = Sum(
    left=Suspension(
      expression=beta,
    ),
    right=Composition(
      left=eta_2,
      right=gamma,
    ),
  )

  decomposition_map = (
    TodaProp44DecompositionMap(
      source_group=source_group,
      target_group=target_group,
      alpha=eta_2,
      beta=beta,
      gamma=gamma,
      formula=formula,
    )
  )

  decomposition_map_step = ProofStep(
    conclusion=decomposition_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  premise_steps = (
    eta_2_definition_step,
    hopf_relation_step,
    decomposition_map_step,
  )

  expected_statement = (
    TodaProp44IsomorphismStatement(
      map=decomposition_map,
    )
  )

  rule = (
    toda_prop44_eta2_n2_isomorphism_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  isomorphism_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase49": phase49,
    "i": i,
    "i_minus_one": i_minus_one,
    "eta_2": eta_2,
    "beta": beta,
    "gamma": gamma,
    "first_summand": first_summand,
    "second_summand": second_summand,
    "source_group": source_group,
    "target_group": target_group,
    "formula": formula,
    "decomposition_map": (
      decomposition_map
    ),
    "eta_2_definition_step": (
      eta_2_definition_step
    ),
    "hopf_relation_step": (
      hopf_relation_step
    ),
    "decomposition_map_step": (
      decomposition_map_step
    ),
    "premise_steps": premise_steps,
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "result": result,
    "isomorphism_steps": (
      isomorphism_steps
    ),
  }


def test_phase56_3_rule_matches_n2_eta2_specialization():
  data = build_phase56_3_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase56_3_derives_prop44_isomorphism():
  data = build_phase56_3_data()

  steps = data[
    "isomorphism_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaProp44IsomorphismStatement,
  )

  assert (
    steps[
      0
    ].conclusion
    == data[
      "expected_statement"
    ]
  )


def test_phase56_3_specialization_has_expected_source_and_target():
  data = build_phase56_3_data()

  decomposition_map = (
    data[
      "isomorphism_steps"
    ][
      0
    ].conclusion.map
  )

  assert (
    decomposition_map.source_group
    == DirectSumGroup(
      summands=(
        TodaPrimaryGroup(
          group_dimension=ScalarSum(
            left=data[
              "i"
            ],
            right=-1,
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
    decomposition_map.target_group
    == TodaPrimaryGroup(
      group_dimension=data[
        "i"
      ],
      sphere_dimension=2,
    )
  )


def test_phase56_3_specialization_preserves_eta2_formula():
  data = build_phase56_3_data()

  decomposition_map = (
    data[
      "isomorphism_steps"
    ][
      0
    ].conclusion.map
  )

  assert (
    decomposition_map.formula
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


def test_phase56_3_result_is_inference():
  data = build_phase56_3_data()

  step = data[
    "isomorphism_steps"
  ][
    0
  ]

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert step.inference_rule is not None

  assert (
    step.inference_rule.name
    == (
      "Toda Proposition 4.4 "
      "eta_2 n=2 specialization"
    )
  )


def test_phase56_3_preserves_derived_eta2_provenance():
  data = build_phase56_3_data()

  step = data[
    "isomorphism_steps"
  ][
    0
  ]

  assert (
    step.premises
    == data[
      "premise_steps"
    ]
  )

  assert (
    data[
      "eta_2_definition_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "hopf_relation_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase56_3_phase49_dependencies_are_not_given():
  data = build_phase56_3_data()

  initial_conclusions = tuple(
    step.conclusion
    for step in data[
      "phase49"
    ][
      "premise_steps"
    ]
  )

  assert (
    data[
      "eta_2_definition_step"
    ].conclusion
    not in initial_conclusions
  )

  assert (
    data[
      "hopf_relation_step"
    ].conclusion
    not in initial_conclusions
  )


def test_phase56_3_rejects_given_hopf_relation():
  data = build_phase56_3_data()

  given_hopf_step = ProofStep(
    conclusion=data[
      "hopf_relation_step"
    ].conclusion,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  steps = (
    data[
      "eta_2_definition_step"
    ],
    given_hopf_step,
    data[
      "decomposition_map_step"
    ],
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    steps,
  ) is None


def test_phase56_3_rejects_given_eta2_definition():
  data = build_phase56_3_data()

  given_definition_step = ProofStep(
    conclusion=data[
      "eta_2_definition_step"
    ].conclusion,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  steps = (
    given_definition_step,
    data[
      "hopf_relation_step"
    ],
    data[
      "decomposition_map_step"
    ],
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    steps,
  ) is None


def test_phase56_3_rejects_wrong_alpha():
  data = build_phase56_3_data()

  wrong_alpha = HomotopyElement(
    name="α",
    dimension=3,
    source=3,
    target=2,
  )

  wrong_map = TodaProp44DecompositionMap(
    source_group=data[
      "source_group"
    ],
    target_group=data[
      "target_group"
    ],
    alpha=wrong_alpha,
    beta=data[
      "beta"
    ],
    gamma=data[
      "gamma"
    ],
    formula=Sum(
      left=Suspension(
        expression=data[
          "beta"
        ],
      ),
      right=Composition(
        left=wrong_alpha,
        right=data[
          "gamma"
        ],
      ),
    ),
  )

  wrong_map_step = ProofStep(
    conclusion=wrong_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  steps = (
    data[
      "eta_2_definition_step"
    ],
    data[
      "hopf_relation_step"
    ],
    wrong_map_step,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    steps,
  ) is None


def test_phase56_3_reaches_fixed_point_in_one_round():
  data = build_phase56_3_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 1

  assert len(
    result.round_results[
      0
    ].new_steps
  ) == 1



