from dataclasses import dataclass
from functools import lru_cache

from proof import (
  InferenceRule,
  PremisePattern,
  ProofRule,
)
from proof_repository import ProofRepository
from repository_inference import (
  BoundedProducerSearchStatus,
  build_depth_two_producer_search_report,
  diagnose_depth_two_producer_search_failure,
  repository_available_steps,
  select_unique_depth_two_producer_chain,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)


@dataclass(frozen=True)
class Phase86DepthThreeAStatement:
  pass


@dataclass(frozen=True)
class Phase86DepthThreeBStatement:
  pass


@dataclass(frozen=True)
class Phase86DepthThreeCStatement:
  pass


@dataclass(frozen=True)
class Phase86DepthThreeDStatement:
  pass


@dataclass(frozen=True)
class Phase86DepthThreeGoalStatement:
  pass


def _single_premise_rule(
  name,
  premise_type,
  conclusion_type,
):
  return InferenceRule(
    name=name,
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=premise_type,
      ),
    ),
    conclusion_builder=(
      lambda premises: conclusion_type()
    ),
  )


def _no_premise_rule(
  name,
  conclusion_type,
):
  return InferenceRule(
    name=name,
    premise_patterns=(),
    conclusion_builder=(
      lambda premises: conclusion_type()
    ),
  )


def _register_rule(
  catalog,
  key,
  rule,
  conclusion_type,
):
  catalog.register(
    InferenceRuleCatalogEntry(
      key=key,
      rule=rule,
      conclusion_type=conclusion_type,
      fixed_point_safe=True,
    )
  )


@lru_cache(maxsize=1)
def build_phase86_3_1_data():
  repository = ProofRepository()

  final_rule = _single_premise_rule(
    "phase86 depth-three final",
    Phase86DepthThreeAStatement,
    Phase86DepthThreeGoalStatement,
  )
  a_rule = _single_premise_rule(
    "phase86 depth-three a",
    Phase86DepthThreeBStatement,
    Phase86DepthThreeAStatement,
  )
  b_rule = _single_premise_rule(
    "phase86 depth-three b",
    Phase86DepthThreeCStatement,
    Phase86DepthThreeBStatement,
  )
  c_rule = _no_premise_rule(
    "phase86 depth-three c",
    Phase86DepthThreeCStatement,
  )

  catalog = InferenceRuleCatalog()

  for key, rule, conclusion_type in (
    (
      "phase86.depth-three.final",
      final_rule,
      Phase86DepthThreeGoalStatement,
    ),
    (
      "phase86.depth-three.a",
      a_rule,
      Phase86DepthThreeAStatement,
    ),
    (
      "phase86.depth-three.b",
      b_rule,
      Phase86DepthThreeBStatement,
    ),
    (
      "phase86.depth-three.c",
      c_rule,
      Phase86DepthThreeCStatement,
    ),
  ):
    _register_rule(
      catalog,
      key,
      rule,
      conclusion_type,
    )

  return {
    "repository": repository,
    "catalog": catalog,
    "goal": Phase86DepthThreeGoalStatement(),
    "final_rule": final_rule,
    "a_rule": a_rule,
    "b_rule": b_rule,
    "c_rule": c_rule,
  }


def test_phase86_3_1_fixture_is_empty_depth_three_chain():
  data = build_phase86_3_1_data()

  assert repository_available_steps(
    data[
      "repository"
    ]
  ) == ()

  assert data[
    "final_rule"
  ].premise_patterns[
    0
  ].statement_type is Phase86DepthThreeAStatement

  assert data[
    "a_rule"
  ].premise_patterns[
    0
  ].statement_type is Phase86DepthThreeBStatement

  assert data[
    "b_rule"
  ].premise_patterns[
    0
  ].statement_type is Phase86DepthThreeCStatement

  assert data[
    "c_rule"
  ].premise_patterns == ()


def test_phase86_3_1_max_depth_two_reports_depth_limit():
  data = build_phase86_3_1_data()

  report = build_depth_two_producer_search_report(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
    max_depth=2,
  )

  assert report.status is (
    BoundedProducerSearchStatus.DEPTH_LIMIT
  )
  assert report.search_result is None
  assert report.diagnostic is not None
  assert report.diagnostic.current_depth == 2
  assert report.diagnostic.required_next_depth == 3
  assert report.diagnostic.requesting_rule is data[
    "b_rule"
  ]
  assert report.diagnostic.producer_candidates == (
    data[
      "c_rule"
    ],
  )


def test_phase86_3_1_max_depth_two_preserves_repository():
  data = build_phase86_3_1_data()

  initial_steps = repository_available_steps(
    data[
      "repository"
    ]
  )

  build_depth_two_producer_search_report(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
    max_depth=2,
  )

  assert repository_available_steps(
    data[
      "repository"
    ]
  ) == initial_steps


def test_phase86_3_2_max_depth_three_selects_dependency_first_chain():
  data = build_phase86_3_1_data()

  result = select_unique_depth_two_producer_chain(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
    max_depth=3,
  )

  assert result is not None
  assert result.max_depth == 3
  assert tuple(
    node.producer_rule
    for node
    in result.producer_nodes
  ) == (
    data[
      "c_rule"
    ],
    data[
      "b_rule"
    ],
    data[
      "a_rule"
    ],
  )
  assert tuple(
    node.depths
    for node
    in result.producer_nodes
  ) == (
    (
      3,
    ),
    (
      2,
    ),
    (
      1,
    ),
  )
  assert result.producer_nodes[
    1
  ].dependencies == (
    result.producer_nodes[
      0
    ],
  )
  assert result.producer_nodes[
    2
  ].dependencies == (
    result.producer_nodes[
      1
    ],
  )
  assert result.is_within_depth_limit


def test_phase86_3_2_selection_preserves_repository():
  data = build_phase86_3_1_data()

  initial_steps = repository_available_steps(
    data[
      "repository"
    ]
  )

  result = select_unique_depth_two_producer_chain(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
    max_depth=3,
  )

  assert result is not None
  assert repository_available_steps(
    data[
      "repository"
    ]
  ) == initial_steps


@lru_cache(maxsize=1)
def build_phase86_3_3_depth_limit_data():
  repository = ProofRepository()

  final_rule = _single_premise_rule(
    "phase86 diagnostic final",
    Phase86DepthThreeAStatement,
    Phase86DepthThreeGoalStatement,
  )
  a_rule = _single_premise_rule(
    "phase86 diagnostic a",
    Phase86DepthThreeBStatement,
    Phase86DepthThreeAStatement,
  )
  b_rule = _single_premise_rule(
    "phase86 diagnostic b",
    Phase86DepthThreeCStatement,
    Phase86DepthThreeBStatement,
  )
  c_rule = _single_premise_rule(
    "phase86 diagnostic c",
    Phase86DepthThreeDStatement,
    Phase86DepthThreeCStatement,
  )
  d_rule = _no_premise_rule(
    "phase86 diagnostic d",
    Phase86DepthThreeDStatement,
  )

  catalog = InferenceRuleCatalog()

  for key, rule, conclusion_type in (
    (
      "phase86.diagnostic.final",
      final_rule,
      Phase86DepthThreeGoalStatement,
    ),
    (
      "phase86.diagnostic.a",
      a_rule,
      Phase86DepthThreeAStatement,
    ),
    (
      "phase86.diagnostic.b",
      b_rule,
      Phase86DepthThreeBStatement,
    ),
    (
      "phase86.diagnostic.c",
      c_rule,
      Phase86DepthThreeCStatement,
    ),
    (
      "phase86.diagnostic.d",
      d_rule,
      Phase86DepthThreeDStatement,
    ),
  ):
    _register_rule(
      catalog,
      key,
      rule,
      conclusion_type,
    )

  return {
    "repository": repository,
    "catalog": catalog,
    "goal": Phase86DepthThreeGoalStatement(),
    "final_rule": final_rule,
    "a_rule": a_rule,
    "b_rule": b_rule,
    "c_rule": c_rule,
    "d_rule": d_rule,
  }


@lru_cache(maxsize=1)
def build_phase86_3_3_cycle_data():
  repository = ProofRepository()

  final_rule = _single_premise_rule(
    "phase86 cycle final",
    Phase86DepthThreeAStatement,
    Phase86DepthThreeGoalStatement,
  )
  a_rule = _single_premise_rule(
    "phase86 cycle a",
    Phase86DepthThreeBStatement,
    Phase86DepthThreeAStatement,
  )
  b_rule = _single_premise_rule(
    "phase86 cycle b",
    Phase86DepthThreeCStatement,
    Phase86DepthThreeBStatement,
  )
  c_rule = _single_premise_rule(
    "phase86 cycle c",
    Phase86DepthThreeAStatement,
    Phase86DepthThreeCStatement,
  )

  catalog = InferenceRuleCatalog()

  for key, rule, conclusion_type in (
    (
      "phase86.cycle.final",
      final_rule,
      Phase86DepthThreeGoalStatement,
    ),
    (
      "phase86.cycle.a",
      a_rule,
      Phase86DepthThreeAStatement,
    ),
    (
      "phase86.cycle.b",
      b_rule,
      Phase86DepthThreeBStatement,
    ),
    (
      "phase86.cycle.c",
      c_rule,
      Phase86DepthThreeCStatement,
    ),
  ):
    _register_rule(
      catalog,
      key,
      rule,
      conclusion_type,
    )

  return {
    "repository": repository,
    "catalog": catalog,
    "goal": Phase86DepthThreeGoalStatement(),
    "final_rule": final_rule,
    "a_rule": a_rule,
    "b_rule": b_rule,
    "c_rule": c_rule,
  }


def test_phase86_3_3_max_depth_three_reports_depth_limit_at_depth_four():
  data = build_phase86_3_3_depth_limit_data()

  diagnostic = (
    diagnose_depth_two_producer_search_failure(
      data[
        "repository"
      ],
      data[
        "catalog"
      ],
      data[
        "goal"
      ],
      max_depth=3,
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus.DEPTH_LIMIT
  )
  assert diagnostic.requesting_rule is data[
    "c_rule"
  ]
  assert diagnostic.current_depth == 3
  assert diagnostic.required_next_depth == 4
  assert diagnostic.producer_candidates == (
    data[
      "d_rule"
    ],
  )
  assert diagnostic.ancestor_rules == (
    data[
      "final_rule"
    ],
    data[
      "a_rule"
    ],
    data[
      "b_rule"
    ],
    data[
      "c_rule"
    ],
  )


def test_phase86_3_3_max_depth_three_reports_cycle_before_depth_limit():
  data = build_phase86_3_3_cycle_data()

  diagnostic = (
    diagnose_depth_two_producer_search_failure(
      data[
        "repository"
      ],
      data[
        "catalog"
      ],
      data[
        "goal"
      ],
      max_depth=3,
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus.CYCLE_DETECTED
  )
  assert diagnostic.requesting_rule is data[
    "c_rule"
  ]
  assert diagnostic.current_depth == 3
  assert diagnostic.required_next_depth == 4
  assert diagnostic.producer_candidates == (
    data[
      "a_rule"
    ],
  )
  assert diagnostic.ancestor_rules == (
    data[
      "final_rule"
    ],
    data[
      "a_rule"
    ],
    data[
      "b_rule"
    ],
    data[
      "c_rule"
    ],
  )


def test_phase86_3_3_max_depth_three_returns_none_for_valid_chain():
  data = build_phase86_3_1_data()

  assert diagnose_depth_two_producer_search_failure(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
    max_depth=3,
  ) is None


def test_phase86_3_3_max_depth_two_boundary_is_unchanged():
  data = build_phase86_3_3_depth_limit_data()

  diagnostic = (
    diagnose_depth_two_producer_search_failure(
      data[
        "repository"
      ],
      data[
        "catalog"
      ],
      data[
        "goal"
      ],
      max_depth=2,
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus.DEPTH_LIMIT
  )
  assert diagnostic.requesting_rule is data[
    "b_rule"
  ]
  assert diagnostic.current_depth == 2
  assert diagnostic.required_next_depth == 3
  assert diagnostic.producer_candidates == (
    data[
      "c_rule"
    ],
  )


def test_phase86_3_3_diagnostics_preserve_repository():
  data = build_phase86_3_3_depth_limit_data()
  initial_steps = repository_available_steps(
    data[
      "repository"
    ]
  )

  diagnose_depth_two_producer_search_failure(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
    max_depth=3,
  )

  assert repository_available_steps(
    data[
      "repository"
    ]
  ) == initial_steps


def test_phase86_3_4_max_depth_three_report_succeeds_for_valid_chain():
  data = build_phase86_3_1_data()

  report = build_depth_two_producer_search_report(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
    max_depth=3,
  )

  assert report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )
  assert report.diagnostic is None
  assert report.search_result is not None
  assert report.search_result.max_depth == 3
  assert tuple(
    node.producer_rule
    for node
    in report.search_result.producer_nodes
  ) == (
    data[
      "c_rule"
    ],
    data[
      "b_rule"
    ],
    data[
      "a_rule"
    ],
  )
  assert tuple(
    node.depths
    for node
    in report.search_result.producer_nodes
  ) == (
    (
      3,
    ),
    (
      2,
    ),
    (
      1,
    ),
  )


def test_phase86_3_4_max_depth_three_report_wraps_depth_limit_diagnostic():
  data = build_phase86_3_3_depth_limit_data()

  report = build_depth_two_producer_search_report(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
    max_depth=3,
  )

  assert report.status is (
    BoundedProducerSearchStatus.DEPTH_LIMIT
  )
  assert report.search_result is None
  assert report.diagnostic is not None
  assert report.diagnostic.status is (
    BoundedProducerSearchStatus.DEPTH_LIMIT
  )
  assert report.diagnostic.requesting_rule is data[
    "c_rule"
  ]
  assert report.diagnostic.current_depth == 3
  assert report.diagnostic.required_next_depth == 4
  assert report.diagnostic.producer_candidates == (
    data[
      "d_rule"
    ],
  )


def test_phase86_3_4_max_depth_three_report_wraps_cycle_diagnostic():
  data = build_phase86_3_3_cycle_data()

  report = build_depth_two_producer_search_report(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
    max_depth=3,
  )

  assert report.status is (
    BoundedProducerSearchStatus.CYCLE_DETECTED
  )
  assert report.search_result is None
  assert report.diagnostic is not None
  assert report.diagnostic.status is (
    BoundedProducerSearchStatus.CYCLE_DETECTED
  )
  assert report.diagnostic.requesting_rule is data[
    "c_rule"
  ]
  assert report.diagnostic.current_depth == 3
  assert report.diagnostic.required_next_depth == 4
  assert report.diagnostic.producer_candidates == (
    data[
      "a_rule"
    ],
  )


def test_phase86_3_4_max_depth_three_report_preserves_repository():
  data = build_phase86_3_1_data()
  initial_steps = repository_available_steps(
    data[
      "repository"
    ]
  )

  report = build_depth_two_producer_search_report(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
    max_depth=3,
  )

  assert report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )
  assert repository_available_steps(
    data[
      "repository"
    ]
  ) == initial_steps
