from proof import (
  ProofRule,
)
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)
from toda_phase65_bootstrap import (
  build_toda_prop56_bootstrap_step,
)
from toda_rules import (
  TodaProp56FiniteDimensionalStatement,
)


def build_phase100_12b1_data():
  phase65 = build_phase65_9_data()

  phase65_2 = phase65[
    "phase65_2"
  ]
  phase65_4 = phase65[
    "phase65_4"
  ]
  phase65_5 = phase65[
    "phase65_5"
  ]
  phase65_7 = phase65[
    "phase65_7"
  ]
  phase65_8 = phase65[
    "phase65_8"
  ]

  phase65_3 = phase65_4[
    "phase65_3"
  ]

  bootstrap_step = (
    build_toda_prop56_bootstrap_step(
      phase65_2[
        "toda52_step"
      ],
      phase65_2[
        "pi5_3_step"
      ],
      phase65_3[
        "hopf_nu_prime_step"
      ],
      phase65_3[
        "prop53_step"
      ],
      phase65_4[
        "double_step"
      ],
      phase65_4[
        "membership_step"
      ],
      phase65_4[
        "hopf_surjective_step"
      ],
      phase65_4[
        "pi6_5_step"
      ],
      phase65_7[
        "toda55_step"
      ],
      phase65_5[
        "toda56_step"
      ],
      phase65_8[
        "stable_isomorphism_step"
      ],
    )
  )

  return {
    "phase65": phase65,
    "bootstrap_step": bootstrap_step,
  }


def test_phase100_12b1_bootstrap_derives_prop56():
  data = build_phase100_12b1_data()

  step = data[
    "bootstrap_step"
  ]

  assert isinstance(
    step.conclusion,
    TodaProp56FiniteDimensionalStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase100_12b1_bootstrap_matches_existing_prop56_conclusion():
  data = build_phase100_12b1_data()

  assert (
    data[
      "bootstrap_step"
    ].conclusion
    == data[
      "phase65"
    ][
      "integration_step"
    ].conclusion
  )


def test_phase100_12b1_bootstrap_preserves_six_aggregate_premises():
  data = build_phase100_12b1_data()

  step = data[
    "bootstrap_step"
  ]

  assert len(
    step.premises
  ) == 6

  assert all(
    premise.rule
    in (
      ProofRule.INFERENCE,
      ProofRule.GIVEN,
    )
    for premise in step.premises
  )

  assert tuple(
    premise.conclusion
    for premise in step.premises
  ) == tuple(
    premise.conclusion
    for premise in data[
      "phase65"
    ][
      "premise_steps"
    ]
  )


def test_phase100_12b1_bootstrap_preserves_branch_provenance():
  data = build_phase100_12b1_data()

  bootstrap_premises = data[
    "bootstrap_step"
  ].premises

  existing_premises = data[
    "phase65"
  ][
    "premise_steps"
  ]

  assert all(
    bootstrap.rule
    == existing.rule
    for bootstrap, existing in zip(
      bootstrap_premises,
      existing_premises,
    )
  )

  assert all(
    len(
      bootstrap.premises
    )
    == len(
      existing.premises
    )
    for bootstrap, existing in zip(
      bootstrap_premises,
      existing_premises,
    )
  )


def test_phase100_12b1_bootstrap_rebuilds_phase65_owned_steps():
  data = build_phase100_12b1_data()

  bootstrap_premises = data[
    "bootstrap_step"
  ].premises

  existing_premises = data[
    "phase65"
  ][
    "premise_steps"
  ]

  assert all(
    bootstrap is not existing
    for bootstrap, existing in zip(
      bootstrap_premises[
        :5
      ],
      existing_premises[
        :5
      ],
    )
  )


def test_phase100_12b1_bootstrap_keeps_range_as_explicit_given():
  data = build_phase100_12b1_data()

  higher_range_step = data[
    "bootstrap_step"
  ].premises[
    5
  ]

  assert (
    higher_range_step.rule
    == ProofRule.GIVEN
  )

  assert (
    higher_range_step
    .conclusion
    .right
    == 6
  )
