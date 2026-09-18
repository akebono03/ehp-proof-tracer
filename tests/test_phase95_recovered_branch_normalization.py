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
from toda_calculation_goal_normalization import (
  normalize_recovered_toda_calculation_goal_candidate,
)
from toda_group_query import TodaGroupQuery


def make_phase95_15_entry(
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


def extract_single_phase95_15_candidate(
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


def test_phase95_15_normalizes_phase65_direct_branch():
  data = build_phase65_9_data()

  entry = make_phase95_15_entry(
    key="phase95.prop56",
    step=data[
      "integration_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6",
  )

  candidate = (
    extract_single_phase95_15_candidate(
      entry,
      TodaGroupQuery(
        n=4,
        k=3,
      ),
    )
  )

  results = (
    normalize_recovered_toda_calculation_goal_candidate(
      candidate
    )
  )

  assert len(
    results
  ) == 1

  result = results[
    0
  ]

  assert (
    result.target
    == candidate.target
  )
  assert (
    result.group_structure
    == candidate.goal.rhs
  )
  assert (
    result.proof_step
    is data[
      "pi7_4_step"
    ]
  )
  assert (
    result.source_entry.step
    is result.proof_step
  )


def test_phase95_15_ephemeral_entry_preserves_aggregate_metadata():
  data = build_phase65_9_data()

  entry = make_phase95_15_entry(
    key="phase95.prop56",
    step=data[
      "integration_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6",
  )

  candidate = (
    extract_single_phase95_15_candidate(
      entry,
      TodaGroupQuery(
        n=4,
        k=3,
      ),
    )
  )

  result = (
    normalize_recovered_toda_calculation_goal_candidate(
      candidate
    )[
      0
    ]
  )

  assert (
    result.source_entry.key
    == (
      "phase95.prop56::"
      "pi7_4_group_relation"
    )
  )
  assert (
    result.source_entry.phase
    == entry.phase
  )
  assert (
    result.source_entry.theorem
    == entry.theorem
  )
  assert (
    result.source_entry
    is not entry
  )


def test_phase95_15_normalizes_phase73_nested_branch():
  data = build_phase73_8e_data()

  entry = make_phase95_15_entry(
    key="phase95.prop511",
    step=data[
      "final_step"
    ],
    phase="73",
    theorem="Toda Proposition 5.11",
  )

  candidate = (
    extract_single_phase95_15_candidate(
      entry,
      TodaGroupQuery(
        n=5,
        k=6,
      ),
    )
  )

  result = (
    normalize_recovered_toda_calculation_goal_candidate(
      candidate
    )[
      0
    ]
  )

  expected_step = (
    data[
      "phase73_8c"
    ][
      "pi11_5_step"
    ]
  )

  assert (
    result.proof_step
    is expected_step
  )
  assert (
    result.source_entry.step
    is expected_step
  )
  assert (
    result.source_entry.key
    == (
      "phase95.prop511::"
      "nu_squared_finite_dimensional."
      "pi11_5_group_relation"
    )
  )


def test_phase95_15_normalizes_phase75_zero_branch():
  data = build_phase75_9_data()

  entry = make_phase95_15_entry(
    key="phase95.prop515",
    step=data[
      "aggregate_step"
    ],
    phase="75",
    theorem="Toda Proposition 5.15",
  )

  candidate = (
    extract_single_phase95_15_candidate(
      entry,
      TodaGroupQuery(
        n=2,
        k=7,
      ),
    )
  )

  result = (
    normalize_recovered_toda_calculation_goal_candidate(
      candidate
    )[
      0
    ]
  )

  assert (
    result.proof_step
    is data[
      "pi9_2_step"
    ]
  )
  assert result.group_structure is None
  assert result.generators == ()
  assert result.generator_orders == ()


def test_phase95_15_preserves_group_generator_structure():
  data = build_phase65_9_data()

  entry = make_phase95_15_entry(
    key="phase95.prop56",
    step=data[
      "integration_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6",
  )

  candidate = (
    extract_single_phase95_15_candidate(
      entry,
      TodaGroupQuery(
        n=4,
        k=3,
      ),
    )
  )

  result = (
    normalize_recovered_toda_calculation_goal_candidate(
      candidate
    )[
      0
    ]
  )

  assert len(
    result.generators
  ) == 2
  assert (
    result.generator_orders
    == (
      None,
      4,
    )
  )


def test_phase95_15_candidate_without_source_returns_empty_tuple():
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
    normalize_recovered_toda_calculation_goal_candidate(
      candidate
    )
    == ()
  )


def test_phase95_15_unrecoverable_candidate_returns_empty_tuple():
  data = build_phase65_9_data()

  entry = make_phase95_15_entry(
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
    normalize_recovered_toda_calculation_goal_candidate(
      candidate
    )
    == ()
  )


def test_phase95_15_preserves_multiple_recovered_steps_without_selection():
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

  entry = make_phase95_15_entry(
    key="phase95.prop56.multiple",
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

  results = (
    normalize_recovered_toda_calculation_goal_candidate(
      candidate
    )
  )

  assert len(
    results
  ) == 2
  assert (
    results[
      0
    ].proof_step
    is original
  )
  assert (
    results[
      1
    ].proof_step
    is duplicate
  )
  assert all(
    result.source_entry.key
    == (
      "phase95.prop56.multiple::"
      "pi7_4_group_relation"
    )
    for result in results
  )


def test_phase95_15_ephemeral_entries_do_not_replace_aggregate_source():
  data = build_phase73_8e_data()

  entry = make_phase95_15_entry(
    key="phase95.prop511",
    step=data[
      "final_step"
    ],
    phase="73",
    theorem="Toda Proposition 5.11",
  )

  candidate = (
    extract_single_phase95_15_candidate(
      entry,
      TodaGroupQuery(
        n=5,
        k=6,
      ),
    )
  )

  result = (
    normalize_recovered_toda_calculation_goal_candidate(
      candidate
    )[
      0
    ]
  )

  assert (
    candidate.source.source_entry
    is entry
  )
  assert (
    result.source_entry
    is not entry
  )
  assert (
    candidate.source.source_entry.step
    is data[
      "final_step"
    ]
  )
  assert (
    result.proof_step
    is (
      data[
        "phase73_8c"
      ][
        "pi11_5_step"
      ]
    )
  )


def test_phase95_15_rejects_non_candidate():
  with pytest.raises(
    TypeError,
    match=(
      "candidate must be a "
      "TodaCalculationGoalCandidate"
    ),
  ):
    normalize_recovered_toda_calculation_goal_candidate(
      "not-a-candidate"
    )
