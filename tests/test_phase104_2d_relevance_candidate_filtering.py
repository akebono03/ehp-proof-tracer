import pytest

from repository_generator_applicability_selection import (
  RepositoryGeneratorApplicabilitySelection,
  select_repository_generator_applicability_by_relevance,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from rule_applicability import (
  InferenceRuleApplicabilityCandidate,
)
from rule_catalog import (
  InferenceRuleCatalogEntry,
  RuleRelevanceCategory,
)
from test_phase103_grouped_applicability_presentation import (
  build_grouped_fixture,
)


def build_phase104_2d_fixture():
  data = build_grouped_fixture()

  first_entry = InferenceRuleCatalogEntry(
    key="phase104.2d.first",
    rule=(
      data[
        "first_entry"
      ].rule
    ),
    conclusion_type=object,
    fixed_point_safe=False,
    relevance_category=(
      RuleRelevanceCategory
      .THEOREM_SPECIFIC
    ),
  )

  second_entry = InferenceRuleCatalogEntry(
    key="phase104.2d.second",
    rule=(
      data[
        "second_entry"
      ].rule
    ),
    conclusion_type=object,
    fixed_point_safe=True,
    relevance_category=(
      RuleRelevanceCategory
      .MAP_PROPERTY
    ),
  )

  def wrap(
    source_candidate,
    entry,
  ):
    premise_index = (
      source_candidate
      .candidate
      .premise_index
    )

    return (
      RepositoryProofScopeApplicabilityCandidate(
        scope_node=(
          source_candidate.scope_node
        ),
        candidate=(
          InferenceRuleApplicabilityCandidate(
            catalog_entry=entry,
            premise_index=premise_index,
            premise_pattern=(
              entry
              .rule
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
          )
        ),
      )
    )

  source_candidates = data[
    "candidates"
  ]

  candidates = (
    wrap(
      source_candidates[0],
      first_entry,
    ),
    wrap(
      source_candidates[1],
      first_entry,
    ),
    wrap(
      source_candidates[2],
      second_entry,
    ),
    wrap(
      source_candidates[3],
      first_entry,
    ),
  )

  applicability_result = type(
    data[
      "result"
    ]
  )(
    proof_scope_exploration=(
      data[
        "result"
      ]
      .proof_scope_exploration
    ),
    candidates=candidates,
  )

  return {
    "applicability_result": applicability_result,
    "candidates": candidates,
    "first_entry": first_entry,
    "second_entry": second_entry,
  }


def test_phase104_2d_single_category_returns_matching_original_candidates():
  data = build_phase104_2d_fixture()

  selection = (
    select_repository_generator_applicability_by_relevance(
      data[
        "applicability_result"
      ],
      (
        RuleRelevanceCategory
        .THEOREM_SPECIFIC,
      ),
    )
  )

  assert isinstance(
    selection,
    RepositoryGeneratorApplicabilitySelection,
  )

  assert (
    selection.applicability_result
    is data[
      "applicability_result"
    ]
  )

  assert selection.candidates == (
    data[
      "candidates"
    ][0],
    data[
      "candidates"
    ][1],
    data[
      "candidates"
    ][3],
  )

  assert all(
    selected is expected
    for selected, expected in zip(
      selection.candidates,
      (
        data[
          "candidates"
        ][0],
        data[
          "candidates"
        ][1],
        data[
          "candidates"
        ][3],
      ),
    )
  )


def test_phase104_2d_multiple_categories_preserve_discovery_order():
  data = build_phase104_2d_fixture()

  selection = (
    select_repository_generator_applicability_by_relevance(
      data[
        "applicability_result"
      ],
      (
        RuleRelevanceCategory
        .MAP_PROPERTY,
        RuleRelevanceCategory
        .THEOREM_SPECIFIC,
      ),
    )
  )

  assert selection.candidates == data[
    "candidates"
  ]


def test_phase104_2d_category_argument_order_does_not_rank_candidates():
  data = build_phase104_2d_fixture()

  first = (
    select_repository_generator_applicability_by_relevance(
      data[
        "applicability_result"
      ],
      (
        RuleRelevanceCategory
        .THEOREM_SPECIFIC,
        RuleRelevanceCategory
        .MAP_PROPERTY,
      ),
    )
  )

  second = (
    select_repository_generator_applicability_by_relevance(
      data[
        "applicability_result"
      ],
      (
        RuleRelevanceCategory
        .MAP_PROPERTY,
        RuleRelevanceCategory
        .THEOREM_SPECIFIC,
      ),
    )
  )

  assert first.candidates == data[
    "candidates"
  ]

  assert second.candidates == data[
    "candidates"
  ]


def test_phase104_2d_empty_categories_return_empty_selection():
  data = build_phase104_2d_fixture()

  selection = (
    select_repository_generator_applicability_by_relevance(
      data[
        "applicability_result"
      ],
      (),
    )
  )

  assert selection.candidates == ()


def test_phase104_2d_duplicate_categories_do_not_duplicate_candidates():
  data = build_phase104_2d_fixture()

  selection = (
    select_repository_generator_applicability_by_relevance(
      data[
        "applicability_result"
      ],
      (
        RuleRelevanceCategory
        .THEOREM_SPECIFIC,
        RuleRelevanceCategory
        .THEOREM_SPECIFIC,
      ),
    )
  )

  assert selection.candidates == (
    data[
      "candidates"
    ][0],
    data[
      "candidates"
    ][1],
    data[
      "candidates"
    ][3],
  )


def test_phase104_2d_rejects_non_applicability_result():
  with pytest.raises(
    TypeError,
    match=(
      "applicability_result must be a "
      "RepositoryGeneratorApplicabilityExplorationResult"
    ),
  ):
    select_repository_generator_applicability_by_relevance(
      object(),
      (),
    )


def test_phase104_2d_requires_category_tuple():
  data = build_phase104_2d_fixture()

  with pytest.raises(
    TypeError,
    match=(
      "relevance_categories must be a tuple"
    ),
  ):
    select_repository_generator_applicability_by_relevance(
      data[
        "applicability_result"
      ],
      [
        RuleRelevanceCategory
        .THEOREM_SPECIFIC,
      ],
    )


def test_phase104_2d_rejects_non_category_member():
  data = build_phase104_2d_fixture()

  with pytest.raises(
    TypeError,
    match=(
      "relevance_categories must contain only "
      "RuleRelevanceCategory objects"
    ),
  ):
    select_repository_generator_applicability_by_relevance(
      data[
        "applicability_result"
      ],
      (
        "theorem_specific",
      ),
    )
