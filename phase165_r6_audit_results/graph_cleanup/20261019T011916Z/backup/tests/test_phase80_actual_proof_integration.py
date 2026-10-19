from functools import lru_cache

from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_inference import (
  derive_goal_from_repository,
  repository_available_steps,
)
from test_phase77_applicability_provenance import (
  build_phase77_6_data,
)


@lru_cache(maxsize=1)
def build_phase80_5_data():
  phase77 = build_phase77_6_data()

  bracket_sum_step = phase77[
    "bracket_sum_step"
  ]
  composition_step = phase77[
    "composition_step"
  ]
  original_final_step = phase77[
    "final_step"
  ]
  final_rule = phase77[
    "data"
  ][
    "final_rule"
  ]

  repository = ProofRepository()

  bracket_sum_entry = ProofRepositoryEntry(
    key=(
      "phase80.phase77."
      "bracket_sum"
    ),
    step=bracket_sum_step,
    phase="77",
    theorem=(
      "Toda Lemma 5.16 "
      "bracket-sum premise"
    ),
  )

  composition_entry = ProofRepositoryEntry(
    key=(
      "phase80.phase77."
      "scaled_composition"
    ),
    step=composition_step,
    phase="77",
    theorem=(
      "Toda Lemma 5.16 "
      "scaled-composition premise"
    ),
  )

  repository.register(
    bracket_sum_entry
  )
  repository.register(
    composition_entry
  )

  goal = (
    original_final_step.conclusion
  )

  return {
    "phase77": phase77,
    "repository": repository,
    "bracket_sum_entry": (
      bracket_sum_entry
    ),
    "composition_entry": (
      composition_entry
    ),
    "bracket_sum_step": (
      bracket_sum_step
    ),
    "composition_step": (
      composition_step
    ),
    "original_final_step": (
      original_final_step
    ),
    "final_rule": final_rule,
    "goal": goal,
  }


def test_phase80_5_repository_contains_only_actual_phase77_direct_premises():
  data = build_phase80_5_data()

  assert (
    data[
      "repository"
    ].entries()
    == (
      data[
        "bracket_sum_entry"
      ],
      data[
        "composition_entry"
      ],
    )
  )

  assert (
    repository_available_steps(
      data[
        "repository"
      ]
    )
    == (
      data[
        "bracket_sum_step"
      ],
      data[
        "composition_step"
      ],
    )
  )


def test_phase80_5_goal_is_not_registered_initially():
  data = build_phase80_5_data()

  assert (
    data[
      "repository"
    ].find_by_conclusion(
      data[
        "goal"
      ]
    )
    == ()
  )

  assert all(
    step.conclusion
    != data[
      "goal"
    ]
    for step in (
      repository_available_steps(
        data[
          "repository"
        ]
      )
    )
  )


def test_phase80_5_repository_assisted_runner_derives_actual_phase77_goal():
  data = build_phase80_5_data()

  result = (
    derive_goal_from_repository(
      data[
        "repository"
      ],
      (
        data[
          "final_rule"
        ],
      ),
      data[
        "goal"
      ],
    )
  )

  assert result.goal_step is not None
  assert (
    result.goal_step.conclusion
    == data[
      "goal"
    ]
  )
  assert (
    result.goal_step.rule
    == ProofRule.INFERENCE
  )


def test_phase80_5_derived_goal_is_new_proof_step_not_original_final_step():
  data = build_phase80_5_data()

  result = (
    derive_goal_from_repository(
      data[
        "repository"
      ],
      (
        data[
          "final_rule"
        ],
      ),
      data[
        "goal"
      ],
    )
  )

  assert result.goal_step is not None
  assert (
    result.goal_step
    is not data[
      "original_final_step"
    ]
  )
  assert (
    result.goal_step.conclusion
    == data[
      "original_final_step"
    ].conclusion
  )


def test_phase80_5_derived_goal_uses_exact_repository_steps_as_premises():
  data = build_phase80_5_data()

  result = (
    derive_goal_from_repository(
      data[
        "repository"
      ],
      (
        data[
          "final_rule"
        ],
      ),
      data[
        "goal"
      ],
    )
  )

  goal_step = result.goal_step

  assert goal_step is not None
  assert goal_step.premises == (
    data[
      "bracket_sum_step"
    ],
    data[
      "composition_step"
    ],
  )
  assert (
    goal_step.premises[0]
    is data[
      "bracket_sum_step"
    ]
  )
  assert (
    goal_step.premises[1]
    is data[
      "composition_step"
    ]
  )


def test_phase80_5_derived_goal_records_existing_phase77_final_rule():
  data = build_phase80_5_data()

  result = (
    derive_goal_from_repository(
      data[
        "repository"
      ],
      (
        data[
          "final_rule"
        ],
      ),
      data[
        "goal"
      ],
    )
  )

  assert result.goal_step is not None
  assert (
    result.goal_step.inference_rule
    is data[
      "final_rule"
    ]
  )


def test_phase80_5_actual_inference_reaches_fixed_point():
  data = build_phase80_5_data()

  result = (
    derive_goal_from_repository(
      data[
        "repository"
      ],
      (
        data[
          "final_rule"
        ],
      ),
      data[
        "goal"
      ],
    )
  )

  assert (
    result
    .inference_result
    .termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase80_5_inference_result_preserves_initial_repository_step_identity():
  data = build_phase80_5_data()

  result = (
    derive_goal_from_repository(
      data[
        "repository"
      ],
      (
        data[
          "final_rule"
        ],
      ),
      data[
        "goal"
      ],
    )
  )

  assert (
    result
    .inference_result
    .steps[0]
    is data[
      "bracket_sum_step"
    ]
  )
  assert (
    result
    .inference_result
    .steps[1]
    is data[
      "composition_step"
    ]
  )


def test_phase80_5_goal_step_is_exact_step_in_inference_result():
  data = build_phase80_5_data()

  result = (
    derive_goal_from_repository(
      data[
        "repository"
      ],
      (
        data[
          "final_rule"
        ],
      ),
      data[
        "goal"
      ],
    )
  )

  assert result.goal_step is not None
  assert any(
    step is result.goal_step
    for step in (
      result
      .inference_result
      .steps
    )
  )


def test_phase80_5_repository_is_not_mutated_by_actual_inference():
  data = build_phase80_5_data()

  repository = data[
    "repository"
  ]

  before_entries = (
    repository.entries()
  )

  result = (
    derive_goal_from_repository(
      repository,
      (
        data[
          "final_rule"
        ],
      ),
      data[
        "goal"
      ],
    )
  )

  assert result.goal_step is not None
  assert (
    repository.entries()
    == before_entries
  )
  assert (
    repository.find_by_conclusion(
      data[
        "goal"
      ]
    )
    == ()
  )
