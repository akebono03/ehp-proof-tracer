import pytest

from proof_repository import (
  ProofRepository,
)
from standard_repository import (
  build_standard_proof_repository,
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
from toda_calculation import (
  build_toda_calculation_result,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)
from toda_group_query import (
  TodaGroupQuery,
)
from toda_proof_builders import (
  build_toda_prop56_proof_step,
  build_toda_prop58_proof_step,
  build_toda_prop511_proof_step,
  build_toda_prop515_proof_step,
)


def build_phase100_11_standard_data():
  phase65 = build_phase65_9_data()
  phase68 = build_phase68_11_data()
  phase73 = build_phase73_8e_data()
  phase75 = build_phase75_9_data()

  prop56_step = build_toda_prop56_proof_step(
    phase65[
      "pi5_2_step"
    ],
    phase65[
      "pi6_3_step"
    ],
    phase65[
      "pi7_4_step"
    ],
    phase65[
      "pi8_5_step"
    ],
    phase65[
      "higher_step"
    ],
    phase65[
      "higher_range_step"
    ],
  )

  prop58_step = build_toda_prop58_proof_step(
    phase68[
      "pi6_2_step"
    ],
    phase68[
      "pi7_3_step"
    ],
    phase68[
      "pi8_4_step"
    ],
    phase68[
      "pi9_5_step"
    ],
    phase68[
      "higher_zero_step"
    ],
    phase68[
      "higher_range_step"
    ],
  )

  prop511_step = build_toda_prop511_proof_step(
    phase73[
      "pi8_2_step"
    ],
    phase73[
      "pi9_3_zero_step"
    ],
    phase73[
      "pi10_4_step"
    ],
    phase73[
      "nu_squared_step"
    ],
  )

  prop515_step = build_toda_prop515_proof_step(
    phase75[
      "pi9_2_step"
    ],
    phase75[
      "pi10_3_step"
    ],
    phase75[
      "pi11_4_step"
    ],
    phase75[
      "pi12_5_step"
    ],
    phase75[
      "pi13_6_step"
    ],
    phase75[
      "pi14_7_step"
    ],
    phase75[
      "pi15_8_step"
    ],
    phase75[
      "higher_step"
    ],
    phase75[
      "higher_range_step"
    ],
  )

  repository = build_standard_proof_repository(
    prop56_step,
    prop58_step,
    prop511_step,
    prop515_step,
  )

  return {
    "phase65": phase65,
    "phase68": phase68,
    "phase73": phase73,
    "phase75": phase75,
    "prop56_step": prop56_step,
    "prop58_step": prop58_step,
    "prop511_step": prop511_step,
    "prop515_step": prop515_step,
    "repository": repository,
  }


def test_phase100_11_standard_repository_has_deterministic_entry_order():
  data = build_phase100_11_standard_data()

  entries = data[
    "repository"
  ].entries()

  assert tuple(
    entry.key
    for entry in entries
  ) == (
    "standard.toda.prop56",
    "standard.toda.prop58",
    "standard.toda.prop511",
    "standard.toda.prop515",
  )

  assert tuple(
    entry.phase
    for entry in entries
  ) == (
    "65",
    "68",
    "73",
    "75",
  )

  assert tuple(
    entry.theorem
    for entry in entries
  ) == (
    "Toda Proposition 5.6",
    "Toda Proposition 5.8",
    "Toda Proposition 5.11",
    "Toda Proposition 5.15",
  )


def test_phase100_11_standard_repository_preserves_aggregate_step_identity():
  data = build_phase100_11_standard_data()

  entries = data[
    "repository"
  ].entries()

  expected_steps = (
    data[
      "prop56_step"
    ],
    data[
      "prop58_step"
    ],
    data[
      "prop511_step"
    ],
    data[
      "prop515_step"
    ],
  )

  assert all(
    entry.step is expected_step
    for entry, expected_step in zip(
      entries,
      expected_steps,
    )
  )


@pytest.mark.parametrize(
  (
    "n",
    "k",
  ),
  (
    (
      4,
      3,
    ),
    (
      5,
      4,
    ),
    (
      4,
      6,
    ),
    (
      5,
      6,
    ),
    (
      2,
      7,
    ),
    (
      5,
      7,
    ),
  ),
)
def test_phase100_11_standard_repository_finds_representative_group_queries(
  n,
  k,
):
  data = build_phase100_11_standard_data()

  result = build_toda_calculation_result(
    data[
      "repository"
    ],
    TodaGroupQuery(
      n=n,
      k=k,
    ),
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )

  assert len(
    result.candidates
  ) == 1


def test_phase100_11_standard_repository_preserves_nested_branch_provenance():
  data = build_phase100_11_standard_data()

  result = build_toda_calculation_result(
    data[
      "repository"
    ],
    TodaGroupQuery(
      n=5,
      k=6,
    ),
  )

  candidate = result.candidates[
    0
  ]

  assert (
    candidate
    .goal_source
    .source_entry
    .key
    == "standard.toda.prop511"
  )

  assert (
    candidate
    .goal_source
    .branch_name
    == (
      "nu_squared_finite_dimensional."
      "pi11_5_group_relation"
    )
  )

  assert (
    candidate
    .group_result
    .proof_step
    is data[
      "phase73"
    ][
      "phase73_8c"
    ][
      "pi11_5_step"
    ]
  )


def test_phase100_11_standard_repository_queries_do_not_mutate_entries():
  data = build_phase100_11_standard_data()

  repository = data[
    "repository"
  ]

  before = repository.entries()

  build_toda_calculation_result(
    repository,
    TodaGroupQuery(
      n=5,
      k=4,
    ),
  )

  after = repository.entries()

  assert after == before

  assert all(
    actual is expected
    for actual, expected in zip(
      after,
      before,
    )
  )


def test_phase100_11_standard_repository_builder_returns_fresh_repository():
  data = build_phase100_11_standard_data()

  first = build_standard_proof_repository(
    data[
      "prop56_step"
    ],
    data[
      "prop58_step"
    ],
    data[
      "prop511_step"
    ],
    data[
      "prop515_step"
    ],
  )

  second = build_standard_proof_repository(
    data[
      "prop56_step"
    ],
    data[
      "prop58_step"
    ],
    data[
      "prop511_step"
    ],
    data[
      "prop515_step"
    ],
  )

  assert isinstance(
    first,
    ProofRepository,
  )

  assert isinstance(
    second,
    ProofRepository,
  )

  assert first is not second

  assert tuple(
    entry.key
    for entry in first.entries()
  ) == tuple(
    entry.key
    for entry in second.entries()
  )


def test_phase100_11_standard_repository_rejects_wrong_theorem_role():
  data = build_phase100_11_standard_data()

  with pytest.raises(
    ValueError,
    match=(
      "prop56_step has the wrong "
      "conclusion type"
    ),
  ):
    build_standard_proof_repository(
      data[
        "prop58_step"
      ],
      data[
        "prop58_step"
      ],
      data[
        "prop511_step"
      ],
      data[
        "prop515_step"
      ],
    )


def test_phase100_11_standard_repository_rejects_non_proof_step():
  data = build_phase100_11_standard_data()

  with pytest.raises(
    TypeError,
    match=(
      "prop56_step must be a ProofStep"
    ),
  ):
    build_standard_proof_repository(
      "not-a-proof-step",
      data[
        "prop58_step"
      ],
      data[
        "prop511_step"
      ],
      data[
        "prop515_step"
      ],
    )
