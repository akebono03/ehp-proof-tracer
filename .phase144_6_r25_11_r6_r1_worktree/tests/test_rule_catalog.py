from dataclasses import dataclass

import pytest

from proof import InferenceRule
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
  find_goal_compatible_rule_entries,
  find_goal_compatible_rules,
)


@dataclass(frozen=True)
class ExampleStatement:
  value: str


@dataclass(frozen=True)
class OtherStatement:
  value: str


def make_rule(
  name="example rule",
):
  return InferenceRule(
    name=name,
  )


def test_rule_catalog_entry_accepts_minimum_valid_data():
  rule = make_rule()

  entry = InferenceRuleCatalogEntry(
    key="phase81.example",
    rule=rule,
    conclusion_type=ExampleStatement,
  )

  assert (
    entry.key
    == "phase81.example"
  )

  assert (
    entry.rule
    is rule
  )

  assert (
    entry.conclusion_type
    is ExampleStatement
  )

  assert (
    entry.fixed_point_safe
    is False
  )


def test_rule_catalog_entry_accepts_fixed_point_safe_true():
  rule = make_rule()

  entry = InferenceRuleCatalogEntry(
    key="phase81.safe",
    rule=rule,
    conclusion_type=ExampleStatement,
    fixed_point_safe=True,
  )

  assert (
    entry.fixed_point_safe
    is True
  )


def test_rule_catalog_entry_rejects_empty_key():
  rule = make_rule()

  with pytest.raises(
    ValueError,
    match="key must not be empty",
  ):
    InferenceRuleCatalogEntry(
      key="",
      rule=rule,
      conclusion_type=ExampleStatement,
    )


def test_rule_catalog_entry_rejects_non_string_key():
  rule = make_rule()

  with pytest.raises(
    TypeError,
    match="key must be a str",
  ):
    InferenceRuleCatalogEntry(
      key=81,
      rule=rule,
      conclusion_type=ExampleStatement,
    )


def test_rule_catalog_entry_rejects_non_inference_rule():
  with pytest.raises(
    TypeError,
    match="rule must be an InferenceRule",
  ):
    InferenceRuleCatalogEntry(
      key="phase81.invalid",
      rule="not-a-rule",
      conclusion_type=ExampleStatement,
    )


def test_rule_catalog_entry_rejects_non_type_conclusion_type():
  rule = make_rule()

  with pytest.raises(
    TypeError,
    match="conclusion_type must be a type",
  ):
    InferenceRuleCatalogEntry(
      key="phase81.invalid",
      rule=rule,
      conclusion_type=ExampleStatement(
        value="not-a-type",
      ),
    )


def test_rule_catalog_entry_rejects_non_bool_fixed_point_safe():
  rule = make_rule()

  with pytest.raises(
    TypeError,
    match="fixed_point_safe must be a bool",
  ):
    InferenceRuleCatalogEntry(
      key="phase81.invalid",
      rule=rule,
      conclusion_type=ExampleStatement,
      fixed_point_safe=1,
    )


def test_rule_catalog_register_and_get_preserve_identity():
  catalog = InferenceRuleCatalog()
  rule = make_rule()

  entry = InferenceRuleCatalogEntry(
    key="phase81.example",
    rule=rule,
    conclusion_type=ExampleStatement,
    fixed_point_safe=True,
  )

  catalog.register(
    entry
  )

  found = catalog.get(
    "phase81.example"
  )

  assert (
    found
    is entry
  )

  assert (
    found.rule
    is rule
  )


def test_rule_catalog_get_raises_key_error_for_missing_key():
  catalog = InferenceRuleCatalog()

  with pytest.raises(
    KeyError,
  ):
    catalog.get(
      "missing"
    )


def test_rule_catalog_register_rejects_non_entry():
  catalog = InferenceRuleCatalog()

  with pytest.raises(
    TypeError,
    match=(
      "entry must be an "
      "InferenceRuleCatalogEntry"
    ),
  ):
    catalog.register(
      "not-an-entry"
    )


def test_rule_catalog_register_rejects_duplicate_key():
  catalog = InferenceRuleCatalog()

  first_entry = InferenceRuleCatalogEntry(
    key="phase81.same",
    rule=make_rule(
      "first rule"
    ),
    conclusion_type=ExampleStatement,
  )

  second_entry = InferenceRuleCatalogEntry(
    key="phase81.same",
    rule=make_rule(
      "second rule"
    ),
    conclusion_type=OtherStatement,
  )

  catalog.register(
    first_entry
  )

  with pytest.raises(
    ValueError,
    match="duplicate rule catalog key",
  ):
    catalog.register(
      second_entry
    )


def test_rule_catalog_entries_preserve_registration_order():
  catalog = InferenceRuleCatalog()

  first_entry = InferenceRuleCatalogEntry(
    key="phase81.first",
    rule=make_rule(
      "first rule"
    ),
    conclusion_type=ExampleStatement,
  )

  second_entry = InferenceRuleCatalogEntry(
    key="phase81.second",
    rule=make_rule(
      "second rule"
    ),
    conclusion_type=OtherStatement,
  )

  catalog.register(
    first_entry
  )

  catalog.register(
    second_entry
  )

  assert (
    catalog.entries()
    == (
      first_entry,
      second_entry,
    )
  )


def test_rule_catalog_rules_preserve_registration_order_and_identity():
  catalog = InferenceRuleCatalog()

  first_rule = make_rule(
    "first rule"
  )

  second_rule = make_rule(
    "second rule"
  )

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.first",
      rule=first_rule,
      conclusion_type=ExampleStatement,
    )
  )

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.second",
      rule=second_rule,
      conclusion_type=OtherStatement,
    )
  )

  rules = catalog.rules()

  assert (
    rules
    == (
      first_rule,
      second_rule,
    )
  )

  assert (
    rules[0]
    is first_rule
  )

  assert (
    rules[1]
    is second_rule
  )


def test_rule_catalog_allows_same_rule_with_different_keys():
  catalog = InferenceRuleCatalog()

  rule = make_rule()

  first_entry = InferenceRuleCatalogEntry(
    key="phase81.first",
    rule=rule,
    conclusion_type=ExampleStatement,
  )

  second_entry = InferenceRuleCatalogEntry(
    key="phase81.alias",
    rule=rule,
    conclusion_type=ExampleStatement,
  )

  catalog.register(
    first_entry
  )

  catalog.register(
    second_entry
  )

  assert (
    catalog.entries()
    == (
      first_entry,
      second_entry,
    )
  )

  assert (
    catalog.rules()
    == (
      rule,
      rule,
    )
  )

  assert (
    catalog.rules()[0]
    is rule
  )

  assert (
    catalog.rules()[1]
    is rule
  )


def test_find_goal_compatible_rule_entries_selects_safe_exact_type():
  catalog = InferenceRuleCatalog()

  compatible_entry = InferenceRuleCatalogEntry(
    key="phase81.compatible",
    rule=make_rule(
      "compatible rule"
    ),
    conclusion_type=ExampleStatement,
    fixed_point_safe=True,
  )

  unrelated_entry = InferenceRuleCatalogEntry(
    key="phase81.unrelated",
    rule=make_rule(
      "unrelated rule"
    ),
    conclusion_type=OtherStatement,
    fixed_point_safe=True,
  )

  catalog.register(
    compatible_entry
  )

  catalog.register(
    unrelated_entry
  )

  goal = ExampleStatement(
    value="goal"
  )

  assert (
    find_goal_compatible_rule_entries(
      catalog,
      goal,
    )
    == (
      compatible_entry,
    )
  )


def test_find_goal_compatible_rule_entries_excludes_unsafe_rule():
  catalog = InferenceRuleCatalog()

  unsafe_entry = InferenceRuleCatalogEntry(
    key="phase81.unsafe",
    rule=make_rule(
      "unsafe rule"
    ),
    conclusion_type=ExampleStatement,
    fixed_point_safe=False,
  )

  catalog.register(
    unsafe_entry
  )

  goal = ExampleStatement(
    value="goal"
  )

  assert (
    find_goal_compatible_rule_entries(
      catalog,
      goal,
    )
    == ()
  )


def test_find_goal_compatible_rule_entries_requires_exact_conclusion_type():
  @dataclass(frozen=True)
  class DerivedExampleStatement(
    ExampleStatement
  ):
    pass

  catalog = InferenceRuleCatalog()

  entry = InferenceRuleCatalogEntry(
    key="phase81.base",
    rule=make_rule(
      "base rule"
    ),
    conclusion_type=ExampleStatement,
    fixed_point_safe=True,
  )

  catalog.register(
    entry
  )

  goal = DerivedExampleStatement(
    value="goal"
  )

  assert (
    find_goal_compatible_rule_entries(
      catalog,
      goal,
    )
    == ()
  )


def test_find_goal_compatible_rule_entries_preserves_registration_order():
  catalog = InferenceRuleCatalog()

  first_entry = InferenceRuleCatalogEntry(
    key="phase81.first",
    rule=make_rule(
      "first compatible rule"
    ),
    conclusion_type=ExampleStatement,
    fixed_point_safe=True,
  )

  second_entry = InferenceRuleCatalogEntry(
    key="phase81.second",
    rule=make_rule(
      "second compatible rule"
    ),
    conclusion_type=ExampleStatement,
    fixed_point_safe=True,
  )

  catalog.register(
    first_entry
  )

  catalog.register(
    second_entry
  )

  goal = ExampleStatement(
    value="goal"
  )

  assert (
    find_goal_compatible_rule_entries(
      catalog,
      goal,
    )
    == (
      first_entry,
      second_entry,
    )
  )


def test_find_goal_compatible_rule_entries_preserves_rule_alias_entries():
  catalog = InferenceRuleCatalog()

  rule = make_rule(
    "shared rule"
  )

  first_entry = InferenceRuleCatalogEntry(
    key="phase81.first",
    rule=rule,
    conclusion_type=ExampleStatement,
    fixed_point_safe=True,
  )

  second_entry = InferenceRuleCatalogEntry(
    key="phase81.alias",
    rule=rule,
    conclusion_type=ExampleStatement,
    fixed_point_safe=True,
  )

  catalog.register(
    first_entry
  )

  catalog.register(
    second_entry
  )

  goal = ExampleStatement(
    value="goal"
  )

  assert (
    find_goal_compatible_rule_entries(
      catalog,
      goal,
    )
    == (
      first_entry,
      second_entry,
    )
  )


def test_find_goal_compatible_rules_returns_rule_objects():
  catalog = InferenceRuleCatalog()

  first_rule = make_rule(
    "first compatible rule"
  )

  second_rule = make_rule(
    "second compatible rule"
  )

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.first",
      rule=first_rule,
      conclusion_type=ExampleStatement,
      fixed_point_safe=True,
    )
  )

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.second",
      rule=second_rule,
      conclusion_type=ExampleStatement,
      fixed_point_safe=True,
    )
  )

  goal = ExampleStatement(
    value="goal"
  )

  rules = find_goal_compatible_rules(
    catalog,
    goal,
  )

  assert (
    rules
    == (
      first_rule,
      second_rule,
    )
  )

  assert (
    rules[0]
    is first_rule
  )

  assert (
    rules[1]
    is second_rule
  )


def test_find_goal_compatible_rules_deduplicates_rule_alias_by_identity():
  catalog = InferenceRuleCatalog()

  rule = make_rule(
    "shared rule"
  )

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.first",
      rule=rule,
      conclusion_type=ExampleStatement,
      fixed_point_safe=True,
    )
  )

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.alias",
      rule=rule,
      conclusion_type=ExampleStatement,
      fixed_point_safe=True,
    )
  )

  goal = ExampleStatement(
    value="goal"
  )

  rules = find_goal_compatible_rules(
    catalog,
    goal,
  )

  assert (
    rules
    == (
      rule,
    )
  )

  assert (
    rules[0]
    is rule
  )


def test_find_goal_compatible_rule_entries_rejects_non_catalog():
  goal = ExampleStatement(
    value="goal"
  )

  with pytest.raises(
    TypeError,
    match=(
      "catalog must be an "
      "InferenceRuleCatalog"
    ),
  ):
    find_goal_compatible_rule_entries(
      "not-a-catalog",
      goal,
    )


def test_find_goal_compatible_rules_returns_empty_when_no_candidate_exists():
  catalog = InferenceRuleCatalog()

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.unrelated",
      rule=make_rule(
        "unrelated rule"
      ),
      conclusion_type=OtherStatement,
      fixed_point_safe=True,
    )
  )

  goal = ExampleStatement(
    value="goal"
  )

  assert (
    find_goal_compatible_rules(
      catalog,
      goal,
    )
    == ()
  )



