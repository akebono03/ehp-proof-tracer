from functools import lru_cache

from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
)
from test_phase90_actual_known_group_lookup import (
  build_phase90_3_3_data,
)
from toda_group_lookup import (
  find_normalized_toda_group_results,
)
from toda_group_query import (
  TodaGroupQuery,
)
from toda_group_result import (
  TodaGroupResult,
  normalize_toda_group_result,
)


@lru_cache(maxsize=1)
def build_phase91_3_data():
  phase90 = build_phase90_3_3_data()

  repository = phase90[
    "repository"
  ]

  initial_entries = (
    repository.entries()
  )

  pi7_4_results = (
    find_normalized_toda_group_results(
      repository,
      phase90[
        "pi7_4_query"
      ],
    )
  )
  pi10_4_results = (
    find_normalized_toda_group_results(
      repository,
      phase90[
        "pi10_4_query"
      ],
    )
  )
  pi9_2_results = (
    find_normalized_toda_group_results(
      repository,
      phase90[
        "pi9_2_query"
      ],
    )
  )

  final_entries = (
    repository.entries()
  )

  return {
    "phase90": phase90,
    "repository": repository,
    "initial_entries": initial_entries,
    "pi7_4_results": pi7_4_results,
    "pi10_4_results": pi10_4_results,
    "pi9_2_results": pi9_2_results,
    "final_entries": final_entries,
  }


def test_phase91_3_pi7_4_actual_result_is_normalized():
  data = build_phase91_3_data()

  result = data[
    "pi7_4_results"
  ][
    0
  ]

  conclusion = (
    data[
      "phase90"
    ][
      "pi7_4_step"
    ].conclusion
  )

  assert isinstance(
    result,
    TodaGroupResult,
  )
  assert (
    result.target
    == data[
      "phase90"
    ][
      "pi7_4_query"
    ].target
  )
  assert isinstance(
    result.group_structure,
    DirectSumGroup,
  )
  assert (
    result.group_structure
    is conclusion.rhs
  )
  assert (
    result.generators
    == (
      conclusion.rhs.summands[
        0
      ].generator,
      conclusion.rhs.summands[
        1
      ].generator,
    )
  )
  assert (
    result.generator_orders
    == (
      None,
      4,
    )
  )


def test_phase91_3_pi10_4_actual_result_is_normalized():
  data = build_phase91_3_data()

  result = data[
    "pi10_4_results"
  ][
    0
  ]

  conclusion = (
    data[
      "phase90"
    ][
      "pi10_4_step"
    ].conclusion
  )

  assert isinstance(
    result.group_structure,
    FiniteCyclicGroup,
  )
  assert (
    result.group_structure
    is conclusion.rhs
  )
  assert (
    result.generators
    == (
      conclusion.rhs.generator,
    )
  )
  assert (
    result.generator_orders
    == (
      8,
    )
  )


def test_phase91_3_pi9_2_actual_zero_result_is_normalized():
  data = build_phase91_3_data()

  result = data[
    "pi9_2_results"
  ][
    0
  ]

  assert (
    result.target
    == data[
      "phase90"
    ][
      "pi9_2_query"
    ].target
  )
  assert result.group_structure is None
  assert result.generators == ()
  assert result.generator_orders == ()


def test_phase91_3_preserves_actual_source_entry_identity():
  data = build_phase91_3_data()

  assert (
    data[
      "pi7_4_results"
    ][
      0
    ].source_entry
    is data[
      "phase90"
    ][
      "pi7_4_entry"
    ]
  )
  assert (
    data[
      "pi10_4_results"
    ][
      0
    ].source_entry
    is data[
      "phase90"
    ][
      "pi10_4_entry"
    ]
  )
  assert (
    data[
      "pi9_2_results"
    ][
      0
    ].source_entry
    is data[
      "phase90"
    ][
      "pi9_2_entry"
    ]
  )


def test_phase91_3_preserves_actual_proof_step_identity():
  data = build_phase91_3_data()

  assert (
    data[
      "pi7_4_results"
    ][
      0
    ].proof_step
    is data[
      "phase90"
    ][
      "pi7_4_step"
    ]
  )
  assert (
    data[
      "pi10_4_results"
    ][
      0
    ].proof_step
    is data[
      "phase90"
    ][
      "pi10_4_step"
    ]
  )
  assert (
    data[
      "pi9_2_results"
    ][
      0
    ].proof_step
    is data[
      "phase90"
    ][
      "pi9_2_step"
    ]
  )


def test_phase91_3_preserves_actual_proof_provenance():
  data = build_phase91_3_data()

  assert (
    data[
      "pi7_4_results"
    ][
      0
    ].proof_step.premises
    == data[
      "phase90"
    ][
      "pi7_4_step"
    ].premises
  )
  assert (
    data[
      "pi10_4_results"
    ][
      0
    ].proof_step.premises
    == data[
      "phase90"
    ][
      "pi10_4_step"
    ].premises
  )
  assert (
    data[
      "pi9_2_results"
    ][
      0
    ].proof_step.premises
    == data[
      "phase90"
    ][
      "pi9_2_step"
    ].premises
  )


def test_phase91_3_normalize_entry_matches_query_integration():
  data = build_phase91_3_data()

  phase90 = data[
    "phase90"
  ]

  assert (
    normalize_toda_group_result(
      phase90[
        "pi7_4_entry"
      ]
    )
    == data[
      "pi7_4_results"
    ][
      0
    ]
  )
  assert (
    normalize_toda_group_result(
      phase90[
        "pi10_4_entry"
      ]
    )
    == data[
      "pi10_4_results"
    ][
      0
    ]
  )
  assert (
    normalize_toda_group_result(
      phase90[
        "pi9_2_entry"
      ]
    )
    == data[
      "pi9_2_results"
    ][
      0
    ]
  )


def test_phase91_3_unregistered_query_returns_empty_tuple():
  data = build_phase91_3_data()

  phase90 = data[
    "phase90"
  ]

  results = (
    find_normalized_toda_group_results(
      data[
        "repository"
      ],
      TodaGroupQuery(
        n=5,
        k=6,
      ),
    )
  )

  assert results == ()


def test_phase91_3_normalization_does_not_mutate_repository():
  data = build_phase91_3_data()

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
