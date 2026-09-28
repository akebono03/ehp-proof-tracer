from dataclasses import (
  replace,
)
from functools import (
  lru_cache,
)

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  Sum,
  Suspension,
)
from homotopy_groups import (
  FreeCyclicGroup,
  TodaDeltaMap,
  TodaPrimaryGroup,
)
from low_dimensional_facts import (
  pi_17_17_free_cyclic_fact,
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
from test_phase76_delta_e_exactness_bridge import (
  build_phase76_3_data,
)
from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
  toda_516_delta_iota17_generator_inference_rule,
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
def build_phase76_4_data():
  phase76_3 = (
    build_phase76_3_data()
  )

  delta_image_step = (
    phase76_3[
      "final_step"
    ]
  )

  pi17_17_relation = (
    pi_17_17_free_cyclic_fact()
  )

  pi17_17_step = ProofStep(
    conclusion=pi17_17_relation,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_516_delta_iota17_generator_inference_rule()
  )

  initial_steps = (
    pi17_17_step,
    delta_image_step,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        rule,
      ),
      initial_steps,
    )
  )

  iota_17 = (
    pi17_17_relation
    .rhs
    .generator
  )

  positive_value = (
    delta_image_step
    .conclusion
    .image_group
    .generator
  )

  expected_final = (
    TodaDeltaImageUpToSignStatement(
      map=(
        delta_image_step
        .conclusion
        .map
      ),
      element=iota_17,
      positive_value=positive_value,
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
    "phase76_3": phase76_3,
    "delta_image_step": (
      delta_image_step
    ),
    "pi17_17_relation": (
      pi17_17_relation
    ),
    "pi17_17_step": (
      pi17_17_step
    ),
    "iota_17": iota_17,
    "positive_value": (
      positive_value
    ),
    "rule": rule,
    "initial_steps": (
      initial_steps
    ),
    "result": result,
    "expected_final": (
      expected_final
    ),
    "final_step": final_step,
  }


def test_phase76_4_pi17_17_fact_has_expected_group():
  data = build_phase76_4_data()

  relation = (
    data[
      "pi17_17_relation"
    ]
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=17,
      sphere_dimension=17,
    )
  )

  assert (
    relation.relation_type
    == RelationType.EQUALITY
  )


def test_phase76_4_pi17_17_fact_is_free_cyclic():
  data = build_phase76_4_data()

  assert isinstance(
    data[
      "pi17_17_relation"
    ].rhs,
    FreeCyclicGroup,
  )


def test_phase76_4_pi17_17_generator_is_iota17():
  data = build_phase76_4_data()

  iota_17 = (
    data[
      "iota_17"
    ]
  )

  assert isinstance(
    iota_17,
    HomotopyElement,
  )

  assert (
    iota_17.dimension
    == 17
  )

  assert (
    iota_17.generator
    == GeneratorSymbol(
      family="ι",
      index=17,
    )
  )


def test_phase76_4_pi17_17_fact_remains_given():
  data = build_phase76_4_data()

  assert (
    data[
      "pi17_17_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase76_4_reuses_phase76_3_delta_image():
  data = build_phase76_4_data()

  step = (
    data[
      "delta_image_step"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    step.conclusion,
    TodaDeltaImageFreeCyclicStatement,
  )


def test_phase76_4_delta_image_map_has_expected_groups():
  data = build_phase76_4_data()

  delta_map = (
    data[
      "delta_image_step"
    ].conclusion
    .map
  )

  assert (
    delta_map
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


def test_phase76_4_phase76_3_image_is_free_cyclic():
  data = build_phase76_4_data()

  assert isinstance(
    data[
      "delta_image_step"
    ].conclusion
    .image_group,
    FreeCyclicGroup,
  )


def test_phase76_4_positive_value_has_expected_sum_shape():
  data = build_phase76_4_data()

  positive_value = (
    data[
      "positive_value"
    ]
  )

  assert isinstance(
    positive_value,
    Sum,
  )

  assert isinstance(
    positive_value.left,
    Multiple,
  )

  assert (
    positive_value.left.coefficient
    == 2
  )

  assert isinstance(
    positive_value.right,
    Multiple,
  )

  assert (
    positive_value.right.coefficient
    == -1
  )


def test_phase76_4_positive_value_first_term_is_sigma8():
  data = build_phase76_4_data()

  sigma8 = (
    data[
      "positive_value"
    ]
    .left
    .expression
  )

  assert isinstance(
    sigma8,
    HomotopyElement,
  )

  assert (
    sigma8.source
    == 15
  )

  assert (
    sigma8.target
    == 8
  )

  assert (
    sigma8.generator
    == GeneratorSymbol(
      family="σ",
      index=8,
    )
  )


def test_phase76_4_positive_value_second_term_is_e_sigma_prime():
  data = build_phase76_4_data()

  e_sigma_prime = (
    data[
      "positive_value"
    ]
    .right
    .expression
  )

  assert isinstance(
    e_sigma_prime,
    Suspension,
  )

  sigma_prime = (
    e_sigma_prime
    .expression
  )

  assert isinstance(
    sigma_prime,
    HomotopyElement,
  )

  assert (
    sigma_prime.source
    == 14
  )

  assert (
    sigma_prime.target
    == 7
  )

  assert (
    sigma_prime.generator
    == GeneratorSymbol(
      family="σ",
      decoration="'",
    )
  )


def test_phase76_4_rule_matches_valid_inputs():
  data = build_phase76_4_data()

  assert (
    find_inference_match(
      data[
        "rule"
      ],
      data[
        "initial_steps"
      ],
    )
    is not None
  )


def test_phase76_4_derives_delta_iota17_up_to_sign():
  data = build_phase76_4_data()

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


def test_phase76_4_final_uses_same_delta_map():
  data = build_phase76_4_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .map
    is data[
      "delta_image_step"
    ].conclusion
    .map
  )


def test_phase76_4_final_uses_iota17_generator():
  data = build_phase76_4_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .element
    is data[
      "iota_17"
    ]
  )


def test_phase76_4_final_reuses_exact_image_generator():
  data = build_phase76_4_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .positive_value
    is data[
      "delta_image_step"
    ].conclusion
    .image_group
    .generator
  )


def test_phase76_4_final_is_toda_delta_image_up_to_sign_statement():
  data = build_phase76_4_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion,
    TodaDeltaImageUpToSignStatement,
  )


def test_phase76_4_final_has_exact_direct_premises():
  data = build_phase76_4_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi17_17_step"
      ],
      data[
        "delta_image_step"
      ],
    )
  )


def test_phase76_4_final_not_present_initially():
  data = build_phase76_4_data()

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


def test_phase76_4_rejects_inference_source_group_fact():
  data = build_phase76_4_data()

  source_step = ProofStep(
    conclusion=(
      data[
        "pi17_17_relation"
      ]
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert (
    find_inference_match(
      data[
        "rule"
      ],
      (
        source_step,
        data[
          "delta_image_step"
        ],
      ),
    )
    is None
  )


def test_phase76_4_rejects_given_delta_image():
  data = build_phase76_4_data()

  assert (
    find_inference_match(
      data[
        "rule"
      ],
      (
        data[
          "pi17_17_step"
        ],
        _as_given(
          data[
            "delta_image_step"
          ]
        ),
      ),
    )
    is None
  )


def test_phase76_4_rejects_wrong_source_group():
  data = build_phase76_4_data()

  wrong_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=15,
      sphere_dimension=15,
    ),
    rhs=FreeCyclicGroup(
      generator=(
        data[
          "iota_17"
        ]
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    find_inference_match(
      data[
        "rule"
      ],
      (
        wrong_step,
        data[
          "delta_image_step"
        ],
      ),
    )
    is None
  )


def test_phase76_4_rejects_wrong_iota_generator():
  data = build_phase76_4_data()

  wrong_iota = HomotopyElement(
    name="ι_15",
    dimension=15,
    generator=GeneratorSymbol(
      family="ι",
      index=15,
    ),
  )

  wrong_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=17,
      sphere_dimension=17,
    ),
    rhs=FreeCyclicGroup(
      generator=wrong_iota,
    ),
    relation_type=RelationType.EQUALITY,
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    find_inference_match(
      data[
        "rule"
      ],
      (
        wrong_step,
        data[
          "delta_image_step"
        ],
      ),
    )
    is None
  )


def test_phase76_4_rejects_wrong_delta_target():
  data = build_phase76_4_data()

  original = (
    data[
      "delta_image_step"
    ].conclusion
  )

  wrong_image = replace(
    original,
    map=TodaDeltaMap(
      source_group=TodaPrimaryGroup(
        group_dimension=17,
        sphere_dimension=17,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=14,
        sphere_dimension=8,
      ),
    ),
  )

  wrong_step = (
    _inference_step_with_conclusion(
      data[
        "delta_image_step"
      ],
      wrong_image,
    )
  )

  assert (
    find_inference_match(
      data[
        "rule"
      ],
      (
        data[
          "pi17_17_step"
        ],
        wrong_step,
      ),
    )
    is None
  )


def test_phase76_4_rejects_wrong_sigma8_coefficient():
  data = build_phase76_4_data()

  original = (
    data[
      "delta_image_step"
    ].conclusion
  )

  original_generator = (
    original
    .image_group
    .generator
  )

  wrong_generator = Sum(
    left=Multiple(
      coefficient=4,
      expression=(
        original_generator
        .left
        .expression
      ),
    ),
    right=(
      original_generator.right
    ),
  )

  wrong_image = replace(
    original,
    image_group=FreeCyclicGroup(
      generator=wrong_generator,
    ),
  )

  wrong_step = (
    _inference_step_with_conclusion(
      data[
        "delta_image_step"
      ],
      wrong_image,
    )
  )

  assert (
    find_inference_match(
      data[
        "rule"
      ],
      (
        data[
          "pi17_17_step"
        ],
        wrong_step,
      ),
    )
    is None
  )


def test_phase76_4_rejects_wrong_sigma_prime_sign():
  data = build_phase76_4_data()

  original = (
    data[
      "delta_image_step"
    ].conclusion
  )

  original_generator = (
    original
    .image_group
    .generator
  )

  wrong_generator = Sum(
    left=(
      original_generator.left
    ),
    right=Multiple(
      coefficient=1,
      expression=(
        original_generator
        .right
        .expression
      ),
    ),
  )

  wrong_image = replace(
    original,
    image_group=FreeCyclicGroup(
      generator=wrong_generator,
    ),
  )

  wrong_step = (
    _inference_step_with_conclusion(
      data[
        "delta_image_step"
      ],
      wrong_image,
    )
  )

  assert (
    find_inference_match(
      data[
        "rule"
      ],
      (
        data[
          "pi17_17_step"
        ],
        wrong_step,
      ),
    )
    is None
  )


def test_phase76_4_reaches_fixed_point():
  data = build_phase76_4_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


