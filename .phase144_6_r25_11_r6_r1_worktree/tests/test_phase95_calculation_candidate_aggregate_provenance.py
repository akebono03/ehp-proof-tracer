import pytest

from proof_repository import (
  ProofRepositoryEntry,
)
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)
from toda_calculation_goal_extraction import (
  extract_concrete_toda_calculation_goal_candidates,
)
from toda_calculation_goal_normalization import (
  normalize_recovered_toda_calculation_goal_candidate,
)
from toda_calculation_result import (
  TodaCalculationCandidate,
)
from toda_explanation import (
  build_toda_representative_explanation,
)
from toda_group_query import TodaGroupQuery


def build_phase95_17_data():
  data = build_phase65_9_data()

  entry = ProofRepositoryEntry(
    key="phase95.prop56",
    step=data[
      "integration_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6",
  )

  goal_candidates = (
    extract_concrete_toda_calculation_goal_candidates(
      entry,
      TodaGroupQuery(
        n=4,
        k=3,
      ),
    )
  )

  assert len(
    goal_candidates
  ) == 1

  goal_candidate = (
    goal_candidates[
      0
    ]
  )

  group_results = (
    normalize_recovered_toda_calculation_goal_candidate(
      goal_candidate
    )
  )

  assert len(
    group_results
  ) == 1

  group_result = (
    group_results[
      0
    ]
  )

  explanation = (
    build_toda_representative_explanation(
      group_result
    )
  )

  return {
    "data": data,
    "entry": entry,
    "goal_candidate": (
      goal_candidate
    ),
    "group_result": (
      group_result
    ),
    "explanation": explanation,
  }


def test_phase95_17_direct_candidate_default_goal_source_is_none():
  data = build_phase95_17_data()

  candidate = TodaCalculationCandidate(
    group_result=data[
      "group_result"
    ],
    explanation=data[
      "explanation"
    ],
  )

  assert candidate.goal_source is None


def test_phase95_17_aggregate_candidate_preserves_goal_source_identity():
  data = build_phase95_17_data()

  candidate = TodaCalculationCandidate(
    group_result=data[
      "group_result"
    ],
    explanation=data[
      "explanation"
    ],
    goal_source=(
      data[
        "goal_candidate"
      ].source
    ),
  )

  assert (
    candidate.goal_source
    is data[
      "goal_candidate"
    ].source
  )


def test_phase95_17_aggregate_candidate_preserves_original_source_entry_identity():
  data = build_phase95_17_data()

  candidate = TodaCalculationCandidate(
    group_result=data[
      "group_result"
    ],
    explanation=data[
      "explanation"
    ],
    goal_source=(
      data[
        "goal_candidate"
      ].source
    ),
  )

  assert (
    candidate
    .goal_source
    .source_entry
    is data[
      "entry"
    ]
  )


def test_phase95_17_aggregate_candidate_preserves_branch_name():
  data = build_phase95_17_data()

  candidate = TodaCalculationCandidate(
    group_result=data[
      "group_result"
    ],
    explanation=data[
      "explanation"
    ],
    goal_source=(
      data[
        "goal_candidate"
      ].source
    ),
  )

  assert (
    candidate
    .goal_source
    .branch_name
    == "pi7_4_group_relation"
  )


def test_phase95_17_aggregate_source_and_ephemeral_group_source_are_distinct():
  data = build_phase95_17_data()

  candidate = TodaCalculationCandidate(
    group_result=data[
      "group_result"
    ],
    explanation=data[
      "explanation"
    ],
    goal_source=(
      data[
        "goal_candidate"
      ].source
    ),
  )

  assert (
    candidate
    .goal_source
    .source_entry
    is data[
      "entry"
    ]
  )
  assert (
    candidate
    .group_result
    .source_entry
    is not data[
      "entry"
    ]
  )
  assert (
    candidate
    .group_result
    .proof_step
    is data[
      "data"
    ][
      "pi7_4_step"
    ]
  )


def test_phase95_17_existing_group_result_explanation_identity_invariant_is_preserved():
  data = build_phase95_17_data()

  candidate = TodaCalculationCandidate(
    group_result=data[
      "group_result"
    ],
    explanation=data[
      "explanation"
    ],
    goal_source=(
      data[
        "goal_candidate"
      ].source
    ),
  )

  assert (
    candidate
    .explanation
    .group_result
    is candidate.group_result
  )


def test_phase95_17_rejects_invalid_goal_source_type():
  data = build_phase95_17_data()

  with pytest.raises(
    TypeError,
    match=(
      "goal_source must be a "
      "TodaCalculationGoalSource "
      "or None"
    ),
  ):
    TodaCalculationCandidate(
      group_result=data[
        "group_result"
      ],
      explanation=data[
        "explanation"
      ],
      goal_source="not-a-goal-source",
    )
