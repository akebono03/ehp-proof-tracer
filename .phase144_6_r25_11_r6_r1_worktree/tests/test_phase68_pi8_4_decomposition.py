from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  TodaPrimaryGroup,
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
from probes.probe_phase55_capabilities import (
  build_phase55_representative_result,
)
from test_phase63_toda56_integration import (
  build_phase63_6_data,
)
from test_phase68_pi7_3_nu_prime_eta6 import (
  build_phase68_3_data,
)
from toda_rules import (
  Toda56Nu4DecompositionStatement,
  TodaProp51FiniteDimensionalStatement,
  toda_prop58_e_nu_prime_eta6_bridge_inference_rule,
  toda_prop58_pi8_4_decomposition_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase68_4_data():
  phase63_6 = (
    build_phase63_6_data()
  )

  phase68_3 = (
    build_phase68_3_data()
  )

  phase55 = (
    build_phase55_representative_result()
  )

  toda56_step = (
    phase63_6[
      "integration_step"
    ]
  )

  pi7_3_step = (
    phase68_3[
      "final_step"
    ]
  )

  prop51_step = (
    phase55[
      "prop51_steps"
    ][
      0
    ]
  )

  bridge_rule = (
    toda_prop58_e_nu_prime_eta6_bridge_inference_rule()
  )

  decomposition_rule = (
    toda_prop58_pi8_4_decomposition_inference_rule()
  )

  rules = (
    bridge_rule,
    decomposition_rule,
  )

  premise_steps = (
    toda56_step,
    pi7_3_step,
    prop51_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  nu_prime_eta6 = (
    pi7_3_step
    .conclusion
    .rhs
    .generator
  )

  nu_prime = (
    nu_prime_eta6.left
  )

  eta_7 = HomotopyElement(
    name="η₇",
    dimension=7,
    source=8,
    target=7,
    generator=GeneratorSymbol(
      family="η",
      index=7,
    ),
  )

  expected_bridge = Relation(
    lhs=Suspension(
      expression=nu_prime_eta6,
    ),
    rhs=Composition(
      left=Suspension(
        expression=nu_prime,
      ),
      right=eta_7,
    ),
    relation_type=RelationType.EQUALITY,
  )

  bridge_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_bridge
    )
  )

  nu_4 = (
    toda56_step
    .conclusion
    .lemma54_statement
    .nu4
  )

  nu4_eta7 = Composition(
    left=nu_4,
    right=eta_7,
  )

  e_nu_prime_eta7 = (
    expected_bridge.rhs
  )

  expected_final = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=4,
    ),
    rhs=DirectSumGroup(
      summands=(
        FiniteCyclicGroup(
          order=2,
          generator=nu4_eta7,
        ),
        FiniteCyclicGroup(
          order=2,
          generator=e_nu_prime_eta7,
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_final
    )
  )

  return {
    "phase63_6": phase63_6,
    "phase68_3": phase68_3,
    "phase55": phase55,
    "toda56_step": toda56_step,
    "pi7_3_step": pi7_3_step,
    "prop51_step": prop51_step,
    "bridge_rule": bridge_rule,
    "decomposition_rule": (
      decomposition_rule
    ),
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "nu_prime_eta6": (
      nu_prime_eta6
    ),
    "nu_prime": nu_prime,
    "eta_7": eta_7,
    "expected_bridge": (
      expected_bridge
    ),
    "bridge_step": bridge_step,
    "nu_4": nu_4,
    "nu4_eta7": nu4_eta7,
    "e_nu_prime_eta7": (
      e_nu_prime_eta7
    ),
    "expected_final": (
      expected_final
    ),
    "final_step": final_step,
  }


def test_phase68_4_reuses_derived_toda56():
  data = build_phase68_4_data()

  assert isinstance(
    data[
      "toda56_step"
    ].conclusion,
    Toda56Nu4DecompositionStatement,
  )

  assert (
    data[
      "toda56_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_4_reuses_derived_pi7_3():
  data = build_phase68_4_data()

  assert (
    data[
      "pi7_3_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi7_3_step"
    ].conclusion
    .lhs
    == TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=3,
    )
  )


def test_phase68_4_reuses_derived_prop51():
  data = build_phase68_4_data()

  assert isinstance(
    data[
      "prop51_step"
    ].conclusion,
    TodaProp51FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop51_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_4_derives_suspension_bridge():
  data = build_phase68_4_data()

  assert (
    data[
      "bridge_step"
    ].conclusion
    == data[
      "expected_bridge"
    ]
  )

  assert (
    data[
      "bridge_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_4_bridge_is_e_nu_prime_eta6_equals_e_nu_prime_eta7():
  data = build_phase68_4_data()

  assert (
    data[
      "bridge_step"
    ].conclusion.lhs
    == Suspension(
      expression=data[
        "nu_prime_eta6"
      ],
    )
  )

  assert (
    data[
      "bridge_step"
    ].conclusion.rhs
    == Composition(
      left=Suspension(
        expression=data[
          "nu_prime"
        ],
      ),
      right=data[
        "eta_7"
      ],
    )
  )


def test_phase68_4_bridge_uses_exact_dependencies():
  data = build_phase68_4_data()

  assert (
    data[
      "bridge_step"
    ].premises
    == (
      data[
        "pi7_3_step"
      ],
      data[
        "prop51_step"
      ],
    )
  )


def test_phase68_4_final_is_pi8_4():
  data = build_phase68_4_data()

  assert (
    data[
      "final_step"
    ].conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=4,
    )
  )


def test_phase68_4_final_is_direct_sum():
  data = build_phase68_4_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion.rhs,
    DirectSumGroup,
  )

  assert (
    len(
      data[
        "final_step"
      ].conclusion
      .rhs
      .summands
    )
    == 2
  )


def test_phase68_4_first_summand_is_z2_nu4_eta7():
  data = build_phase68_4_data()

  first = (
    data[
      "final_step"
    ].conclusion
    .rhs
    .summands[
      0
    ]
  )

  assert isinstance(
    first,
    FiniteCyclicGroup,
  )

  assert first.order == 2

  assert (
    first.generator
    == data[
      "nu4_eta7"
    ]
  )


def test_phase68_4_second_summand_is_z2_e_nu_prime_eta7():
  data = build_phase68_4_data()

  second = (
    data[
      "final_step"
    ].conclusion
    .rhs
    .summands[
      1
    ]
  )

  assert isinstance(
    second,
    FiniteCyclicGroup,
  )

  assert second.order == 2

  assert (
    second.generator
    == data[
      "e_nu_prime_eta7"
    ]
  )


def test_phase68_4_derives_expected_decomposition():
  data = build_phase68_4_data()

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


def test_phase68_4_final_uses_exact_four_dependencies():
  data = build_phase68_4_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "toda56_step"
      ],
      data[
        "pi7_3_step"
      ],
      data[
        "prop51_step"
      ],
      data[
        "bridge_step"
      ],
    )
  )


def test_phase68_4_bridge_rejects_given_pi7_3():
  data = build_phase68_4_data()

  given_pi7_3 = ProofStep(
    conclusion=(
      data[
        "pi7_3_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "bridge_rule"
    ],
    (
      given_pi7_3,
      data[
        "prop51_step"
      ],
    ),
  ) is None


def test_phase68_4_bridge_rejects_given_prop51():
  data = build_phase68_4_data()

  given_prop51 = ProofStep(
    conclusion=(
      data[
        "prop51_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "bridge_rule"
    ],
    (
      data[
        "pi7_3_step"
      ],
      given_prop51,
    ),
  ) is None


def test_phase68_4_final_rejects_given_toda56():
  data = build_phase68_4_data()

  given_toda56 = ProofStep(
    conclusion=(
      data[
        "toda56_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "decomposition_rule"
    ],
    (
      given_toda56,
      data[
        "pi7_3_step"
      ],
      data[
        "prop51_step"
      ],
      data[
        "bridge_step"
      ],
    ),
  ) is None


def test_phase68_4_final_rejects_given_pi7_3():
  data = build_phase68_4_data()

  given_pi7_3 = ProofStep(
    conclusion=(
      data[
        "pi7_3_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "decomposition_rule"
    ],
    (
      data[
        "toda56_step"
      ],
      given_pi7_3,
      data[
        "prop51_step"
      ],
      data[
        "bridge_step"
      ],
    ),
  ) is None


def test_phase68_4_final_rejects_given_bridge():
  data = build_phase68_4_data()

  given_bridge = ProofStep(
    conclusion=(
      data[
        "bridge_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "decomposition_rule"
    ],
    (
      data[
        "toda56_step"
      ],
      data[
        "pi7_3_step"
      ],
      data[
        "prop51_step"
      ],
      given_bridge,
    ),
  ) is None


def test_phase68_4_final_rejects_wrong_eta7_bridge():
  data = build_phase68_4_data()

  eta_8 = HomotopyElement(
    name="η₈",
    dimension=8,
    source=9,
    target=8,
    generator=GeneratorSymbol(
      family="η",
      index=8,
    ),
  )

  wrong_bridge = replace(
    data[
      "bridge_step"
    ].conclusion,
    rhs=Composition(
      left=Suspension(
        expression=data[
          "nu_prime"
        ],
      ),
      right=eta_8,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_bridge,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "decomposition_rule"
    ],
    (
      data[
        "toda56_step"
      ],
      data[
        "pi7_3_step"
      ],
      data[
        "prop51_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase68_4_final_result_is_not_given():
  data = build_phase68_4_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "expected_final"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase68_4_reaches_fixed_point():
  data = build_phase68_4_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


