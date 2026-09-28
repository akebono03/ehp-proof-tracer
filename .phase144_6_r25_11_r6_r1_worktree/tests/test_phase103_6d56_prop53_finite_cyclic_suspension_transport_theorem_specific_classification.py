from collections import (
  Counter,
  defaultdict,
)

from rule_catalog import (
  RuleRelevanceCategory,
)
from standard_production_applicability_catalog import (
  _inference_rule_factory_name,
  _phase103_6d56_apply_theorem_specific_classification,
  _phase103_6d56_original_builder,
)


PHASE103_6D56_TARGET_FAMILIES = (
  "Toda Proposition 5.3 n=3 pi_5^3 finite-cyclic transport",
  "Toda Proposition 5.3 n=4 pi_6^4 finite-cyclic transport",
)

PHASE103_6D56_TARGET_FACTORIES = (
  "toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule",
  "toda_prop53_n4_pi6_4_finite_cyclic_transport_inference_rule",
)


def _build_catalog():
  return (
    _phase103_6d56_apply_theorem_specific_classification(
      _phase103_6d56_original_builder()
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


def test_phase103_6d56_classifies_the_two_audited_prop53_transport_families_as_theorem_specific():
  catalog = _build_catalog()
  families = _families(
    catalog
  )

  for family in PHASE103_6D56_TARGET_FAMILIES:
    assert family in families

    assert all(
      entry.relevance_category
      is RuleRelevanceCategory.THEOREM_SPECIFIC
      for entry in families[
        family
      ]
    )


def test_phase103_6d56_target_entries_are_exactly_the_two_audited_factories():
  catalog = _build_catalog()

  target_entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.rule.name
      in PHASE103_6D56_TARGET_FAMILIES
    )
  )

  assert len(
    target_entries
  ) == 14

  assert {
    _inference_rule_factory_name(
      entry.rule
    )
    for entry in target_entries
  } == set(
    PHASE103_6D56_TARGET_FACTORIES
  )


def test_phase103_6d56_changes_exactly_fourteen_entries_from_6d53_boundary():
  before = (
    _phase103_6d56_original_builder()
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
      in PHASE103_6D56_TARGET_FACTORIES
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
  ) == 14


def test_phase103_6d56_target_cluster_is_closed():
  catalog = _build_catalog()

  target_entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      _inference_rule_factory_name(
        entry.rule
      )
      in PHASE103_6D56_TARGET_FACTORIES
    )
  )

  assert len(
    target_entries
  ) == 14

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in target_entries
  )


def test_phase103_6d56_family_coverage_counts():
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
  assert classified == 124
  assert unclassified == 143


def test_phase103_6d56_entry_coverage_counts():
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
    == 430
  )


def test_phase103_6d56_theorem_specific_entry_count_increases_by_exactly_fourteen():
  before = (
    _phase103_6d56_original_builder()
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
    == before_count + 14
  )


def test_phase103_6d56_preserves_6d53_composition_zero_closure():
  catalog = _build_catalog()

  target_families = {
    "Toda Proposition 5.8 eta_5 nu_6 zero",
    "Toda Proposition 3.1 nu_6 eta_9 zero consequence",
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
  ) == 6

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in entries
  )


def test_phase103_6d56_preserves_6d50_toda52_transport_closure():
  catalog = _build_catalog()

  target_families = {
    "Toda Proposition 5.6 pi_5^2 eta_2 cube",
    "Toda Proposition 5.9 pi_7^2 eta_2 nu-prime eta_6",
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
  ) == 5

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in entries
  )


def test_phase103_6d56_catalog_size_and_fixed_point_safety_are_unchanged():
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
