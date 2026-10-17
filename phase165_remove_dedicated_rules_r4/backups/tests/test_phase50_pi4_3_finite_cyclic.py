from typing import (
  get_type_hints,
)

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  Suspension,
)
from homotopy_groups import (
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
from toda_rules import (
  TodaSuspensionKernelFreeCyclicStatement,
  TodaSuspensionSurjectiveStatement,
  toda_pi4_3_finite_cyclic_inference_rule,
)


def build_phase50_4d_data():
  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  pi_4_3 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
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

  source_group_relation = Relation(
    lhs=pi_3_2,
    rhs=FreeCyclicGroup(
      generator=eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  suspension_map = TodaSuspensionMap(
    source_group=pi_3_2,
    target_group=pi_4_3,
  )

  kernel_statement = (
    TodaSuspensionKernelFreeCyclicStatement(
      map=suspension_map,
      kernel_group=FreeCyclicGroup(
        generator=Multiple(
          coefficient=2,
          expression=eta_2,
        ),
      ),
    )
  )

  surjectivity = (
    TodaSuspensionSurjectiveStatement(
      map=suspension_map,
    )
  )

  final_relation = Relation(
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
    "pi_3_2": pi_3_2,
    "pi_4_3": pi_4_3,
    "eta_2": eta_2,
    "source_group_relation": (
      source_group_relation
    ),
    "suspension_map": (
      suspension_map
    ),
    "kernel_statement": (
      kernel_statement
    ),
    "surjectivity": (
      surjectivity
    ),
    "final_relation": (
      final_relation
    ),
  }


def build_phase50_4d_steps(
  data,
):
  return (
    ProofStep(
      conclusion=data[
        "source_group_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "kernel_statement"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "surjectivity"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def test_phase50_4d_finite_cyclic_order_type():
  type_hints = get_type_hints(
    FiniteCyclicGroup
  )

  assert type_hints[
    "order"
  ] is int


def test_phase50_4d_finite_cyclic_generator_uses_expression():
  type_hints = get_type_hints(
    FiniteCyclicGroup
  )

  assert (
    type_hints[
      "generator"
    ].__name__
    == "Expression"
  )


def test_phase50_4d_expected_group_has_order_two():
  data = build_phase50_4d_data()

  assert data[
    "final_relation"
  ].rhs.order == 2


def test_phase50_4d_expected_generator_is_suspension_eta_2():
  data = build_phase50_4d_data()

  assert data[
    "final_relation"
  ].rhs.generator == (
    Suspension(
      expression=data[
        "eta_2"
      ],
    )
  )


def test_phase50_4d_rule_requires_three_premises():
  rule = (
    toda_pi4_3_finite_cyclic_inference_rule()
  )

  assert len(
    rule.premise_patterns
  ) == 3


def test_phase50_4d_valid_instance_matches():
  data = build_phase50_4d_data()

  assert find_inference_match(
    toda_pi4_3_finite_cyclic_inference_rule(),
    build_phase50_4d_steps(
      data
    ),
  ) is not None


def test_phase50_4d_valid_instance_derives_final_group():
  data = build_phase50_4d_data()

  result = (
    run_inference_until_stable_with_history(
      toda_pi4_3_finite_cyclic_inference_rule(),
      build_phase50_4d_steps(
        data
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "final_relation"
  ] in conclusions


def test_phase50_4d_final_group_is_pi_4_3():
  data = build_phase50_4d_data()

  relation = data[
    "final_relation"
  ]

  assert relation.lhs == (
    TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    )
  )


def test_phase50_4d_final_group_is_finite_cyclic():
  data = build_phase50_4d_data()

  assert isinstance(
    data[
      "final_relation"
    ].rhs,
    FiniteCyclicGroup,
  )


def test_phase50_4d_wrong_kernel_coefficient_is_rejected():
  data = build_phase50_4d_data()

  wrong_kernel = (
    TodaSuspensionKernelFreeCyclicStatement(
      map=data[
        "suspension_map"
      ],
      kernel_group=FreeCyclicGroup(
        generator=Multiple(
          coefficient=3,
          expression=data[
            "eta_2"
          ],
        ),
      ),
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "source_group_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_kernel,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "surjectivity"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_pi4_3_finite_cyclic_inference_rule(),
    steps,
  ) is None


def test_phase50_4d_wrong_source_generator_is_rejected():
  data = build_phase50_4d_data()

  wrong_source = Relation(
    lhs=data[
      "pi_3_2"
    ],
    rhs=FreeCyclicGroup(
      generator=HomotopyElement(
        name="x",
        dimension=2,
        source=3,
        target=2,
        generator=GeneratorSymbol(
          family="x",
          index=2,
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  steps = (
    ProofStep(
      conclusion=wrong_source,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "kernel_statement"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "surjectivity"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_pi4_3_finite_cyclic_inference_rule(),
    steps,
  ) is None


def test_phase50_4d_wrong_surjectivity_instance_is_rejected():
  data = build_phase50_4d_data()

  wrong_surjectivity = (
    TodaSuspensionSurjectiveStatement(
      map=TodaSuspensionMap(
        source_group=data[
          "pi_3_2"
        ],
        target_group=TodaPrimaryGroup(
          group_dimension=5,
          sphere_dimension=4,
        ),
      ),
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "source_group_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "kernel_statement"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_surjectivity,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_pi4_3_finite_cyclic_inference_rule(),
    steps,
  ) is None


def test_phase50_4d_wrong_target_group_is_rejected():
  data = build_phase50_4d_data()

  wrong_map = TodaSuspensionMap(
    source_group=data[
      "pi_3_2"
    ],
    target_group=TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=4,
    ),
  )

  wrong_kernel = (
    TodaSuspensionKernelFreeCyclicStatement(
      map=wrong_map,
      kernel_group=FreeCyclicGroup(
        generator=Multiple(
          coefficient=2,
          expression=data[
            "eta_2"
          ],
        ),
      ),
    )
  )

  wrong_surjectivity = (
    TodaSuspensionSurjectiveStatement(
      map=wrong_map,
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "source_group_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_kernel,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_surjectivity,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_pi4_3_finite_cyclic_inference_rule(),
    steps,
  ) is None


def test_phase50_4d_derived_step_is_inference():
  data = build_phase50_4d_data()

  result = (
    run_inference_until_stable_with_history(
      toda_pi4_3_finite_cyclic_inference_rule(),
      build_phase50_4d_steps(
        data
      ),
    )
  )

  derived = next(
    step
    for step in result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion
      == data[
        "final_relation"
      ]
    )
  )

  assert derived.rule == (
    ProofRule.INFERENCE
  )


def test_phase50_4d_derived_step_preserves_all_premises():
  data = build_phase50_4d_data()

  steps = build_phase50_4d_steps(
    data
  )

  result = (
    run_inference_until_stable_with_history(
      toda_pi4_3_finite_cyclic_inference_rule(),
      steps,
    )
  )

  derived = next(
    step
    for step in result.steps
    if step.conclusion
    == data[
      "final_relation"
    ]
  )

  assert derived.premises == steps


def test_phase50_4d_derived_step_preserves_inference_rule():
  data = build_phase50_4d_data()

  rule = (
    toda_pi4_3_finite_cyclic_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      build_phase50_4d_steps(
        data
      ),
    )
  )

  derived = next(
    step
    for step in result.steps
    if step.conclusion
    == data[
      "final_relation"
    ]
  )

  assert derived.inference_rule == rule


def test_phase50_4d_reaches_fixed_point_in_one_round():
  data = build_phase50_4d_data()

  result = (
    run_inference_until_stable_with_history(
      toda_pi4_3_finite_cyclic_inference_rule(),
      build_phase50_4d_steps(
        data
      ),
    )
  )

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



