from __future__ import annotations

from collections import Counter, defaultdict
import inspect

import standard_production_applicability_catalog as production_catalog
from rule_catalog import RuleRelevanceCategory


TARGET_SHAPE = (
  ("TodaSuspensionIsomorphismStatement",),
  (
    "TodaProp44IsomorphismStatement",
    "TodaPrimaryGroupZeroStatement",
  ),
  True,
  False,
  True,
)

TARGET_FAMILY = (
  "Toda Proposition 5.11 pi_14^8 Proposition 4.4 "
  "zero-second-summand suspension isomorphism"
)


def _required_parameter_count(
  fn,
) -> int:
  signature = inspect.signature(
    fn
  )

  return sum(
    1
    for parameter in signature.parameters.values()
    if (
      parameter.kind
      not in (
        inspect.Parameter.VAR_POSITIONAL,
        inspect.Parameter.VAR_KEYWORD,
      )
      and parameter.default
      is inspect.Parameter.empty
    )
  )


def _build_catalog():
  preferred_names = (
    "build_standard_production_applicability_catalog",
    "standard_production_applicability_catalog",
    "build_standard_production_rule_catalog",
    "build_standard_production_catalog",
  )

  for name in preferred_names:
    candidate = getattr(
      production_catalog,
      name,
      None,
    )

    if (
      callable(candidate)
      and _required_parameter_count(candidate) == 0
    ):
      value = candidate()

      if hasattr(
        value,
        "entries",
      ):
        return value

  raise AssertionError(
    "standard production catalog builder not found"
  )


def _type_names(
  value,
) -> tuple[str, ...]:
  if value is None:
    return ()

  values = (
    value
    if isinstance(
      value,
      tuple,
    )
    else (
      value,
    )
  )

  result = []

  for item in values:
    if item is None:
      continue

    if isinstance(
      item,
      type,
    ):
      result.append(
        item.__name__
      )
    else:
      result.append(
        type(
          item
        ).__name__
      )

  return tuple(
    result
  )


def _premise_signature(
  rule,
) -> tuple[str, ...]:
  names = []

  for pattern in getattr(
    rule,
    "premise_patterns",
    (),
  ):
    statement_type = getattr(
      pattern,
      "statement_type",
      None,
    )

    if statement_type is not None:
      names.extend(
        _type_names(
          statement_type
        )
      )
      continue

    statement_pattern = getattr(
      pattern,
      "statement_pattern",
      None,
    )

    if statement_pattern is not None:
      names.extend(
        _type_names(
          statement_pattern
        )
      )

  return tuple(
    names
  )


def _shape(
  entry,
):
  rule = entry.rule

  return (
    _type_names(
      entry.conclusion_type
    ),
    _premise_signature(
      rule
    ),
    (
      getattr(
        rule,
        "conclusion_builder",
        None,
      )
      is not None
    ),
    (
      getattr(
        rule,
        "conclusion_pattern",
        None,
      )
      is not None
    ),
    (
      getattr(
        rule,
        "match_guard",
        None,
      )
      is not None
    ),
  )


def _family_groups(
  entries,
):
  grouped = defaultdict(
    list
  )

  for entry in entries:
    family = str(
      getattr(
        entry.rule,
        "name",
        entry.key,
      )
    )

    grouped[
      family
    ].append(
      entry
    )

  return grouped


def test_phase103_6d20_target_route_is_structural():
  catalog = _build_catalog()

  matching = tuple(
    entry
    for entry in catalog.entries()
    if _shape(
      entry
    )
    == TARGET_SHAPE
  )

  assert len(
    matching
  ) == 1

  assert (
    matching[
      0
    ].rule.name
    == TARGET_FAMILY
  )

  assert (
    matching[
      0
    ].relevance_category
    is RuleRelevanceCategory.STRUCTURAL
  )


def test_phase103_6d20_promotes_only_the_audited_route():
  catalog = _build_catalog()

  original_builder = getattr(
    production_catalog,
    "_phase103_6d20_original_builder",
  )

  baseline = original_builder()

  before = {
    entry.key: entry
    for entry in baseline.entries()
  }

  after = {
    entry.key: entry
    for entry in catalog.entries()
  }

  assert before.keys() == after.keys()

  changed = []

  for key, before_entry in before.items():
    after_entry = after[
      key
    ]

    if _shape(
      before_entry
    ) == TARGET_SHAPE:
      assert (
        before_entry.relevance_category
        is RuleRelevanceCategory.UNCLASSIFIED
      )
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
  ) == 1


def test_phase103_6d20_closes_suspension_isomorphism_relevance():
  catalog = _build_catalog()

  matching = tuple(
    entry
    for entry in catalog.entries()
    if _type_names(
      entry.conclusion_type
    )
    == (
      "TodaSuspensionIsomorphismStatement",
    )
  )

  assert len(
    matching
  ) == 17

  category_counts = Counter(
    entry.relevance_category
    for entry in matching
  )

  assert (
    category_counts[
      RuleRelevanceCategory.MAP_PROPERTY
    ]
    == 16
  )

  assert (
    category_counts[
      RuleRelevanceCategory.STRUCTURAL
    ]
    == 1
  )

  assert (
    category_counts[
      RuleRelevanceCategory.UNCLASSIFIED
    ]
    == 0
  )


def test_phase103_6d20_family_coverage_counts():
  catalog = _build_catalog()
  entries = tuple(
    catalog.entries()
  )

  families = _family_groups(
    entries
  )

  categories_by_family = {
    family: {
      entry.relevance_category
      for entry in members
    }
    for family, members
    in families.items()
  }

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
    entries
  ) == 1188

  assert len(
    families
  ) == 267

  assert classified == 91
  assert unclassified == 176


def test_phase103_6d20_entry_coverage_counts():
  catalog = _build_catalog()
  entries = tuple(
    catalog.entries()
  )

  map_property = sum(
    1
    for entry in entries
    if (
      entry.relevance_category
      is RuleRelevanceCategory.MAP_PROPERTY
    )
  )

  structural = sum(
    1
    for entry in entries
    if (
      entry.relevance_category
      is RuleRelevanceCategory.STRUCTURAL
    )
  )

  unclassified = sum(
    1
    for entry in entries
    if (
      entry.relevance_category
      is RuleRelevanceCategory.UNCLASSIFIED
    )
  )

  assert map_property == 47
  assert structural == 184
  assert unclassified == 494
