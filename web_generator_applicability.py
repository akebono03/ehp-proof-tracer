from dataclasses import dataclass

from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from repository_generator_applicability_facade import (
  explore_standard_repository_generator_applicability_input,
)
from repository_generator_applicability_presentation import (
  ApplicabilityRuleFamilyPresentation,
  ApplicabilitySourceGroupPresentation,
  build_repository_generator_applicability_presentation,
)
from toda_human_readable_renderer import (
  _render_generator_symbol_latex,
)


@dataclass(frozen=True)
class WebGeneratorApplicabilityRuleFamilyView:
  name: str
  catalog_entry_count: int
  raw_candidate_count: int

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.name,
      str,
    ):
      raise TypeError(
        "name must be a str"
      )

    if not self.name:
      raise ValueError(
        "name must not be empty"
      )

    for field_name, value in (
      (
        "catalog_entry_count",
        self.catalog_entry_count,
      ),
      (
        "raw_candidate_count",
        self.raw_candidate_count,
      ),
    ):
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
          f"{field_name} must be an int"
        )

      if value < 0:
        raise ValueError(
          f"{field_name} must be nonnegative"
        )


@dataclass(frozen=True)
class WebGeneratorApplicabilitySourceView:
  statement_latex: str | None
  fallback_type_name: str | None
  root_key: str
  depth: int
  source_statement_type: str
  raw_candidate_count: int
  rule_family_count: int
  rule_families: tuple[
    WebGeneratorApplicabilityRuleFamilyView,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if (
      self.statement_latex is not None
      and not isinstance(
        self.statement_latex,
        str,
      )
    ):
      raise TypeError(
        "statement_latex must be a str or None"
      )

    if (
      self.fallback_type_name is not None
      and not isinstance(
        self.fallback_type_name,
        str,
      )
    ):
      raise TypeError(
        "fallback_type_name must be a str or None"
      )

    if (
      self.statement_latex is None
      and self.fallback_type_name is None
    ):
      raise ValueError(
        "source view must have statement_latex "
        "or fallback_type_name"
      )

    if (
      self.statement_latex is not None
      and self.fallback_type_name is not None
    ):
      raise ValueError(
        "source view must not have both "
        "statement_latex and fallback_type_name"
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
      self.source_statement_type,
      str,
    ):
      raise TypeError(
        "source_statement_type must be a str"
      )

    if not self.source_statement_type:
      raise ValueError(
        "source_statement_type must not be empty"
      )

    for field_name, value in (
      (
        "raw_candidate_count",
        self.raw_candidate_count,
      ),
      (
        "rule_family_count",
        self.rule_family_count,
      ),
    ):
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
          f"{field_name} must be an int"
        )

      if value < 0:
        raise ValueError(
          f"{field_name} must be nonnegative"
        )

    if not isinstance(
      self.rule_families,
      tuple,
    ):
      raise TypeError(
        "rule_families must be a tuple"
      )

    for rule_family in self.rule_families:
      if not isinstance(
        rule_family,
        WebGeneratorApplicabilityRuleFamilyView,
      ):
        raise TypeError(
          "rule_families must contain only "
          "WebGeneratorApplicabilityRuleFamilyView values"
        )

    if (
      self.rule_family_count
      != len(
        self.rule_families
      )
    ):
      raise ValueError(
        "rule_family_count must match rule_families"
      )


@dataclass(frozen=True)
class WebGeneratorApplicabilityView:
  generator_input: str
  generator_latex: str
  occurrence_count: int
  candidate_count: int
  source_count: int
  rule_group_count: int
  rule_family_count: int
  toda_memberships: tuple[
    WebGeneratorApplicabilitySourceView,
    ...,
  ]
  map_relations: tuple[
    WebGeneratorApplicabilitySourceView,
    ...,
  ]
  other_sources: tuple[
    WebGeneratorApplicabilitySourceView,
    ...,
  ]

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

    for field_name, value in (
      (
        "occurrence_count",
        self.occurrence_count,
      ),
      (
        "candidate_count",
        self.candidate_count,
      ),
      (
        "source_count",
        self.source_count,
      ),
      (
        "rule_group_count",
        self.rule_group_count,
      ),
      (
        "rule_family_count",
        self.rule_family_count,
      ),
    ):
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
          f"{field_name} must be an int"
        )

      if value < 0:
        raise ValueError(
          f"{field_name} must be nonnegative"
        )

    groups = (
      self.toda_memberships,
      self.map_relations,
      self.other_sources,
    )

    for group in groups:
      if not isinstance(
        group,
        tuple,
      ):
        raise TypeError(
          "source groups must be tuples"
        )

      for source in group:
        if not isinstance(
          source,
          WebGeneratorApplicabilitySourceView,
        ):
          raise TypeError(
            "source groups must contain only "
            "WebGeneratorApplicabilitySourceView values"
          )

    if (
      self.source_count
      != sum(
        len(
          group
        )
        for group in groups
      )
    ):
      raise ValueError(
        "source_count must match grouped sources"
      )


def _build_rule_family_view(
  rule_family: ApplicabilityRuleFamilyPresentation,
) -> WebGeneratorApplicabilityRuleFamilyView:
  if not isinstance(
    rule_family,
    ApplicabilityRuleFamilyPresentation,
  ):
    raise TypeError(
      "rule_family must be an "
      "ApplicabilityRuleFamilyPresentation"
    )

  return WebGeneratorApplicabilityRuleFamilyView(
    name=rule_family.name,
    catalog_entry_count=len(
      rule_family.rule_groups
    ),
    raw_candidate_count=(
      rule_family.raw_candidate_count
    ),
  )


def _render_source_statement(
  source_group: ApplicabilitySourceGroupPresentation,
) -> tuple[
  str | None,
  str | None,
]:
  statement = (
    source_group.source_statement
  )

  try:
    return (
      render_repository_conclusion_latex(
        statement
      ),
      None,
    )
  except (
    TypeError,
    ValueError,
  ):
    return (
      None,
      type(
        statement
      ).__name__,
    )


def _build_source_view(
  source_group: ApplicabilitySourceGroupPresentation,
) -> WebGeneratorApplicabilitySourceView:
  if not isinstance(
    source_group,
    ApplicabilitySourceGroupPresentation,
  ):
    raise TypeError(
      "source_group must be an "
      "ApplicabilitySourceGroupPresentation"
    )

  statement_latex, fallback_type_name = (
    _render_source_statement(
      source_group
    )
  )

  rule_families = tuple(
    _build_rule_family_view(
      rule_family
    )
    for rule_family in (
      source_group.rule_families
    )
  )

  return WebGeneratorApplicabilitySourceView(
    statement_latex=statement_latex,
    fallback_type_name=fallback_type_name,
    root_key=(
      source_group
      .scope_node
      .root_entry
      .key
    ),
    depth=(
      source_group
      .scope_node
      .shortest_depth
    ),
    source_statement_type=type(
      source_group.source_statement
    ).__name__,
    raw_candidate_count=len(
      source_group.candidates
    ),
    rule_family_count=len(
      rule_families
    ),
    rule_families=rule_families,
  )


def _build_source_views(
  source_groups: tuple[
    ApplicabilitySourceGroupPresentation,
    ...,
  ],
) -> tuple[
  WebGeneratorApplicabilitySourceView,
  ...,
]:
  return tuple(
    _build_source_view(
      source_group
    )
    for source_group in source_groups
  )


def build_standard_web_generator_applicability_view(
  generator_input: str,
) -> WebGeneratorApplicabilityView:
  if not isinstance(
    generator_input,
    str,
  ):
    raise TypeError(
      "generator_input must be a str"
    )

  generator_input = (
    generator_input.strip()
  )

  if not generator_input:
    raise ValueError(
      "generator is required"
    )

  result = (
    explore_standard_repository_generator_applicability_input(
      generator_input
    )
  )

  presentation = (
    build_repository_generator_applicability_presentation(
      result
    )
  )

  toda_memberships = (
    _build_source_views(
      presentation
      .toda_membership_source_groups
    )
  )
  map_relations = (
    _build_source_views(
      presentation
      .map_relation_source_groups
    )
  )
  other_sources = (
    _build_source_views(
      presentation
      .other_source_groups
    )
  )

  return WebGeneratorApplicabilityView(
    generator_input=generator_input,
    generator_latex=(
      _render_generator_symbol_latex(
        result.generator
      )
    ),
    occurrence_count=len(
      result
      .proof_scope_exploration
      .occurrences
    ),
    candidate_count=len(
      result.candidates
    ),
    source_count=len(
      presentation.source_groups
    ),
    rule_group_count=(
      presentation.rule_group_count
    ),
    rule_family_count=(
      presentation.rule_family_count
    ),
    toda_memberships=toda_memberships,
    map_relations=map_relations,
    other_sources=other_sources,
  )
