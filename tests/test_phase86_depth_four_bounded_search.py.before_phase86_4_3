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
  _validate_bounded_search_selection_max_depth,
  build_depth_two_producer_search_report,
  repository_available_steps,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)


@dataclass(frozen=True)
class Phase86DepthFourAStatement:
  pass


@dataclass(frozen=True)
class Phase86DepthFourBStatement:
  pass


@dataclass(frozen=True)
class Phase86DepthFourCStatement:
  pass


@dataclass(frozen=True)
class Phase86DepthFourDStatement:
  pass


@dataclass(frozen=True)
class Phase86DepthFourGoalStatement:
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
def build_phase86_4_2_data():
  repository = ProofRepository()

  final_rule = _single_premise_rule(
    "phase86 depth-four final",
    Phase86DepthFourAStatement,
    Phase86DepthFourGoalStatement,
  )
  a_rule = _single_premise_rule(
    "phase86 depth-four a",
    Phase86DepthFourBStatement,
    Phase86DepthFourAStatement,
  )
  b_rule = _single_premise_rule(
    "phase86 depth-four b",
    Phase86DepthFourCStatement,
    Phase86DepthFourBStatement,
  )
  c_rule = _single_premise_rule(
    "phase86 depth-four c",
    Phase86DepthFourDStatement,
    Phase86DepthFourCStatement,
  )
  d_rule = _no_premise_rule(
    "phase86 depth-four d",
    Phase86DepthFourDStatement,
  )

  catalog = InferenceRuleCatalog()

  for key, rule, conclusion_type in (
    (
      "phase86.depth-four.final",
      final_rule,
      Phase86DepthFourGoalStatement,
    ),
    (
      "phase86.depth-four.a",
      a_rule,
      Phase86DepthFourAStatement,
    ),
    (
      "phase86.depth-four.b",
      b_rule,
      Phase86DepthFourBStatement,
    ),
    (
      "phase86.depth-four.c",
      c_rule,
      Phase86DepthFourCStatement,
    ),
    (
      "phase86.depth-four.d",
      d_rule,
      Phase86DepthFourDStatement,
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
    "goal": Phase86DepthFourGoalStatement(),
    "final_rule": final_rule,
    "a_rule": a_rule,
    "b_rule": b_rule,
    "c_rule": c_rule,
    "d_rule": d_rule,
  }


def test_phase86_4_2_fixture_is_empty_depth_four_chain():
  data = build_phase86_4_2_data()

  assert repository_available_steps(
    data[
      "repository"
    ]
  ) == ()

  assert data[
    "final_rule"
  ].premise_patterns[
    0
  ].statement_type is Phase86DepthFourAStatement

  assert data[
    "a_rule"
  ].premise_patterns[
    0
  ].statement_type is Phase86DepthFourBStatement

  assert data[
    "b_rule"
  ].premise_patterns[
    0
  ].statement_type is Phase86DepthFourCStatement

  assert data[
    "c_rule"
  ].premise_patterns[
    0
  ].statement_type is Phase86DepthFourDStatement

  assert data[
    "d_rule"
  ].premise_patterns == ()


def test_phase86_4_2_max_depth_three_reports_depth_limit_at_depth_four():
  data = build_phase86_4_2_data()

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

  assert report.diagnostic.current_depth == 3
  assert report.diagnostic.required_next_depth == 4

  assert report.diagnostic.requesting_rule is data[
    "c_rule"
  ]

  assert report.diagnostic.producer_candidates == (
    data[
      "d_rule"
    ],
  )

  assert report.diagnostic.ancestor_rules == (
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


def test_phase86_4_2_validator_accepts_max_depth_four():
  _validate_bounded_search_selection_max_depth(
    4
  )
