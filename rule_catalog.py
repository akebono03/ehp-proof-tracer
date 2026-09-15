from dataclasses import dataclass

from proof import InferenceRule


@dataclass(frozen=True)
class InferenceRuleCatalogEntry:
  key: str
  rule: InferenceRule
  conclusion_type: type
  fixed_point_safe: bool = False

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


