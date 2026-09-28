from dataclasses import dataclass

import pytest

from proof import InferenceRule
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
  RuleRelevanceCategory,
  find_goal_compatible_rule_entries,
)


@dataclass(frozen=True)
class Phase103RelevanceStatement:
  value: str


def make_phase103_rule(
  name="phase103 relevance rule",
):
  return InferenceRule(
    name=name,
  )


def test_phase103_6d2_relevance_category_defaults_to_unclassified():
  entry = InferenceRuleCatalogEntry(
    key="phase103.6d2.default",
    rule=make_phase103_rule(),
    conclusion_type=(
      Phase103RelevanceStatement
    ),
  )

  assert (
    entry.relevance_category
    is RuleRelevanceCategory.UNCLASSIFIED
  )


@pytest.mark.parametrize(
  "category",
  tuple(
    RuleRelevanceCategory
  ),
)
def test_phase103_6d2_relevance_category_accepts_all_explicit_categories(
  category,
):
  entry = InferenceRuleCatalogEntry(
    key=(
      "phase103.6d2."
      f"{category.value}"
    ),
    rule=make_phase103_rule(
      category.value
    ),
    conclusion_type=(
      Phase103RelevanceStatement
    ),
    relevance_category=category,
  )

  assert (
    entry.relevance_category
    is category
  )


def test_phase103_6d2_relevance_category_rejects_non_category():
  with pytest.raises(
    TypeError,
    match=(
      "relevance_category must be a "
      "RuleRelevanceCategory"
    ),
  ):
    InferenceRuleCatalogEntry(
      key="phase103.6d2.invalid",
      rule=make_phase103_rule(),
      conclusion_type=(
        Phase103RelevanceStatement
      ),
      relevance_category=(
        "theorem_specific"
      ),
    )


def test_phase103_6d2_relevance_category_does_not_change_goal_lookup():
  catalog = InferenceRuleCatalog()

  first_entry = (
    InferenceRuleCatalogEntry(
      key="phase103.6d2.first",
      rule=make_phase103_rule(
        "first rule"
      ),
      conclusion_type=(
        Phase103RelevanceStatement
      ),
      fixed_point_safe=True,
      relevance_category=(
        RuleRelevanceCategory
        .GENERIC_RELATION
      ),
    )
  )

  second_entry = (
    InferenceRuleCatalogEntry(
      key="phase103.6d2.second",
      rule=make_phase103_rule(
        "second rule"
      ),
      conclusion_type=(
        Phase103RelevanceStatement
      ),
      fixed_point_safe=True,
      relevance_category=(
        RuleRelevanceCategory
        .THEOREM_SPECIFIC
      ),
    )
  )

  catalog.register(
    first_entry
  )
  catalog.register(
    second_entry
  )

  goal = (
    Phase103RelevanceStatement(
      value="goal"
    )
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
