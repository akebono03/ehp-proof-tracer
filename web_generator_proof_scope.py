from dataclasses import dataclass

from toda_conclusion_latex_renderer import render_repository_conclusion_latex
from toda_human_readable_renderer import (
  _render_generator_symbol_latex,
)


@dataclass(frozen=True)
class WebGeneratorProofScopeTodaMembershipView:
  statement_latex: str
  root_key: str
  depth: int
  match_labels: tuple[
    str,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.statement_latex,
      str,
    ):
      raise TypeError(
        "statement_latex must be a str"
      )

    if not self.statement_latex:
      raise ValueError(
        "statement_latex must not be empty"
      )

    if not isinstance(
      self.root_key,
      str,
    ):
      raise TypeError(
        "root_key must be a str"
      )

    if not self.root_key:
      raise ValueError(
        "root_key must not be empty"
      )

    if (
      isinstance(
        self.depth,
        bool,
      )
      or not isinstance(
        self.depth,
        int,
      )
    ):
      raise TypeError(
        "depth must be an int"
      )

    if self.depth < 0:
      raise ValueError(
        "depth must be nonnegative"
      )

    if not isinstance(
      self.match_labels,
      tuple,
    ):
      raise TypeError(
        "match_labels must be a tuple"
      )

    if not self.match_labels:
      raise ValueError(
        "match_labels must not be empty"
      )

    for match_label in self.match_labels:
      if not isinstance(
        match_label,
        str,
      ):
        raise TypeError(
          "match_labels must contain only str values"
        )

      if not match_label:
        raise ValueError(
          "match_labels must not contain empty values"
        )


@dataclass(frozen=True)
class WebGeneratorProofScopeMapRelationView:
  statement_latex: str
  root_key: str
  depth: int

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.statement_latex,
      str,
    ):
      raise TypeError(
        "statement_latex must be a str"
      )

    if not self.statement_latex:
      raise ValueError(
        "statement_latex must not be empty"
      )

    if not isinstance(
      self.root_key,
      str,
    ):
      raise TypeError(
        "root_key must be a str"
      )

    if not self.root_key:
      raise ValueError(
        "root_key must not be empty"
      )

    if (
      isinstance(
        self.depth,
        bool,
      )
      or not isinstance(
        self.depth,
        int,
      )
    ):
      raise TypeError(
        "depth must be an int"
      )

    if self.depth < 0:
      raise ValueError(
        "depth must be nonnegative"
      )


@dataclass(frozen=True)
class WebGeneratorProofScopeView:
  generator_input: str
  generator_latex: str
  occurrence_count: int
  toda_membership_count: int
  map_relation_count: int
  toda_memberships: tuple[
    WebGeneratorProofScopeTodaMembershipView,
    ...,
  ]
  map_relations: tuple[
    WebGeneratorProofScopeMapRelationView,
    ...,
  ]

  search_status: str = "not_searched"
  diagnostics: tuple[str, ...] = ()
  open_goal_count: int = 0

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.generator_input,
      str,
    ):
      raise TypeError(
        "generator_input must be a str"
      )

    if not self.generator_input:
      raise ValueError(
        "generator_input must not be empty"
      )

    if not isinstance(
      self.generator_latex,
      str,
    ):
      raise TypeError(
        "generator_latex must be a str"
      )

    if not self.generator_latex:
      raise ValueError(
        "generator_latex must not be empty"
      )

    count_fields = (
      (
        "occurrence_count",
        self.occurrence_count,
      ),
      (
        "toda_membership_count",
        self.toda_membership_count,
      ),
      (
        "map_relation_count",
        self.map_relation_count,
      ),
    )

    for name, value in count_fields:
      if (
        isinstance(
          value,
          bool,
        )
        or not isinstance(
          value,
          int,
        )
      ):
        raise TypeError(
          f"{name} must be an int"
        )

      if value < 0:
        raise ValueError(
          f"{name} must be nonnegative"
        )

    if not isinstance(
      self.toda_memberships,
      tuple,
    ):
      raise TypeError(
        "toda_memberships must be a tuple"
      )

    for membership in self.toda_memberships:
      if not isinstance(
        membership,
        WebGeneratorProofScopeTodaMembershipView,
      ):
        raise TypeError(
          "toda_memberships must contain only "
          "WebGeneratorProofScopeTodaMembershipView values"
        )

    if not isinstance(
      self.map_relations,
      tuple,
    ):
      raise TypeError(
        "map_relations must be a tuple"
      )

    for map_relation in self.map_relations:
      if not isinstance(
        map_relation,
        WebGeneratorProofScopeMapRelationView,
      ):
        raise TypeError(
          "map_relations must contain only "
          "WebGeneratorProofScopeMapRelationView values"
        )

    if (
      self.toda_membership_count
      != len(
        self.toda_memberships
      )
    ):
      raise ValueError(
        "toda_membership_count must match toda_memberships"
      )

    if (
      self.map_relation_count
      != len(
        self.map_relations
      )
    ):
      raise ValueError(
        "map_relation_count must match map_relations"
      )








def build_standard_web_generator_proof_scope_view(generator_input: str) -> WebGeneratorProofScopeView:
  if not isinstance(generator_input, str):
    raise TypeError("generator_input must be a str")
  generator_input = generator_input.strip()
  if not generator_input:
    raise ValueError("generator is required")
  from generator_input import resolve_generator_input
  from phase165_r27_r34_typed_lookup import search_typed_generator_statements
  symbol = resolve_generator_input(generator_input)
  result = search_typed_generator_statements(generator_input)
  return WebGeneratorProofScopeView(
    generator_input=generator_input,
    generator_latex=_render_generator_symbol_latex(symbol),
    occurrence_count=len(result.proven_steps),
    toda_membership_count=0,
    map_relation_count=0,
    toda_memberships=(),
    map_relations=(),
    search_status=result.status.value,
    diagnostics=result.diagnostics,
    open_goal_count=len(result.open_goals),
  )
