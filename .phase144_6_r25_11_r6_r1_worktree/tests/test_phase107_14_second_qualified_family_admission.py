import pytest

from repository_generator_applicability_execution_entry import (
  first_qualified_production_execution_family_name,
  is_first_qualified_production_execution_candidate,
  is_qualified_production_execution_candidate,
  qualified_production_execution_family_name,
)
from repository_generator_applicability_facade import (
  RepositoryGeneratorApplicabilityExplorationResult,
)
from repository_generator_qualified_execution_family import (
  group_qualified_repository_generator_execution_families,
)
from repository_generator_qualified_execution_selection import (
  select_all_qualified_repository_generator_applicability_candidates,
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
  toda_58_delta_iota9_nu4_nu_prime_inference_rule,
  toda_lemma57_pi6_2_eta2_nu_prime_inference_rule,
)


_FIRST_FAMILY = (
  "toda_58_delta_iota9_nu4_nu_prime_inference_rule"
)

_SECOND_FAMILY = (
  "toda_lemma57_pi6_2_eta2_nu_prime_inference_rule"
)


def _wrap_candidate(
  source_candidate,
  inference_rule,
  premise_index,
  key,
):
  entry = InferenceRuleCatalogEntry(
    key=key,
    rule=inference_rule,
    conclusion_type=object,
    fixed_point_safe=False,
  )

  return RepositoryProofScopeApplicabilityCandidate(
    scope_node=source_candidate.scope_node,
    candidate=InferenceRuleApplicabilityCandidate(
      catalog_entry=entry,
      premise_index=premise_index,
      premise_pattern=(
        inference_rule
        .premise_patterns[
          premise_index
        ]
      ),
      source_step=(
        source_candidate
        .scope_node
        .proof_step
      ),
      bindings=(),
    ),
  )


def _build_phase107_14_fixture():
  data = build_grouped_fixture()

  first_rule = (
    toda_58_delta_iota9_nu4_nu_prime_inference_rule()
  )
  second_rule = (
    toda_lemma57_pi6_2_eta2_nu_prime_inference_rule()
  )

  first_candidate = (
    _wrap_candidate(
      data[
        "candidates"
      ][
        0
      ],
      first_rule,
      0,
      "phase107.14.first",
    )
  )

  second_candidate = (
    _wrap_candidate(
      data[
        "candidates"
      ][
        3
      ],
      second_rule,
      0,
      "phase107.14.second",
    )
  )

  unqualified_candidate = (
    data[
      "candidates"
    ][
      2
    ]
  )

  applicability_result = (
    RepositoryGeneratorApplicabilityExplorationResult(
      proof_scope_exploration=(
        data[
          "result"
        ].proof_scope_exploration
      ),
      candidates=(
        first_candidate,
        second_candidate,
        unqualified_candidate,
      ),
    )
  )

  return {
    "applicability_result": applicability_result,
    "first_candidate": first_candidate,
    "second_candidate": second_candidate,
    "unqualified_candidate": unqualified_candidate,
  }


def test_phase107_14_generic_qualification_accepts_first_family():
  data = _build_phase107_14_fixture()

  assert (
    is_qualified_production_execution_candidate(
      data[
        "first_candidate"
      ]
    )
    is True
  )

  assert (
    qualified_production_execution_family_name(
      data[
        "first_candidate"
      ]
    )
    == _FIRST_FAMILY
  )


def test_phase107_14_generic_qualification_accepts_second_family():
  data = _build_phase107_14_fixture()

  assert (
    is_qualified_production_execution_candidate(
      data[
        "second_candidate"
      ]
    )
    is True
  )

  assert (
    qualified_production_execution_family_name(
      data[
        "second_candidate"
      ]
    )
    == _SECOND_FAMILY
  )


def test_phase107_14_first_family_compatibility_predicate_rejects_second_family():
  data = _build_phase107_14_fixture()

  assert (
    is_first_qualified_production_execution_candidate(
      data[
        "first_candidate"
      ]
    )
    is True
  )

  assert (
    is_first_qualified_production_execution_candidate(
      data[
        "second_candidate"
      ]
    )
    is False
  )


def test_phase107_14_first_family_name_compatibility_rejects_second_family():
  data = _build_phase107_14_fixture()

  assert (
    first_qualified_production_execution_family_name(
      data[
        "first_candidate"
      ]
    )
    == _FIRST_FAMILY
  )

  with pytest.raises(
    ValueError,
    match=(
      "candidate rule is not the first qualified "
      "production execution rule"
    ),
  ):
    first_qualified_production_execution_family_name(
      data[
        "second_candidate"
      ]
    )


def test_phase107_14_legacy_selection_remains_first_family_only():
  data = _build_phase107_14_fixture()

  selection = (
    select_qualified_repository_generator_applicability_candidates(
      data[
        "applicability_result"
      ]
    )
  )

  assert selection.candidates == (
    data[
      "first_candidate"
    ],
  )


def test_phase107_14_multi_family_selection_admits_both_families_in_order():
  data = _build_phase107_14_fixture()

  selection = (
    select_all_qualified_repository_generator_applicability_candidates(
      data[
        "applicability_result"
      ]
    )
  )

  assert selection.candidates == (
    data[
      "first_candidate"
    ],
    data[
      "second_candidate"
    ],
  )

  assert (
    selection.candidates[
      0
    ]
    is data[
      "first_candidate"
    ]
  )

  assert (
    selection.candidates[
      1
    ]
    is data[
      "second_candidate"
    ]
  )


def test_phase107_14_multi_family_selection_rejects_unqualified_candidate():
  data = _build_phase107_14_fixture()

  assert (
    is_qualified_production_execution_candidate(
      data[
        "unqualified_candidate"
      ]
    )
    is False
  )

  selection = (
    select_all_qualified_repository_generator_applicability_candidates(
      data[
        "applicability_result"
      ]
    )
  )

  assert (
    data[
      "unqualified_candidate"
    ]
    not in selection.candidates
  )


def test_phase107_14_grouping_uses_generic_family_name():
  data = _build_phase107_14_fixture()

  selection = (
    select_all_qualified_repository_generator_applicability_candidates(
      data[
        "applicability_result"
      ]
    )
  )

  grouping = (
    group_qualified_repository_generator_execution_families(
      selection
    )
  )

  assert len(
    grouping.groups
  ) == 2

  assert (
    grouping.groups[
      0
    ].family_name
    == _FIRST_FAMILY
  )

  assert (
    grouping.groups[
      1
    ].family_name
    == _SECOND_FAMILY
  )

  assert (
    grouping.groups[
      0
    ].representative
    is data[
      "first_candidate"
    ]
  )

  assert (
    grouping.groups[
      1
    ].representative
    is data[
      "second_candidate"
    ]
  )


def test_phase107_14_generic_qualification_rejects_non_candidate():
  with pytest.raises(
    TypeError,
    match=(
      "candidate must be a "
      "RepositoryProofScopeApplicabilityCandidate"
    ),
  ):
    is_qualified_production_execution_candidate(
      object()
    )


def test_phase107_14_generic_family_name_rejects_non_candidate():
  with pytest.raises(
    TypeError,
    match=(
      "candidate must be a "
      "RepositoryProofScopeApplicabilityCandidate"
    ),
  ):
    qualified_production_execution_family_name(
      object()
    )


def test_phase107_14_multi_family_selection_rejects_non_result():
  with pytest.raises(
    TypeError,
    match=(
      "applicability_result must be a "
      "RepositoryGeneratorApplicabilityExplorationResult"
    ),
  ):
    select_all_qualified_repository_generator_applicability_candidates(
      object()
    )
