import pytest

from repository_generator_applicability_execution_entry import (
  is_first_qualified_production_execution_candidate,
)
from repository_generator_applicability_facade import (
  RepositoryGeneratorApplicabilityExplorationResult,
)
from repository_generator_qualified_execution_selection import (
  RepositoryGeneratorQualifiedExecutionSelection,
  RepositoryGeneratorQualifiedExecutionSelectionStatus,
  select_qualified_repository_generator_applicability_candidates,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from rule_applicability import (
  InferenceRuleApplicabilityCandidate,
)
from rule_catalog import (
  InferenceRuleCatalogEntry,
)
from test_phase103_grouped_applicability_presentation import (
  build_grouped_fixture,
)
from test_phase105_5_minimal_production_execution_seed_adapter import (
  build_phase105_5_actual_data,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  toda_58_delta_iota9_nu4_nu_prime_inference_rule,
)


def _wrap_candidate_with_rule(
  source_candidate,
  inference_rule,
  key,
):
  entry = InferenceRuleCatalogEntry(
    key=key,
    rule=inference_rule,
    conclusion_type=(
      TodaDeltaImageUpToSignStatement
    ),
    fixed_point_safe=False,
  )

  return RepositoryProofScopeApplicabilityCandidate(
    scope_node=source_candidate.scope_node,
    candidate=InferenceRuleApplicabilityCandidate(
      catalog_entry=entry,
      premise_index=0,
      premise_pattern=(
        inference_rule.premise_patterns[
          0
        ]
      ),
      source_step=(
        source_candidate.scope_node.proof_step
      ),
      bindings=(),
    ),
  )


def _build_phase105_9_synthetic_result(
  qualified_count,
):
  data = build_grouped_fixture()

  source_candidates = data[
    "candidates"
  ]

  candidates = []

  for index in range(
    qualified_count
  ):
    candidates.append(
      _wrap_candidate_with_rule(
        source_candidates[
          index
        ],
        (
          toda_58_delta_iota9_nu4_nu_prime_inference_rule()
        ),
        (
          "phase105.9.qualified."
          f"{index}"
        ),
      )
    )

  if qualified_count < len(
    source_candidates
  ):
    candidates.append(
      source_candidates[
        qualified_count
      ]
    )

  return RepositoryGeneratorApplicabilityExplorationResult(
    proof_scope_exploration=(
      data[
        "result"
      ].proof_scope_exploration
    ),
    candidates=tuple(
      candidates
    ),
  )


def test_phase105_9_public_qualification_predicate_accepts_actual_candidate():
  data = build_phase105_5_actual_data()

  assert (
    is_first_qualified_production_execution_candidate(
      data[
        "candidate"
      ]
    )
    is True
  )


def test_phase105_9_public_qualification_predicate_rejects_non_candidate():
  with pytest.raises(
    TypeError,
    match=(
      "candidate must be a "
      "RepositoryProofScopeApplicabilityCandidate"
    ),
  ):
    is_first_qualified_production_execution_candidate(
      object()
    )


def test_phase105_9_none_status_preserves_empty_selection():
  result = (
    _build_phase105_9_synthetic_result(
      0
    )
  )

  selection = (
    select_qualified_repository_generator_applicability_candidates(
      result
    )
  )

  assert isinstance(
    selection,
    RepositoryGeneratorQualifiedExecutionSelection,
  )
  assert selection.applicability_result is result
  assert selection.candidates == ()
  assert selection.status is (
    RepositoryGeneratorQualifiedExecutionSelectionStatus
    .NONE
  )
  assert selection.unique_candidate is None


def test_phase105_9_unique_status_preserves_original_candidate_identity():
  result = (
    _build_phase105_9_synthetic_result(
      1
    )
  )

  qualified_candidate = result.candidates[
    0
  ]

  selection = (
    select_qualified_repository_generator_applicability_candidates(
      result
    )
  )

  assert selection.candidates == (
    qualified_candidate,
  )
  assert (
    selection.candidates[
      0
    ]
    is qualified_candidate
  )
  assert selection.status is (
    RepositoryGeneratorQualifiedExecutionSelectionStatus
    .UNIQUE
  )
  assert (
    selection.unique_candidate
    is qualified_candidate
  )


def test_phase105_9_ambiguous_status_preserves_all_candidates_and_order():
  result = (
    _build_phase105_9_synthetic_result(
      2
    )
  )

  first = result.candidates[
    0
  ]
  second = result.candidates[
    1
  ]

  selection = (
    select_qualified_repository_generator_applicability_candidates(
      result
    )
  )

  assert selection.candidates == (
    first,
    second,
  )
  assert (
    selection.candidates[
      0
    ]
    is first
  )
  assert (
    selection.candidates[
      1
    ]
    is second
  )
  assert selection.status is (
    RepositoryGeneratorQualifiedExecutionSelectionStatus
    .AMBIGUOUS
  )
  assert selection.unique_candidate is None


def test_phase105_9_filtering_ignores_discovery_fixed_point_safe_flag():
  result = (
    _build_phase105_9_synthetic_result(
      1
    )
  )

  qualified_candidate = result.candidates[
    0
  ]

  assert (
    qualified_candidate
    .candidate
    .catalog_entry
    .fixed_point_safe
    is False
  )

  selection = (
    select_qualified_repository_generator_applicability_candidates(
      result
    )
  )

  assert selection.candidates == (
    qualified_candidate,
  )


def test_phase105_9_filtering_does_not_use_relevance_as_safety():
  result = (
    _build_phase105_9_synthetic_result(
      0
    )
  )

  assert result.candidates

  selection = (
    select_qualified_repository_generator_applicability_candidates(
      result
    )
  )

  assert selection.candidates == ()


def test_phase105_9_rejects_non_applicability_result():
  with pytest.raises(
    TypeError,
    match=(
      "applicability_result must be a "
      "RepositoryGeneratorApplicabilityExplorationResult"
    ),
  ):
    select_qualified_repository_generator_applicability_candidates(
      object()
    )
