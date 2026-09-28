from collections import (
  Counter,
  defaultdict,
)

from rule_catalog import (
  RuleRelevanceCategory,
)
from standard_production_applicability_catalog import (
  _inference_rule_factory_name,
  _phase103_6d71_apply_theorem_specific_classification,
  _phase103_6d71_original_builder,
)


PHASE103_6D71_TARGET_FAMILIES = (
  "Toda Proposition 5.1 eta_4 order-two consequence",
  "Toda Lemma 5.4 eta_6 twice zero",
  "Toda Lemma 5.10 eta_8 two iota_9 zero",
  "Toda Lemma 5.10 eta_9 two iota_10 zero",
)

PHASE103_6D71_TARGET_FACTORIES = (
  "toda_prop51_eta4_twice_zero_inference_rule",
  "toda_lemma54_eta6_twice_zero_inference_rule",
  "toda_lemma510_eta8_two_iota9_zero_inference_rule",
  "toda_lemma510_eta9_two_iota10_zero_inference_rule",
)

PHASE103_6D71_DEFERRED_FAMILY = (
  "Toda Proposition 5.11 pi_14^13 eta_13"
)

PHASE103_6D71_DEFERRED_FACTORY = (
  "toda_prop511_pi14_13_eta13_inference_rule"
)


def _build_catalog():
  return (
    _phase103_6d71_apply_theorem_specific_classification(
      _phase103_6d71_original_builder()
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


def test_phase103_6d71_classifies_exactly_the_four_audited_eta_zero_relation_families():
  catalog = _build_catalog()
  families = _families(
    catalog
  )

  for family in PHASE103_6D71_TARGET_FAMILIES:
    assert family in families

    assert all(
      entry.relevance_category
      is RuleRelevanceCategory.THEOREM_SPECIFIC
      for entry in families[
        family
      ]
    )


def test_phase103_6d71_target_factories_are_exactly_the_audited_allowlist():
  catalog = _build_catalog()

  target_entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.rule.name
      in PHASE103_6D71_TARGET_FAMILIES
    )
  )

  assert target_entries

  assert {
    _inference_rule_factory_name(
      entry.rule
    )
    for entry in target_entries
  } == set(
    PHASE103_6D71_TARGET_FACTORIES
  )


def test_phase103_6d71_changes_only_entries_from_the_four_target_factories():
  before = (
    _phase103_6d71_original_builder()
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

  expected_changed = {
    key
    for key, entry in before_by_key.items()
    if (
      entry.relevance_category
      is RuleRelevanceCategory.UNCLASSIFIED
      and _inference_rule_factory_name(
        entry.rule
      )
      in PHASE103_6D71_TARGET_FACTORIES
    )
  }

  actual_changed = set()

  for key, before_entry in before_by_key.items():
    after_entry = after_by_key[
      key
    ]

    if (
      before_entry.relevance_category
      is not after_entry.relevance_category
    ):
      actual_changed.add(
        key
      )

      assert (
        before_entry.relevance_category
        is RuleRelevanceCategory.UNCLASSIFIED
      )

      assert (
        after_entry.relevance_category
        is RuleRelevanceCategory.THEOREM_SPECIFIC
      )

  assert expected_changed
  assert actual_changed == expected_changed


def test_phase103_6d71_target_cluster_is_closed():
  catalog = _build_catalog()

  target_entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      _inference_rule_factory_name(
        entry.rule
      )
      in PHASE103_6D71_TARGET_FACTORIES
    )
  )

  assert target_entries

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in target_entries
  )


def test_phase103_6d71_deliberately_leaves_pi14_13_eta13_unclassified():
  catalog = _build_catalog()

  deferred_entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.rule.name
      == PHASE103_6D71_DEFERRED_FAMILY
    )
  )

  assert deferred_entries

  assert {
    _inference_rule_factory_name(
      entry.rule
    )
    for entry in deferred_entries
  } == {
    PHASE103_6D71_DEFERRED_FACTORY
  }

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.UNCLASSIFIED
    for entry in deferred_entries
  )


def test_phase103_6d71_family_coverage_changes_by_exactly_four_families():
  before = (
    _phase103_6d71_original_builder()
  )
  after = (
    _build_catalog()
  )

  before_families = _families(
    before
  )
  after_families = _families(
    after
  )

  def classified_count(
    families,
  ):
    return sum(
      1
      for entries in families.values()
      if {
        entry.relevance_category
        for entry in entries
      }
      != {
        RuleRelevanceCategory.UNCLASSIFIED
      }
    )

  assert len(
    before_families
  ) == 267

  assert len(
    after_families
  ) == 267

  assert (
    classified_count(
      after_families
    )
    == classified_count(
      before_families
    ) + 4
  )


def test_phase103_6d71_entry_coverage_delta_matches_exact_target_entry_count():
  before = (
    _phase103_6d71_original_builder()
  )
  after = (
    _build_catalog()
  )

  before_entries = tuple(
    before.entries()
  )
  after_entries = tuple(
    after.entries()
  )

  before_counts = Counter(
    entry.relevance_category
    for entry in before_entries
  )

  after_counts = Counter(
    entry.relevance_category
    for entry in after_entries
  )

  target_count = sum(
    1
    for entry in before_entries
    if (
      entry.relevance_category
      is RuleRelevanceCategory.UNCLASSIFIED
      and _inference_rule_factory_name(
        entry.rule
      )
      in PHASE103_6D71_TARGET_FACTORIES
    )
  )

  assert target_count > 0

  assert len(
    before_entries
  ) == 1188
  assert len(
    after_entries
  ) == 1188

  assert (
    after_counts[
      RuleRelevanceCategory.UNCLASSIFIED
    ]
    == before_counts[
      RuleRelevanceCategory.UNCLASSIFIED
    ] - target_count
  )

  assert (
    after_counts[
      RuleRelevanceCategory.THEOREM_SPECIFIC
    ]
    == before_counts[
      RuleRelevanceCategory.THEOREM_SPECIFIC
    ] + target_count
  )


def test_phase103_6d71_preserves_6d68_stable_range_transport_closure():
  catalog = _build_catalog()

  target_families = {
    "Toda Proposition 5.3 eta_4 squared stable transport",
    "Toda Proposition 5.6 nu_5 stable transport",
    "Toda Proposition 5.11 higher six-stem nu squared transport",
  }

  entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.rule.name
      in target_families
    )
  )

  assert entries

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in entries
  )


def test_phase103_6d71_preserves_6d65_finite_dimensional_nu_squared_closure():
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

  assert entries

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in entries
  )


def test_phase103_6d71_catalog_size_and_fixed_point_safety_are_unchanged():
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
