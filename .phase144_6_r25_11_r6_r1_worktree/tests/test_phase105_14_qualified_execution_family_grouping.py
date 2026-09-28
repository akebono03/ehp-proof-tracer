import pytest

from repository_generator_applicability_execution_entry import (
  first_qualified_production_execution_family_name,
)
from repository_generator_applicability_facade import (
  RepositoryGeneratorApplicabilityExplorationResult,
)
from repository_generator_qualified_execution_family import (
  RepositoryGeneratorQualifiedExecutionFamilyGroup,
  RepositoryGeneratorQualifiedExecutionFamilyGrouping,
  group_qualified_repository_generator_execution_families,
)
from repository_generator_qualified_execution_selection import (
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
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  toda_58_delta_iota9_nu4_nu_prime_inference_rule,
)


def _qualified_clone(
  source_candidate,
  key,
):
  inference_rule = (
    toda_58_delta_iota9_nu4_nu_prime_inference_rule()
  )

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


def _build_phase105_14_fixture():
  data = build_grouped_fixture()

  first_source = data[
    "candidates"
  ][0]
  second_source = data[
    "candidates"
  ][3]

  first_family_candidates = (
    _qualified_clone(
      first_source,
      "phase105.14.first.1",
    ),
    _qualified_clone(
      first_source,
      "phase105.14.first.2",
    ),
    _qualified_clone(
      first_source,
      "phase105.14.first.3",
    ),
  )

  second_family_candidates = (
    _qualified_clone(
      second_source,
      "phase105.14.second.1",
    ),
    _qualified_clone(
      second_source,
      "phase105.14.second.2",
    ),
    _qualified_clone(
      second_source,
      "phase105.14.second.3",
    ),
  )

  candidates = (
    first_family_candidates
    + second_family_candidates
  )

  applicability_result = (
    RepositoryGeneratorApplicabilityExplorationResult(
      proof_scope_exploration=(
        data[
          "result"
        ].proof_scope_exploration
      ),
      candidates=candidates,
    )
  )

  selection = (
    select_qualified_repository_generator_applicability_candidates(
      applicability_result
    )
  )

  return {
    "selection": selection,
    "first_family_candidates": first_family_candidates,
    "second_family_candidates": second_family_candidates,
  }


def test_phase105_14_public_family_name_accepts_qualified_candidate():
  data = _build_phase105_14_fixture()

  assert (
    first_qualified_production_execution_family_name(
      data[
        "first_family_candidates"
      ][0]
    )
    == "toda_58_delta_iota9_nu4_nu_prime_inference_rule"
  )


def test_phase105_14_groups_equivalent_rule_clones_at_same_source():
  data = _build_phase105_14_fixture()

  grouping = (
    group_qualified_repository_generator_execution_families(
      data[
        "selection"
      ]
    )
  )

  assert isinstance(
    grouping,
    RepositoryGeneratorQualifiedExecutionFamilyGrouping,
  )
  assert len(
    grouping.groups
  ) == 2

  assert (
    grouping.groups[
      0
    ].candidates
    == data[
      "first_family_candidates"
    ]
  )
  assert (
    grouping.groups[
      1
    ].candidates
    == data[
      "second_family_candidates"
    ]
  )


def test_phase105_14_representative_is_first_original_candidate_in_group():
  data = _build_phase105_14_fixture()

  grouping = (
    group_qualified_repository_generator_execution_families(
      data[
        "selection"
      ]
    )
  )

  assert (
    grouping.groups[
      0
    ].representative
    is data[
      "first_family_candidates"
    ][0]
  )
  assert (
    grouping.groups[
      1
    ].representative
    is data[
      "second_family_candidates"
    ][0]
  )

  assert grouping.representatives == (
    data[
      "first_family_candidates"
    ][0],
    data[
      "second_family_candidates"
    ][0],
  )


def test_phase105_14_preserves_all_candidate_identities_and_order():
  data = _build_phase105_14_fixture()

  grouping = (
    group_qualified_repository_generator_execution_families(
      data[
        "selection"
      ]
    )
  )

  flattened = tuple(
    candidate
    for group
    in grouping.groups
    for candidate
    in group.candidates
  )

  assert flattened == (
    data[
      "selection"
    ].candidates
  )

  assert all(
    actual is expected
    for actual, expected
    in zip(
      flattened,
      data[
        "selection"
      ].candidates,
    )
  )


def test_phase105_14_does_not_merge_distinct_source_nodes():
  data = _build_phase105_14_fixture()

  grouping = (
    group_qualified_repository_generator_execution_families(
      data[
        "selection"
      ]
    )
  )

  first_group = grouping.groups[
    0
  ]
  second_group = grouping.groups[
    1
  ]

  assert (
    first_group.scope_node
    is not second_group.scope_node
  )
  assert (
    first_group.source_step
    is not second_group.source_step
  )


def test_phase105_14_family_group_rejects_mixed_sources():
  data = _build_phase105_14_fixture()

  with pytest.raises(
    ValueError,
    match=(
      "candidates must belong to one qualified "
      "execution family at one source"
    ),
  ):
    RepositoryGeneratorQualifiedExecutionFamilyGroup(
      candidates=(
        data[
          "first_family_candidates"
        ][0],
        data[
          "second_family_candidates"
        ][0],
      ),
    )


def test_phase105_14_grouping_rejects_non_qualified_selection():
  with pytest.raises(
    TypeError,
    match=(
      "selection must be a "
      "RepositoryGeneratorQualifiedExecutionSelection"
    ),
  ):
    group_qualified_repository_generator_execution_families(
      object()
    )
