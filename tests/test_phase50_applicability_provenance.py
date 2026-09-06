from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Multiple,
  Suspension,
  WhiteheadProduct,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
)
from low_dimensional_facts import (
  pi_4_5_zero_fact,
  pi_5_5_free_cyclic_fact,
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
  run_inference_until_stable_with_history,
)
from toda_rules import (
  TodaHopfInvariantInjectiveStatement,
  TodaPi32Eta2DefinitionStatement,
  TodaPi32WhiteheadSquareUpToSignStatement,
  TodaProp42ExactnessStatement,
  TodaDeltaImageUpToSignStatement,
  toda_delta_iota5_whitehead_square_inference_rule,
  toda_eta3_suspension_relation_inference_rule,
  toda_eta_family_definition_statement,
  toda_pi3_2_whitehead_square_up_to_sign_inference_rule,
  toda_pi4_3_delta_image_free_cyclic_inference_rule,
  toda_pi4_3_eta3_generator_inference_rule,
  toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule,
  toda_pi4_3_finite_cyclic_inference_rule,
  toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule,
  toda_prop27_iota2_whitehead_hopf_invariant_inference_rule,
)


def build_phase50_5_data():
  pi_5_5 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )

  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  pi_3_3 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=3,
  )

  pi_4_3 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
  )

  pi_4_5 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=5,
  )

  iota_2 = HomotopyElement(
    name="ι_2",
    dimension=2,
    generator=GeneratorSymbol(
      family="ι",
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

  whitehead_square = WhiteheadProduct(
    left=iota_2,
    right=iota_2,
  )

  hopf_map = TodaHopfInvariantMap(
    source_group=pi_3_2,
    target_group=pi_3_3,
  )

  eta_2_definition = (
    TodaPi32Eta2DefinitionStatement(
      map=hopf_map,
      element=eta_2,
      image=iota_3,
    )
  )

  eta_2_hopf_relation = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=eta_2,
    ),
    rhs=iota_3,
    relation_type=RelationType.EQUALITY,
  )

  hopf_injectivity = (
    TodaHopfInvariantInjectiveStatement(
      map=hopf_map,
    )
  )

  pi_3_2_relation = Relation(
    lhs=pi_3_2,
    rhs=FreeCyclicGroup(
      generator=eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  delta_map = TodaDeltaMap(
    source_group=pi_5_5,
    target_group=pi_3_2,
  )

  delta_e_exactness = (
    TodaProp42ExactnessStatement(
      window=TodaEHPExactnessWindow(
        source_term=pi_5_5,
        middle_term=pi_3_2,
        target_term=pi_4_3,
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
      ),
    )
  )

  e_h_exactness = (
    TodaProp42ExactnessStatement(
      window=TodaEHPExactnessWindow(
        source_term=pi_3_2,
        middle_term=pi_4_3,
        target_term=pi_4_5,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
      ),
    )
  )

  eta_3_definition = (
    toda_eta_family_definition_statement(
      3
    )
  )

  final_relation = Relation(
    lhs=pi_4_3,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=eta_3,
    ),
    relation_type=RelationType.EQUALITY,
  )

  intermediate_relation = Relation(
    lhs=pi_4_3,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=Suspension(
        expression=eta_2,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  return {
    "pi_5_5": pi_5_5,
    "pi_3_2": pi_3_2,
    "pi_3_3": pi_3_3,
    "pi_4_3": pi_4_3,
    "pi_4_5": pi_4_5,
    "iota_2": iota_2,
    "iota_3": iota_3,
    "eta_2": eta_2,
    "eta_3": eta_3,
    "whitehead_square": (
      whitehead_square
    ),
    "hopf_map": hopf_map,
    "eta_2_definition": (
      eta_2_definition
    ),
    "eta_2_hopf_relation": (
      eta_2_hopf_relation
    ),
    "hopf_injectivity": (
      hopf_injectivity
    ),
    "pi_3_2_relation": (
      pi_3_2_relation
    ),
    "delta_map": delta_map,
    "delta_e_exactness": (
      delta_e_exactness
    ),
    "e_h_exactness": (
      e_h_exactness
    ),
    "eta_3_definition": (
      eta_3_definition
    ),
    "final_relation": (
      final_relation
    ),
    "intermediate_relation": (
      intermediate_relation
    ),
  }


def build_phase50_5_initial_steps(
  data,
):
  return (
    ProofStep(
      conclusion=data[
        "whitehead_square"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "eta_2_definition"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "eta_2_hopf_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "hopf_injectivity"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=pi_5_5_free_cyclic_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "delta_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "delta_e_exactness"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=pi_4_5_zero_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "e_h_exactness"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "pi_3_2_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "eta_3_definition"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def build_phase50_5_rules():
  return (
    toda_prop27_iota2_whitehead_hopf_invariant_inference_rule(),
    toda_pi3_2_whitehead_square_up_to_sign_inference_rule(),
    toda_delta_iota5_whitehead_square_inference_rule(),
    toda_pi4_3_delta_image_free_cyclic_inference_rule(),
    toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule(),
    toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule(),
    toda_pi4_3_finite_cyclic_inference_rule(),
    toda_eta3_suspension_relation_inference_rule(),
    toda_pi4_3_eta3_generator_inference_rule(),
  )


def run_phase50_5(
  initial_steps,
):
  return (
    run_inference_until_stable_with_history(
      build_phase50_5_rules(),
      initial_steps,
    )
  )


def find_final_step(
  result,
  final_relation,
):
  return next(
    (
      step
      for step in result.steps
      if step.conclusion
      == final_relation
    ),
    None,
  )


def test_phase50_5_valid_chain_derives_final_pi4_3_group():
  data = build_phase50_5_data()

  result = run_phase50_5(
    build_phase50_5_initial_steps(
      data
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "final_relation"
  ] in conclusions


def test_phase50_5_intermediate_e_eta2_group_is_derived():
  data = build_phase50_5_data()

  result = run_phase50_5(
    build_phase50_5_initial_steps(
      data
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "intermediate_relation"
  ] in conclusions


def test_phase50_5_final_pi4_3_group_is_not_given():
  data = build_phase50_5_data()

  result = run_phase50_5(
    build_phase50_5_initial_steps(
      data
    )
  )

  final_step = find_final_step(
    result,
    data[
      "final_relation"
    ],
  )

  assert final_step is not None

  assert final_step.rule == (
    ProofRule.INFERENCE
  )


def test_phase50_5_final_step_preserves_inference_rule():
  data = build_phase50_5_data()

  result = run_phase50_5(
    build_phase50_5_initial_steps(
      data
    )
  )

  final_step = find_final_step(
    result,
    data[
      "final_relation"
    ],
  )

  assert final_step is not None

  assert final_step.inference_rule is not None

  assert (
    final_step.inference_rule.name
    == (
      "Toda pi_4^3 eta_3 "
      "generator notation"
    )
  )


def test_phase50_5_final_step_depends_only_on_derived_premises():
  data = build_phase50_5_data()

  result = run_phase50_5(
    build_phase50_5_initial_steps(
      data
    )
  )

  final_step = find_final_step(
    result,
    data[
      "final_relation"
    ],
  )

  assert final_step is not None

  assert len(
    final_step.premises
  ) == 2

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in final_step.premises
  )


def test_phase50_5_wrong_hopf_instance_blocks_final_result():
  data = build_phase50_5_data()

  wrong_hopf_injectivity = (
    TodaHopfInvariantInjectiveStatement(
      map=TodaHopfInvariantMap(
        source_group=data[
          "pi_3_2"
        ],
        target_group=data[
          "pi_4_5"
        ],
      ),
    )
  )

  initial_steps = tuple(
    ProofStep(
      conclusion=(
        wrong_hopf_injectivity
        if step.conclusion
        == data[
          "hopf_injectivity"
        ]
        else step.conclusion
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    )
    for step in (
      build_phase50_5_initial_steps(
        data
      )
    )
  )

  result = run_phase50_5(
    initial_steps
  )

  assert find_final_step(
    result,
    data[
      "final_relation"
    ],
  ) is None


def test_phase50_5_wrong_delta_instance_blocks_final_result():
  data = build_phase50_5_data()

  wrong_delta_map = TodaDeltaMap(
    source_group=data[
      "pi_4_5"
    ],
    target_group=data[
      "pi_3_2"
    ],
  )

  initial_steps = tuple(
    ProofStep(
      conclusion=(
        wrong_delta_map
        if step.conclusion
        == data[
          "delta_map"
        ]
        else step.conclusion
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    )
    for step in (
      build_phase50_5_initial_steps(
        data
      )
    )
  )

  result = run_phase50_5(
    initial_steps
  )

  assert find_final_step(
    result,
    data[
      "final_relation"
    ],
  ) is None


def test_phase50_5_wrong_delta_exactness_window_blocks_final_result():
  data = build_phase50_5_data()

  wrong_exactness = (
    TodaProp42ExactnessStatement(
      window=TodaEHPExactnessWindow(
        source_term=data[
          "pi_5_5"
        ],
        middle_term=data[
          "pi_3_2"
        ],
        target_term=data[
          "pi_4_5"
        ],
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
      ),
    )
  )

  initial_steps = tuple(
    ProofStep(
      conclusion=(
        wrong_exactness
        if step.conclusion
        == data[
          "delta_e_exactness"
        ]
        else step.conclusion
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    )
    for step in (
      build_phase50_5_initial_steps(
        data
      )
    )
  )

  result = run_phase50_5(
    initial_steps
  )

  assert find_final_step(
    result,
    data[
      "final_relation"
    ],
  ) is None


def test_phase50_5_wrong_eta_family_index_blocks_eta3_final_result():
  data = build_phase50_5_data()

  eta_4_definition = (
    toda_eta_family_definition_statement(
      4
    )
  )

  initial_steps = tuple(
    ProofStep(
      conclusion=(
        eta_4_definition
        if step.conclusion
        == data[
          "eta_3_definition"
        ]
        else step.conclusion
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    )
    for step in (
      build_phase50_5_initial_steps(
        data
      )
    )
  )

  result = run_phase50_5(
    initial_steps
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "intermediate_relation"
  ] in conclusions

  assert data[
    "final_relation"
  ] not in conclusions


def test_phase50_5_missing_pi3_2_group_structure_blocks_final_result():
  data = build_phase50_5_data()

  initial_steps = tuple(
    step
    for step in (
      build_phase50_5_initial_steps(
        data
      )
    )
    if step.conclusion
    != data[
      "pi_3_2_relation"
    ]
  )

  result = run_phase50_5(
    initial_steps
  )

  assert find_final_step(
    result,
    data[
      "final_relation"
    ],
  ) is None


def test_phase50_5_does_not_invent_whitehead_sign_specific_equality():
  data = build_phase50_5_data()

  result = run_phase50_5(
    build_phase50_5_initial_steps(
      data
    )
  )

  positive_relation = Relation(
    lhs=data[
      "whitehead_square"
    ],
    rhs=Multiple(
      coefficient=2,
      expression=data[
        "eta_2"
      ],
    ),
    relation_type=RelationType.EQUALITY,
  )

  negative_relation = Relation(
    lhs=data[
      "whitehead_square"
    ],
    rhs=Multiple(
      coefficient=-2,
      expression=data[
        "eta_2"
      ],
    ),
    relation_type=RelationType.EQUALITY,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert positive_relation not in conclusions
  assert negative_relation not in conclusions

  assert any(
    isinstance(
      conclusion,
      TodaPi32WhiteheadSquareUpToSignStatement,
    )
    for conclusion in conclusions
  )


def test_phase50_5_does_not_invent_delta_sign_specific_equality():
  data = build_phase50_5_data()

  result = run_phase50_5(
    build_phase50_5_initial_steps(
      data
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert any(
    isinstance(
      conclusion,
      TodaDeltaImageUpToSignStatement,
    )
    for conclusion in conclusions
  )

  delta_positive_relation = Relation(
    lhs=MapApplication(
      map=EHP_DELTA_MAP,
      expression=HomotopyElement(
        name="ι_5",
        dimension=5,
        generator=GeneratorSymbol(
          family="ι",
          index=5,
        ),
      ),
    ),
    rhs=data[
      "whitehead_square"
    ],
    relation_type=RelationType.EQUALITY,
  )

  assert (
    delta_positive_relation
    not in conclusions
  )


def test_phase50_5_valid_chain_reaches_fixed_point():
  data = build_phase50_5_data()

  result = run_phase50_5(
    build_phase50_5_initial_steps(
      data
    )
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase50_5_all_new_phase50_results_are_inference_derived():
  data = build_phase50_5_data()

  initial_steps = (
    build_phase50_5_initial_steps(
      data
    )
  )

  result = run_phase50_5(
    initial_steps
  )

  initial_conclusions = {
    step.conclusion
    for step in initial_steps
  }

  derived = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      not in initial_conclusions
    )
  )

  assert derived

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in derived
  )

  assert all(
    step.inference_rule
    is not None
    for step in derived
  )



