from expression import GeneratorSymbol
from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from repository_proof_scope_facade import (
  RepositoryProofScopeExplorationResult,
)
from toda_human_readable_renderer import (
  _render_generator_symbol_latex,
)


def _root_depth_lines(
  root_key: str,
  depth: int,
) -> tuple[
  str,
  ...,
]:
  return (
    "  - Root: " + root_key,
    "  - Depth: " + str(
      depth
    ),
  )


def render_repository_proof_scope_exploration_markdown(
  result: RepositoryProofScopeExplorationResult,
) -> str:
  if not isinstance(
    result,
    RepositoryProofScopeExplorationResult,
  ):
    raise TypeError(
      "result must be a "
      "RepositoryProofScopeExplorationResult"
    )

  generator = result.generator

  if not isinstance(
    generator,
    GeneratorSymbol,
  ):
    raise TypeError(
      "result generator must be a GeneratorSymbol"
    )

  lines = [
    (
      "# $"
      + _render_generator_symbol_latex(
        generator
      )
      + "$"
    ),
    "",
    (
      "Proof-scope occurrences: "
      + str(
        len(
          result.occurrences
        )
      )
    ),
    (
      "Toda memberships: "
      + str(
        len(
          result.toda_memberships
        )
      )
    ),
    (
      "Map relations: "
      + str(
        len(
          result.map_relations
        )
      )
    ),
  ]

  if result.toda_memberships:
    lines.extend(
      (
        "",
        "## Toda memberships",
        "",
      )
    )

    for index, membership in enumerate(
      result.toda_memberships
    ):
      if index:
        lines.append(
          ""
        )

      node = (
        membership
        .source_occurrence
        .scope_node
      )

      lines.append(
        (
          "- $"
          + render_repository_conclusion_latex(
            membership.statement
          )
          + "$"
        )
      )

      lines.extend(
        _root_depth_lines(
          node.root_entry.key,
          node.shortest_depth,
        )
      )

      match_parts = []

      if membership.is_membership_element:
        match_parts.append(
          "membership element"
        )

      match_parts.extend(
        "Toda bracket " + position
        for position in membership.bracket_positions
      )

      lines.append(
        (
          "  - Match: "
          + ", ".join(
            match_parts
          )
        )
      )

  if result.map_relations:
    lines.extend(
      (
        "",
        "## Map relations",
        "",
      )
    )

    for index, map_relation in enumerate(
      result.map_relations
    ):
      if index:
        lines.append(
          ""
        )

      node = (
        map_relation
        .source_occurrence
        .scope_node
      )

      lines.append(
        (
          "- $"
          + render_repository_conclusion_latex(
            map_relation.relation
          )
          + "$"
        )
      )

      lines.extend(
        _root_depth_lines(
          node.root_entry.key,
          node.shortest_depth,
        )
      )

  return "\n".join(
    lines
  ) + "\n"
