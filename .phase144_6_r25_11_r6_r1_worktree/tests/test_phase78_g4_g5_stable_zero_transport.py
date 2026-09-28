from functools import lru_cache

from homotopy_groups import (
  StableHomotopyGroup,
  StablePrimaryComponent,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase68_pi_n_plus_4_n_zero import (
  build_phase68_10_data,
)
from test_phase70_pi_n_plus_5_n_zero import (
  build_phase70_9_data,
)
from toda_rules import (
  Toda45StableTwoPrimaryIdentificationStatement,
  Toda45StableTwoPrimaryZeroStatement,
  toda_45_stable_two_primary_identification_inference_rule,
  toda_prop58_g4_two_primary_zero_inference_rule,
  toda_prop59_g5_two_primary_zero_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase78_9_data():
  phase68_10 = (
    build_phase68_10_data()
  )

  phase70_9 = (
    build_phase70_9_data()
  )

  pi10_6_zero_step = (
    phase68_10[
      "pi10_6_zero_step"
    ]
  )

  pi12_7_zero_step = (
    phase70_9[
      "pi12_7_zero_step"
    ]
  )

  g4_source_group = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=6,
  )

  g5_source_group = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=7,
  )

  g4_source_group_step = ProofStep(
    conclusion=g4_source_group,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  g5_source_group_step = ProofStep(
    conclusion=g5_source_group,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  identification_rule = (
    toda_45_stable_two_primary_identification_inference_rule()
  )

  g4_zero_rule = (
    toda_prop58_g4_two_primary_zero_inference_rule()
  )

  g5_zero_rule = (
    toda_prop59_g5_two_primary_zero_inference_rule()
  )

  rules = (
    identification_rule,
    g4_zero_rule,
    g5_zero_rule,
  )

  premise_steps = (
    pi10_6_zero_step,
    pi12_7_zero_step,
    g4_source_group_step,
    g5_source_group_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  expected_g4_identification = (
    Toda45StableTwoPrimaryIdentificationStatement(
      source_group=g4_source_group,
      target_component=StablePrimaryComponent(
        group=StableHomotopyGroup(
          stem=4,
        ),
        prime=2,
      ),
    )
  )

  expected_g5_identification = (
    Toda45StableTwoPrimaryIdentificationStatement(
      source_group=g5_source_group,
      target_component=StablePrimaryComponent(
        group=StableHomotopyGroup(
          stem=5,
        ),
        prime=2,
      ),
    )
  )

  g4_identification_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_g4_identification
    )
  )

  g5_identification_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_g5_identification
    )
  )

  expected_g4_zero = (
    Toda45StableTwoPrimaryZeroStatement(
      source_zero=(
        pi10_6_zero_step
        .conclusion
      ),
      identification=(
        g4_identification_step
        .conclusion
      ),
      stable_component=StablePrimaryComponent(
        group=StableHomotopyGroup(
          stem=4,
        ),
        prime=2,
      ),
    )
  )

  expected_g5_zero = (
    Toda45StableTwoPrimaryZeroStatement(
      source_zero=(
        pi12_7_zero_step
        .conclusion
      ),
      identification=(
        g5_identification_step
        .conclusion
      ),
      stable_component=StablePrimaryComponent(
        group=StableHomotopyGroup(
          stem=5,
        ),
        prime=2,
      ),
    )
  )

  g4_zero_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_g4_zero
    )
  )

  g5_zero_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_g5_zero
    )
  )

  return {
    "phase68_10": phase68_10,
    "phase70_9": phase70_9,
    "pi10_6_zero_step": (
      pi10_6_zero_step
    ),
    "pi12_7_zero_step": (
      pi12_7_zero_step
    ),
    "g4_source_group": (
      g4_source_group
    ),
    "g5_source_group": (
      g5_source_group
    ),
    "g4_source_group_step": (
      g4_source_group_step
    ),
    "g5_source_group_step": (
      g5_source_group_step
    ),
    "identification_rule": (
      identification_rule
    ),
    "g4_zero_rule": g4_zero_rule,
    "g5_zero_rule": g5_zero_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "g4_identification_step": (
      g4_identification_step
    ),
    "g5_identification_step": (
      g5_identification_step
    ),
    "expected_g4_zero": (
      expected_g4_zero
    ),
    "expected_g5_zero": (
      expected_g5_zero
    ),
    "g4_zero_step": g4_zero_step,
    "g5_zero_step": g5_zero_step,
  }


def test_phase78_9_reuses_derived_pi10_6_zero():
  data = build_phase78_9_data()

  assert (
    data[
      "pi10_6_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi10_6_zero_step"
    ].conclusion
    == TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=6,
      ),
    )
  )


def test_phase78_9_reuses_derived_pi12_7_zero():
  data = build_phase78_9_data()

  assert (
    data[
      "pi12_7_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi12_7_zero_step"
    ].conclusion
    == TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=12,
        sphere_dimension=7,
      ),
    )
  )


def test_phase78_9_derives_g4_stable_identification():
  data = build_phase78_9_data()

  assert (
    data[
      "g4_identification_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "g4_identification_step"
    ].conclusion
    .target_component
    == StablePrimaryComponent(
      group=StableHomotopyGroup(
        stem=4,
      ),
      prime=2,
    )
  )


def test_phase78_9_derives_g5_stable_identification():
  data = build_phase78_9_data()

  assert (
    data[
      "g5_identification_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "g5_identification_step"
    ].conclusion
    .target_component
    == StablePrimaryComponent(
      group=StableHomotopyGroup(
        stem=5,
      ),
      prime=2,
    )
  )


def test_phase78_9_derives_g4_two_primary_zero():
  data = build_phase78_9_data()

  assert (
    data[
      "g4_zero_step"
    ].conclusion
    == data[
      "expected_g4_zero"
    ]
  )

  assert (
    data[
      "g4_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase78_9_g4_zero_targets_exact_component():
  data = build_phase78_9_data()

  assert (
    data[
      "g4_zero_step"
    ].conclusion
    .stable_component
    == StablePrimaryComponent(
      group=StableHomotopyGroup(
        stem=4,
      ),
      prime=2,
    )
  )


def test_phase78_9_g4_zero_uses_exact_dependencies():
  data = build_phase78_9_data()

  assert (
    data[
      "g4_zero_step"
    ].premises
    == (
      data[
        "pi10_6_zero_step"
      ],
      data[
        "g4_identification_step"
      ],
    )
  )


def test_phase78_9_derives_g5_two_primary_zero():
  data = build_phase78_9_data()

  assert (
    data[
      "g5_zero_step"
    ].conclusion
    == data[
      "expected_g5_zero"
    ]
  )

  assert (
    data[
      "g5_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase78_9_g5_zero_targets_exact_component():
  data = build_phase78_9_data()

  assert (
    data[
      "g5_zero_step"
    ].conclusion
    .stable_component
    == StablePrimaryComponent(
      group=StableHomotopyGroup(
        stem=5,
      ),
      prime=2,
    )
  )


def test_phase78_9_g5_zero_uses_exact_dependencies():
  data = build_phase78_9_data()

  assert (
    data[
      "g5_zero_step"
    ].premises
    == (
      data[
        "pi12_7_zero_step"
      ],
      data[
        "g5_identification_step"
      ],
    )
  )


def test_phase78_9_g4_zero_not_present_initially():
  data = build_phase78_9_data()

  assert (
    data[
      "expected_g4_zero"
    ]
    not in tuple(
      step.conclusion
      for step
      in data[
        "premise_steps"
      ]
    )
  )


def test_phase78_9_g5_zero_not_present_initially():
  data = build_phase78_9_data()

  assert (
    data[
      "expected_g5_zero"
    ]
    not in tuple(
      step.conclusion
      for step
      in data[
        "premise_steps"
      ]
    )
  )


def test_phase78_9_g4_rejects_given_source_zero():
  data = build_phase78_9_data()

  given_source_zero = ProofStep(
    conclusion=(
      data[
        "pi10_6_zero_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "g4_zero_rule"
    ],
    (
      given_source_zero,
      data[
        "g4_identification_step"
      ],
    ),
  ) is None


def test_phase78_9_g5_rejects_given_source_zero():
  data = build_phase78_9_data()

  given_source_zero = ProofStep(
    conclusion=(
      data[
        "pi12_7_zero_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "g5_zero_rule"
    ],
    (
      given_source_zero,
      data[
        "g5_identification_step"
      ],
    ),
  ) is None


def test_phase78_9_g4_rejects_given_identification():
  data = build_phase78_9_data()

  given_identification = ProofStep(
    conclusion=(
      data[
        "g4_identification_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "g4_zero_rule"
    ],
    (
      data[
        "pi10_6_zero_step"
      ],
      given_identification,
    ),
  ) is None


def test_phase78_9_g5_rejects_given_identification():
  data = build_phase78_9_data()

  given_identification = ProofStep(
    conclusion=(
      data[
        "g5_identification_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "g5_zero_rule"
    ],
    (
      data[
        "pi12_7_zero_step"
      ],
      given_identification,
    ),
  ) is None


def test_phase78_9_g4_rule_rejects_g5_zero():
  data = build_phase78_9_data()

  assert find_inference_match(
    data[
      "g4_zero_rule"
    ],
    (
      data[
        "pi12_7_zero_step"
      ],
      data[
        "g5_identification_step"
      ],
    ),
  ) is None


def test_phase78_9_g5_rule_rejects_g4_zero():
  data = build_phase78_9_data()

  assert find_inference_match(
    data[
      "g5_zero_rule"
    ],
    (
      data[
        "pi10_6_zero_step"
      ],
      data[
        "g4_identification_step"
      ],
    ),
  ) is None


def test_phase78_9_reaches_fixed_point():
  data = build_phase78_9_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )
  


