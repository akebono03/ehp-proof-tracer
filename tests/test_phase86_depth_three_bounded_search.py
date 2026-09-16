from dataclasses import dataclass
from functools import lru_cache

import pytest

from proof import (
  InferenceRule,
  PremisePattern,
  ProofRule,
)
from proof_repository import ProofRepository
from repository_inference import (
  BoundedProducerSearchStatus,
  build_depth_two_producer_search_report,
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


def test_phase86_3_1_max_depth_three_is_preimplementation_boundary():
  data = build_phase86_3_1_data()

  with pytest.raises(
    ValueError,
    match=(
      "max_depth must be 2 for "
      "depth-two producer search"
    ),
  ):
    select_unique_depth_two_producer_chain(
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
