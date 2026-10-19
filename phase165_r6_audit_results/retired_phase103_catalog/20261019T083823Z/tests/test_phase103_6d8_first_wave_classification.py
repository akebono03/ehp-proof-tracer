from collections import defaultdict

from rule_catalog import (
  RuleRelevanceCategory,
)
from standard_production_applicability_catalog import (
  build_standard_production_applicability_catalog,
)


EXPECTED_FIRST_WAVE = {
  (
    "equality preserved under "
    "right composition"
  ): (
    RuleRelevanceCategory
    .GENERIC_RELATION,
    7,
  ),
  (
    "equality preserved under "
    "left composition"
  ): (
    RuleRelevanceCategory
    .GENERIC_RELATION,
    7,
  ),
  "equality preserved under multiple": (
    RuleRelevanceCategory
    .GENERIC_RELATION,
    7,
  ),
  "nested integer multiple": (
    RuleRelevanceCategory
    .GENERIC_RELATION,
    7,
  ),
  (
    "Toda Prop.3.1 Barratt-Hilton "
    "first formula"
  ): (
    RuleRelevanceCategory
    .THEOREM_SPECIFIC,
    3,
  ),
  (
    "Toda Prop.3.1 Barratt-Hilton "
    "second formula"
  ): (
    RuleRelevanceCategory
    .THEOREM_SPECIFIC,
    3,
  ),
}


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


def test_phase103_6d8_first_wave_families_have_explicit_categories():
  catalog = (
    build_standard_production_applicability_catalog()
  )

  families = _families(
    catalog
  )

  for (
    name,
    (
      expected_category,
      expected_entry_count,
    ),
  ) in EXPECTED_FIRST_WAVE.items():
    entries = families[
      name
    ]

    assert len(
      entries
    ) == expected_entry_count

    assert all(
      entry.relevance_category
      is expected_category
      for entry in entries
    )


def test_phase103_6d8_first_wave_classifies_exactly_34_catalog_entries():
  catalog = (
    build_standard_production_applicability_catalog()
  )

  families = _families(
    catalog
  )

  affected_entries = tuple(
    entry
    for name in EXPECTED_FIRST_WAVE
    for entry in families[
      name
    ]
  )

  assert len(
    affected_entries
  ) == 34

  assert all(
    entry.relevance_category
    is not RuleRelevanceCategory.UNCLASSIFIED
    for entry in affected_entries
  )


def test_phase103_6d8_first_wave_families_remain_consistently_classified():
  catalog = (
    build_standard_production_applicability_catalog()
  )

  families = _families(
    catalog
  )

  for (
    name,
    (
      expected_category,
      expected_entry_count,
    ),
  ) in EXPECTED_FIRST_WAVE.items():
    entries = families[
      name
    ]

    assert len(
      entries
    ) == expected_entry_count

    categories = {
      entry.relevance_category
      for entry in entries
    }

    assert categories == {
      expected_category
    }

  assert len(
    families
  ) == 267


def test_phase103_6d8_catalog_entry_count_and_discovery_safety_are_unchanged():
  catalog = (
    build_standard_production_applicability_catalog()
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
