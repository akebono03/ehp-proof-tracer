from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from repository_generator_applicability_facade import (
  RepositoryGeneratorApplicabilityExplorationResult,
)
from repository_generator_applicability_presentation import (
  ApplicabilitySourceGroupPresentation,
  RepositoryGeneratorApplicabilityPresentation,
  build_repository_generator_applicability_presentation,
)
from toda_human_readable_renderer import (
  _render_generator_symbol_latex,
)


def _source_heading(
  source_group: ApplicabilitySourceGroupPresentation,
) -> str:
  statement = (
    source_group.source_statement
  )

  try:
    rendered = (
      render_repository_conclusion_latex(
        statement
      )
    )
  except (
    TypeError,
    ValueError,
  ):
    return (
      "#### Source statement: "
      + type(
        statement
      ).__name__
    )

  return (
    "#### $"
    + rendered
    + "$"
  )


def _append_source_group(
  lines: list[str],
  source_group: ApplicabilitySourceGroupPresentation,
) -> None:
  lines.extend(
    (
      "",
      _source_heading(
        source_group
      ),
      "",
      (
        "- Root: "
        + source_group
        .scope_node
        .root_entry
        .key
      ),
      (
        "- Depth: "
        + str(
          source_group
          .scope_node
          .shortest_depth
        )
      ),
      (
        "- Source statement type: "
        + type(
          source_group
          .source_statement
        ).__name__
      ),
      (
        "- Raw candidates: "
        + str(
          len(
            source_group.candidates
          )
        )
      ),
    )
  )

  for rule_group in (
    source_group.rule_groups
  ):
    lines.extend(
      (
        "",
        (
          "- Rule: "
          + rule_group
          .inference_rule
          .name
        ),
        (
          "  - Catalog: `"
          + rule_group
          .catalog_entry
          .key
          + "`"
        ),
        (
          "  - Fixed-point safe: "
          + (
            "yes"
            if rule_group.fixed_point_safe
            else "no"
          )
        ),
      )
    )

    for candidate in (
      rule_group.candidates
    ):
      lines.append(
        (
          "  - Premise index: "
          + str(
            candidate
            .candidate
            .premise_index
          )
          + "; Bindings: "
          + str(
            len(
              candidate
              .candidate
              .bindings
            )
          )
        )
      )


def _append_source_section(
  lines: list[str],
  title: str,
  source_groups: tuple[
    ApplicabilitySourceGroupPresentation,
    ...,
  ],
) -> None:
  if not source_groups:
    return

  lines.extend(
    (
      "",
      "### " + title,
    )
  )

  for source_group in source_groups:
    _append_source_group(
      lines,
      source_group,
    )


def _render_grouped_presentation_markdown(
  presentation: RepositoryGeneratorApplicabilityPresentation,
) -> str:
  result = (
    presentation.source_result
  )

  lines = [
    (
      "# Applicable theorem / lemma candidates for $"
      + _render_generator_symbol_latex(
        result.generator
      )
      + "$"
    ),
    "",
    (
      "Proof-scope occurrences: "
      + str(
        len(
          result
          .proof_scope_exploration
          .occurrences
        )
      )
    ),
    (
      "Applicability candidates: "
      + str(
        len(
          result.candidates
        )
      )
    ),
    (
      "Source statements with candidates: "
      + str(
        len(
          presentation.source_groups
        )
      )
    ),
    (
      "Rule groups: "
      + str(
        presentation.rule_group_count
      )
    ),
  ]

  if result.candidates:
    lines.extend(
      (
        "",
        "## Candidates",
      )
    )

    _append_source_section(
      lines,
      "Toda memberships",
      presentation
      .toda_membership_source_groups,
    )

    _append_source_section(
      lines,
      "Map relations",
      presentation
      .map_relation_source_groups,
    )

    _append_source_section(
      lines,
      "Other statements",
      presentation
      .other_source_groups,
    )

  return "\n".join(
    lines
  ) + "\n"


def render_repository_generator_applicability_markdown(
  result: RepositoryGeneratorApplicabilityExplorationResult,
) -> str:
  if not isinstance(
    result,
    RepositoryGeneratorApplicabilityExplorationResult,
  ):
    raise TypeError(
      "result must be a "
      "RepositoryGeneratorApplicabilityExplorationResult"
    )

  presentation = (
    build_repository_generator_applicability_presentation(
      result
    )
  )

  return _render_grouped_presentation_markdown(
    presentation
  )
