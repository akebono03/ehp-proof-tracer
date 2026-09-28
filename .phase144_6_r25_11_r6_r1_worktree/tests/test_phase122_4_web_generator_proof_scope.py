import pytest

from repository_element_facade import (
  explore_standard_repository_generator_input,
)
from repository_proof_scope_facade import (
  explore_standard_repository_generator_proof_scope_input,
)
from web_generator_proof_scope import (
  WebGeneratorProofScopeMapRelationView,
  WebGeneratorProofScopeTodaMembershipView,
  WebGeneratorProofScopeView,
  build_standard_web_generator_proof_scope_view,
)


def test_phase122_4_nu_prime_returns_structured_web_proof_scope_view():
  view = (
    build_standard_web_generator_proof_scope_view(
      "nu_prime"
    )
  )

  assert isinstance(
    view,
    WebGeneratorProofScopeView,
  )

  assert (
    view.generator_input
    == "nu_prime"
  )

  assert (
    view.generator_latex
    == r"\nu'"
  )

  assert (
    view.occurrence_count
    > 0
  )

  assert (
    view.toda_membership_count
    > 0
  )

  assert (
    view.map_relation_count
    > 0
  )


def test_phase122_4_counts_match_existing_proof_scope_facade():
  result = (
    explore_standard_repository_generator_proof_scope_input(
      "nu_prime"
    )
  )

  view = (
    build_standard_web_generator_proof_scope_view(
      "nu_prime"
    )
  )

  assert (
    view.occurrence_count
    == len(
      result.occurrences
    )
  )

  assert (
    view.toda_membership_count
    == len(
      result.toda_memberships
    )
  )

  assert (
    view.map_relation_count
    == len(
      result.map_relations
    )
  )


def test_phase122_4_toda_membership_preserves_latex_root_depth_and_match():
  view = (
    build_standard_web_generator_proof_scope_view(
      "nu_prime"
    )
  )

  membership = (
    view.toda_memberships[
      0
    ]
  )

  assert isinstance(
    membership,
    WebGeneratorProofScopeTodaMembershipView,
  )

  assert membership.statement_latex
  assert membership.root_key
  assert membership.depth >= 0
  assert membership.match_labels


def test_phase122_4_map_relation_preserves_latex_root_and_depth():
  view = (
    build_standard_web_generator_proof_scope_view(
      "nu_prime"
    )
  )

  map_relation = (
    view.map_relations[
      0
    ]
  )

  assert isinstance(
    map_relation,
    WebGeneratorProofScopeMapRelationView,
  )

  assert map_relation.statement_latex
  assert map_relation.root_key
  assert map_relation.depth >= 0


def test_phase122_4_sigma11_preserves_recursive_proof_scope_specialization():
  direct_report = (
    explore_standard_repository_generator_input(
      "sigma_11"
    )
  )

  proof_scope_view = (
    build_standard_web_generator_proof_scope_view(
      "sigma_11"
    )
  )

  assert (
    len(
      direct_report.presentation.occurrences
    )
    == 0
  )

  assert (
    proof_scope_view.occurrence_count
    > 0
  )


def test_phase122_4_unknown_generator_is_normal_zero_result():
  view = (
    build_standard_web_generator_proof_scope_view(
      "eta_999"
    )
  )

  assert (
    view.generator_latex
    == r"\eta_{999}"
  )

  assert view.occurrence_count == 0
  assert view.toda_membership_count == 0
  assert view.map_relation_count == 0
  assert view.toda_memberships == ()
  assert view.map_relations == ()


def test_phase122_4_blank_generator_is_rejected():
  with pytest.raises(
    ValueError,
    match="generator is required",
  ):
    build_standard_web_generator_proof_scope_view(
      "  "
    )


def test_phase122_4_non_string_generator_is_rejected():
  with pytest.raises(
    TypeError,
    match="generator_input must be a str",
  ):
    build_standard_web_generator_proof_scope_view(
      None
    )
