from typing import (
  get_type_hints,
)

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  WhiteheadProduct,
)
from homotopy_groups import (
  FreeCyclicGroup,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
  TodaSuspensionMap,
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
  find_inference_match,
  run_inference_until_stable_with_history,
)
from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
  TodaPi32WhiteheadSquareUpToSignStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionKernelFreeCyclicStatement,
  TodaSuspensionSurjectiveStatement,
  toda_pi4_3_delta_image_free_cyclic_inference_rule,
  toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule,
  toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule,
)


def build_phase50_4c_data():
  pi_5_5 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )

  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  pi_4_3 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
  )

  pi_4_5 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=5,
  )

  iota_5 = HomotopyElement(
    name="ι_5",
    dimension=5,
    generator=GeneratorSymbol(
      family="ι",
      index=5,
    ),
  )

  iota_2 = HomotopyElement(
    name="ι_2",
    dimension=2,
    generator=GeneratorSymbol(
      family="ι",
      index=2,
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

  whitehead_square = WhiteheadProduct(
    left=iota_2,
    right=iota_2,
  )

  two_eta_2 = Multiple(
    coefficient=2,
    expression=eta_2,
  )

  delta_map = TodaDeltaMap(
    source_group=pi_5_5,
    target_group=pi_3_2,
  )

  delta_up_to_sign = (
    TodaDeltaImageUpToSignStatement(
      map=delta_map,
      element=iota_5,
      positive_value=whitehead_square,
    )
  )

  whitehead_up_to_sign = (
    TodaPi32WhiteheadSquareUpToSignStatement(
      whitehead_square=whitehead_square,
      positive_value=two_eta_2,
    )
  )

  delta_image = (
    TodaDeltaImageFreeCyclicStatement(
      map=delta_map,
      image_group=FreeCyclicGroup(
        generator=two_eta_2,
      ),
    )
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

  suspension_map = TodaSuspensionMap(
    source_group=pi_3_2,
    target_group=pi_4_3,
  )

  suspension_kernel = (
    TodaSuspensionKernelFreeCyclicStatement(
      map=suspension_map,
      kernel_group=FreeCyclicGroup(
        generator=two_eta_2,
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

  suspension_surjective = (
    TodaSuspensionSurjectiveStatement(
      map=suspension_map,
    )
  )

  return {
    "pi_5_5": pi_5_5,
    "pi_3_2": pi_3_2,
    "pi_4_3": pi_4_3,
    "pi_4_5": pi_4_5,
    "iota_5": iota_5,
    "iota_2": iota_2,
    "eta_2": eta_2,
    "whitehead_square": (
      whitehead_square
    ),
    "two_eta_2": two_eta_2,
    "delta_map": delta_map,
    "delta_up_to_sign": (
      delta_up_to_sign
    ),
    "whitehead_up_to_sign": (
      whitehead_up_to_sign
    ),
    "delta_image": delta_image,
    "delta_e_exactness": (
      delta_e_exactness
    ),
    "suspension_map": (
      suspension_map
    ),
    "suspension_kernel": (
      suspension_kernel
    ),
    "e_h_exactness": (
      e_h_exactness
    ),
    "suspension_surjective": (
      suspension_surjective
    ),
  }


def test_phase50_4c_delta_image_statement_uses_specific_delta_map():
  type_hints = get_type_hints(
    TodaDeltaImageFreeCyclicStatement
  )

  assert type_hints[
    "map"
  ] is TodaDeltaMap


def test_phase50_4c_delta_image_statement_uses_free_cyclic_group():
  type_hints = get_type_hints(
    TodaDeltaImageFreeCyclicStatement
  )

  assert type_hints[
    "image_group"
  ] is FreeCyclicGroup


def test_phase50_4c_kernel_statement_uses_specific_suspension_map():
  type_hints = get_type_hints(
    TodaSuspensionKernelFreeCyclicStatement
  )

  assert type_hints[
    "map"
  ] is TodaSuspensionMap


def test_phase50_4c_surjective_statement_uses_specific_suspension_map():
  type_hints = get_type_hints(
    TodaSuspensionSurjectiveStatement
  )

  assert type_hints[
    "map"
  ] is TodaSuspensionMap


def test_phase50_4c_delta_image_rule_matches_valid_instance():
  data = build_phase50_4c_data()

  steps = (
    ProofStep(
      conclusion=pi_5_5_free_cyclic_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "delta_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "whitehead_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_pi4_3_delta_image_free_cyclic_inference_rule(),
    steps,
  ) is not None


def test_phase50_4c_delta_image_rule_derives_expected_image():
  data = build_phase50_4c_data()

  steps = (
    ProofStep(
      conclusion=pi_5_5_free_cyclic_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "delta_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "whitehead_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  result = (
    run_inference_until_stable_with_history(
      toda_pi4_3_delta_image_free_cyclic_inference_rule(),
      steps,
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "delta_image"
  ] in conclusions


def test_phase50_4c_delta_image_is_generated_by_two_eta_2():
  data = build_phase50_4c_data()

  assert data[
    "delta_image"
  ].image_group == (
    FreeCyclicGroup(
      generator=data[
        "two_eta_2"
      ],
    )
  )


def test_phase50_4c_delta_image_rule_rejects_wrong_source_generator():
  data = build_phase50_4c_data()

  wrong_fact = pi_5_5_free_cyclic_fact()

  wrong_fact = type(
    wrong_fact
  )(
    lhs=wrong_fact.lhs,
    rhs=FreeCyclicGroup(
      generator=HomotopyElement(
        name="x",
        dimension=5,
        generator=GeneratorSymbol(
          family="x",
          index=5,
        ),
      ),
    ),
    relation_type=wrong_fact.relation_type,
  )

  steps = (
    ProofStep(
      conclusion=wrong_fact,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "delta_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "whitehead_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_pi4_3_delta_image_free_cyclic_inference_rule(),
    steps,
  ) is None


def test_phase50_4c_kernel_rule_matches_valid_instance():
  data = build_phase50_4c_data()

  steps = (
    ProofStep(
      conclusion=data[
        "delta_image"
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
  )

  assert find_inference_match(
    toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule(),
    steps,
  ) is not None


def test_phase50_4c_kernel_rule_derives_expected_kernel():
  data = build_phase50_4c_data()

  steps = (
    ProofStep(
      conclusion=data[
        "delta_image"
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
  )

  result = (
    run_inference_until_stable_with_history(
      toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule(),
      steps,
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "suspension_kernel"
  ] in conclusions


def test_phase50_4c_kernel_preserves_two_eta_2():
  data = build_phase50_4c_data()

  assert data[
    "suspension_kernel"
  ].kernel_group == (
    FreeCyclicGroup(
      generator=data[
        "two_eta_2"
      ],
    )
  )


def test_phase50_4c_kernel_rule_rejects_wrong_delta_instance():
  data = build_phase50_4c_data()

  wrong_image = (
    TodaDeltaImageFreeCyclicStatement(
      map=TodaDeltaMap(
        source_group=data[
          "pi_4_5"
        ],
        target_group=data[
          "pi_3_2"
        ],
      ),
      image_group=data[
        "delta_image"
      ].image_group,
    )
  )

  steps = (
    ProofStep(
      conclusion=wrong_image,
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
  )

  assert find_inference_match(
    toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule(),
    steps,
  ) is None


def test_phase50_4c_surjectivity_rule_matches_valid_instance():
  data = build_phase50_4c_data()

  steps = (
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
  )

  assert find_inference_match(
    toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule(),
    steps,
  ) is not None


def test_phase50_4c_surjectivity_rule_derives_expected_result():
  data = build_phase50_4c_data()

  steps = (
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
  )

  result = (
    run_inference_until_stable_with_history(
      toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule(),
      steps,
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "suspension_surjective"
  ] in conclusions


def test_phase50_4c_surjectivity_rule_rejects_wrong_zero_group():
  data = build_phase50_4c_data()

  wrong_zero = type(
    pi_4_5_zero_fact()
  )(
    group=data[
      "pi_3_2"
    ],
  )

  steps = (
    ProofStep(
      conclusion=wrong_zero,
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
  )

  assert find_inference_match(
    toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule(),
    steps,
  ) is None


def test_phase50_4c_end_to_end_derives_image_kernel_and_surjectivity():
  data = build_phase50_4c_data()

  initial_steps = (
    ProofStep(
      conclusion=pi_5_5_free_cyclic_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "delta_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "whitehead_up_to_sign"
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
  )

  rules = (
    toda_pi4_3_delta_image_free_cyclic_inference_rule(),
    toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule(),
    toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule(),
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      initial_steps,
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "delta_image"
  ] in conclusions

  assert data[
    "suspension_kernel"
  ] in conclusions

  assert data[
    "suspension_surjective"
  ] in conclusions


def test_phase50_4c_end_to_end_reaches_fixed_point_in_two_rounds():
  data = build_phase50_4c_data()

  initial_steps = (
    ProofStep(
      conclusion=pi_5_5_free_cyclic_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "delta_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "whitehead_up_to_sign"
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
  )

  rules = (
    toda_pi4_3_delta_image_free_cyclic_inference_rule(),
    toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule(),
    toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule(),
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      initial_steps,
    )
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2


def test_phase50_4c_all_derived_steps_preserve_provenance():
  data = build_phase50_4c_data()

  initial_steps = (
    ProofStep(
      conclusion=pi_5_5_free_cyclic_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "delta_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "whitehead_up_to_sign"
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
  )

  rules = (
    toda_pi4_3_delta_image_free_cyclic_inference_rule(),
    toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule(),
    toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule(),
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      initial_steps,
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


