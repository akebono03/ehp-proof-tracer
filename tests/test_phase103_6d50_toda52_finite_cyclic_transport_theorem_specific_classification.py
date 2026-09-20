from collections import (
  Counter,
  defaultdict,
)

from rule_catalog import (
  RuleRelevanceCategory,
)
from standard_production_applicability_catalog import (
  _inference_rule_factory_name,
  _phase103_6d50_apply_theorem_specific_classification,
  _phase103_6d50_original_builder,
)


PHASE103_6D50_TARGET_FAMILIES = (
  "Toda Proposition 5.6 pi_5^2 eta_2 cube",
  "Toda Proposition 5.9 pi_7^2 eta_2 nu-prime eta_6",
)

PHASE103_6D50_TARGET_FACTORIES = (
  "toda_prop56_pi5_2_eta2_cube_inference_rule",
  "toda_prop59_pi7_2_eta2_nu_prime_eta6_inference_rule",
)


def _build_catalog():
  return (
    _phase103_6d50_apply_theorem_specific_classification(
      _phase103_6d50_original_builder()
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


def test_phase103_6d50_classifies_only_the_two_audited_toda52_transport_families_as_theorem_specific():
  catalog = _build_catalog()
  families = _families(
    catalog
  )

  assert len(
    families[
      PHASE103_6D50_TARGET_FAMILIES[
        0
      ]
    ]
  ) == 4

  assert len(
    families[
      PHASE103_6D50_TARGET_FAMILIES[
        1
      ]
    ]
  ) == 1

  for family in PHASE103_6D50_TARGET_FAMILIES:
    assert all(
      entry.relevance_category
      is RuleRelevanceCategory.THEOREM_SPECIFIC
      for entry in families[
        family
      ]
    )


def test_phase103_6d50_target_entries_are_exactly_the_two_audited_factories():
  catalog = _build_catalog()

  target_entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.rule.name
      in PHASE103_6D50_TARGET_FAMILIES
    )
  )

  assert len(
    target_entries
  ) == 5

  assert {
    _inference_rule_factory_name(
      entry.rule
    )
    for entry in target_entries
  } == set(
    PHASE103_6D50_TARGET_FACTORIES
  )


def test_phase103_6d50_changes_exactly_five_entries_from_6d47_boundary():
  before = (
    _phase103_6d50_original_builder()
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
      in PHASE103_6D50_TARGET_FACTORIES
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
  ) == 5


def test_phase103_6d50_target_cluster_is_closed():
  catalog = _build_catalog()

  target_entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.rule.name
      in PHASE103_6D50_TARGET_FAMILIES
    )
  )

  assert len(
    target_entries
  ) == 5

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in target_entries
  )


def test_phase103_6d50_family_coverage_counts():
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
  assert classified == 120
  assert unclassified == 147


def test_phase103_6d50_entry_coverage_counts():
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
    == 450
  )


def test_phase103_6d50_theorem_specific_entry_count_increases_by_exactly_five():
  before = (
    _phase103_6d50_original_builder()
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
    == before_count + 5
  )


def test_phase103_6d50_preserves_6d47_stable_zero_transport_closure():
  catalog = _build_catalog()

  target_families = {
    "Toda Proposition 5.8 higher four-stem zero transport",
    "Toda Proposition 5.9 higher five-stem zero transport",
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
    is RuleRelevanceCategory.STRUCTURAL
    for entry in entries
  )


def test_phase103_6d50_preserves_6d44_prop56_specialization_closure():
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


def test_phase103_6d50_catalog_size_and_fixed_point_safety_are_unchanged():
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
