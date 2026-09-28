from copy import copy
from dataclasses import dataclass

from proof import (
  InferenceRule,
  PremisePattern,
  ProofRule,
)
from proof_repository import ProofRepository
from repository_inference import (
  BoundedProducerSearchStatus,
  diagnose_depth_two_producer_search_failure,
  repository_available_steps,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)
from test_phase84_bounded_depth_two_execution import (
  build_phase84_5_data,
)


@dataclass(frozen=True)
class Phase85NestedAStatement:
  pass


@dataclass(frozen=True)
class Phase85NestedBStatement:
  pass


@dataclass(frozen=True)
class Phase85NestedCStatement:
  pass


@dataclass(frozen=True)
class Phase85NestedGoalStatement:
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


def _base_rules():
  return {
    "final_rule": _single_premise_rule(
      "phase85 nested final",
      Phase85NestedAStatement,
      Phase85NestedGoalStatement,
    ),
    "a_rule": _single_premise_rule(
      "phase85 nested a",
      Phase85NestedBStatement,
      Phase85NestedAStatement,
    ),
    "b_rule": _single_premise_rule(
      "phase85 nested b",
      Phase85NestedCStatement,
      Phase85NestedBStatement,
    ),
    "c_rule": _no_premise_rule(
      "phase85 nested c",
      Phase85NestedCStatement,
    ),
  }


def _catalog(
  rules,
  include_b=True,
  include_c=True,
  b_safe=True,
  c_safe=True,
  extra_b_rules=(),
  extra_c_rules=(),
):
  catalog = InferenceRuleCatalog()

  _register_rule(
    catalog,
    "phase85.nested.final",
    rules[
      "final_rule"
    ],
    Phase85NestedGoalStatement,
  )
  _register_rule(
    catalog,
    "phase85.nested.a",
    rules[
      "a_rule"
    ],
    Phase85NestedAStatement,
  )

  if include_b:
    _register_rule(
      catalog,
      "phase85.nested.b",
      rules[
        "b_rule"
      ],
      Phase85NestedBStatement,
      fixed_point_safe=b_safe,
    )

  for index, rule in enumerate(
    extra_b_rules
  ):
    _register_rule(
      catalog,
      f"phase85.nested.b-extra-{index}",
      rule,
      Phase85NestedBStatement,
    )

  if include_c:
    _register_rule(
      catalog,
      "phase85.nested.c",
      rules[
        "c_rule"
      ],
      Phase85NestedCStatement,
      fixed_point_safe=c_safe,
    )

  for index, rule in enumerate(
    extra_c_rules
  ):
    _register_rule(
      catalog,
      f"phase85.nested.c-extra-{index}",
      rule,
      Phase85NestedCStatement,
    )

  return catalog


def _diagnose(
  catalog,
):
  return diagnose_depth_two_producer_search_failure(
    ProofRepository(),
    catalog,
    Phase85NestedGoalStatement(),
  )


def test_phase85_4_classifies_missing_nested_producer():
  rules = _base_rules()
  diagnostic = _diagnose(
    _catalog(
      rules,
      include_b=False,
      include_c=False,
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus.NO_PRODUCER
  )
  assert diagnostic.requesting_rule is rules[
    "a_rule"
  ]
  assert diagnostic.premise_index == 0
  assert diagnostic.current_depth == 1
  assert diagnostic.required_next_depth == 2
  assert diagnostic.ancestor_rules == (
    rules[
      "final_rule"
    ],
    rules[
      "a_rule"
    ],
  )


def test_phase85_4_classifies_unsafe_nested_producer():
  rules = _base_rules()
  diagnostic = _diagnose(
    _catalog(
      rules,
      include_c=False,
      b_safe=False,
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus.UNSAFE_PRODUCER
  )
  assert diagnostic.producer_candidates == ()
  assert diagnostic.unsafe_producer_candidates == (
    rules[
      "b_rule"
    ],
  )


def test_phase85_4_classifies_ambiguous_nested_producer():
  rules = _base_rules()
  second_b_rule = copy(
    rules[
      "b_rule"
    ]
  )
  diagnostic = _diagnose(
    _catalog(
      rules,
      include_c=False,
      extra_b_rules=(
        second_b_rule,
      ),
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus
    .AMBIGUOUS_PRODUCER
  )
  assert diagnostic.producer_candidates == (
    rules[
      "b_rule"
    ],
    second_b_rule,
  )


def test_phase85_4_classifies_cycle_at_nested_level():
  rules = _base_rules()
  rules[
    "a_rule"
  ] = _single_premise_rule(
    "phase85 nested self cycle",
    Phase85NestedAStatement,
    Phase85NestedAStatement,
  )
  diagnostic = _diagnose(
    _catalog(
      rules,
      include_b=False,
      include_c=False,
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus.CYCLE_DETECTED
  )
  assert diagnostic.current_depth == 1
  assert diagnostic.required_next_depth == 2
  assert diagnostic.producer_candidates == (
    rules[
      "a_rule"
    ],
  )


def test_phase85_4_classifies_cycle_at_depth_boundary():
  rules = _base_rules()
  rules[
    "b_rule"
  ] = _single_premise_rule(
    "phase85 nested boundary cycle",
    Phase85NestedAStatement,
    Phase85NestedBStatement,
  )
  diagnostic = _diagnose(
    _catalog(
      rules,
      include_c=False,
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus.CYCLE_DETECTED
  )
  assert diagnostic.requesting_rule is rules[
    "b_rule"
  ]
  assert diagnostic.current_depth == 2
  assert diagnostic.required_next_depth == 3
  assert diagnostic.producer_candidates == (
    rules[
      "a_rule"
    ],
  )


def test_phase85_4_classifies_depth_limit():
  rules = _base_rules()
  diagnostic = _diagnose(
    _catalog(
      rules,
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus.DEPTH_LIMIT
  )
  assert diagnostic.requesting_rule is rules[
    "b_rule"
  ]
  assert diagnostic.current_depth == 2
  assert diagnostic.required_next_depth == 3
  assert diagnostic.producer_candidates == (
    rules[
      "c_rule"
    ],
  )
  assert diagnostic.ancestor_rules == (
    rules[
      "final_rule"
    ],
    rules[
      "a_rule"
    ],
    rules[
      "b_rule"
    ],
  )


def test_phase85_4_classifies_missing_boundary_producer():
  rules = _base_rules()
  diagnostic = _diagnose(
    _catalog(
      rules,
      include_c=False,
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus.NO_PRODUCER
  )
  assert diagnostic.current_depth == 2
  assert diagnostic.required_next_depth == 3


def test_phase85_4_classifies_unsafe_boundary_producer():
  rules = _base_rules()
  diagnostic = _diagnose(
    _catalog(
      rules,
      c_safe=False,
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus.UNSAFE_PRODUCER
  )
  assert diagnostic.unsafe_producer_candidates == (
    rules[
      "c_rule"
    ],
  )


def test_phase85_4_classifies_ambiguous_boundary_producer():
  rules = _base_rules()
  second_c_rule = copy(
    rules[
      "c_rule"
    ]
  )
  diagnostic = _diagnose(
    _catalog(
      rules,
      extra_c_rules=(
        second_c_rule,
      ),
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus
    .AMBIGUOUS_PRODUCER
  )
  assert diagnostic.producer_candidates == (
    rules[
      "c_rule"
    ],
    second_c_rule,
  )


def test_phase85_4_returns_none_for_valid_depth_two_chain():
  data = build_phase84_5_data()

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
  ) is None


def test_phase85_4_preserves_direct_failure_classification():
  data = build_phase84_5_data()
  diagnostic = (
    diagnose_depth_two_producer_search_failure(
      data[
        "repository"
      ],
      InferenceRuleCatalog(),
      data[
        "goal"
      ],
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus.NO_FINAL_RULE
  )


def test_phase85_4_diagnostic_does_not_mutate_repository():
  rules = _base_rules()
  repository = ProofRepository()
  initial_steps = repository_available_steps(
    repository
  )

  diagnose_depth_two_producer_search_failure(
    repository,
    _catalog(
      rules,
    ),
    Phase85NestedGoalStatement(),
  )

  assert repository_available_steps(
    repository
  ) == initial_steps
