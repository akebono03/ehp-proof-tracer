from dataclasses import dataclass

import pytest

from proof import InferenceRule
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
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


