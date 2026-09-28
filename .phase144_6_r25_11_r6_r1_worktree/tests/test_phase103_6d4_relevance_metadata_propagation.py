from expression import (
  GeneratorSymbol,
)
from map_property_rules import (
  injective_map_reflects_equality_inference_rule,
)
from proof import (
  InferenceRule,
)
from relation_rules import (
  equality_symmetry_inference_rule,
  equality_transitivity_inference_rule,
  iterated_suspension_one_bridge_inference_rule,
)
from repository_generator_applicability_facade import (
  explore_standard_repository_generator_applicability_input,
)
from repository_generator_applicability_presentation import (
  build_repository_generator_applicability_presentation,
)
from rule_catalog import (
  RuleRelevanceCategory,
)
from standard_production_applicability_catalog import (
  _representative_relevance_category,
  build_standard_production_applicability_catalog,
)
from toda_rules import (
  Toda53NuPrimeBracketSpecializationStatement,
)


def _entries_by_rule_name(
  catalog,
  rule_name,
):
  return tuple(
    entry
    for entry in catalog.entries()
    if entry.rule.name == rule_name
  )


def test_phase103_6d4_classifier_covers_representative_categories():
  probes = (
    (
      equality_symmetry_inference_rule(),
      object,
      RuleRelevanceCategory
      .GENERIC_RELATION,
    ),
    (
      equality_transitivity_inference_rule(),
      object,
      RuleRelevanceCategory
      .GENERIC_RELATION,
    ),
    (
      injective_map_reflects_equality_inference_rule(),
      object,
      RuleRelevanceCategory
      .MAP_PROPERTY,
    ),
    (
      InferenceRule(
        name="phase103 theorem-specific probe",
      ),
      Toda53NuPrimeBracketSpecializationStatement,
      RuleRelevanceCategory
      .THEOREM_SPECIFIC,
    ),
    (
      iterated_suspension_one_bridge_inference_rule(
        GeneratorSymbol(
          family="eta",
          index=2,
        )
      ),
      object,
      RuleRelevanceCategory
      .BRIDGE,
    ),
  )

  for (
    inference_rule,
    conclusion_type,
    expected_category,
  ) in probes:
    assert (
      _representative_relevance_category(
        inference_rule,
        conclusion_type,
      )
      is expected_category
    )


def test_phase103_6d4_actual_generic_relation_entries_are_classified():
  catalog = (
    build_standard_production_applicability_catalog()
  )

  entries = _entries_by_rule_name(
    catalog,
    "equality symmetry",
  )

  assert (
    entries
  )

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory
    .GENERIC_RELATION
    for entry in entries
  )


def test_phase103_6d4_actual_theorem_specific_entries_are_classified():
  catalog = (
    build_standard_production_applicability_catalog()
  )

  entries = _entries_by_rule_name(
    catalog,
    (
      "Toda 5.3 nu-prime "
      "Lemma 5.2 bracket specialization"
    ),
  )

  assert (
    entries
  )

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory
    .THEOREM_SPECIFIC
    for entry in entries
  )


def test_phase103_6d4_unclassified_remains_for_nonrepresentative_rules():
  catalog = (
    build_standard_production_applicability_catalog()
  )

  assert any(
    entry.relevance_category
    is RuleRelevanceCategory.UNCLASSIFIED
    for entry in catalog.entries()
  )


def test_phase103_6d4_catalog_remains_discovery_only():
  catalog = (
    build_standard_production_applicability_catalog()
  )

  assert all(
    entry.fixed_point_safe
    is False
    for entry in catalog.entries()
  )


def test_phase103_6d4_theorem_category_reaches_nu_prime_candidate():
  result = (
    explore_standard_repository_generator_applicability_input(
      "nu_prime"
    )
  )

  theorem_candidates = tuple(
    candidate
    for candidate in result.candidates
    if (
      candidate
      .candidate
      .catalog_entry
      .relevance_category
      is RuleRelevanceCategory
      .THEOREM_SPECIFIC
      and candidate
      .candidate
      .inference_rule
      .name
      == (
        "Toda 5.3 nu-prime "
        "Lemma 5.2 bracket specialization"
      )
    )
  )

  assert (
    theorem_candidates
  )


def test_phase103_6d4_group_presentation_preserves_catalog_entry_category():
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

  theorem_groups = tuple(
    rule_group
    for source_group
    in presentation.source_groups
    for rule_group
    in source_group.rule_groups
    if (
      rule_group
      .catalog_entry
      .relevance_category
      is RuleRelevanceCategory
      .THEOREM_SPECIFIC
      and rule_group
      .inference_rule
      .name
      == (
        "Toda 5.3 nu-prime "
        "Lemma 5.2 bracket specialization"
      )
    )
  )

  assert (
    theorem_groups
  )

  assert all(
    candidate
    .candidate
    .catalog_entry
    is rule_group.catalog_entry
    for rule_group in theorem_groups
    for candidate in rule_group.candidates
  )


def test_phase103_6d4_rule_family_preserves_classified_catalog_entries():
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

  theorem_families = tuple(
    family
    for source_group
    in presentation.source_groups
    for family
    in source_group.rule_families
    if (
      family.name
      == (
        "Toda 5.3 nu-prime "
        "Lemma 5.2 bracket specialization"
      )
    )
  )

  assert (
    theorem_families
  )

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory
    .THEOREM_SPECIFIC
    for family in theorem_families
    for entry in family.catalog_entries
  )
