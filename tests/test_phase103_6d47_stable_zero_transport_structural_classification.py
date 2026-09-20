from collections import (
  Counter,
  defaultdict,
)

from rule_catalog import (
  RuleRelevanceCategory,
)
from standard_production_applicability_catalog import (
  _inference_rule_factory_name,
  _phase103_6d47_apply_structural_classification,
  _phase103_6d47_original_builder,
)


PHASE103_6D47_TARGET_FAMILIES = (
  "Toda Proposition 5.8 higher four-stem zero transport",
  "Toda Proposition 5.9 higher five-stem zero transport",
)

PHASE103_6D47_TARGET_FACTORIES = (
  "toda_prop58_higher_four_stem_zero_transport_inference_rule",
  "toda_prop59_higher_five_stem_zero_transport_inference_rule",
)


def _build_catalog():
  return (
    _phase103_6d47_apply_structural_classification(
      _phase103_6d47_original_builder()
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


def test_phase103_6d47_classifies_only_the_two_audited_stable_zero_transport_families_as_structural():
  catalog = _build_catalog()

  families = _families(
    catalog
  )

  assert len(
    families[
      PHASE103_6D47_TARGET_FAMILIES[
        0
      ]
    ]
  ) == 2

  assert len(
    families[
      PHASE103_6D47_TARGET_FAMILIES[
        1
      ]
    ]
  ) == 1

  for family in (
    PHASE103_6D47_TARGET_FAMILIES
  ):
    assert all(
      entry.relevance_category
      is RuleRelevanceCategory.STRUCTURAL
      for entry in families[
        family
      ]
    )


def test_phase103_6d47_target_entries_are_exactly_the_two_audited_factories():
  catalog = _build_catalog()

  target_entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.rule.name
      in PHASE103_6D47_TARGET_FAMILIES
    )
  )

  assert len(
    target_entries
  ) == 3

  assert {
    _inference_rule_factory_name(
      entry.rule
    )
    for entry in target_entries
  } == set(
    PHASE103_6D47_TARGET_FACTORIES
  )


def test_phase103_6d47_changes_exactly_three_entries_from_6d44_boundary():
  before = (
    _phase103_6d47_original_builder()
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

    factory_name = (
      _inference_rule_factory_name(
        before_entry.rule
      )
    )

    if (
      before_entry.relevance_category
      is RuleRelevanceCategory.UNCLASSIFIED
      and factory_name
      in PHASE103_6D47_TARGET_FACTORIES
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
  ) == 3


def test_phase103_6d47_target_cluster_is_closed():
  catalog = _build_catalog()

  target_entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.rule.name
      in PHASE103_6D47_TARGET_FAMILIES
    )
  )

  assert len(
    target_entries
  ) == 3

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.STRUCTURAL
    for entry in target_entries
  )


def test_phase103_6d47_family_coverage_counts():
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

  assert classified == 118
  assert unclassified == 149


def test_phase103_6d47_entry_coverage_counts():
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
    == 201
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
    == 455
  )


def test_phase103_6d47_structural_entry_count_increases_by_exactly_three():
  before = (
    _phase103_6d47_original_builder()
  )

  after = (
    _build_catalog()
  )

  before_count = sum(
    1
    for entry in before.entries()
    if (
      entry.relevance_category
      is RuleRelevanceCategory.STRUCTURAL
    )
  )

  after_count = sum(
    1
    for entry in after.entries()
    if (
      entry.relevance_category
      is RuleRelevanceCategory.STRUCTURAL
    )
  )

  assert (
    after_count
    == before_count + 3
  )


def test_phase103_6d47_preserves_6d44_prop56_specialization_closure():
  catalog = _build_catalog()

  target_families = {
    "Toda Proposition 5.11 pi_10^7 nu_7 specialization",
    "Toda Proposition 5.11 pi_12^9 nu_9 specialization",
  }

  entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.rule.name
      in target_families
    )
  )

  assert len(
    entries
  ) == 3

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in entries
  )


def test_phase103_6d47_preserves_6d38_zero_group_exactness_closure():
  catalog = _build_catalog()

  target_families = {
    "Toda Proposition 5.11 pi_9^3 zero",
    "Toda Proposition 5.15 pi_10^3 zero",
  }

  entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.rule.name
      in target_families
    )
  )

  assert len(
    entries
  ) == 2

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.STRUCTURAL
    for entry in entries
  )


def test_phase103_6d47_catalog_size_and_fixed_point_safety_are_unchanged():
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
