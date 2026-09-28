import pytest

from proof import (
  ProofRule,
  ProofStep,
)
from proof_repository import (
  ProofRepositoryEntry,
)
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)
from test_phase68_prop58_integration import (
  build_phase68_11_data,
)
from test_phase73_prop511_finite_dimensional_integration import (
  build_phase73_8e_data,
)
from test_phase75_prop515_integration import (
  build_phase75_9_data,
)
from toda_calculation_goal import (
  TodaCalculationGoalCandidate,
  TodaCalculationGoalSource,
)
from toda_calculation_goal_extraction import (
  extract_concrete_toda_calculation_goal_candidates,
)
from toda_calculation_goal_recovery import (
  recover_toda_calculation_goal_candidate_steps,
)
from toda_group_query import TodaGroupQuery


def make_phase95_13_entry(
  key,
  step,
  phase,
  theorem,
):
  return ProofRepositoryEntry(
    key=key,
    step=step,
    phase=phase,
    theorem=theorem,
  )


def extract_single_phase95_13_candidate(
  entry,
  query,
):
  candidates = (
    extract_concrete_toda_calculation_goal_candidates(
      entry,
      query,
    )
  )

  assert len(
    candidates
  ) == 1

  return candidates[
    0
  ]


def test_phase95_13_recovers_phase65_direct_branch_identity():
  data = build_phase65_9_data()

  entry = make_phase95_13_entry(
    key="phase95.prop56",
    step=data[
      "integration_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6",
  )

  candidate = (
    extract_single_phase95_13_candidate(
      entry,
      TodaGroupQuery(
        n=4,
        k=3,
      ),
    )
  )

  recovered = (
    recover_toda_calculation_goal_candidate_steps(
      candidate
    )
  )

  assert recovered == (
    data[
      "pi7_4_step"
    ],
  )
  assert (
    recovered[
      0
    ]
    is data[
      "pi7_4_step"
    ]
  )


def test_phase95_13_recovers_phase68_direct_branch_identity():
  data = build_phase68_11_data()

  entry = make_phase95_13_entry(
    key="phase95.prop58",
    step=data[
      "integration_step"
    ],
    phase="68",
    theorem="Toda Proposition 5.8",
  )

  candidate = (
    extract_single_phase95_13_candidate(
      entry,
      TodaGroupQuery(
        n=5,
        k=4,
      ),
    )
  )

  recovered = (
    recover_toda_calculation_goal_candidate_steps(
      candidate
    )
  )

  assert recovered == (
    data[
      "pi9_5_step"
    ],
  )
  assert (
    recovered[
      0
    ]
    is data[
      "pi9_5_step"
    ]
  )


def test_phase95_13_recovers_phase73_direct_branch_identity():
  data = build_phase73_8e_data()

  entry = make_phase95_13_entry(
    key="phase95.prop511",
    step=data[
      "final_step"
    ],
    phase="73",
    theorem="Toda Proposition 5.11",
  )

  candidate = (
    extract_single_phase95_13_candidate(
      entry,
      TodaGroupQuery(
        n=4,
        k=6,
      ),
    )
  )

  recovered = (
    recover_toda_calculation_goal_candidate_steps(
      candidate
    )
  )

  assert recovered == (
    data[
      "pi10_4_step"
    ],
  )
  assert (
    recovered[
      0
    ]
    is data[
      "pi10_4_step"
    ]
  )


def test_phase95_13_recovers_phase73_nested_branch_identity():
  data = build_phase73_8e_data()

  entry = make_phase95_13_entry(
    key="phase95.prop511",
    step=data[
      "final_step"
    ],
    phase="73",
    theorem="Toda Proposition 5.11",
  )

  candidate = (
    extract_single_phase95_13_candidate(
      entry,
      TodaGroupQuery(
        n=5,
        k=6,
      ),
    )
  )

  assert (
    candidate.source.branch_name
    == (
      "nu_squared_finite_dimensional."
      "pi11_5_group_relation"
    )
  )

  recovered = (
    recover_toda_calculation_goal_candidate_steps(
      candidate
    )
  )

  expected = (
    data[
      "phase73_8c"
    ][
      "pi11_5_step"
    ]
  )

  assert recovered == (
    expected,
  )
  assert (
    recovered[
      0
    ]
    is expected
  )


def test_phase95_13_recovers_phase75_zero_branch_identity():
  data = build_phase75_9_data()

  entry = make_phase95_13_entry(
    key="phase95.prop515",
    step=data[
      "aggregate_step"
    ],
    phase="75",
    theorem="Toda Proposition 5.15",
  )

  candidate = (
    extract_single_phase95_13_candidate(
      entry,
      TodaGroupQuery(
        n=2,
        k=7,
      ),
    )
  )

  recovered = (
    recover_toda_calculation_goal_candidate_steps(
      candidate
    )
  )

  assert recovered == (
    data[
      "pi9_2_step"
    ],
  )
  assert (
    recovered[
      0
    ]
    is data[
      "pi9_2_step"
    ]
  )


def test_phase95_13_recovers_phase75_nonzero_branch_identity():
  data = build_phase75_9_data()

  entry = make_phase95_13_entry(
    key="phase95.prop515",
    step=data[
      "aggregate_step"
    ],
    phase="75",
    theorem="Toda Proposition 5.15",
  )

  candidate = (
    extract_single_phase95_13_candidate(
      entry,
      TodaGroupQuery(
        n=5,
        k=7,
      ),
    )
  )

  recovered = (
    recover_toda_calculation_goal_candidate_steps(
      candidate
    )
  )

  assert recovered == (
    data[
      "pi12_5_step"
    ],
  )
  assert (
    recovered[
      0
    ]
    is data[
      "pi12_5_step"
    ]
  )


def test_phase95_13_candidate_without_source_returns_empty_tuple():
  data = build_phase65_9_data()

  candidate = TodaCalculationGoalCandidate(
    target=(
      data[
        "pi7_4_step"
      ].conclusion.lhs
    ),
    goal=(
      data[
        "pi7_4_step"
      ].conclusion
    ),
  )

  assert (
    recover_toda_calculation_goal_candidate_steps(
      candidate
    )
    == ()
  )


def test_phase95_13_wrong_branch_name_returns_empty_tuple():
  data = build_phase65_9_data()

  entry = make_phase95_13_entry(
    key="phase95.prop56",
    step=data[
      "integration_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6",
  )

  candidate = TodaCalculationGoalCandidate(
    target=(
      data[
        "pi7_4_step"
      ].conclusion.lhs
    ),
    goal=(
      data[
        "pi7_4_step"
      ].conclusion
    ),
    source=TodaCalculationGoalSource(
      source_entry=entry,
      branch_name="missing_branch",
    ),
  )

  assert (
    recover_toda_calculation_goal_candidate_steps(
      candidate
    )
    == ()
  )


def test_phase95_13_branch_goal_mismatch_returns_empty_tuple():
  data = build_phase65_9_data()

  entry = make_phase95_13_entry(
    key="phase95.prop56",
    step=data[
      "integration_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6",
  )

  candidate = TodaCalculationGoalCandidate(
    target=(
      data[
        "pi7_4_step"
      ].conclusion.lhs
    ),
    goal=(
      data[
        "pi7_4_step"
      ].conclusion
    ),
    source=TodaCalculationGoalSource(
      source_entry=entry,
      branch_name="pi8_5_group_relation",
    ),
  )

  assert (
    recover_toda_calculation_goal_candidate_steps(
      candidate
    )
    == ()
  )


def test_phase95_13_preserves_distinct_matching_steps_without_silent_selection():
  data = build_phase65_9_data()

  original = data[
    "pi7_4_step"
  ]

  duplicate = ProofStep(
    conclusion=original.conclusion,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  aggregate_step = ProofStep(
    conclusion=(
      data[
        "integration_step"
      ].conclusion
    ),
    premises=(
      original,
      duplicate,
    ),
    rule=ProofRule.INFERENCE,
  )

  entry = make_phase95_13_entry(
    key="phase95.prop56.ambiguous",
    step=aggregate_step,
    phase="65",
    theorem="Toda Proposition 5.6",
  )

  candidate = TodaCalculationGoalCandidate(
    target=original.conclusion.lhs,
    goal=original.conclusion,
    source=TodaCalculationGoalSource(
      source_entry=entry,
      branch_name="pi7_4_group_relation",
    ),
  )

  recovered = (
    recover_toda_calculation_goal_candidate_steps(
      candidate
    )
  )

  assert recovered == (
    original,
    duplicate,
  )
  assert (
    recovered[
      0
    ]
    is original
  )
  assert (
    recovered[
      1
    ]
    is duplicate
  )


def test_phase95_13_identity_deduplicates_same_step_repeated_in_premises():
  data = build_phase65_9_data()

  original = data[
    "pi7_4_step"
  ]

  aggregate_step = ProofStep(
    conclusion=(
      data[
        "integration_step"
      ].conclusion
    ),
    premises=(
      original,
      original,
    ),
    rule=ProofRule.INFERENCE,
  )

  entry = make_phase95_13_entry(
    key="phase95.prop56.repeated",
    step=aggregate_step,
    phase="65",
    theorem="Toda Proposition 5.6",
  )

  candidate = TodaCalculationGoalCandidate(
    target=original.conclusion.lhs,
    goal=original.conclusion,
    source=TodaCalculationGoalSource(
      source_entry=entry,
      branch_name="pi7_4_group_relation",
    ),
  )

  recovered = (
    recover_toda_calculation_goal_candidate_steps(
      candidate
    )
  )

  assert recovered == (
    original,
  )


def test_phase95_13_rejects_non_candidate():
  with pytest.raises(
    TypeError,
    match=(
      "candidate must be a "
      "TodaCalculationGoalCandidate"
    ),
  ):
    recover_toda_calculation_goal_candidate_steps(
      "not-a-candidate"
    )
