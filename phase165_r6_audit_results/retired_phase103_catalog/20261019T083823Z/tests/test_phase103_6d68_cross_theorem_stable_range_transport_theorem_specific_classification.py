from collections import (
  Counter,
  defaultdict,
)

from rule_catalog import (
  RuleRelevanceCategory,
)
from standard_production_applicability_catalog import (
  _inference_rule_factory_name,
  _phase103_6d68_apply_theorem_specific_classification,
  _phase103_6d68_original_builder,
)


PHASE103_6D68_TARGET_FAMILIES = (
  "Toda Proposition 5.3 eta_4 squared stable transport",
  "Toda Proposition 5.6 nu_5 stable transport",
  "Toda Proposition 5.11 higher six-stem nu squared transport",
)

PHASE103_6D68_TARGET_FACTORIES = (
  "toda_prop53_eta4_squared_stable_transport_inference_rule",
  "toda_prop56_nu5_stable_transport_inference_rule",
  "toda_prop511_higher_six_stem_nu_squared_transport_inference_rule",
)


def _build_catalog():
  return (
    _phase103_6d68_apply_theorem_specific_classification(
      _phase103_6d68_original_builder()
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


def test_phase103_6d68_classifies_the_three_audited_stable_range_transport_families_as_theorem_specific():
  catalog = _build_catalog()
  families = _families(
    catalog
  )

  for family in PHASE103_6D68_TARGET_FAMILIES:
    assert family in families

    assert all(
      entry.relevance_category
      is RuleRelevanceCategory.THEOREM_SPECIFIC
      for entry in families[
        family
      ]
    )


def test_phase103_6d68_target_entries_are_exactly_the_three_audited_factories():
  catalog = _build_catalog()

  target_entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.rule.name
      in PHASE103_6D68_TARGET_FAMILIES
    )
  )

  assert len(
    target_entries
  ) == 12

  assert {
    _inference_rule_factory_name(
      entry.rule
    )
    for entry in target_entries
  } == set(
    PHASE103_6D68_TARGET_FACTORIES
  )


def test_phase103_6d68_changes_exactly_twelve_entries_from_6d65_boundary():
  before = (
    _phase103_6d68_original_builder()
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

  for key, before_entry in before_by_key.items():
    after_entry = after_by_key[
      key
    ]

    factory_name = (
      _inference_rule_factory_name(
        before_entry.rule
      )
    )

    if (
      before_entry.relevance_category
      is RuleRelevanceCategory.UNCLASSIFIED
      and factory_name
      in PHASE103_6D68_TARGET_FACTORIES
    ):
      assert (
        after_entry.relevance_category
        is RuleRelevanceCategory.THEOREM_SPECIFIC
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
  ) == 12


def test_phase103_6d68_target_cluster_is_closed():
  catalog = _build_catalog()

  target_entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      _inference_rule_factory_name(
        entry.rule
      )
      in PHASE103_6D68_TARGET_FACTORIES
    )
  )

  assert len(
    target_entries
  ) == 12

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in target_entries
  )


def test_phase103_6d68_family_coverage_counts():
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
    for categories
    in categories_by_family.values()
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
  assert classified == 134
  assert unclassified == 133


def test_phase103_6d68_entry_coverage_counts():
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
    == 387
  )


def test_phase103_6d68_theorem_specific_entry_count_increases_by_exactly_twelve():
  before = (
    _phase103_6d68_original_builder()
  )
  after = (
    _build_catalog()
  )

  before_count = sum(
    1
    for entry in before.entries()
    if (
      entry.relevance_category
      is RuleRelevanceCategory.THEOREM_SPECIFIC
    )
  )

  after_count = sum(
    1
    for entry in after.entries()
    if (
      entry.relevance_category
      is RuleRelevanceCategory.THEOREM_SPECIFIC
    )
  )

  assert (
    after_count
    == before_count + 12
  )


def test_phase103_6d68_preserves_6d65_prop511_finite_dimensional_nu_squared_closure():
  catalog = _build_catalog()

  target_families = {
    "Toda Proposition 5.11 pi_12^6 nu_6 squared",
    "Toda Proposition 5.11 pi_13^7 nu_7 squared",
    "Toda Proposition 5.11 pi_14^8 nu_8 squared",
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


def test_phase103_6d68_preserves_6d62_lemma54_nu4_consequence_closure():
  catalog = _build_catalog()

  target_families = {
    "Toda Lemma 5.4 nu_4 Hopf correction",
    "Toda Lemma 5.4 nu_4 double suspension",
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
  ) == 14

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in entries
  )


def test_phase103_6d68_catalog_size_and_fixed_point_safety_are_unchanged():
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
