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


def _summary_lines(
  presentation: RepositoryGeneratorApplicabilityPresentation,
) -> list[str]:
  result = (
    presentation.source_result
  )

  return [
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
    (
      "Rule families: "
      + str(
        presentation.rule_family_count
      )
    ),
  ]


def _append_compact_source_group(
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
      (
        "- Rule families: "
        + str(
          len(
            source_group.rule_families
          )
        )
      ),
    )
  )

  for rule_family in (
    source_group.rule_families
  ):
    lines.extend(
      (
        "",
        (
          "- Rule: "
          + rule_family.name
        ),
        (
          "  - Catalog entries: "
          + str(
            len(
              rule_family.rule_groups
            )
          )
        ),
        (
          "  - Raw candidates: "
          + str(
            rule_family
            .raw_candidate_count
          )
        ),
      )
    )


def _append_detailed_source_group(
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
      (
        "- Rule groups: "
        + str(
          len(
            source_group.rule_groups
          )
        )
      ),
      (
        "- Rule families: "
        + str(
          len(
            source_group.rule_families
          )
        )
      ),
    )
  )

  for rule_family in (
    source_group.rule_families
  ):
    lines.extend(
      (
        "",
        (
          "- Rule: "
          + rule_family.name
        ),
        (
          "  - Catalog entries: "
          + str(
            len(
              rule_family.rule_groups
            )
          )
        ),
        (
          "  - Raw candidates: "
          + str(
            rule_family
            .raw_candidate_count
          )
        ),
      )
    )

    for rule_group in (
      rule_family.rule_groups
    ):
      lines.append(
        (
          "  - Catalog: `"
          + rule_group
          .catalog_entry
          .key
          + "`; Fixed-point safe: "
          + (
            "yes"
            if rule_group.fixed_point_safe
            else "no"
          )
        )
      )

      for candidate in (
        rule_group.candidates
      ):
        lines.append(
          (
            "    - Premise index: "
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
  detailed: bool,
) -> None:
  if not source_groups:
    return

  lines.extend(
    (
      "",
      "### " + title,
    )
  )

  append_source_group = (
    _append_detailed_source_group
    if detailed
    else _append_compact_source_group
  )

  for source_group in source_groups:
    append_source_group(
      lines,
      source_group,
    )


def _render_presentation_markdown(
  presentation: RepositoryGeneratorApplicabilityPresentation,
  detailed: bool,
) -> str:
  lines = _summary_lines(
    presentation
  )

  result = (
    presentation.source_result
  )

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
      detailed=detailed,
    )

    _append_source_section(
      lines,
      "Map relations",
      presentation
      .map_relation_source_groups,
      detailed=detailed,
    )

    _append_source_section(
      lines,
      "Other statements",
      presentation
      .other_source_groups,
      detailed=detailed,
    )

  return "\n".join(
    lines
  ) + "\n"


def _build_presentation(
  result: RepositoryGeneratorApplicabilityExplorationResult,
) -> RepositoryGeneratorApplicabilityPresentation:
  if not isinstance(
    result,
    RepositoryGeneratorApplicabilityExplorationResult,
  ):
    raise TypeError(
      "result must be a "
      "RepositoryGeneratorApplicabilityExplorationResult"
    )

  return (
    build_repository_generator_applicability_presentation(
      result
    )
  )


def render_repository_generator_applicability_compact_markdown(
  result: RepositoryGeneratorApplicabilityExplorationResult,
) -> str:
  presentation = (
    _build_presentation(
      result
    )
  )

  return _render_presentation_markdown(
    presentation,
    detailed=False,
  )


def render_repository_generator_applicability_detailed_markdown(
  result: RepositoryGeneratorApplicabilityExplorationResult,
) -> str:
  presentation = (
    _build_presentation(
      result
    )
  )

  return _render_presentation_markdown(
    presentation,
    detailed=True,
  )


def render_repository_generator_applicability_markdown(
  result: RepositoryGeneratorApplicabilityExplorationResult,
) -> str:
  return (
    render_repository_generator_applicability_detailed_markdown(
      result
    )
  )
