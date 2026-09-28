import pytest

from repository_generator_applicability_facade import (
  explore_standard_repository_generator_applicability_input,
)
from repository_generator_applicability_presentation import (
  build_repository_generator_applicability_presentation,
)
from web_generator_applicability import (
  WebGeneratorApplicabilityRuleFamilyView,
  WebGeneratorApplicabilitySourceView,
  WebGeneratorApplicabilityView,
  build_standard_web_generator_applicability_view,
)


def test_phase123_4_nu_prime_returns_structured_web_applicability_view():
  view = (
    build_standard_web_generator_applicability_view(
      "nu_prime"
    )
  )

  assert isinstance(
    view,
    WebGeneratorApplicabilityView,
  )

  assert (
    view.generator_input
    == "nu_prime"
  )

  assert (
    view.generator_latex
    == r"\nu'"
  )

  assert view.occurrence_count > 0
  assert view.candidate_count > 0
  assert view.source_count > 0
  assert view.rule_group_count > 0
  assert view.rule_family_count > 0


def test_phase123_4_counts_match_existing_applicability_presentation():
  result = (
    explore_standard_repository_generator_applicability_input(
      "nu_prime"
    )
  )

  presentation = (
    build_repository_generator_applicability_presentation(
      result
    )
  )

  view = (
    build_standard_web_generator_applicability_view(
      "nu_prime"
    )
  )

  assert (
    view.occurrence_count
    == len(
      result
      .proof_scope_exploration
      .occurrences
    )
  )

  assert (
    view.candidate_count
    == len(
      result.candidates
    )
  )

  assert (
    view.source_count
    == len(
      presentation.source_groups
    )
  )

  assert (
    view.rule_group_count
    == presentation.rule_group_count
  )

  assert (
    view.rule_family_count
    == presentation.rule_family_count
  )


def test_phase123_4_source_grouping_matches_existing_presentation():
  result = (
    explore_standard_repository_generator_applicability_input(
      "nu_prime"
    )
  )

  presentation = (
    build_repository_generator_applicability_presentation(
      result
    )
  )

  view = (
    build_standard_web_generator_applicability_view(
      "nu_prime"
    )
  )

  assert (
    len(
      view.toda_memberships
    )
    == len(
      presentation
      .toda_membership_source_groups
    )
  )

  assert (
    len(
      view.map_relations
    )
    == len(
      presentation
      .map_relation_source_groups
    )
  )

  assert (
    len(
      view.other_sources
    )
    == len(
      presentation
      .other_source_groups
    )
  )


def test_phase123_4_compact_source_preserves_display_fields():
  view = (
    build_standard_web_generator_applicability_view(
      "nu_prime"
    )
  )

  sources = (
    view.toda_memberships
    + view.map_relations
    + view.other_sources
  )

  source = sources[
    0
  ]

  assert isinstance(
    source,
    WebGeneratorApplicabilitySourceView,
  )

  assert (
    source.statement_latex
    or source.fallback_type_name
  )
  assert source.root_key
  assert source.depth >= 0
  assert source.source_statement_type
  assert source.raw_candidate_count > 0
  assert source.rule_family_count > 0

  rule_family = (
    source.rule_families[
      0
    ]
  )

  assert isinstance(
    rule_family,
    WebGeneratorApplicabilityRuleFamilyView,
  )

  assert rule_family.name
  assert rule_family.catalog_entry_count > 0
  assert rule_family.raw_candidate_count > 0

  assert not hasattr(
    rule_family,
    "fixed_point_safe",
  )
  assert not hasattr(
    rule_family,
    "premise_indexes",
  )
  assert not hasattr(
    rule_family,
    "bindings",
  )


def test_phase123_4_unknown_generator_is_normal_zero_result():
  view = (
    build_standard_web_generator_applicability_view(
      "eta_999"
    )
  )

  assert (
    view.generator_latex
    == r"\eta_{999}"
  )

  assert view.occurrence_count == 0
  assert view.candidate_count == 0
  assert view.source_count == 0
  assert view.rule_group_count == 0
  assert view.rule_family_count == 0
  assert view.toda_memberships == ()
  assert view.map_relations == ()
  assert view.other_sources == ()


def test_phase123_4_blank_generator_is_rejected():
  with pytest.raises(
    ValueError,
    match="generator is required",
  ):
    build_standard_web_generator_applicability_view(
      "  "
    )


def test_phase123_4_non_string_generator_is_rejected():
  with pytest.raises(
    TypeError,
    match="generator_input must be a str",
  ):
    build_standard_web_generator_applicability_view(
      None
    )
