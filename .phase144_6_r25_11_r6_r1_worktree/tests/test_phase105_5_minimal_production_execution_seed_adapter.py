from dataclasses import replace
from functools import lru_cache

import pytest

from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_generator_applicability_execution_seed import (
  build_repository_generator_applicability_execution_seed_repository,
)
from repository_generator_applicability_handoff import (
  RepositoryGeneratorApplicabilityCandidateHandoff,
  RepositoryGeneratorApplicabilityHandoffValidationStatus,
  build_repository_generator_applicability_handoff_search_report,
  execute_repository_generator_applicability_handoff_search_report,
  validate_repository_generator_applicability_handoff,
)
from repository_inference import (
  BoundedProducerSearchStatus,
  repository_available_steps,
)
from repository_proof_scope import (
  build_repository_proof_scope,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from rule_applicability import (
  build_inference_rule_premise_pattern_index,
  find_indexed_inference_rule_applicability_candidates,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)
from standard_production_applicability_catalog import (
  _inference_rule_factory_name,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)


_TARGET_FACTORY = (
  "toda_58_delta_iota9_nu4_nu_prime_inference_rule"
)


@lru_cache(maxsize=1)
def build_phase105_5_actual_data():
  production_repository = (
    build_standard_production_proof_repository()
  )
  scope = build_repository_proof_scope(
    production_repository
  )

  actual_target_nodes = tuple(
    node
    for node in scope.nodes
    if (
      node.root_entry.key
      == "standard.toda.prop58"
      and node.proof_step.inference_rule
      is not None
      and _inference_rule_factory_name(
        node.proof_step.inference_rule
      )
      == _TARGET_FACTORY
    )
  )

  assert len(
    actual_target_nodes
  ) == 1

  actual_target_step = (
    actual_target_nodes[
      0
    ].proof_step
  )

  assert len(
    actual_target_step.premises
  ) == 1

  source_step = (
    actual_target_step.premises[
      0
    ]
  )

  target_scope_node = (
    actual_target_nodes[
      0
    ]
  )

  source_scope_node = next(
    node
    for node in scope.nodes
    if (
      node.root_entry
      is target_scope_node.root_entry
      and node.proof_step
      is source_step
    )
  )

  actual_rule = (
    actual_target_step
    .inference_rule
  )
  assert actual_rule is not None

  discovery_entry = (
    InferenceRuleCatalogEntry(
      key=(
        "phase105.5.discovery."
        "delta-iota9-nu-expression"
      ),
      rule=actual_rule,
      conclusion_type=type(
        actual_target_step.conclusion
      ),
      fixed_point_safe=False,
    )
  )

  target_only_catalog = (
    InferenceRuleCatalog()
  )
  target_only_catalog.register(
    discovery_entry
  )

  index = (
    build_inference_rule_premise_pattern_index(
      target_only_catalog
    )
  )

  raw_candidates = (
    find_indexed_inference_rule_applicability_candidates(
      index,
      source_step,
    )
  )

  assert len(
    raw_candidates
  ) == 1

  candidate = (
    RepositoryProofScopeApplicabilityCandidate(
      scope_node=source_scope_node,
      candidate=raw_candidates[
        0
      ],
    )
  )

  seed_repository = (
    build_repository_generator_applicability_execution_seed_repository(
      candidate
    )
  )

  goal = (
    actual_target_step.conclusion
  )

  execution_entry = replace(
    discovery_entry,
    key=(
      "phase105.5.execution."
      "delta-iota9-nu-expression"
    ),
    fixed_point_safe=True,
    goal_compatibility=(
      lambda candidate_goal:
      candidate_goal == goal
    ),
  )

  execution_catalog = (
    InferenceRuleCatalog()
  )
  execution_catalog.register(
    execution_entry
  )

  handoff = (
    RepositoryGeneratorApplicabilityCandidateHandoff(
      candidate=candidate,
      goal=goal,
    )
  )

  validation = (
    validate_repository_generator_applicability_handoff(
      handoff,
      execution_catalog,
    )
  )

  search_report = (
    build_repository_generator_applicability_handoff_search_report(
      validation,
      seed_repository,
      execution_catalog,
    )
  )

  execution_result = (
    execute_repository_generator_applicability_handoff_search_report(
      search_report,
      seed_repository,
    )
  )

  return {
    "production_repository": production_repository,
    "scope": scope,
    "actual_target_step": actual_target_step,
    "source_step": source_step,
    "source_scope_node": source_scope_node,
    "discovery_entry": discovery_entry,
    "candidate": candidate,
    "seed_repository": seed_repository,
    "goal": goal,
    "execution_entry": execution_entry,
    "execution_catalog": execution_catalog,
    "handoff": handoff,
    "validation": validation,
    "search_report": search_report,
    "execution_result": execution_result,
  }


def test_phase105_5_adapter_rejects_non_candidate():
  with pytest.raises(
    TypeError,
    match=(
      "candidate must be a "
      "RepositoryProofScopeApplicabilityCandidate"
    ),
  ):
    build_repository_generator_applicability_execution_seed_repository(
      object()
    )


def test_phase105_5_adapter_returns_temporary_repository():
  data = build_phase105_5_actual_data()

  assert isinstance(
    data[
      "seed_repository"
    ],
    ProofRepository,
  )
  assert (
    data[
      "seed_repository"
    ]
    is not data[
      "production_repository"
    ]
  )


def test_phase105_5_seed_repository_contains_only_exact_candidate_source_step():
  data = build_phase105_5_actual_data()

  seed_steps = (
    repository_available_steps(
      data[
        "seed_repository"
      ]
    )
  )

  assert seed_steps == (
    data[
      "source_step"
    ],
  )
  assert (
    seed_steps[
      0
    ]
    is data[
      "candidate"
    ].candidate.source_step
  )
  assert (
    seed_steps[
      0
    ]
    is data[
      "candidate"
    ].scope_node.proof_step
  )


def test_phase105_5_seed_entry_preserves_root_metadata():
  data = build_phase105_5_actual_data()

  entries = (
    data[
      "seed_repository"
    ].entries()
  )

  assert len(
    entries
  ) == 1

  seed_entry = entries[
    0
  ]
  root_entry = (
    data[
      "candidate"
    ].root_entry
  )

  assert isinstance(
    seed_entry,
    ProofRepositoryEntry,
  )
  assert seed_entry.step is data[
    "source_step"
  ]
  assert seed_entry.phase == root_entry.phase
  assert seed_entry.theorem == root_entry.theorem


def test_phase105_5_adapter_does_not_mutate_standard_production_repository():
  data = build_phase105_5_actual_data()

  production_entries = (
    data[
      "production_repository"
    ].entries()
  )

  assert len(
    production_entries
  ) == 4
  assert all(
    entry
    not in data[
      "seed_repository"
    ].entries()
    for entry in production_entries
  )


def test_phase105_5_execution_entry_preserves_discovered_rule_identity():
  data = build_phase105_5_actual_data()

  assert (
    data[
      "execution_entry"
    ].rule
    is data[
      "discovery_entry"
    ].rule
  )
  assert (
    data[
      "execution_entry"
    ].rule
    is data[
      "candidate"
    ].candidate.inference_rule
  )


def test_phase105_5_actual_handoff_is_ready():
  data = build_phase105_5_actual_data()

  assert (
    data[
      "validation"
    ].status
    is RepositoryGeneratorApplicabilityHandoffValidationStatus.READY
  )
  assert (
    data[
      "validation"
    ].execution_entry
    is data[
      "execution_entry"
    ]
  )


def test_phase105_5_actual_search_succeeds_without_producers():
  data = build_phase105_5_actual_data()

  report = (
    data[
      "search_report"
    ].report
  )

  assert report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )
  assert report.search_result is not None
  assert (
    report.search_result.final_rule
    is data[
      "execution_entry"
    ].rule
  )
  assert report.search_result.producer_nodes == ()


def test_phase105_5_actual_execution_derives_expected_goal():
  data = build_phase105_5_actual_data()

  repository_result = (
    data[
      "execution_result"
    ]
    .execution_result
    .repository_inference_result
  )

  assert repository_result is not None
  assert repository_result.goal_step is not None
  assert (
    repository_result.goal_step.conclusion
    == data[
      "goal"
    ]
  )
  assert (
    repository_result.goal_step
    is not data[
      "actual_target_step"
    ]
  )


def test_phase105_5_actual_execution_preserves_seed_and_rule_provenance():
  data = build_phase105_5_actual_data()

  search_result = (
    data[
      "search_report"
    ].report.search_result
  )
  assert search_result is not None

  repository_result = (
    data[
      "execution_result"
    ]
    .execution_result
    .repository_inference_result
  )
  assert repository_result is not None
  assert repository_result.goal_step is not None

  goal_step = (
    repository_result.goal_step
  )

  assert (
    data[
      "candidate"
    ].candidate.inference_rule
    is data[
      "validation"
    ].execution_entry.rule
    is search_result.final_rule
    is goal_step.inference_rule
  )
  assert goal_step.premises == (
    data[
      "source_step"
    ],
  )
  assert (
    goal_step.premises[
      0
    ]
    is data[
      "candidate"
    ].candidate.source_step
  )
