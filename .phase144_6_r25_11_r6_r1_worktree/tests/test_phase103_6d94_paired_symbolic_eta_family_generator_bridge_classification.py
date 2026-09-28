from collections import (
  Counter,
  defaultdict,
)

from rule_catalog import (
  RuleRelevanceCategory,
)
from standard_production_applicability_catalog import (
  _inference_rule_factory_name,
  _phase103_6d94_apply_bridge_classification,
  _phase103_6d94_original_builder,
)


PHASE103_6D94_TARGET_FACTORIES = frozenset(
  (
    "toda_prop53_higher_eta_squared_finite_cyclic_generator_inference_rule",
    "toda_higher_eta_finite_cyclic_generator_inference_rule",
  )
)

PHASE103_6D94_TARGET_FAMILIES = frozenset(
  (
    "Toda Proposition 5.3 higher eta-squared finite-cyclic generator bridge",
    "Toda higher eta-family finite-cyclic generator bridge",
  )
)


def _build_catalog():
  return (
    _phase103_6d94_apply_bridge_classification(
      _phase103_6d94_original_builder()
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


def test_phase103_6d94_classifies_both_symbolic_eta_generator_bridge_families_as_bridge():
  catalog = _build_catalog()
  families = _families(
    catalog
  )

  for family_name in (
    PHASE103_6D94_TARGET_FAMILIES
  ):
    assert family_name in families

    entries = families[
      family_name
    ]

    assert len(
      entries
    ) == 7

    assert all(
      entry.relevance_category
      is RuleRelevanceCategory.BRIDGE
      for entry in entries
    )


def test_phase103_6d94_target_factories_are_exactly_the_audited_pair():
  catalog = _build_catalog()

  entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      _inference_rule_factory_name(
        entry.rule
      )
      in PHASE103_6D94_TARGET_FACTORIES
    )
  )

  assert len(
    entries
  ) == 14

  assert {
    _inference_rule_factory_name(
      entry.rule
    )
    for entry in entries
  } == PHASE103_6D94_TARGET_FACTORIES


def test_phase103_6d94_changes_only_the_two_target_factories():
  before = (
    _phase103_6d94_original_builder()
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
      in PHASE103_6D94_TARGET_FACTORIES
    )
  }

  assert len(
    expected_changed
  ) == 14

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
        is RuleRelevanceCategory.BRIDGE
      )

  assert actual_changed == expected_changed


def test_phase103_6d94_both_target_clusters_are_closed():
  catalog = _build_catalog()

  for factory_name in (
    PHASE103_6D94_TARGET_FACTORIES
  ):
    entries = tuple(
      entry
      for entry in catalog.entries()
      if (
        _inference_rule_factory_name(
          entry.rule
        )
        == factory_name
      )
    )

    assert len(
      entries
    ) == 7

    assert all(
      entry.relevance_category
      is RuleRelevanceCategory.BRIDGE
      for entry in entries
    )


def test_phase103_6d94_family_coverage_changes_by_exactly_two_families():
  before = (
    _phase103_6d94_original_builder()
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
    == 145
  )

  assert (
    classified_count(
      after_families
    )
    == 147
  )


def test_phase103_6d94_entry_coverage_delta_matches_fourteen_target_entries():
  before = (
    _phase103_6d94_original_builder()
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
    ] - 14
  )

  assert (
    after_counts[
      RuleRelevanceCategory.BRIDGE
    ]
    == before_counts[
      RuleRelevanceCategory.BRIDGE
    ] + 14
  )

  assert (
    after_counts[
      RuleRelevanceCategory.UNCLASSIFIED
    ]
    == 350
  )

  assert (
    after_counts[
      RuleRelevanceCategory.BRIDGE
    ]
    == 134
  )


def test_phase103_6d94_preserves_theorem_specific_count():
  catalog = _build_catalog()

  counts = Counter(
    entry.relevance_category
    for entry in catalog.entries()
  )

  assert (
    counts[
      RuleRelevanceCategory.THEOREM_SPECIFIC
    ]
    == 391
  )


def test_phase103_6d94_preserves_structural_map_property_and_generic_relation_counts():
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
      RuleRelevanceCategory.MAP_PROPERTY
    ]
    == 49
  )

  assert (
    counts[
      RuleRelevanceCategory.GENERIC_RELATION
    ]
    == 63
  )


def test_phase103_6d94_catalog_size_and_fixed_point_safety_are_unchanged():
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
