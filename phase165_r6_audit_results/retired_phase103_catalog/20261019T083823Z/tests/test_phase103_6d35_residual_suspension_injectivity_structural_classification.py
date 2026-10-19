from collections import (
  Counter,
  defaultdict,
)

from rule_catalog import (
  RuleRelevanceCategory,
)
from standard_production_applicability_catalog import (
  _phase103_6d35_apply_structural_classification,
  _phase103_6d35_original_builder,
)


PHASE103_6D35_TARGET_FAMILIES = (
  "Toda Proposition 5.11 pi_12^6 suspension injective",
  "Toda Proposition 5.11 pi_13^7 suspension injective",
)


def _build_catalog():
  return (
    _phase103_6d35_apply_structural_classification(
      _phase103_6d35_original_builder()
    )
  )


def _families(
  catalog,
):
  result = defaultdict(
    list
  )

  for entry in catalog.entries():
    result[
      entry.rule.name
    ].append(
      entry
    )

  return {
    name: tuple(
      entries
    )
    for name, entries
    in result.items()
  }


def _suspension_injective_entries(
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
      == "TodaSuspensionInjectiveStatement"
    )
  )


def test_phase103_6d35_classifies_only_the_two_audited_residual_families_as_structural():
  catalog = _build_catalog()

  families = _families(
    catalog
  )

  for family in (
    PHASE103_6D35_TARGET_FAMILIES
  ):
    entries = families[
      family
    ]

    assert len(
      entries
    ) == 1

    assert all(
      entry.relevance_category
      is RuleRelevanceCategory.STRUCTURAL
      for entry in entries
    )


def test_phase103_6d35_changes_exactly_two_entries_from_6d32_boundary():
  before = (
    _phase103_6d35_original_builder()
  )

  after = (
    _build_catalog()
  )

  before_by_key = {
    entry.key: entry
    for entry in before.entries()
  }

  after_by_key = {
    entry.key: entry
    for entry in after.entries()
  }

  assert (
    before_by_key.keys()
    == after_by_key.keys()
  )

  changed = []

  for key, before_entry in (
    before_by_key.items()
  ):
    after_entry = (
      after_by_key[
        key
      ]
    )

    if (
      before_entry.relevance_category
      is RuleRelevanceCategory.UNCLASSIFIED
      and before_entry.rule.name
      in PHASE103_6D35_TARGET_FAMILIES
    ):
      assert (
        after_entry.relevance_category
        is RuleRelevanceCategory.STRUCTURAL
      )

      changed.append(
        key
      )
    else:
      assert (
        after_entry.relevance_category
        is before_entry.relevance_category
      )

  assert len(
    changed
  ) == 2


def test_phase103_6d35_suspension_injectivity_residual_cluster_is_closed():
  catalog = _build_catalog()

  entries = (
    _suspension_injective_entries(
      catalog
    )
  )

  residual_target_entries = tuple(
    entry
    for entry in entries
    if (
      entry.rule.name
      in PHASE103_6D35_TARGET_FAMILIES
    )
  )

  assert len(
    residual_target_entries
  ) == 2

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.STRUCTURAL
    for entry in residual_target_entries
  )


def test_phase103_6d35_family_coverage_counts():
  catalog = _build_catalog()

  families = _families(
    catalog
  )

  categories_by_family = {
    family: {
      entry.relevance_category
      for entry in entries
    }
    for family, entries
    in families.items()
  }

  assert all(
    len(
      categories
    )
    == 1
    for categories in (
      categories_by_family.values()
    )
  )

  classified = sum(
    1
    for categories
    in categories_by_family.values()
    if categories
    != {
      RuleRelevanceCategory.UNCLASSIFIED
    }
  )

  unclassified = sum(
    1
    for categories
    in categories_by_family.values()
    if categories
    == {
      RuleRelevanceCategory.UNCLASSIFIED
    }
  )

  assert len(
    families
  ) == 267

  assert classified == 110
  assert unclassified == 157


def test_phase103_6d35_entry_coverage_counts():
  catalog = _build_catalog()

  entries = tuple(
    catalog.entries()
  )

  counts = Counter(
    entry.relevance_category
    for entry in entries
  )

  assert len(
    entries
  ) == 1188

  assert (
    counts[
      RuleRelevanceCategory.STRUCTURAL
    ]
    == 196
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
    == 465
  )


def test_phase103_6d35_preserves_delta_injectivity_closure():
  catalog = _build_catalog()

  delta_entries = tuple(
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

  counts = Counter(
    entry.relevance_category
    for entry in delta_entries
  )

  assert len(
    delta_entries
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


def test_phase103_6d35_catalog_size_and_fixed_point_safety_are_unchanged():
  catalog = _build_catalog()

  entries = tuple(
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
