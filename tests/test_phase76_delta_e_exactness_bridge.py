from dataclasses import (
  replace,
)
from functools import (
  lru_cache,
)

from homotopy_groups import (
  FreeCyclicGroup,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
  TodaSuspensionMap,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase76_sigma8_suspension_kernel import (
  build_phase76_2_data,
)
from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionKernelFreeCyclicStatement,
  toda_516_concrete_delta_e_exactness_inference_rule,
  toda_516_exactness_kernel_to_delta_image_inference_rule,
)


def _as_given(
  step,
):
  return ProofStep(
    conclusion=step.conclusion,
    premises=(),
    rule=ProofRule.GIVEN,
  )


def _inference_step_with_conclusion(
  step,
  conclusion,
):
  return ProofStep(
    conclusion=conclusion,
    premises=step.premises,
    rule=ProofRule.INFERENCE,
    note=step.note,
    inference_rule=step.inference_rule,
  )


@lru_cache(maxsize=1)
def build_phase76_3_data():
  phase76_2 = (
    build_phase76_2_data()
  )

  kernel_step = (
    phase76_2[
      "final_step"
    ]
  )

  pi17_17 = (
    TodaPrimaryGroup(
      group_dimension=17,
      sphere_dimension=17,
    )
  )

  pi15_8 = (
    TodaPrimaryGroup(
      group_dimension=15,
      sphere_dimension=8,
    )
  )

  pi16_9 = (
    TodaPrimaryGroup(
      group_dimension=16,
      sphere_dimension=9,
    )
  )

  window = (
    TodaEHPExactnessWindow(
      source_term=pi17_17,
      middle_term=pi15_8,
      target_term=pi16_9,
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
    )
  )

  window_step = ProofStep(
    conclusion=window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  exactness_rule = (
    toda_516_concrete_delta_e_exactness_inference_rule()
  )

  image_rule = (
    toda_516_exactness_kernel_to_delta_image_inference_rule()
  )

  rules = (
    exactness_rule,
    image_rule,
  )

  initial_steps = (
    window_step,
    kernel_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      initial_steps,
    )
  )

  expected_exactness = (
    TodaProp42ExactnessStatement(
      window=window,
    )
  )

  exactness_step = next(
    step
    for step
    in result.steps
    if (
      step.conclusion
      == expected_exactness
    )
  )

  expected_delta_map = (
    TodaDeltaMap(
      source_group=pi17_17,
      target_group=pi15_8,
    )
  )

  expected_final = (
    TodaDeltaImageFreeCyclicStatement(
      map=expected_delta_map,
      image_group=(
        kernel_step
        .conclusion
        .kernel_group
      ),
    )
  )

  final_step = next(
    step
    for step
    in result.steps
    if (
      step.conclusion
      == expected_final
    )
  )

  return {
    "phase76_2": phase76_2,
    "kernel_step": kernel_step,
    "pi17_17": pi17_17,
    "pi15_8": pi15_8,
    "pi16_9": pi16_9,
    "window": window,
    "window_step": window_step,
    "exactness_rule": exactness_rule,
    "image_rule": image_rule,
    "rules": rules,
    "initial_steps": initial_steps,
    "result": result,
    "expected_exactness": (
      expected_exactness
    ),
    "exactness_step": (
      exactness_step
    ),
    "expected_delta_map": (
      expected_delta_map
    ),
    "expected_final": (
      expected_final
    ),
    "final_step": final_step,
  }


def test_phase76_3_structural_window_is_given():
  data = build_phase76_3_data()

  assert (
    data[
      "window_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase76_3_window_has_expected_groups():
  data = build_phase76_3_data()

  window = (
    data[
      "window"
    ]
  )

  assert (
    window.source_term
    == TodaPrimaryGroup(
      group_dimension=17,
      sphere_dimension=17,
    )
  )

  assert (
    window.middle_term
    == TodaPrimaryGroup(
      group_dimension=15,
      sphere_dimension=8,
    )
  )

  assert (
    window.target_term
    == TodaPrimaryGroup(
      group_dimension=16,
      sphere_dimension=9,
    )
  )


def test_phase76_3_window_has_delta_then_suspension():
  data = build_phase76_3_data()

  window = (
    data[
      "window"
    ]
  )

  assert (
    window.first_map
    == EHP_DELTA_MAP
  )

  assert (
    window.second_map
    == EHP_E_MAP
  )


def test_phase76_3_exactness_rule_matches_concrete_window():
  data = build_phase76_3_data()

  assert (
    find_inference_match(
      data[
        "exactness_rule"
      ],
      (
        data[
          "window_step"
        ],
      ),
    )
    is not None
  )


def test_phase76_3_derives_exactness():
  data = build_phase76_3_data()

  assert (
    data[
      "exactness_step"
    ].conclusion
    == data[
      "expected_exactness"
    ]
  )

  assert (
    data[
      "exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase76_3_exactness_uses_structural_window_directly():
  data = build_phase76_3_data()

  assert (
    data[
      "exactness_step"
    ].conclusion
    .window
    is data[
      "window"
    ]
  )


def test_phase76_3_exactness_has_exact_direct_premise():
  data = build_phase76_3_data()

  assert (
    data[
      "exactness_step"
    ].premises
    == (
      data[
        "window_step"
      ],
    )
  )


def test_phase76_3_reuses_phase76_2_kernel():
  data = build_phase76_3_data()

  kernel_step = (
    data[
      "kernel_step"
    ]
  )

  assert (
    kernel_step.rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    kernel_step.conclusion,
    TodaSuspensionKernelFreeCyclicStatement,
  )

  assert isinstance(
    kernel_step
    .conclusion
    .kernel_group,
    FreeCyclicGroup,
  )


def test_phase76_3_kernel_map_matches_exactness_right_map():
  data = build_phase76_3_data()

  kernel_map = (
    data[
      "kernel_step"
    ].conclusion
    .map
  )

  assert (
    kernel_map
    == TodaSuspensionMap(
      source_group=(
        data[
          "pi15_8"
        ]
      ),
      target_group=(
        data[
          "pi16_9"
        ]
      ),
    )
  )


def test_phase76_3_image_rule_matches_kernel_and_exactness():
  data = build_phase76_3_data()

  assert (
    find_inference_match(
      data[
        "image_rule"
      ],
      (
        data[
          "kernel_step"
        ],
        data[
          "exactness_step"
        ],
      ),
    )
    is not None
  )


def test_phase76_3_derives_delta_image():
  data = build_phase76_3_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_final"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase76_3_delta_image_uses_expected_map():
  data = build_phase76_3_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .map
    == TodaDeltaMap(
      source_group=TodaPrimaryGroup(
        group_dimension=17,
        sphere_dimension=17,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=15,
        sphere_dimension=8,
      ),
    )
  )


def test_phase76_3_delta_image_is_free_cyclic():
  data = build_phase76_3_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion
    .image_group,
    FreeCyclicGroup,
  )


def test_phase76_3_delta_image_reuses_kernel_group_object():
  data = build_phase76_3_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .image_group
    is data[
      "kernel_step"
    ].conclusion
    .kernel_group
  )


def test_phase76_3_delta_image_generator_reuses_phase76_2_generator():
  data = build_phase76_3_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .image_group
    .generator
    is data[
      "kernel_step"
    ].conclusion
    .kernel_group
    .generator
  )


def test_phase76_3_final_has_exact_direct_premises():
  data = build_phase76_3_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "kernel_step"
      ],
      data[
        "exactness_step"
      ],
    )
  )


def test_phase76_3_final_not_present_initially():
  data = build_phase76_3_data()

  assert (
    data[
      "expected_final"
    ]
    not in tuple(
      step.conclusion
      for step
      in data[
        "initial_steps"
      ]
    )
  )


def test_phase76_3_exactness_rule_rejects_inference_window():
  data = build_phase76_3_data()

  inference_window_step = ProofStep(
    conclusion=data[
      "window"
    ],
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert (
    find_inference_match(
      data[
        "exactness_rule"
      ],
      (
        inference_window_step,
      ),
    )
    is None
  )


def test_phase76_3_exactness_rule_rejects_wrong_source_dimension():
  data = build_phase76_3_data()

  wrong_window = replace(
    data[
      "window"
    ],
    source_term=TodaPrimaryGroup(
      group_dimension=15,
      sphere_dimension=15,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    find_inference_match(
      data[
        "exactness_rule"
      ],
      (
        wrong_step,
      ),
    )
    is None
  )


def test_phase76_3_exactness_rule_rejects_wrong_middle_group():
  data = build_phase76_3_data()

  wrong_window = replace(
    data[
      "window"
    ],
    middle_term=TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=8,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    find_inference_match(
      data[
        "exactness_rule"
      ],
      (
        wrong_step,
      ),
    )
    is None
  )


def test_phase76_3_exactness_rule_rejects_wrong_target_group():
  data = build_phase76_3_data()

  wrong_window = replace(
    data[
      "window"
    ],
    target_term=TodaPrimaryGroup(
      group_dimension=16,
      sphere_dimension=10,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    find_inference_match(
      data[
        "exactness_rule"
      ],
      (
        wrong_step,
      ),
    )
    is None
  )


def test_phase76_3_exactness_rule_rejects_wrong_map_order():
  data = build_phase76_3_data()

  wrong_window = replace(
    data[
      "window"
    ],
    first_map=EHP_E_MAP,
    second_map=EHP_DELTA_MAP,
  )

  wrong_step = ProofStep(
    conclusion=wrong_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    find_inference_match(
      data[
        "exactness_rule"
      ],
      (
        wrong_step,
      ),
    )
    is None
  )


def test_phase76_3_image_rule_rejects_given_kernel():
  data = build_phase76_3_data()

  assert (
    find_inference_match(
      data[
        "image_rule"
      ],
      (
        _as_given(
          data[
            "kernel_step"
          ]
        ),
        data[
          "exactness_step"
        ],
      ),
    )
    is None
  )


def test_phase76_3_image_rule_rejects_given_exactness():
  data = build_phase76_3_data()

  assert (
    find_inference_match(
      data[
        "image_rule"
      ],
      (
        data[
          "kernel_step"
        ],
        _as_given(
          data[
            "exactness_step"
          ]
        ),
      ),
    )
    is None
  )


def test_phase76_3_image_rule_rejects_wrong_kernel_map():
  data = build_phase76_3_data()

  original_kernel = (
    data[
      "kernel_step"
    ].conclusion
  )

  wrong_kernel = replace(
    original_kernel,
    map=TodaSuspensionMap(
      source_group=TodaPrimaryGroup(
        group_dimension=14,
        sphere_dimension=7,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=15,
        sphere_dimension=8,
      ),
    ),
  )

  wrong_kernel_step = (
    _inference_step_with_conclusion(
      data[
        "kernel_step"
      ],
      wrong_kernel,
    )
  )

  assert (
    find_inference_match(
      data[
        "image_rule"
      ],
      (
        wrong_kernel_step,
        data[
          "exactness_step"
        ],
      ),
    )
    is None
  )


def test_phase76_3_image_rule_rejects_wrong_exactness_window():
  data = build_phase76_3_data()

  wrong_window = replace(
    data[
      "window"
    ],
    source_term=TodaPrimaryGroup(
      group_dimension=15,
      sphere_dimension=15,
    ),
  )

  wrong_exactness = (
    TodaProp42ExactnessStatement(
      window=wrong_window,
    )
  )

  wrong_exactness_step = (
    _inference_step_with_conclusion(
      data[
        "exactness_step"
      ],
      wrong_exactness,
    )
  )

  assert (
    find_inference_match(
      data[
        "image_rule"
      ],
      (
        data[
          "kernel_step"
        ],
        wrong_exactness_step,
      ),
    )
    is None
  )


def test_phase76_3_reaches_fixed_point():
  data = build_phase76_3_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


