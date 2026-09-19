from proof import (
  InferenceRule,
  PremisePattern,
)
from repository_generator_applicability_facade import (
  RepositoryGeneratorApplicabilityExplorationResult,
  explore_standard_repository_generator_applicability_input,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)


def build_wildcard_catalog(
  *,
  fixed_point_safe=False,
):
  catalog = InferenceRuleCatalog()

  rule = InferenceRule(
    name=(
      "phase103 generator facade "
      "wildcard rule"
    ),
    premise_patterns=(
      PremisePattern(),
    ),
  )

  entry = InferenceRuleCatalogEntry(
    key=(
      "phase103.generator-facade."
      "wildcard"
    ),
    rule=rule,
    conclusion_type=object,
    fixed_point_safe=(
      fixed_point_safe
    ),
  )

  catalog.register(
    entry
  )

  return {
    "catalog": catalog,
    "entry": entry,
    "rule": rule,
  }


def test_phase103_5_standard_nu_prime_returns_generator_specific_candidates():
  data = build_wildcard_catalog()

  result = (
    explore_standard_repository_generator_applicability_input(
      "nu_prime",
      data[
        "catalog"
      ],
    )
  )

  assert isinstance(
    result,
    RepositoryGeneratorApplicabilityExplorationResult,
  )

  assert (
    result
    .proof_scope_exploration
    .occurrences
  )

  assert (
    result.candidates
  )

  assert all(
    isinstance(
      candidate,
      RepositoryProofScopeApplicabilityCandidate,
    )
    for candidate in result.candidates
  )


def test_phase103_5_candidates_only_use_nodes_that_contain_generator():
  data = build_wildcard_catalog()

  result = (
    explore_standard_repository_generator_applicability_input(
      "nu_prime",
      data[
        "catalog"
      ],
    )
  )

  occurrence_node_ids = {
    id(
      occurrence.scope_node
    )
    for occurrence
    in result
    .proof_scope_exploration
    .occurrences
  }

  assert all(
    id(
      candidate.scope_node
    ) in occurrence_node_ids
    for candidate in result.candidates
  )


def test_phase103_5_wildcard_candidate_count_matches_unique_occurrence_nodes():
  data = build_wildcard_catalog()

  result = (
    explore_standard_repository_generator_applicability_input(
      "nu_prime",
      data[
        "catalog"
      ],
    )
  )

  unique_node_ids = {
    id(
      occurrence.scope_node
    )
    for occurrence
    in result
    .proof_scope_exploration
    .occurrences
  }

  assert len(
    result.candidates
  ) == len(
    unique_node_ids
  )


def test_phase103_5_unknown_generator_has_no_candidates():
  data = build_wildcard_catalog()

  result = (
    explore_standard_repository_generator_applicability_input(
      "eta_999",
      data[
        "catalog"
      ],
    )
  )

  assert (
    result
    .proof_scope_exploration
    .occurrences
    == ()
  )

  assert (
    result.candidates
    == ()
  )


def test_phase103_5_preserves_candidate_metadata():
  data = build_wildcard_catalog(
    fixed_point_safe=False,
  )

  result = (
    explore_standard_repository_generator_applicability_input(
      "nu_prime",
      data[
        "catalog"
      ],
    )
  )

  candidate = result.candidates[
    0
  ]

  assert (
    candidate
    .candidate
    .catalog_entry
    is data[
      "entry"
    ]
  )

  assert (
    candidate
    .candidate
    .inference_rule
    is data[
      "rule"
    ]
  )

  assert (
    candidate
    .candidate
    .fixed_point_safe
    is False
  )

  assert (
    candidate
    .candidate
    .source_step
    is candidate.scope_node.proof_step
  )


def test_phase103_5_standard_facade_does_not_mutate_catalog():
  data = build_wildcard_catalog()

  before = (
    data[
      "catalog"
    ].entries()
  )

  explore_standard_repository_generator_applicability_input(
    "nu_prime",
    data[
      "catalog"
    ],
  )

  after = (
    data[
      "catalog"
    ].entries()
  )

  assert (
    after
    == before
  )

  assert all(
    actual is expected
    for actual, expected in zip(
      after,
      before,
    )
  )


def test_phase103_5_standard_facade_rejects_invalid_generator_input():
  data = build_wildcard_catalog()

  import pytest

  with pytest.raises(
    TypeError,
    match=(
      "generator_input must be a str"
    ),
  ):
    explore_standard_repository_generator_applicability_input(
      object(),
      data[
        "catalog"
      ],
    )


def test_phase103_5_standard_facade_rejects_invalid_catalog():
  import pytest

  with pytest.raises(
    TypeError,
    match=(
      "catalog must be an "
      "InferenceRuleCatalog"
    ),
  ):
    explore_standard_repository_generator_applicability_input(
      "nu_prime",
      object(),
    )
