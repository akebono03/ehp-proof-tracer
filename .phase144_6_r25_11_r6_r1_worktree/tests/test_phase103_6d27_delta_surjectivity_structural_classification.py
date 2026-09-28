from __future__ import annotations

from collections import Counter, defaultdict
import inspect

import standard_production_applicability_catalog as production_catalog
from rule_catalog import RuleRelevanceCategory


TARGET_SHAPES = frozenset(
  (
    (
      ("TodaDeltaSurjectiveStatement",),
      (
        "TodaPrimaryGroupZeroStatement",
        "TodaProp42ExactnessStatement",
      ),
      True,
      False,
      True,
    ),
    (
      ("TodaDeltaSurjectiveStatement",),
      (
        "TodaSuspensionZeroStatement",
        "TodaProp42ExactnessStatement",
      ),
      True,
      False,
      True,
    ),
    (
      ("TodaDeltaSurjectiveStatement",),
      (
        "Relation",
        "Relation",
        "TodaProp42ExactnessStatement",
      ),
      True,
      False,
      True,
    ),
    (
      ("TodaDeltaSurjectiveStatement",),
      (
        "TodaProp511FiniteDimensionalStatement",
        "TodaProp42ExactnessStatement",
      ),
      True,
      False,
      True,
    ),
  )
)

RESIDUAL_SHAPE = (
  ("TodaDeltaSurjectiveStatement",),
  (
    "Relation",
    "Relation",
  ),
  True,
  False,
  True,
)

RESIDUAL_FAMILY = (
  "Toda Proposition 5.9 pi_13^13 Delta surjective"
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
  builder = getattr(
    production_catalog,
    "_phase103_6d30_original_builder",
  )

  value = builder()

  if hasattr(
    value,
    "entries",
  ):
    return value

  raise AssertionError(
    "Phase 103-6D27 catalog builder did not return a catalog"
  )


def _build_phase6d24_catalog():
  builder = getattr(
    production_catalog,
    "_phase103_6d27_original_builder",
  )

  value = builder()

  if hasattr(
    value,
    "entries",
  ):
    return value

  raise AssertionError(
    "Phase 103-6D24 catalog builder did not return a catalog"
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


def test_phase103_6d27_target_routes_are_structural():
  catalog = _build_catalog()

  matching = tuple(
    entry
    for entry in catalog.entries()
    if _shape(
      entry
    )
    in TARGET_SHAPES
  )

  families = _family_groups(
    matching
  )

  assert len(
    matching
  ) == 4

  assert len(
    families
  ) == 4

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.STRUCTURAL
    for entry in matching
  )


def test_phase103_6d27_promotes_only_the_audited_routes():
  catalog = _build_catalog()
  baseline = _build_phase6d24_catalog()

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

    if (
      before_entry.relevance_category
      is RuleRelevanceCategory.UNCLASSIFIED
      and _shape(
        before_entry
      )
      in TARGET_SHAPES
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

  changed_entries = tuple(
    after[
      key
    ]
    for key in changed
  )

  changed_families = _family_groups(
    changed_entries
  )

  assert len(
    changed
  ) == 4

  assert len(
    changed_families
  ) == 4


def test_phase103_6d27_baseline_targets_were_unclassified():
  baseline = _build_phase6d24_catalog()

  matching = tuple(
    entry
    for entry in baseline.entries()
    if _shape(
      entry
    )
    in TARGET_SHAPES
  )

  assert len(
    matching
  ) == 4

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.UNCLASSIFIED
    for entry in matching
  )


def test_phase103_6d27_preserves_generator_image_route_unclassified():
  catalog = _build_catalog()

  matching = tuple(
    entry
    for entry in catalog.entries()
    if _shape(
      entry
    )
    == RESIDUAL_SHAPE
    and entry.rule.name
    == RESIDUAL_FAMILY
  )

  assert len(
    matching
  ) == 1

  assert (
    matching[
      0
    ].relevance_category
    is RuleRelevanceCategory.UNCLASSIFIED
  )


def test_phase103_6d27_delta_surjectivity_boundary():
  catalog = _build_catalog()

  matching = tuple(
    entry
    for entry in catalog.entries()
    if _type_names(
      entry.conclusion_type
    )
    == (
      "TodaDeltaSurjectiveStatement",
    )
  )

  assert len(
    matching
  ) == 5

  category_counts = Counter(
    entry.relevance_category
    for entry in matching
  )

  assert (
    category_counts[
      RuleRelevanceCategory.STRUCTURAL
    ]
    == 4
  )

  assert (
    category_counts[
      RuleRelevanceCategory.UNCLASSIFIED
    ]
    == 1
  )

  residual = tuple(
    entry
    for entry in matching
    if (
      entry.relevance_category
      is RuleRelevanceCategory.UNCLASSIFIED
    )
  )

  assert len(
    residual
  ) == 1

  assert (
    residual[
      0
    ].rule.name
    == RESIDUAL_FAMILY
  )


def test_phase103_6d27_family_coverage_counts():
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

  assert classified == 99
  assert unclassified == 168


def test_phase103_6d27_entry_coverage_counts():
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
  assert structural == 194
  assert unclassified == 484
