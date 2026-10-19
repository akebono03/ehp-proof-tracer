from collections import (
  Counter,
  defaultdict,
)

from rule_catalog import (
  RuleRelevanceCategory,
)
from standard_production_applicability_catalog import (
  build_standard_production_applicability_catalog,
)


PHASE103_6D32_EXPECTED_THEOREM_SPECIFIC_FAMILIES = (
  "Toda (5.12) n=4 Delta injective",
  "Toda (5.12) n=5 Delta injective",
  "Toda Proposition 5.1 n=3 Delta injectivity",
  "Toda Proposition 5.11 pi_9^5 to pi_7^2 Delta injective",
  "Toda Proposition 5.15 pi_10^5 to pi_8^2 Delta injective",
  "Toda Proposition 5.8 pi_9^9 Delta injective",
  "Toda Proposition 5.9 pi_10^9 Delta injective",
)

PHASE103_6D32_N6_MAP_PROPERTY_FAMILY = (
  "Toda (5.12) n=6 Delta injective"
)


def _build_catalog():
  from standard_production_applicability_catalog import (
    _phase103_6d32_apply_theorem_specific_classification,
    _phase103_6d32_original_builder,
  )

  return (
    _phase103_6d32_apply_theorem_specific_classification(
      _phase103_6d32_original_builder()
    )
  )


def _families(
  catalog,
):
  families = defaultdict(
    list
  )

  for entry in catalog.entries():
    families[
      entry.rule.name
    ].append(
      entry
    )

  return {
    name: tuple(
      entries
    )
    for name, entries
    in families.items()
  }


def _delta_injective_entries(
  catalog,
):
  return tuple(
    entry
    for entry in catalog.entries()
    if (
      getattr(
        entry.conclusion_type,
        "__name__",
        None,
      )
      == "TodaDeltaInjectiveStatement"
    )
  )


def test_phase103_6d32_classifies_all_7_residual_delta_injectivity_families_as_theorem_specific():
  catalog = (
    _build_catalog()
  )

  families = _families(
    catalog
  )

  for name in (
    PHASE103_6D32_EXPECTED_THEOREM_SPECIFIC_FAMILIES
  ):
    entries = families[
      name
    ]

    assert entries

    assert all(
      entry.relevance_category
      is RuleRelevanceCategory.THEOREM_SPECIFIC
      for entry in entries
    )


def test_phase103_6d32_classifies_exactly_15_residual_delta_injectivity_entries():
  catalog = (
    _build_catalog()
  )

  families = _families(
    catalog
  )

  affected_entries = tuple(
    entry
    for name in (
      PHASE103_6D32_EXPECTED_THEOREM_SPECIFIC_FAMILIES
    )
    for entry in families[
      name
    ]
  )

  assert len(
    affected_entries
  ) == 15

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in affected_entries
  )


def test_phase103_6d32_preserves_n6_generator_image_delta_injectivity_as_map_property():
  catalog = (
    _build_catalog()
  )

  families = _families(
    catalog
  )

  entries = families[
    PHASE103_6D32_N6_MAP_PROPERTY_FAMILY
  ]

  assert len(
    entries
  ) == 1

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.MAP_PROPERTY
    for entry in entries
  )


def test_phase103_6d32_closes_delta_injectivity_relevance_classification():
  catalog = (
    _build_catalog()
  )

  entries = (
    _delta_injective_entries(
      catalog
    )
  )

  counts = Counter(
    entry.relevance_category
    for entry in entries
  )

  assert len(
    entries
  ) == 16

  assert (
    counts[
      RuleRelevanceCategory.THEOREM_SPECIFIC
    ]
    == 15
  )

  assert (
    counts[
      RuleRelevanceCategory.MAP_PROPERTY
    ]
    == 1
  )

  assert (
    counts[
      RuleRelevanceCategory.UNCLASSIFIED
    ]
    == 0
  )


def test_phase103_6d32_updates_production_family_coverage_only_by_7_families():
  catalog = (
    _build_catalog()
  )

  families = _families(
    catalog
  )

  classified = 0
  unclassified = 0

  for entries in families.values():
    categories = {
      entry.relevance_category
      for entry in entries
    }

    assert len(
      categories
    ) == 1

    category = next(
      iter(
        categories
      )
    )

    if (
      category
      is RuleRelevanceCategory.UNCLASSIFIED
    ):
      unclassified += 1
    else:
      classified += 1

  assert len(
    families
  ) == 267

  assert classified == 108
  assert unclassified == 159


def test_phase103_6d32_updates_only_unclassified_entry_count_from_6d30_baseline():
  catalog = (
    _build_catalog()
  )

  counts = Counter(
    entry.relevance_category
    for entry in catalog.entries()
  )

  assert (
    counts[
      RuleRelevanceCategory.STRUCTURAL
    ]
    == 194
  )

  assert (
    counts[
      RuleRelevanceCategory.MAP_PROPERTY
    ]
    == 49
  )

  assert (
    counts[
      RuleRelevanceCategory.UNCLASSIFIED
    ]
    == 467
  )


def test_phase103_6d32_catalog_size_and_fixed_point_safety_are_unchanged():
  catalog = (
    _build_catalog()
  )

  entries = (
    catalog.entries()
  )

  assert len(
    entries
  ) == 1188

  assert all(
    entry.fixed_point_safe
    is False
    for entry in entries
  )
