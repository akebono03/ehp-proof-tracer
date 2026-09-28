import pytest

from proof import (
  InferenceRule,
  PremisePattern,
)
from repository_generator_applicability_facade import (
  RepositoryGeneratorApplicabilityExplorationResult,
)
from repository_generator_applicability_selection import (
  RepositoryGeneratorApplicabilitySelection,
  select_repository_generator_applicability_by_rule_family,
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


def test_phase104_3c_selects_family_within_source_node():
  data = build_grouped_fixture()

  selection = (
    select_repository_generator_applicability_by_rule_family(
      data[
        "result"
      ],
      data[
        "first_node"
      ],
      "first grouped rule",
    )
  )

  assert isinstance(
    selection,
    RepositoryGeneratorApplicabilitySelection,
  )

  assert selection.candidates == (
    data[
      "candidates"
    ][0],
    data[
      "candidates"
    ][1],
  )


def test_phase104_3c_same_rule_name_on_other_source_is_not_selected():
  data = build_grouped_fixture()

  selection = (
    select_repository_generator_applicability_by_rule_family(
      data[
        "result"
      ],
      data[
        "first_node"
      ],
      "first grouped rule",
    )
  )

  assert all(
    candidate.scope_node
    is data[
      "first_node"
    ]
    for candidate in selection.candidates
  )

  assert all(
    candidate
    is not data[
      "candidates"
    ][3]
    for candidate in selection.candidates
  )


def test_phase104_3c_family_preserves_multiple_catalog_entries_and_order():
  data = build_grouped_fixture()

  first_node = data[
    "first_node"
  ]

  clone_rule = InferenceRule(
    name="first grouped rule",
    premise_patterns=(
      PremisePattern(),
    ),
  )

  clone_entry = InferenceRuleCatalogEntry(
    key="phase104.3c.first.clone",
    rule=clone_rule,
    conclusion_type=object,
  )

  clone_candidate = (
    RepositoryProofScopeApplicabilityCandidate(
      scope_node=first_node,
      candidate=(
        InferenceRuleApplicabilityCandidate(
          catalog_entry=clone_entry,
          premise_index=0,
          premise_pattern=(
            clone_rule
            .premise_patterns[
              0
            ]
          ),
          source_step=(
            first_node
            .proof_step
          ),
          bindings=(),
        )
      ),
    )
  )

  source_result = data[
    "result"
  ]

  extended_result = (
    RepositoryGeneratorApplicabilityExplorationResult(
      proof_scope_exploration=(
        source_result
        .proof_scope_exploration
      ),
      candidates=(
        source_result.candidates
        + (
          clone_candidate,
        )
      ),
    )
  )

  selection = (
    select_repository_generator_applicability_by_rule_family(
      extended_result,
      first_node,
      "first grouped rule",
    )
  )

  assert selection.candidates == (
    data[
      "candidates"
    ][0],
    data[
      "candidates"
    ][1],
    clone_candidate,
  )

  assert (
    selection.candidates[
      2
    ]
    is clone_candidate
  )


def test_phase104_3c_missing_family_returns_empty_selection():
  data = build_grouped_fixture()

  selection = (
    select_repository_generator_applicability_by_rule_family(
      data[
        "result"
      ],
      data[
        "first_node"
      ],
      "missing family",
    )
  )

  assert selection.candidates == ()


def test_phase104_3c_rejects_foreign_source_node_identity():
  data = build_grouped_fixture()
  foreign_data = build_grouped_fixture()

  with pytest.raises(
    ValueError,
    match=(
      "scope_node must be an original source node "
      "from applicability_result"
    ),
  ):
    select_repository_generator_applicability_by_rule_family(
      data[
        "result"
      ],
      foreign_data[
        "first_node"
      ],
      "first grouped rule",
    )


def test_phase104_3c_rejects_non_applicability_result():
  data = build_grouped_fixture()

  with pytest.raises(
    TypeError,
    match=(
      "applicability_result must be a "
      "RepositoryGeneratorApplicabilityExplorationResult"
    ),
  ):
    select_repository_generator_applicability_by_rule_family(
      object(),
      data[
        "first_node"
      ],
      "first grouped rule",
    )


def test_phase104_3c_rejects_non_scope_node():
  data = build_grouped_fixture()

  with pytest.raises(
    TypeError,
    match=(
      "scope_node must be a RepositoryProofScopeNode"
    ),
  ):
    select_repository_generator_applicability_by_rule_family(
      data[
        "result"
      ],
      object(),
      "first grouped rule",
    )


def test_phase104_3c_requires_rule_name_string():
  data = build_grouped_fixture()

  with pytest.raises(
    TypeError,
    match="rule_name must be a str",
  ):
    select_repository_generator_applicability_by_rule_family(
      data[
        "result"
      ],
      data[
        "first_node"
      ],
      object(),
    )


def test_phase104_3c_rejects_empty_rule_name():
  data = build_grouped_fixture()

  with pytest.raises(
    ValueError,
    match="rule_name must not be empty",
  ):
    select_repository_generator_applicability_by_rule_family(
      data[
        "result"
      ],
      data[
        "first_node"
      ],
      "",
    )
