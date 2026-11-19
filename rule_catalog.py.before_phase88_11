from dataclasses import dataclass

from proof import (
  InferenceRule,
  PremisePattern,
)


@dataclass(frozen=True)
class InferenceRuleCatalogEntry:
  key: str
  rule: InferenceRule
  conclusion_type: type
  fixed_point_safe: bool = False
  goal_compatibility: object = None

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.key,
      str,
    ):
      raise TypeError(
        "key must be a str"
      )

    if not self.key:
      raise ValueError(
        "key must not be empty"
      )

    if not isinstance(
      self.rule,
      InferenceRule,
    ):
      raise TypeError(
        "rule must be an InferenceRule"
      )

    if not isinstance(
      self.conclusion_type,
      type,
    ):
      raise TypeError(
        "conclusion_type must be a type"
      )

    if not isinstance(
      self.fixed_point_safe,
      bool,
    ):
      raise TypeError(
        "fixed_point_safe must be a bool"
      )

    if (
      self.goal_compatibility
      is not None
      and not callable(
        self.goal_compatibility
      )
    ):
      raise TypeError(
        "goal_compatibility must be "
        "callable or None"
      )


class InferenceRuleCatalog:
  def __init__(
    self,
  ) -> None:
    self._entries: dict[
      str,
      InferenceRuleCatalogEntry,
    ] = {}

  def register(
    self,
    entry: InferenceRuleCatalogEntry,
  ) -> None:
    if not isinstance(
      entry,
      InferenceRuleCatalogEntry,
    ):
      raise TypeError(
        "entry must be an "
        "InferenceRuleCatalogEntry"
      )

    if entry.key in self._entries:
      raise ValueError(
        f"duplicate rule catalog key: {entry.key}"
      )

    self._entries[
      entry.key
    ] = entry

  def get(
    self,
    key: str,
  ) -> InferenceRuleCatalogEntry:
    return self._entries[
      key
    ]

  def entries(
    self,
  ) -> tuple[
    InferenceRuleCatalogEntry,
    ...,
  ]:
    return tuple(
      self._entries.values()
    )

  def rules(
    self,
  ) -> tuple[
    InferenceRule,
    ...,
  ]:
    return tuple(
      entry.rule
      for entry in self._entries.values()
    )


def _entry_accepts_goal(
  entry,
  goal,
):
  if (
    entry.goal_compatibility
    is None
  ):
    return True

  result = (
    entry.goal_compatibility(
      goal
    )
  )

  if not isinstance(
    result,
    bool,
  ):
    raise TypeError(
      "goal_compatibility must "
      "return a bool"
    )

  return result


def find_goal_compatible_rule_entries(
  catalog,
  goal,
):
  if not isinstance(
    catalog,
    InferenceRuleCatalog,
  ):
    raise TypeError(
      "catalog must be an "
      "InferenceRuleCatalog"
    )

  goal_type = type(
    goal
  )

  return tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.fixed_point_safe
      and entry.conclusion_type
      is goal_type
      and _entry_accepts_goal(
        entry,
        goal,
      )
    )
  )


def find_goal_compatible_rules(
  catalog,
  goal,
):
  entries = (
    find_goal_compatible_rule_entries(
      catalog,
      goal,
    )
  )

  rules = []
  seen_rule_ids = set()

  for entry in entries:
    rule_id = id(
      entry.rule
    )

    if rule_id in seen_rule_ids:
      continue

    seen_rule_ids.add(
      rule_id
    )

    rules.append(
      entry.rule
    )

  return tuple(
    rules
  )


def find_premise_producer_rule_entries(
  catalog,
  premise_pattern,
):
  return tuple(
    entry
    for entry
    in find_premise_producer_candidate_entries(
      catalog,
      premise_pattern,
    )
    if entry.fixed_point_safe
  )


def find_premise_producer_candidate_entries(
  catalog,
  premise_pattern,
):
  if not isinstance(
    catalog,
    InferenceRuleCatalog,
  ):
    raise TypeError(
      "catalog must be an "
      "InferenceRuleCatalog"
    )

  if not isinstance(
    premise_pattern,
    PremisePattern,
  ):
    raise TypeError(
      "premise_pattern must be a "
      "PremisePattern"
    )

  return tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.conclusion_type
      is premise_pattern.statement_type
    )
  )


def find_premise_producer_rules(
  catalog,
  premise_pattern,
):
  entries = (
    find_premise_producer_rule_entries(
      catalog,
      premise_pattern,
    )
  )

  rules = []
  seen_rule_ids = set()

  for entry in entries:
    rule_id = id(
      entry.rule
    )

    if rule_id in seen_rule_ids:
      continue

    seen_rule_ids.add(
      rule_id
    )

    rules.append(
      entry.rule
    )

  return tuple(
    rules
  )
