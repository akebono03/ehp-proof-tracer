from functools import lru_cache

from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from test_phase90_actual_known_group_lookup import (
  build_phase90_3_3_data,
)
from test_phase92_actual_ehp_extraction import (
  build_phase92_3_data,
)
from toda_ehp_group_enrichment import (
  TodaEHPGroupEnrichmentResult,
  TodaEHPGroupTermResult,
  connect_known_toda_group_results,
)
from toda_group_result import (
  TodaGroupResult,
)


@lru_cache(maxsize=1)
def build_phase92_4_data():
  phase90 = (
    build_phase90_3_3_data()
  )
  phase92_3 = (
    build_phase92_3_data()
  )

  phase68 = (
    phase92_3[
      "phase68"
    ]
  )

  repository = ProofRepository()

  pi8_4_entry = ProofRepositoryEntry(
    key="phase92.actual.pi8_4",
    step=phase68[
      "pi8_4_step"
    ],
    phase="68",
    theorem=(
      "Toda Proposition 5.8 "
      "pi_8^4"
    ),
  )

  pi9_5_entry = (
    phase92_3[
      "entry"
    ]
  )

  pi7_4_entry = (
    phase90[
      "pi7_4_entry"
    ]
  )

  repository.register(
    pi8_4_entry
  )
  repository.register(
    pi9_5_entry
  )
  repository.register(
    pi7_4_entry
  )

  initial_entries = (
    repository.entries()
  )

  enrichment = (
    connect_known_toda_group_results(
      repository,
      phase92_3[
        "ehp_result"
      ],
    )
  )

  final_entries = (
    repository.entries()
  )

  return {
    "phase90": phase90,
    "phase92_3": phase92_3,
    "phase68": phase68,
    "repository": repository,
    "pi8_4_entry": pi8_4_entry,
    "pi9_5_entry": pi9_5_entry,
    "pi7_4_entry": pi7_4_entry,
    "initial_entries": initial_entries,
    "enrichment": enrichment,
    "final_entries": final_entries,
  }


def test_phase92_4_returns_group_enrichment_result():
  data = build_phase92_4_data()

  assert isinstance(
    data[
      "enrichment"
    ],
    TodaEHPGroupEnrichmentResult,
  )


def test_phase92_4_preserves_phase92_3_result_identity():
  data = build_phase92_4_data()

  assert (
    data[
      "enrichment"
    ].ehp_result
    is data[
      "phase92_3"
    ][
      "ehp_result"
    ]
  )


def test_phase92_4_preserves_all_ehp_term_order():
  data = build_phase92_4_data()

  enrichment = data[
    "enrichment"
  ]

  assert tuple(
    term_result.term
    for term_result in (
      enrichment.term_results
    )
  ) == (
    enrichment
    .ehp_result
    .sequence
    .terms
  )


def test_phase92_4_uses_one_term_result_per_ehp_term():
  data = build_phase92_4_data()

  enrichment = data[
    "enrichment"
  ]

  assert len(
    enrichment.term_results
  ) == len(
    enrichment
    .ehp_result
    .sequence
    .terms
  )

  assert all(
    isinstance(
      term_result,
      TodaEHPGroupTermResult,
    )
    for term_result in (
      enrichment.term_results
    )
  )


def test_phase92_4_unknown_pi10_9_remains_unresolved():
  data = build_phase92_4_data()

  result = (
    data[
      "enrichment"
    ].term_results[
      0
    ]
  )

  assert (
    result.term
    == data[
      "phase92_3"
    ][
      "ehp_result"
    ].sequence.terms[
      0
    ]
  )

  assert result.group_results == ()


def test_phase92_4_connects_actual_pi8_4_group():
  data = build_phase92_4_data()

  result = (
    data[
      "enrichment"
    ].term_results[
      1
    ]
  )

  assert len(
    result.group_results
  ) == 1

  group_result = (
    result.group_results[
      0
    ]
  )

  assert isinstance(
    group_result,
    TodaGroupResult,
  )
  assert isinstance(
    group_result.group_structure,
    DirectSumGroup,
  )
  assert (
    group_result.source_entry
    is data[
      "pi8_4_entry"
    ]
  )
  assert (
    group_result.proof_step
    is data[
      "pi8_4_entry"
    ].step
  )


def test_phase92_4_connects_actual_pi9_5_target_group():
  data = build_phase92_4_data()

  result = (
    data[
      "enrichment"
    ].term_results[
      2
    ]
  )

  assert len(
    result.group_results
  ) == 1

  group_result = (
    result.group_results[
      0
    ]
  )

  assert isinstance(
    group_result.group_structure,
    FiniteCyclicGroup,
  )
  assert (
    group_result.group_structure.order
    == 2
  )
  assert (
    group_result.source_entry
    is data[
      "pi9_5_entry"
    ]
  )
  assert (
    group_result.proof_step
    is data[
      "pi9_5_entry"
    ].step
  )


def test_phase92_4_unknown_pi9_9_remains_unresolved():
  data = build_phase92_4_data()

  result = (
    data[
      "enrichment"
    ].term_results[
      3
    ]
  )

  assert result.group_results == ()


def test_phase92_4_connects_actual_pi7_4_group():
  data = build_phase92_4_data()

  result = (
    data[
      "enrichment"
    ].term_results[
      4
    ]
  )

  assert len(
    result.group_results
  ) == 1

  group_result = (
    result.group_results[
      0
    ]
  )

  assert isinstance(
    group_result.group_structure,
    DirectSumGroup,
  )
  assert (
    group_result.source_entry
    is data[
      "pi7_4_entry"
    ]
  )
  assert (
    group_result.proof_step
    is data[
      "pi7_4_entry"
    ].step
  )


def test_phase92_4_group_result_targets_match_ehp_terms():
  data = build_phase92_4_data()

  for term_result in (
    data[
      "enrichment"
    ].term_results
  ):
    assert all(
      group_result.target
      == term_result.term
      for group_result in (
        term_result.group_results
      )
    )


def test_phase92_4_enrichment_does_not_mutate_repository():
  data = build_phase92_4_data()

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


def test_phase92_4_enrichment_keeps_unknown_distinct_from_zero_group():
  data = build_phase92_4_data()

  unknown_result = (
    data[
      "enrichment"
    ].term_results[
      0
    ]
  )

  assert unknown_result.group_results == ()

  known_results = tuple(
    group_result
    for term_result in (
      data[
        "enrichment"
      ].term_results
    )
    for group_result in (
      term_result.group_results
    )
  )

  assert all(
    group_result.group_structure
    is not None
    for group_result in known_results
  )
