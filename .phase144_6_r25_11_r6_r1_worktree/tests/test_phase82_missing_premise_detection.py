from functools import lru_cache

from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_inference import (
  detect_goal_rule_missing_premises,
  detect_missing_premises,
  repository_available_steps,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)
from test_phase77_applicability_provenance import (
  build_phase77_6_data,
)
from toda_rules import (
  TodaLemma516ScaledCompositionBridgeStatement,
)


@lru_cache(maxsize=1)
def build_phase82_2_data():
  phase77 = build_phase77_6_data()

  final_rule = (
    phase77[
      "data"
    ][
      "final_rule"
    ]
  )

  goal = (
    phase77[
      "final_step"
    ].conclusion
  )

  repository = ProofRepository()

  repository.register(
    ProofRepositoryEntry(
      key=(
        "phase82."
        "bracket_sum"
      ),
      step=phase77[
        "bracket_sum_step"
      ],
      phase="82",
      theorem=(
        "Toda Lemma 5.16 "
        "missing-premise detection"
      ),
    )
  )

  repository.register(
    ProofRepositoryEntry(
      key=(
        "phase82."
        "suspension_bridge"
      ),
      step=phase77[
        "suspension_bridge_step"
      ],
      phase="82",
      theorem=(
        "Toda Lemma 5.16 "
        "missing-premise detection"
      ),
    )
  )

  repository.register(
    ProofRepositoryEntry(
      key=(
        "phase82."
        "sigma_definition"
      ),
      step=phase77[
        "sigma_definition_step"
      ],
      phase="82",
      theorem=(
        "Toda Lemma 5.16 "
        "missing-premise detection"
      ),
    )
  )

  catalog = InferenceRuleCatalog()

  catalog.register(
    InferenceRuleCatalogEntry(
      key=(
        "phase82."
        "toda_lemma516_final"
      ),
      rule=final_rule,
      conclusion_type=type(
        goal
      ),
      fixed_point_safe=True,
    )
  )

  direct_detection = (
    detect_missing_premises(
      final_rule,
      repository_available_steps(
        repository
      ),
    )
  )

  goal_detections = (
    detect_goal_rule_missing_premises(
      repository,
      catalog,
      goal,
    )
  )

  return {
    "phase77": phase77,
    "repository": repository,
    "catalog": catalog,
    "goal": goal,
    "final_rule": final_rule,
    "direct_detection": (
      direct_detection
    ),
    "goal_detections": (
      goal_detections
    ),
  }


def test_phase82_2_goal_selects_one_actual_final_rule():
  data = build_phase82_2_data()

  assert len(
    data[
      "goal_detections"
    ]
  ) == 1

  assert (
    data[
      "goal_detections"
    ][
      0
    ].inference_rule
    is data[
      "final_rule"
    ]
  )


def test_phase82_2_detects_exactly_one_missing_premise():
  data = build_phase82_2_data()

  detection = data[
    "direct_detection"
  ]

  assert (
    detection.missing_indices
    == (
      1,
    )
  )

  assert len(
    detection.missing_patterns
  ) == 1

  assert not (
    detection.is_complete
  )


def test_phase82_2_reuses_exact_available_bracket_sum_step():
  data = build_phase82_2_data()

  detection = data[
    "direct_detection"
  ]

  assert (
    detection.matched_steps[
      0
    ]
    is data[
      "phase77"
    ][
      "bracket_sum_step"
    ]
  )


def test_phase82_2_marks_scaled_composition_premise_missing():
  data = build_phase82_2_data()

  detection = data[
    "direct_detection"
  ]

  assert (
    detection.matched_steps[
      1
    ]
    is None
  )

  missing_pattern = (
    detection.missing_patterns[
      0
    ]
  )

  assert (
    missing_pattern.statement_type
    is
    TodaLemma516ScaledCompositionBridgeStatement
  )


def test_phase82_2_missing_pattern_is_exact_final_rule_pattern():
  data = build_phase82_2_data()

  detection = data[
    "direct_detection"
  ]

  assert (
    detection.missing_patterns[
      0
    ]
    is data[
      "final_rule"
    ].premise_patterns[
      1
    ]
  )


def test_phase82_2_composition_step_is_not_initially_available():
  data = build_phase82_2_data()

  available_steps = (
    repository_available_steps(
      data[
        "repository"
      ]
    )
  )

  assert all(
    step
    is not data[
      "phase77"
    ][
      "composition_step"
    ]
    for step in available_steps
  )

  assert all(
    step.conclusion
    != data[
      "phase77"
    ][
      "composition_step"
    ].conclusion
    for step in available_steps
  )


def test_phase82_2_future_producer_premises_do_not_satisfy_final_rule():
  data = build_phase82_2_data()

  detection = data[
    "direct_detection"
  ]

  assert (
    data[
      "phase77"
    ][
      "suspension_bridge_step"
    ]
    in repository_available_steps(
      data[
        "repository"
      ]
    )
  )

  assert (
    data[
      "phase77"
    ][
      "sigma_definition_step"
    ]
    in repository_available_steps(
      data[
        "repository"
      ]
    )
  )

  assert (
    detection.missing_indices
    == (
      1,
    )
  )


def test_phase82_2_goal_level_detection_matches_direct_detection():
  data = build_phase82_2_data()

  detection = (
    data[
      "goal_detections"
    ][
      0
    ]
  )

  direct = data[
    "direct_detection"
  ]

  assert (
    detection.inference_rule
    is direct.inference_rule
  )

  assert (
    detection.matched_steps
    == direct.matched_steps
  )

  assert (
    detection.missing_indices
    == direct.missing_indices
  )


def test_phase82_2_full_premises_report_complete():
  data = build_phase82_2_data()

  phase77 = data[
    "phase77"
  ]

  detection = (
    detect_missing_premises(
      data[
        "final_rule"
      ],
      (
        phase77[
          "bracket_sum_step"
        ],
        phase77[
          "composition_step"
        ],
      ),
    )
  )

  assert detection.is_complete

  assert (
    detection.missing_indices
    == ()
  )

  assert (
    detection.missing_patterns
    == ()
  )

  assert (
    detection.matched_steps
    == (
      phase77[
        "bracket_sum_step"
      ],
      phase77[
        "composition_step"
      ],
    )
  )


def test_phase82_2_does_not_generate_missing_premise():
  data = build_phase82_2_data()

  available_steps = (
    repository_available_steps(
      data[
        "repository"
      ]
    )
  )

  composition_conclusion = (
    data[
      "phase77"
    ][
      "composition_step"
    ].conclusion
  )

  assert all(
    step.conclusion
    != composition_conclusion
    for step in available_steps
  )

  detect_goal_rule_missing_premises(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
  )

  available_steps_after = (
    repository_available_steps(
      data[
        "repository"
      ]
    )
  )

  assert (
    available_steps_after
    == available_steps
  )

  assert all(
    step.conclusion
    != composition_conclusion
    for step in available_steps_after
  )


