from functools import lru_cache

from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  ProofRule,
  Relation,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from test_phase65_pi7_4_decomposition import (
  build_phase65_5_data,
)
from test_phase73_pi10_4_nu4_squared import (
  build_phase73_5_data,
)
from test_phase75_pi9_2_zero import (
  build_phase75_2_data,
)
from toda_group_lookup import (
  find_known_toda_group_results,
)
from toda_group_query import (
  TodaGroupQuery,
)


@lru_cache(maxsize=1)
def build_phase90_3_3_data():
  phase65 = build_phase65_5_data()
  phase73 = build_phase73_5_data()
  phase75 = build_phase75_2_data()

  pi7_4_step = phase65[
    "final_step"
  ]
  pi10_4_step = phase73[
    "final_step"
  ]
  pi9_2_step = phase75[
    "final_step"
  ]

  repository = ProofRepository()

  pi7_4_entry = ProofRepositoryEntry(
    key="phase90.actual.pi7_4",
    step=pi7_4_step,
    phase="65",
    theorem=(
      "Toda Proposition 5.6 "
      "pi_7^4 decomposition"
    ),
  )
  pi10_4_entry = ProofRepositoryEntry(
    key="phase90.actual.pi10_4",
    step=pi10_4_step,
    phase="73",
    theorem=(
      "Toda Proposition 5.11 "
      "pi_10^4"
    ),
  )
  pi9_2_entry = ProofRepositoryEntry(
    key="phase90.actual.pi9_2",
    step=pi9_2_step,
    phase="75",
    theorem=(
      "Toda Proposition 5.15 "
      "pi_9^2"
    ),
  )

  repository.register(
    pi7_4_entry
  )
  repository.register(
    pi10_4_entry
  )
  repository.register(
    pi9_2_entry
  )

  pi7_4_query = TodaGroupQuery(
    n=4,
    k=3,
  )
  pi10_4_query = TodaGroupQuery(
    n=4,
    k=6,
  )
  pi9_2_query = TodaGroupQuery(
    n=2,
    k=7,
  )

  initial_entries = repository.entries()

  pi7_4_results = (
    find_known_toda_group_results(
      repository,
      pi7_4_query,
    )
  )
  pi10_4_results = (
    find_known_toda_group_results(
      repository,
      pi10_4_query,
    )
  )
  pi9_2_results = (
    find_known_toda_group_results(
      repository,
      pi9_2_query,
    )
  )

  final_entries = repository.entries()

  return {
    "phase65": phase65,
    "phase73": phase73,
    "phase75": phase75,
    "repository": repository,
    "pi7_4_step": pi7_4_step,
    "pi10_4_step": pi10_4_step,
    "pi9_2_step": pi9_2_step,
    "pi7_4_entry": pi7_4_entry,
    "pi10_4_entry": pi10_4_entry,
    "pi9_2_entry": pi9_2_entry,
    "pi7_4_query": pi7_4_query,
    "pi10_4_query": pi10_4_query,
    "pi9_2_query": pi9_2_query,
    "initial_entries": initial_entries,
    "pi7_4_results": pi7_4_results,
    "pi10_4_results": pi10_4_results,
    "pi9_2_results": pi9_2_results,
    "final_entries": final_entries,
  }


def test_phase90_3_3_actual_results_are_derived_proof_steps():
  data = build_phase90_3_3_data()

  assert (
    data[
      "pi7_4_step"
    ].rule
    == ProofRule.INFERENCE
  )
  assert (
    data[
      "pi10_4_step"
    ].rule
    == ProofRule.INFERENCE
  )
  assert (
    data[
      "pi9_2_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase90_3_3_pi7_4_query_finds_actual_direct_sum_result():
  data = build_phase90_3_3_data()

  assert (
    data[
      "pi7_4_results"
    ]
    == (
      data[
        "pi7_4_entry"
      ],
    )
  )

  conclusion = (
    data[
      "pi7_4_results"
    ][
      0
    ].step.conclusion
  )

  assert isinstance(
    conclusion,
    Relation,
  )
  assert isinstance(
    conclusion.rhs,
    DirectSumGroup,
  )
  assert (
    conclusion
    == data[
      "phase65"
    ][
      "expected_relation"
    ]
  )


def test_phase90_3_3_pi10_4_query_finds_actual_order_eight_result():
  data = build_phase90_3_3_data()

  assert (
    data[
      "pi10_4_results"
    ]
    == (
      data[
        "pi10_4_entry"
      ],
    )
  )

  conclusion = (
    data[
      "pi10_4_results"
    ][
      0
    ].step.conclusion
  )

  assert isinstance(
    conclusion,
    Relation,
  )
  assert isinstance(
    conclusion.rhs,
    FiniteCyclicGroup,
  )
  assert conclusion.rhs.order == 8
  assert (
    conclusion
    == data[
      "phase73"
    ][
      "expected_final"
    ]
  )


def test_phase90_3_3_pi9_2_query_finds_actual_zero_result():
  data = build_phase90_3_3_data()

  assert (
    data[
      "pi9_2_results"
    ]
    == (
      data[
        "pi9_2_entry"
      ],
    )
  )

  conclusion = (
    data[
      "pi9_2_results"
    ][
      0
    ].step.conclusion
  )

  assert isinstance(
    conclusion,
    TodaPrimaryGroupZeroStatement,
  )
  assert (
    conclusion
    == data[
      "phase75"
    ][
      "expected_statement"
    ]
  )


def test_phase90_3_3_lookup_preserves_actual_proof_step_identity():
  data = build_phase90_3_3_data()

  assert (
    data[
      "pi7_4_results"
    ][
      0
    ].step
    is data[
      "pi7_4_step"
    ]
  )
  assert (
    data[
      "pi10_4_results"
    ][
      0
    ].step
    is data[
      "pi10_4_step"
    ]
  )
  assert (
    data[
      "pi9_2_results"
    ][
      0
    ].step
    is data[
      "pi9_2_step"
    ]
  )


def test_phase90_3_3_lookup_preserves_actual_provenance():
  data = build_phase90_3_3_data()

  assert (
    data[
      "pi7_4_results"
    ][
      0
    ].step.premises
    == data[
      "phase65"
    ][
      "final_step"
    ].premises
  )
  assert (
    data[
      "pi10_4_results"
    ][
      0
    ].step.premises
    == data[
      "phase73"
    ][
      "final_step"
    ].premises
  )
  assert (
    data[
      "pi9_2_results"
    ][
      0
    ].step.premises
    == data[
      "phase75"
    ][
      "final_step"
    ].premises
  )


def test_phase90_3_3_queries_construct_exact_actual_targets():
  data = build_phase90_3_3_data()

  assert (
    data[
      "pi7_4_query"
    ].target
    == data[
      "pi7_4_step"
    ].conclusion.lhs
  )
  assert (
    data[
      "pi10_4_query"
    ].target
    == data[
      "pi10_4_step"
    ].conclusion.lhs
  )
  assert (
    data[
      "pi9_2_query"
    ].target
    == data[
      "pi9_2_step"
    ].conclusion.group
  )


def test_phase90_3_3_lookup_does_not_cross_match_actual_results():
  data = build_phase90_3_3_data()

  assert (
    data[
      "pi7_4_entry"
    ]
    not in data[
      "pi10_4_results"
    ]
  )
  assert (
    data[
      "pi9_2_entry"
    ]
    not in data[
      "pi10_4_results"
    ]
  )
  assert (
    data[
      "pi10_4_entry"
    ]
    not in data[
      "pi7_4_results"
    ]
  )


def test_phase90_3_3_lookup_does_not_mutate_repository():
  data = build_phase90_3_3_data()

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


def test_phase90_3_3_unregistered_actual_target_returns_empty_tuple():
  data = build_phase90_3_3_data()

  results = find_known_toda_group_results(
    data[
      "repository"
    ],
    TodaGroupQuery(
      n=5,
      k=6,
    ),
  )

  assert results == ()
