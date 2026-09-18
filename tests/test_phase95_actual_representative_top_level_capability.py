from functools import lru_cache

from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
)
from proof_repository import (
  ProofRepository,
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
from toda_calculation import (
  build_toda_calculation_result,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)
from toda_group_query import TodaGroupQuery


@lru_cache(maxsize=1)
def build_phase95_20_data():
  phase65 = build_phase65_9_data()
  phase68 = build_phase68_11_data()
  phase73 = build_phase73_8e_data()
  phase75 = build_phase75_9_data()

  repository = ProofRepository()

  phase65_entry = ProofRepositoryEntry(
    key="phase95.actual.prop56",
    step=phase65[
      "integration_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6",
  )

  phase68_entry = ProofRepositoryEntry(
    key="phase95.actual.prop58",
    step=phase68[
      "integration_step"
    ],
    phase="68",
    theorem="Toda Proposition 5.8",
  )

  phase73_entry = ProofRepositoryEntry(
    key="phase95.actual.prop511",
    step=phase73[
      "final_step"
    ],
    phase="73",
    theorem="Toda Proposition 5.11",
  )

  phase75_entry = ProofRepositoryEntry(
    key="phase95.actual.prop515",
    step=phase75[
      "aggregate_step"
    ],
    phase="75",
    theorem="Toda Proposition 5.15",
  )

  for entry in (
    phase65_entry,
    phase68_entry,
    phase73_entry,
    phase75_entry,
  ):
    repository.register(
      entry
    )

  initial_entries = (
    repository.entries()
  )

  queries = {
    "pi7_4": TodaGroupQuery(
      n=4,
      k=3,
    ),
    "pi9_5": TodaGroupQuery(
      n=5,
      k=4,
    ),
    "pi10_4": TodaGroupQuery(
      n=4,
      k=6,
    ),
    "pi11_5": TodaGroupQuery(
      n=5,
      k=6,
    ),
    "pi9_2": TodaGroupQuery(
      n=2,
      k=7,
    ),
    "pi12_5": TodaGroupQuery(
      n=5,
      k=7,
    ),
  }

  results = {
    key: build_toda_calculation_result(
      repository,
      query,
    )
    for key, query in queries.items()
  }

  final_entries = (
    repository.entries()
  )

  return {
    "phase65": phase65,
    "phase68": phase68,
    "phase73": phase73,
    "phase75": phase75,
    "repository": repository,
    "phase65_entry": phase65_entry,
    "phase68_entry": phase68_entry,
    "phase73_entry": phase73_entry,
    "phase75_entry": phase75_entry,
    "initial_entries": initial_entries,
    "queries": queries,
    "results": results,
    "final_entries": final_entries,
  }


def get_single_candidate(
  result,
):
  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )

  assert len(
    result.candidates
  ) == 1

  return result.candidates[
    0
  ]


def test_phase95_20_all_representative_queries_are_found_from_aggregate_entries_only():
  data = build_phase95_20_data()

  assert all(
    result.status
    is TodaCalculationStatus.FOUND
    for result in (
      data[
        "results"
      ].values()
    )
  )


def test_phase95_20_pi7_4_preserves_direct_sum_structure_and_branch_provenance():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi7_4"
    ]
  )

  group_result = (
    candidate.group_result
  )

  assert isinstance(
    group_result.group_structure,
    DirectSumGroup,
  )

  assert (
    group_result.generator_orders
    == (
      None,
      4,
    )
  )

  assert (
    group_result.proof_step
    is data[
      "phase65"
    ][
      "pi7_4_step"
    ]
  )

  assert (
    candidate
    .goal_source
    .source_entry
    is data[
      "phase65_entry"
    ]
  )

  assert (
    candidate
    .goal_source
    .branch_name
    == "pi7_4_group_relation"
  )


def test_phase95_20_pi9_5_preserves_order_two_generator_and_actual_ehp_provenance():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  group_result = (
    candidate.group_result
  )

  assert isinstance(
    group_result.group_structure,
    FiniteCyclicGroup,
  )

  assert (
    group_result.generator_orders
    == (
      2,
    )
  )

  assert (
    group_result.proof_step
    is data[
      "phase68"
    ][
      "pi9_5_step"
    ]
  )

  assert (
    candidate
    .goal_source
    .source_entry
    is data[
      "phase68_entry"
    ]
  )

  assert (
    candidate
    .goal_source
    .branch_name
    == "pi9_5_group_relation"
  )

  assert (
    candidate.explanation.ehp_result
    is not None
  )

  assert (
    len(
      candidate
      .explanation
      .ehp_result
      .windows
    )
    == 3
  )

  assert (
    candidate
    .explanation
    .exactness_provenance
    is not None
  )

  assert (
    candidate
    .explanation
    .dependency_result
    .root_step
    is data[
      "phase68"
    ][
      "pi9_5_step"
    ]
  )

  assert (
    candidate
    .explanation
    .recursive_provenance
    .root_step
    is data[
      "phase68"
    ][
      "pi9_5_step"
    ]
  )


def test_phase95_20_pi10_4_preserves_order_eight_outer_phase73_branch():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi10_4"
    ]
  )

  assert (
    candidate
    .group_result
    .generator_orders
    == (
      8,
    )
  )

  assert (
    candidate
    .group_result
    .proof_step
    is data[
      "phase73"
    ][
      "pi10_4_step"
    ]
  )

  assert (
    candidate
    .goal_source
    .source_entry
    is data[
      "phase73_entry"
    ]
  )

  assert (
    candidate
    .goal_source
    .branch_name
    == "pi10_4_group_relation"
  )


def test_phase95_20_pi11_5_preserves_nested_phase73_branch_path_and_identity():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi11_5"
    ]
  )

  expected_step = (
    data[
      "phase73"
    ][
      "phase73_8c"
    ][
      "pi11_5_step"
    ]
  )

  assert (
    candidate
    .group_result
    .generator_orders
    == (
      2,
    )
  )

  assert (
    candidate
    .group_result
    .proof_step
    is expected_step
  )

  assert (
    candidate
    .goal_source
    .source_entry
    is data[
      "phase73_entry"
    ]
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
    .explanation
    .recursive_provenance
    .root_step
    is expected_step
  )


def test_phase95_20_pi9_2_preserves_zero_group_semantics_and_branch_identity():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_2"
    ]
  )

  group_result = (
    candidate.group_result
  )

  assert group_result.group_structure is None
  assert group_result.generators == ()
  assert group_result.generator_orders == ()

  assert (
    group_result.proof_step
    is data[
      "phase75"
    ][
      "pi9_2_step"
    ]
  )

  assert (
    candidate
    .goal_source
    .source_entry
    is data[
      "phase75_entry"
    ]
  )

  assert (
    candidate
    .goal_source
    .branch_name
    == "pi9_2_zero"
  )


def test_phase95_20_pi12_5_preserves_sigma_triple_prime_order_two_branch():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi12_5"
    ]
  )

  group_result = (
    candidate.group_result
  )

  assert isinstance(
    group_result.group_structure,
    FiniteCyclicGroup,
  )

  assert (
    group_result.generator_orders
    == (
      2,
    )
  )

  assert (
    group_result.proof_step
    is data[
      "phase75"
    ][
      "pi12_5_step"
    ]
  )

  assert (
    group_result.generators[
      0
    ]
    is (
      data[
        "phase75"
      ][
        "pi12_5_step"
      ]
      .conclusion
      .rhs
      .generator
    )
  )

  assert (
    candidate
    .goal_source
    .source_entry
    is data[
      "phase75_entry"
    ]
  )

  assert (
    candidate
    .goal_source
    .branch_name
    == "pi12_5_group_relation"
  )


def test_phase95_20_all_explanations_share_original_branch_root_identity():
  data = build_phase95_20_data()

  expected_steps = {
    "pi7_4": (
      data[
        "phase65"
      ][
        "pi7_4_step"
      ]
    ),
    "pi9_5": (
      data[
        "phase68"
      ][
        "pi9_5_step"
      ]
    ),
    "pi10_4": (
      data[
        "phase73"
      ][
        "pi10_4_step"
      ]
    ),
    "pi11_5": (
      data[
        "phase73"
      ][
        "phase73_8c"
      ][
        "pi11_5_step"
      ]
    ),
    "pi9_2": (
      data[
        "phase75"
      ][
        "pi9_2_step"
      ]
    ),
    "pi12_5": (
      data[
        "phase75"
      ][
        "pi12_5_step"
      ]
    ),
  }

  for key, expected_step in (
    expected_steps.items()
  ):
    candidate = get_single_candidate(
      data[
        "results"
      ][
        key
      ]
    )

    assert (
      candidate
      .group_result
      .proof_step
      is expected_step
    )

    assert (
      candidate
      .explanation
      .dependency_result
      .root_step
      is expected_step
    )

    assert (
      candidate
      .explanation
      .recursive_provenance
      .root_step
      is expected_step
    )


def test_phase95_20_actual_representative_queries_do_not_mutate_repository():
  data = build_phase95_20_data()

  assert (
    data[
      "final_entries"
    ]
    == data[
      "initial_entries"
    ]
  )

  assert all(
    actual is expected
    for actual, expected in zip(
      data[
        "final_entries"
      ],
      data[
        "initial_entries"
      ],
    )
  )
