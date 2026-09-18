import pytest

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
from test_phase73_prop511_nu_squared_finite_dimensional import (
  build_phase73_8c_data,
)
from test_phase75_prop515_integration import (
  build_phase75_9_data,
)
from toda_calculation_goal_extraction import (
  extract_concrete_toda_calculation_goal_candidates,
)
from toda_group_query import TodaGroupQuery


def make_phase95_9_entry(
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


def test_phase95_9_prop56_extracts_matching_concrete_branch():
  data = build_phase65_9_data()

  entry = make_phase95_9_entry(
    key="phase95.prop56",
    step=data[
      "integration_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6",
  )

  result = (
    extract_concrete_toda_calculation_goal_candidates(
      entry,
      TodaGroupQuery(
        n=4,
        k=3,
      ),
    )
  )

  assert len(
    result
  ) == 1

  candidate = result[
    0
  ]

  assert (
    candidate.goal
    is data[
      "pi7_4_step"
    ].conclusion
  )
  assert (
    candidate.source.source_entry
    is entry
  )
  assert (
    candidate.source.branch_name
    == "pi7_4_group_relation"
  )


def test_phase95_9_prop58_extracts_matching_concrete_branch():
  data = build_phase68_11_data()

  entry = make_phase95_9_entry(
    key="phase95.prop58",
    step=data[
      "integration_step"
    ],
    phase="68",
    theorem="Toda Proposition 5.8",
  )

  result = (
    extract_concrete_toda_calculation_goal_candidates(
      entry,
      TodaGroupQuery(
        n=5,
        k=4,
      ),
    )
  )

  assert len(
    result
  ) == 1
  assert (
    result[
      0
    ].goal
    is data[
      "pi9_5_step"
    ].conclusion
  )
  assert (
    result[
      0
    ].source.branch_name
    == "pi9_5_group_relation"
  )


def test_phase95_9_prop511_extracts_direct_concrete_branch():
  data = build_phase73_8e_data()

  entry = make_phase95_9_entry(
    key="phase95.prop511",
    step=data[
      "final_step"
    ],
    phase="73",
    theorem="Toda Proposition 5.11",
  )

  result = (
    extract_concrete_toda_calculation_goal_candidates(
      entry,
      TodaGroupQuery(
        n=4,
        k=6,
      ),
    )
  )

  assert len(
    result
  ) == 1
  assert (
    result[
      0
    ].goal
    is data[
      "pi10_4_step"
    ].conclusion
  )
  assert (
    result[
      0
    ].source.branch_name
    == "pi10_4_group_relation"
  )


def test_phase95_9_prop511_extracts_nested_concrete_branch():
  data = build_phase73_8e_data()

  entry = make_phase95_9_entry(
    key="phase95.prop511",
    step=data[
      "final_step"
    ],
    phase="73",
    theorem="Toda Proposition 5.11",
  )

  result = (
    extract_concrete_toda_calculation_goal_candidates(
      entry,
      TodaGroupQuery(
        n=5,
        k=6,
      ),
    )
  )

  assert len(
    result
  ) == 1

  nested = (
    data[
      "nu_squared_step"
    ]
    .conclusion
  )

  assert (
    result[
      0
    ].goal
    is nested.pi11_5_group_relation
  )
  assert (
    result[
      0
    ].source.branch_name
    == (
      "nu_squared_finite_dimensional."
      "pi11_5_group_relation"
    )
  )


def test_phase95_9_standalone_nu_squared_aggregate_extracts_concrete_branch():
  data = build_phase73_8c_data()

  entry = make_phase95_9_entry(
    key="phase95.prop511.nu2",
    step=data[
      "final_step"
    ],
    phase="73",
    theorem=(
      "Toda Proposition 5.11 "
      "nu squared aggregate"
    ),
  )

  result = (
    extract_concrete_toda_calculation_goal_candidates(
      entry,
      TodaGroupQuery(
        n=8,
        k=6,
      ),
    )
  )

  assert len(
    result
  ) == 1
  assert (
    result[
      0
    ].goal
    is data[
      "pi14_8_relation"
    ]
  )
  assert (
    result[
      0
    ].source.branch_name
    == "pi14_8_group_relation"
  )


def test_phase95_9_prop515_extracts_zero_branch():
  data = build_phase75_9_data()

  entry = make_phase95_9_entry(
    key="phase95.prop515",
    step=data[
      "aggregate_step"
    ],
    phase="75",
    theorem="Toda Proposition 5.15",
  )

  result = (
    extract_concrete_toda_calculation_goal_candidates(
      entry,
      TodaGroupQuery(
        n=2,
        k=7,
      ),
    )
  )

  assert len(
    result
  ) == 1
  assert (
    result[
      0
    ].goal
    is data[
      "pi9_2_step"
    ].conclusion
  )
  assert (
    result[
      0
    ].source.branch_name
    == "pi9_2_zero"
  )


def test_phase95_9_prop515_extracts_nonzero_branch():
  data = build_phase75_9_data()

  entry = make_phase95_9_entry(
    key="phase95.prop515",
    step=data[
      "aggregate_step"
    ],
    phase="75",
    theorem="Toda Proposition 5.15",
  )

  result = (
    extract_concrete_toda_calculation_goal_candidates(
      entry,
      TodaGroupQuery(
        n=5,
        k=7,
      ),
    )
  )

  assert len(
    result
  ) == 1
  assert (
    result[
      0
    ].goal
    is data[
      "pi12_5_step"
    ].conclusion
  )
  assert (
    result[
      0
    ].source.branch_name
    == "pi12_5_group_relation"
  )


def test_phase95_9_does_not_instantiate_symbolic_higher_branch():
  data = build_phase75_9_data()

  entry = make_phase95_9_entry(
    key="phase95.prop515",
    step=data[
      "aggregate_step"
    ],
    phase="75",
    theorem="Toda Proposition 5.15",
  )

  result = (
    extract_concrete_toda_calculation_goal_candidates(
      entry,
      TodaGroupQuery(
        n=9,
        k=7,
      ),
    )
  )

  assert result == ()


def test_phase95_9_unrelated_entry_returns_empty_tuple():
  data = build_phase65_9_data()

  entry = make_phase95_9_entry(
    key="phase95.unrelated",
    step=data[
      "pi7_4_step"
    ],
    phase="65",
    theorem=(
      "Toda Proposition 5.6 "
      "pi_7^4"
    ),
  )

  result = (
    extract_concrete_toda_calculation_goal_candidates(
      entry,
      TodaGroupQuery(
        n=4,
        k=3,
      ),
    )
  )

  assert result == ()


def test_phase95_9_nonmatching_target_returns_empty_tuple():
  data = build_phase65_9_data()

  entry = make_phase95_9_entry(
    key="phase95.prop56",
    step=data[
      "integration_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6",
  )

  result = (
    extract_concrete_toda_calculation_goal_candidates(
      entry,
      TodaGroupQuery(
        n=4,
        k=6,
      ),
    )
  )

  assert result == ()


def test_phase95_9_rejects_non_repository_entry():
  with pytest.raises(
    TypeError,
    match=(
      "source_entry must be "
      "a ProofRepositoryEntry"
    ),
  ):
    extract_concrete_toda_calculation_goal_candidates(
      "not-an-entry",
      TodaGroupQuery(
        n=4,
        k=3,
      ),
    )


def test_phase95_9_rejects_non_query():
  data = build_phase65_9_data()

  entry = make_phase95_9_entry(
    key="phase95.prop56",
    step=data[
      "integration_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6",
  )

  with pytest.raises(
    TypeError,
    match=(
      "query must be "
      "a TodaGroupQuery"
    ),
  ):
    extract_concrete_toda_calculation_goal_candidates(
      entry,
      "not-a-query",
    )
