from copy import copy

from repository_inference import (
  BoundedProducerSearchStatus,
  diagnose_direct_producer_failure,
  repository_available_steps,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)
from test_phase84_bounded_depth_two_execution import (
  Phase84ExecutionGoalStatement,
  Phase84ExecutionIntermediateStatement,
  Phase84ExecutionSharedStatement,
  build_phase84_5_data,
)


def _register_rule(
  catalog,
  key,
  rule,
  conclusion_type,
  fixed_point_safe=True,
):
  catalog.register(
    InferenceRuleCatalogEntry(
      key=key,
      rule=rule,
      conclusion_type=conclusion_type,
      fixed_point_safe=fixed_point_safe,
    )
  )


def _catalog(
  data,
  final_rules=(),
  shared_rules=(),
  intermediate_rules=(),
  shared_safe=True,
):
  catalog = InferenceRuleCatalog()

  for index, final_rule in enumerate(
    final_rules
  ):
    _register_rule(
      catalog,
      f"phase85.direct.final-{index}",
      final_rule,
      Phase84ExecutionGoalStatement,
    )

  for index, shared_rule in enumerate(
    shared_rules
  ):
    _register_rule(
      catalog,
      f"phase85.direct.shared-{index}",
      shared_rule,
      Phase84ExecutionSharedStatement,
      fixed_point_safe=shared_safe,
    )

  for index, intermediate_rule in enumerate(
    intermediate_rules
  ):
    _register_rule(
      catalog,
      f"phase85.direct.intermediate-{index}",
      intermediate_rule,
      Phase84ExecutionIntermediateStatement,
    )

  return catalog


def test_phase85_3_classifies_missing_final_rule():
  data = build_phase84_5_data()
  catalog = InferenceRuleCatalog()

  diagnostic = diagnose_direct_producer_failure(
    data[
      "repository"
    ],
    catalog,
    data[
      "goal"
    ],
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus.NO_FINAL_RULE
  )
  assert diagnostic.final_rule is None


def test_phase85_3_classifies_ambiguous_final_rule():
  data = build_phase84_5_data()
  second_final_rule = copy(
    data[
      "final_rule"
    ]
  )
  catalog = _catalog(
    data,
    final_rules=(
      data[
        "final_rule"
      ],
      second_final_rule,
    ),
  )

  diagnostic = diagnose_direct_producer_failure(
    data[
      "repository"
    ],
    catalog,
    data[
      "goal"
    ],
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus
    .AMBIGUOUS_FINAL_RULE
  )
  assert diagnostic.final_rule_candidates == (
    data[
      "final_rule"
    ],
    second_final_rule,
  )
  assert diagnostic.producer_candidates == ()


def test_phase85_3_classifies_missing_direct_producer():
  data = build_phase84_5_data()
  catalog = _catalog(
    data,
    final_rules=(
      data[
        "final_rule"
      ],
    ),
  )

  diagnostic = diagnose_direct_producer_failure(
    data[
      "repository"
    ],
    catalog,
    data[
      "goal"
    ],
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus.NO_PRODUCER
  )
  assert diagnostic.final_rule is data[
    "final_rule"
  ]
  assert diagnostic.requesting_rule is data[
    "final_rule"
  ]
  assert diagnostic.premise_index == 0
  assert diagnostic.current_depth == 0
  assert diagnostic.required_next_depth == 1
  assert diagnostic.producer_candidates == ()
  assert diagnostic.unsafe_producer_candidates == ()


def test_phase85_3_classifies_unsafe_direct_producer():
  data = build_phase84_5_data()
  catalog = _catalog(
    data,
    final_rules=(
      data[
        "final_rule"
      ],
    ),
    shared_rules=(
      data[
        "shared_rule"
      ],
    ),
    shared_safe=False,
  )

  diagnostic = diagnose_direct_producer_failure(
    data[
      "repository"
    ],
    catalog,
    data[
      "goal"
    ],
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus.UNSAFE_PRODUCER
  )
  assert diagnostic.producer_candidates == ()
  assert diagnostic.unsafe_producer_candidates == (
    data[
      "shared_rule"
    ],
  )


def test_phase85_3_deduplicates_unsafe_rule_aliases():
  data = build_phase84_5_data()
  catalog = _catalog(
    data,
    final_rules=(
      data[
        "final_rule"
      ],
    ),
    shared_rules=(
      data[
        "shared_rule"
      ],
      data[
        "shared_rule"
      ],
    ),
    shared_safe=False,
  )

  diagnostic = diagnose_direct_producer_failure(
    data[
      "repository"
    ],
    catalog,
    data[
      "goal"
    ],
  )

  assert diagnostic is not None
  assert diagnostic.unsafe_producer_candidates == (
    data[
      "shared_rule"
    ],
  )


def test_phase85_3_classifies_ambiguous_direct_producer():
  data = build_phase84_5_data()
  second_shared_rule = copy(
    data[
      "shared_rule"
    ]
  )
  catalog = _catalog(
    data,
    final_rules=(
      data[
        "final_rule"
      ],
    ),
    shared_rules=(
      data[
        "shared_rule"
      ],
      second_shared_rule,
    ),
  )

  diagnostic = diagnose_direct_producer_failure(
    data[
      "repository"
    ],
    catalog,
    data[
      "goal"
    ],
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus
    .AMBIGUOUS_PRODUCER
  )
  assert diagnostic.producer_candidates == (
    data[
      "shared_rule"
    ],
    second_shared_rule,
  )
  assert diagnostic.unsafe_producer_candidates == ()


def test_phase85_3_safe_producer_wins_over_unsafe_candidate():
  data = build_phase84_5_data()
  unsafe_shared_rule = copy(
    data[
      "shared_rule"
    ]
  )
  catalog = _catalog(
    data,
    final_rules=(
      data[
        "final_rule"
      ],
    ),
    shared_rules=(
      data[
        "shared_rule"
      ],
    ),
    intermediate_rules=(
      data[
        "intermediate_rule"
      ],
    ),
  )
  _register_rule(
    catalog,
    "phase85.direct.shared-unsafe",
    unsafe_shared_rule,
    Phase84ExecutionSharedStatement,
    fixed_point_safe=False,
  )

  assert diagnose_direct_producer_failure(
    data[
      "repository"
    ],
    catalog,
    data[
      "goal"
    ],
  ) is None


def test_phase85_3_returns_none_when_direct_checks_pass():
  data = build_phase84_5_data()

  assert diagnose_direct_producer_failure(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
  ) is None


def test_phase85_3_diagnostic_does_not_mutate_repository():
  data = build_phase84_5_data()
  initial_steps = repository_available_steps(
    data[
      "repository"
    ]
  )

  diagnose_direct_producer_failure(
    data[
      "repository"
    ],
    InferenceRuleCatalog(),
    data[
      "goal"
    ],
  )

  assert repository_available_steps(
    data[
      "repository"
    ]
  ) == initial_steps
