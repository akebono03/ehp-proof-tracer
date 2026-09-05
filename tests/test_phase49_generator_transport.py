from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
)
from homotopy_groups import (
  FreeCyclicGroup,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
)
from low_dimensional_facts import (
  pi_3_3_free_cyclic_fact,
)
from map_facts import (
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
from toda_rules import (
  TodaHopfInvariantIsomorphismStatement,
  TodaPi32Eta2DefinitionStatement,
  toda_pi3_2_define_eta2_inference_rule,
  toda_pi3_2_eta2_hopf_relation_inference_rule,
  toda_pi3_2_free_cyclic_generator_inference_rule,
)


def build_phase49_6_data():
  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  pi_3_3 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=3,
  )

  hopf_map = TodaHopfInvariantMap(
    source_group=pi_3_2,
    target_group=pi_3_3,
  )

  isomorphism = (
    TodaHopfInvariantIsomorphismStatement(
      map=hopf_map,
    )
  )

  target_group_relation = (
    pi_3_3_free_cyclic_fact()
  )

  iota_3 = (
    target_group_relation
    .rhs
    .generator
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

  definition = (
    TodaPi32Eta2DefinitionStatement(
      map=hopf_map,
      element=eta_2,
      image=iota_3,
    )
  )

  hopf_relation = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=eta_2,
    ),
    rhs=iota_3,
    relation_type=RelationType.EQUALITY,
  )

  source_group_relation = Relation(
    lhs=pi_3_2,
    rhs=FreeCyclicGroup(
      generator=eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  return {
    "pi_3_2": pi_3_2,
    "pi_3_3": pi_3_3,
    "hopf_map": hopf_map,
    "isomorphism": isomorphism,
    "target_group_relation": (
      target_group_relation
    ),
    "iota_3": iota_3,
    "eta_2": eta_2,
    "definition": definition,
    "hopf_relation": hopf_relation,
    "source_group_relation": (
      source_group_relation
    ),
  }


def build_phase49_6_initial_steps(
  data,
):
  return (
    ProofStep(
      conclusion=data[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "target_group_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def build_phase49_6_rules():
  return (
    toda_pi3_2_define_eta2_inference_rule(),
    toda_pi3_2_eta2_hopf_relation_inference_rule(),
    toda_pi3_2_free_cyclic_generator_inference_rule(),
  )


def test_phase49_6_eta_2_is_not_an_initial_given_premise():
  data = build_phase49_6_data()

  initial_steps = (
    build_phase49_6_initial_steps(
      data
    )
  )

  initial_conclusions = tuple(
    step.conclusion
    for step in initial_steps
  )

  assert data[
    "definition"
  ] not in initial_conclusions

  assert data[
    "hopf_relation"
  ] not in initial_conclusions


def test_phase49_6_definition_statement_names_eta_2():
  data = build_phase49_6_data()

  assert data[
    "definition"
  ].element == (
    HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )
  )


def test_phase49_6_definition_statement_preserves_iota_3():
  data = build_phase49_6_data()

  assert data[
    "definition"
  ].image == (
    data[
      "iota_3"
    ]
  )


def test_phase49_6_definition_statement_preserves_hopf_map():
  data = build_phase49_6_data()

  assert data[
    "definition"
  ].map == (
    data[
      "hopf_map"
    ]
  )


def test_phase49_6_define_eta2_rule_matches_valid_instance():
  data = build_phase49_6_data()

  assert find_inference_match(
    toda_pi3_2_define_eta2_inference_rule(),
    build_phase49_6_initial_steps(
      data
    ),
  ) is not None


def test_phase49_6_define_eta2_rule_derives_definition():
  data = build_phase49_6_data()

  result = (
    run_inference_until_stable_with_history(
      toda_pi3_2_define_eta2_inference_rule(),
      build_phase49_6_initial_steps(
        data
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "definition"
  ] in conclusions


def test_phase49_6_define_eta2_rule_rejects_wrong_source():
  data = build_phase49_6_data()

  wrong_isomorphism = (
    TodaHopfInvariantIsomorphismStatement(
      map=TodaHopfInvariantMap(
        source_group=TodaPrimaryGroup(
          group_dimension=4,
          sphere_dimension=3,
        ),
        target_group=data[
          "pi_3_3"
        ],
      ),
    )
  )

  steps = (
    ProofStep(
      conclusion=wrong_isomorphism,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "target_group_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_pi3_2_define_eta2_inference_rule(),
    steps,
  ) is None


def test_phase49_6_define_eta2_rule_rejects_wrong_target_generator():
  data = build_phase49_6_data()

  wrong_relation = Relation(
    lhs=data[
      "pi_3_3"
    ],
    rhs=FreeCyclicGroup(
      generator=HomotopyElement(
        name="x",
        dimension=3,
        generator=GeneratorSymbol(
          family="x",
          index=3,
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  steps = (
    ProofStep(
      conclusion=data[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_relation,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_pi3_2_define_eta2_inference_rule(),
    steps,
  ) is None


def test_phase49_6_eta2_hopf_rule_matches_definition():
  data = build_phase49_6_data()

  step = ProofStep(
    conclusion=data[
      "definition"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_pi3_2_eta2_hopf_relation_inference_rule(),
    (
      step,
    ),
  ) is not None


def test_phase49_6_eta2_hopf_rule_derives_h_eta2_equals_iota3():
  data = build_phase49_6_data()

  step = ProofStep(
    conclusion=data[
      "definition"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      toda_pi3_2_eta2_hopf_relation_inference_rule(),
      (
        step,
      ),
    )
  )

  conclusions = tuple(
    derived.conclusion
    for derived in result.steps
  )

  assert data[
    "hopf_relation"
  ] in conclusions


def test_phase49_6_free_cyclic_rule_matches_valid_instance():
  data = build_phase49_6_data()

  steps = (
    ProofStep(
      conclusion=data[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "target_group_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "definition"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_pi3_2_free_cyclic_generator_inference_rule(),
    steps,
  ) is not None


def test_phase49_6_free_cyclic_rule_derives_pi_3_2_free_on_eta_2():
  data = build_phase49_6_data()

  steps = (
    ProofStep(
      conclusion=data[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "target_group_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "definition"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  result = (
    run_inference_until_stable_with_history(
      toda_pi3_2_free_cyclic_generator_inference_rule(),
      steps,
    )
  )

  conclusions = tuple(
    derived.conclusion
    for derived in result.steps
  )

  assert data[
    "source_group_relation"
  ] in conclusions


def test_phase49_6_final_relation_is_pi_3_2_free_on_eta_2():
  data = build_phase49_6_data()

  relation = data[
    "source_group_relation"
  ]

  assert relation.lhs == (
    data[
      "pi_3_2"
    ]
  )

  assert relation.rhs == (
    FreeCyclicGroup(
      generator=data[
        "eta_2"
      ],
    )
  )


def test_phase49_6_end_to_end_derives_eta2_definition():
  data = build_phase49_6_data()

  result = (
    run_inference_until_stable_with_history(
      build_phase49_6_rules(),
      build_phase49_6_initial_steps(
        data
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "definition"
  ] in conclusions


def test_phase49_6_end_to_end_derives_h_eta2_equals_iota3():
  data = build_phase49_6_data()

  result = (
    run_inference_until_stable_with_history(
      build_phase49_6_rules(),
      build_phase49_6_initial_steps(
        data
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "hopf_relation"
  ] in conclusions


def test_phase49_6_end_to_end_derives_pi_3_2_free_on_eta2():
  data = build_phase49_6_data()

  result = (
    run_inference_until_stable_with_history(
      build_phase49_6_rules(),
      build_phase49_6_initial_steps(
        data
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "source_group_relation"
  ] in conclusions


def test_phase49_6_end_to_end_reaches_fixed_point_in_two_rounds():
  data = build_phase49_6_data()

  result = (
    run_inference_until_stable_with_history(
      build_phase49_6_rules(),
      build_phase49_6_initial_steps(
        data
      ),
    )
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2


def test_phase49_6_round_one_derives_only_eta2_definition():
  data = build_phase49_6_data()

  result = (
    run_inference_until_stable_with_history(
      build_phase49_6_rules(),
      build_phase49_6_initial_steps(
        data
      ),
    )
  )

  new_steps = (
    result.round_results[
      0
    ].new_steps
  )

  assert len(
    new_steps
  ) == 1

  assert new_steps[
    0
  ].conclusion == (
    data[
      "definition"
    ]
  )


def test_phase49_6_round_two_derives_hopf_relation_and_group_relation():
  data = build_phase49_6_data()

  result = (
    run_inference_until_stable_with_history(
      build_phase49_6_rules(),
      build_phase49_6_initial_steps(
        data
      ),
    )
  )

  new_steps = (
    result.round_results[
      1
    ].new_steps
  )

  conclusions = tuple(
    step.conclusion
    for step in new_steps
  )

  assert len(
    new_steps
  ) == 2

  assert data[
    "hopf_relation"
  ] in conclusions

  assert data[
    "source_group_relation"
  ] in conclusions


def test_phase49_6_all_derived_steps_preserve_provenance():
  data = build_phase49_6_data()

  result = (
    run_inference_until_stable_with_history(
      build_phase49_6_rules(),
      build_phase49_6_initial_steps(
        data
      ),
    )
  )

  derived = tuple(
    step
    for step in result.steps
    if step.rule
    == ProofRule.INFERENCE
  )

  assert len(
    derived
  ) == 3

  assert all(
    step.inference_rule
    is not None
    for step in derived
  )



