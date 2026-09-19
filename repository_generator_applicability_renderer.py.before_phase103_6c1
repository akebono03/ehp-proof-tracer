from repository_generator_applicability_facade import (
  RepositoryGeneratorApplicabilityExplorationResult,
)
from toda_human_readable_renderer import (
  _render_generator_symbol_latex,
)


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
  ]

  if result.candidates:
    lines.extend(
      (
        "",
        "## Candidates",
        "",
      )
    )

    for index, result_candidate in enumerate(
      result.candidates
    ):
      if index:
        lines.append(
          ""
        )

      candidate = (
        result_candidate.candidate
      )

      entry = (
        candidate.catalog_entry
      )

      lines.append(
        "- `" + entry.key + "`"
      )

      lines.append(
        (
          "  - Rule: "
          + candidate.inference_rule.name
        )
      )

      lines.append(
        (
          "  - Premise index: "
          + str(
            candidate.premise_index
          )
        )
      )

      lines.append(
        (
          "  - Fixed-point safe: "
          + (
            "yes"
            if candidate.fixed_point_safe
            else "no"
          )
        )
      )

      lines.append(
        (
          "  - Root: "
          + result_candidate.root_entry.key
        )
      )

      lines.append(
        (
          "  - Depth: "
          + str(
            result_candidate.shortest_depth
          )
        )
      )

      lines.append(
        (
          "  - Source statement type: "
          + type(
            candidate.matched_statement
          ).__name__
        )
      )

      lines.append(
        (
          "  - Bindings: "
          + str(
            len(
              candidate.bindings
            )
          )
        )
      )

  return "\n".join(
    lines
  ) + "\n"
