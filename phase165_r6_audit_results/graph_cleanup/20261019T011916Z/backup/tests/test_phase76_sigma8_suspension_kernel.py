from dataclasses import (
  replace,
)
from functools import (
  lru_cache,
)

from expression import (
  IteratedSuspension,
  Multiple,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
  TodaSuspensionMap,
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
from test_phase75_pi16_9_sigma9 import (
  build_phase75_8c_data,
)
from test_phase75_prop515_integration import (
  build_phase75_9_data,
)
from toda_rules import (
  TodaSuspensionKernelFreeCyclicStatement,
  toda_516_sigma8_suspension_kernel_inference_rule,
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
def build_phase76_2_data():
  phase75_8c = (
    build_phase75_8c_data()
  )

  phase75_9 = (
    build_phase75_9_data()
  )

  sigma8_step = (
    phase75_8c[
      "sigma8_step"
    ]
  )

  sigma9_definition_step = (
    phase75_8c[
      "sigma9_definition_step"
    ]
  )

  pi16_9_step = (
    phase75_8c[
      "final_step"
    ]
  )

  pi15_8_step = (
    phase75_9[
      "pi15_8_step"
    ]
  )

  rule = (
    toda_516_sigma8_suspension_kernel_inference_rule()
  )

  premise_steps = (
    sigma8_step,
    sigma9_definition_step,
    pi15_8_step,
    pi16_9_step,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        rule,
      ),
      premise_steps,
    )
  )

  sigma8_statement = (
    sigma8_step
    .conclusion
  )

  sigma8 = (
    sigma8_statement
    .sigma8
  )

  sigma_prime = (
    sigma8_statement
    .sigma_prime
  )

  kernel_generator = Sum(
    left=Multiple(
      coefficient=2,
      expression=sigma8,
    ),
    right=Multiple(
      coefficient=-1,
      expression=Suspension(
        expression=sigma_prime,
      ),
    ),
  )

  suspension_map = (
    TodaSuspensionMap(
      source_group=TodaPrimaryGroup(
        group_dimension=15,
        sphere_dimension=8,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=16,
        sphere_dimension=9,
      ),
    )
  )

  expected_final = (
    TodaSuspensionKernelFreeCyclicStatement(
      map=suspension_map,
      kernel_group=FreeCyclicGroup(
        generator=kernel_generator,
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
    "phase75_8c": phase75_8c,
    "phase75_9": phase75_9,
    "sigma8_step": sigma8_step,
    "sigma9_definition_step": (
      sigma9_definition_step
    ),
    "pi15_8_step": pi15_8_step,
    "pi16_9_step": pi16_9_step,
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "sigma8_statement": (
      sigma8_statement
    ),
    "sigma8": sigma8,
    "sigma_prime": sigma_prime,
    "kernel_generator": (
      kernel_generator
    ),
    "suspension_map": suspension_map,
    "expected_final": (
      expected_final
    ),
    "final_step": final_step,
  }


def test_phase76_2_reuses_phase75_sigma8_statement():
  data = build_phase76_2_data()

  assert (
    data[
      "sigma8_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "sigma8_statement"
    ]
    is data[
      "sigma8_step"
    ].conclusion
  )


def test_phase76_2_reuses_phase75_sigma9_definition():
  data = build_phase76_2_data()

  statement = (
    data[
      "sigma9_definition_step"
    ].conclusion
  )

  assert (
    data[
      "sigma9_definition_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    statement.index
    == 9
  )

  assert (
    statement.sigma8_statement
    is data[
      "sigma8_statement"
    ]
  )


def test_phase76_2_sigma9_is_suspension_of_same_sigma8():
  data = build_phase76_2_data()

  statement = (
    data[
      "sigma9_definition_step"
    ].conclusion
  )

  assert (
    statement.iterated_suspension
    == IteratedSuspension(
      expression=data[
        "sigma8"
      ],
      exponent=1,
    )
  )


def test_phase76_2_reuses_phase75_pi15_8_relation():
  data = build_phase76_2_data()

  relation = (
    data[
      "pi15_8_step"
    ].conclusion
  )

  assert (
    data[
      "pi15_8_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=15,
      sphere_dimension=8,
    )
  )

  assert isinstance(
    relation.rhs,
    DirectSumGroup,
  )


def test_phase76_2_pi15_8_has_expected_summands():
  data = build_phase76_2_data()

  relation = (
    data[
      "pi15_8_step"
    ].conclusion
  )

  free_summand = (
    relation
    .rhs
    .summands[
      0
    ]
  )

  torsion_summand = (
    relation
    .rhs
    .summands[
      1
    ]
  )

  assert isinstance(
    free_summand,
    FreeCyclicGroup,
  )

  assert (
    free_summand.generator
    is data[
      "sigma8"
    ]
  )

  assert isinstance(
    torsion_summand,
    FiniteCyclicGroup,
  )

  assert (
    torsion_summand.order
    == 8
  )

  assert (
    torsion_summand.generator
    == Suspension(
      expression=data[
        "sigma_prime"
      ],
    )
  )


def test_phase76_2_reuses_phase75_pi16_9_relation():
  data = build_phase76_2_data()

  relation = (
    data[
      "pi16_9_step"
    ].conclusion
  )

  sigma9 = (
    data[
      "sigma9_definition_step"
    ].conclusion
    .element
  )

  assert (
    data[
      "pi16_9_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    relation
    == Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=16,
        sphere_dimension=9,
      ),
      rhs=FiniteCyclicGroup(
        order=16,
        generator=sigma9,
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase76_2_reuses_lemma514_double_suspension_relation():
  data = build_phase76_2_data()

  statement = (
    data[
      "sigma8_statement"
    ]
  )

  assert (
    statement
    .double_suspension_relation
    == Relation(
      lhs=Multiple(
        coefficient=2,
        expression=Suspension(
          expression=data[
            "sigma8"
          ],
        ),
      ),
      rhs=IteratedSuspension(
        expression=data[
          "sigma_prime"
        ],
        exponent=2,
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase76_2_rule_matches_valid_phase75_data():
  data = build_phase76_2_data()

  assert (
    find_inference_match(
      data[
        "rule"
      ],
      data[
        "premise_steps"
      ],
    )
    is not None
  )


def test_phase76_2_derives_suspension_kernel():
  data = build_phase76_2_data()

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


def test_phase76_2_kernel_uses_correct_suspension_map():
  data = build_phase76_2_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .map
    == TodaSuspensionMap(
      source_group=TodaPrimaryGroup(
        group_dimension=15,
        sphere_dimension=8,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=16,
        sphere_dimension=9,
      ),
    )
  )


def test_phase76_2_kernel_is_free_cyclic():
  data = build_phase76_2_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion
    .kernel_group,
    FreeCyclicGroup,
  )


def test_phase76_2_kernel_generator_is_two_sigma8_minus_e_sigma_prime():
  data = build_phase76_2_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .kernel_group
    .generator
    == Sum(
      left=Multiple(
        coefficient=2,
        expression=data[
          "sigma8"
        ],
      ),
      right=Multiple(
        coefficient=-1,
        expression=Suspension(
          expression=data[
            "sigma_prime"
          ],
        ),
      ),
    )
  )


def test_phase76_2_kernel_generator_reuses_same_sigma8_object():
  data = build_phase76_2_data()

  generator = (
    data[
      "final_step"
    ].conclusion
    .kernel_group
    .generator
  )

  assert (
    generator.left.expression
    is data[
      "sigma8"
    ]
  )


def test_phase76_2_kernel_generator_reuses_same_sigma_prime_object():
  data = build_phase76_2_data()

  generator = (
    data[
      "final_step"
    ].conclusion
    .kernel_group
    .generator
  )

  assert (
    generator
    .right
    .expression
    .expression
    is data[
      "sigma_prime"
    ]
  )


def test_phase76_2_final_uses_exact_dependencies():
  data = build_phase76_2_data()

  assert (
    data[
      "final_step"
    ].premises
    == data[
      "premise_steps"
    ]
  )


def test_phase76_2_final_not_present_initially():
  data = build_phase76_2_data()

  assert (
    data[
      "expected_final"
    ]
    not in tuple(
      step.conclusion
      for step
      in data[
        "premise_steps"
      ]
    )
  )


def test_phase76_2_rejects_given_sigma8_statement():
  data = build_phase76_2_data()

  premises = (
    _as_given(
      data[
        "sigma8_step"
      ]
    ),
    data[
      "sigma9_definition_step"
    ],
    data[
      "pi15_8_step"
    ],
    data[
      "pi16_9_step"
    ],
  )

  assert (
    find_inference_match(
      data[
        "rule"
      ],
      premises,
    )
    is None
  )


def test_phase76_2_rejects_given_sigma9_definition():
  data = build_phase76_2_data()

  premises = (
    data[
      "sigma8_step"
    ],
    _as_given(
      data[
        "sigma9_definition_step"
      ]
    ),
    data[
      "pi15_8_step"
    ],
    data[
      "pi16_9_step"
    ],
  )

  assert (
    find_inference_match(
      data[
        "rule"
      ],
      premises,
    )
    is None
  )


def test_phase76_2_rejects_given_pi15_8_relation():
  data = build_phase76_2_data()

  premises = (
    data[
      "sigma8_step"
    ],
    data[
      "sigma9_definition_step"
    ],
    _as_given(
      data[
        "pi15_8_step"
      ]
    ),
    data[
      "pi16_9_step"
    ],
  )

  assert (
    find_inference_match(
      data[
        "rule"
      ],
      premises,
    )
    is None
  )


def test_phase76_2_rejects_given_pi16_9_relation():
  data = build_phase76_2_data()

  premises = (
    data[
      "sigma8_step"
    ],
    data[
      "sigma9_definition_step"
    ],
    data[
      "pi15_8_step"
    ],
    _as_given(
      data[
        "pi16_9_step"
      ]
    ),
  )

  assert (
    find_inference_match(
      data[
        "rule"
      ],
      premises,
    )
    is None
  )


def test_phase76_2_rejects_wrong_pi15_8_torsion_order():
  data = build_phase76_2_data()

  original = (
    data[
      "pi15_8_step"
    ].conclusion
  )

  free_summand = (
    original
    .rhs
    .summands[
      0
    ]
  )

  torsion_summand = (
    original
    .rhs
    .summands[
      1
    ]
  )

  wrong_relation = Relation(
    lhs=original.lhs,
    rhs=DirectSumGroup(
      summands=(
        free_summand,
        FiniteCyclicGroup(
          order=4,
          generator=(
            torsion_summand
            .generator
          ),
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  wrong_step = (
    _inference_step_with_conclusion(
      data[
        "pi15_8_step"
      ],
      wrong_relation,
    )
  )

  premises = (
    data[
      "sigma8_step"
    ],
    data[
      "sigma9_definition_step"
    ],
    wrong_step,
    data[
      "pi16_9_step"
    ],
  )

  assert (
    find_inference_match(
      data[
        "rule"
      ],
      premises,
    )
    is None
  )


def test_phase76_2_rejects_wrong_pi16_9_order():
  data = build_phase76_2_data()

  original = (
    data[
      "pi16_9_step"
    ].conclusion
  )

  wrong_relation = Relation(
    lhs=original.lhs,
    rhs=FiniteCyclicGroup(
      order=8,
      generator=(
        original
        .rhs
        .generator
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  wrong_step = (
    _inference_step_with_conclusion(
      data[
        "pi16_9_step"
      ],
      wrong_relation,
    )
  )

  premises = (
    data[
      "sigma8_step"
    ],
    data[
      "sigma9_definition_step"
    ],
    data[
      "pi15_8_step"
    ],
    wrong_step,
  )

  assert (
    find_inference_match(
      data[
        "rule"
      ],
      premises,
    )
    is None
  )


def test_phase76_2_rejects_wrong_sigma_family_index():
  data = build_phase76_2_data()

  original = (
    data[
      "sigma9_definition_step"
    ].conclusion
  )

  wrong_definition = replace(
    original,
    index=10,
  )

  wrong_step = (
    _inference_step_with_conclusion(
      data[
        "sigma9_definition_step"
      ],
      wrong_definition,
    )
  )

  premises = (
    data[
      "sigma8_step"
    ],
    wrong_step,
    data[
      "pi15_8_step"
    ],
    data[
      "pi16_9_step"
    ],
  )

  assert (
    find_inference_match(
      data[
        "rule"
      ],
      premises,
    )
    is None
  )


def test_phase76_2_rejects_wrong_sigma8_double_suspension_relation():
  data = build_phase76_2_data()

  original_sigma8 = (
    data[
      "sigma8_statement"
    ]
  )

  wrong_sigma8 = replace(
    original_sigma8,
    double_suspension_relation=Relation(
      lhs=Multiple(
        coefficient=4,
        expression=Suspension(
          expression=data[
            "sigma8"
          ],
        ),
      ),
      rhs=IteratedSuspension(
        expression=data[
          "sigma_prime"
        ],
        exponent=2,
      ),
      relation_type=RelationType.EQUALITY,
    ),
  )

  wrong_sigma8_step = (
    _inference_step_with_conclusion(
      data[
        "sigma8_step"
      ],
      wrong_sigma8,
    )
  )

  original_sigma9_definition = (
    data[
      "sigma9_definition_step"
    ].conclusion
  )

  wrong_sigma9_definition = replace(
    original_sigma9_definition,
    sigma8_statement=wrong_sigma8,
  )

  wrong_sigma9_step = (
    _inference_step_with_conclusion(
      data[
        "sigma9_definition_step"
      ],
      wrong_sigma9_definition,
    )
  )

  premises = (
    wrong_sigma8_step,
    wrong_sigma9_step,
    data[
      "pi15_8_step"
    ],
    data[
      "pi16_9_step"
    ],
  )

  assert (
    find_inference_match(
      data[
        "rule"
      ],
      premises,
    )
    is None
  )


def test_phase76_2_reaches_fixed_point():
  data = build_phase76_2_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


