from collections import (
  Counter,
  defaultdict,
)

from rule_catalog import (
  RuleRelevanceCategory,
)
from standard_production_applicability_catalog import (
  _PHASE103_6D108_RELEVANCE_BY_FACTORY,
  _inference_rule_factory_name,
  _phase103_6d108_apply_grouped_relevance_classification,
  _phase103_6d108_original_builder,
)


PHASE103_6D108_EXPECTED_RELEVANCE_BY_FACTORY = {
  "toda_57_nu_prime_eta6_hopf_inference_rule": (
    RuleRelevanceCategory.MAP_PROPERTY
  ),
  "toda_prop56_e2_nu_prime_order_four_inference_rule": (
    RuleRelevanceCategory.THEOREM_SPECIFIC
  ),
  "toda_58_delta_iota9_nu4_nu_prime_inference_rule": (
    RuleRelevanceCategory.MAP_PROPERTY
  ),
  "toda_lemma57_nu_prime_hypothesis_inference_rule": (
    RuleRelevanceCategory.BRIDGE
  ),
  "toda_lemma57_pi6_2_eta2_nu_prime_inference_rule": (
    RuleRelevanceCategory.THEOREM_SPECIFIC
  ),
  "toda_prop58_e_nu_prime_eta6_bridge_inference_rule": (
    RuleRelevanceCategory.BRIDGE
  ),
  "toda_prop511_pi8_2_eta2_nu_prime_eta6_squared_inference_rule": (
    RuleRelevanceCategory.THEOREM_SPECIFIC
  ),
  "toda_prop59_nu_prime_eta6_squared_hopf_inference_rule": (
    RuleRelevanceCategory.MAP_PROPERTY
  ),
}


def _build_catalog():
  return (
    _phase103_6d108_apply_grouped_relevance_classification(
      _phase103_6d108_original_builder()
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


def _entries_by_factory(
  catalog,
):
  result = defaultdict(
    list
  )

  for entry in catalog.entries():
    factory_name = (
      _inference_rule_factory_name(
        entry.rule
      )
    )

    if (
      factory_name
      in PHASE103_6D108_EXPECTED_RELEVANCE_BY_FACTORY
    ):
      result[
        factory_name
      ].append(
        entry
      )

  return {
    factory_name: tuple(
      entries
    )
    for factory_name, entries
    in result.items()
  }


def test_phase103_6d108_mapping_is_exactly_the_grouped_audit_conclusion():
  assert (
    _PHASE103_6D108_RELEVANCE_BY_FACTORY
    == PHASE103_6D108_EXPECTED_RELEVANCE_BY_FACTORY
  )

  assert len(
    _PHASE103_6D108_RELEVANCE_BY_FACTORY
  ) == 8


def test_phase103_6d108_classifies_all_eight_target_factories():
  catalog = _build_catalog()
  by_factory = _entries_by_factory(
    catalog
  )

  assert set(
    by_factory
  ) == set(
    PHASE103_6D108_EXPECTED_RELEVANCE_BY_FACTORY
  )

  for factory_name, expected_category in (
    PHASE103_6D108_EXPECTED_RELEVANCE_BY_FACTORY.items()
  ):
    entries = by_factory[
      factory_name
    ]

    assert entries

    assert all(
      entry.relevance_category
      is expected_category
      for entry in entries
    )


def test_phase103_6d108_target_factories_cover_exactly_eight_families():
  catalog = _build_catalog()
  by_factory = _entries_by_factory(
    catalog
  )

  family_names = set()

  for factory_name, entries in by_factory.items():
    names = {
      entry.rule.name
      for entry in entries
    }

    assert len(
      names
    ) == 1, factory_name

    family_names.update(
      names
    )

  assert len(
    family_names
  ) == 8


def test_phase103_6d108_changes_only_target_factories_and_only_from_unclassified():
  before = (
    _phase103_6d108_original_builder()
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
    for key, entry
    in before_by_key.items()
    if (
      entry.relevance_category
      is RuleRelevanceCategory.UNCLASSIFIED
      and _inference_rule_factory_name(
        entry.rule
      )
      in PHASE103_6D108_EXPECTED_RELEVANCE_BY_FACTORY
    )
  }

  assert expected_changed

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

      factory_name = (
        _inference_rule_factory_name(
          before_entry.rule
        )
      )

      assert (
        before_entry.relevance_category
        is RuleRelevanceCategory.UNCLASSIFIED
      )

      assert (
        factory_name
        in PHASE103_6D108_EXPECTED_RELEVANCE_BY_FACTORY
      )

      assert (
        after_entry.relevance_category
        is PHASE103_6D108_EXPECTED_RELEVANCE_BY_FACTORY[
          factory_name
        ]
      )

  assert (
    actual_changed
    == expected_changed
  )


def test_phase103_6d108_all_target_clusters_are_closed():
  catalog = _build_catalog()
  by_factory = _entries_by_factory(
    catalog
  )

  for factory_name, expected_category in (
    PHASE103_6D108_EXPECTED_RELEVANCE_BY_FACTORY.items()
  ):
    entries = by_factory[
      factory_name
    ]

    assert entries

    assert all(
      entry.relevance_category
      is expected_category
      for entry in entries
    )

    assert all(
      entry.relevance_category
      is not RuleRelevanceCategory.UNCLASSIFIED
      for entry in entries
    )


def test_phase103_6d108_family_coverage_changes_by_exactly_eight_families():
  before = (
    _phase103_6d108_original_builder()
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
      before_families
    )
    == 150
  )

  assert (
    classified_count(
      after_families
    )
    == 158
  )


def test_phase103_6d108_entry_category_deltas_match_changed_target_entries():
  before = (
    _phase103_6d108_original_builder()
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

  assert len(
    before_entries
  ) == 1188

  assert len(
    after_entries
  ) == 1188

  before_counts = Counter(
    entry.relevance_category
    for entry in before_entries
  )
  after_counts = Counter(
    entry.relevance_category
    for entry in after_entries
  )

  assert (
    before_counts[
      RuleRelevanceCategory.UNCLASSIFIED
    ]
    == 325
  )

  assert (
    before_counts[
      RuleRelevanceCategory.THEOREM_SPECIFIC
    ]
    == 416
  )

  assert (
    before_counts[
      RuleRelevanceCategory.MAP_PROPERTY
    ]
    == 49
  )

  assert (
    before_counts[
      RuleRelevanceCategory.BRIDGE
    ]
    == 134
  )

  changed_by_category = Counter()

  before_by_key = {
    entry.key: entry
    for entry in before_entries
  }
  after_by_key = {
    entry.key: entry
    for entry in after_entries
  }

  for key, before_entry in before_by_key.items():
    after_entry = after_by_key[
      key
    ]

    if (
      before_entry.relevance_category
      is after_entry.relevance_category
    ):
      continue

    changed_by_category[
      after_entry.relevance_category
    ] += 1

  total_changed = sum(
    changed_by_category.values()
  )

  assert total_changed > 0

  assert (
    after_counts[
      RuleRelevanceCategory.UNCLASSIFIED
    ]
    == before_counts[
      RuleRelevanceCategory.UNCLASSIFIED
    ] - total_changed
  )

  for category in (
    RuleRelevanceCategory.THEOREM_SPECIFIC,
    RuleRelevanceCategory.MAP_PROPERTY,
    RuleRelevanceCategory.BRIDGE,
  ):
    assert (
      after_counts[
        category
      ]
      == before_counts[
        category
      ] + changed_by_category[
        category
      ]
    )


def test_phase103_6d108_preserves_structural_and_generic_relation_counts():
  catalog = _build_catalog()

  counts = Counter(
    entry.relevance_category
    for entry in catalog.entries()
  )

  assert (
    counts[
      RuleRelevanceCategory.STRUCTURAL
    ]
    == 201
  )

  assert (
    counts[
      RuleRelevanceCategory.GENERIC_RELATION
    ]
    == 63
  )


def test_phase103_6d108_catalog_size_and_fixed_point_safety_are_unchanged():
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
