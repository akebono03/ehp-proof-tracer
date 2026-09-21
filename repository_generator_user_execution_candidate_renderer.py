from formatter import (
  format_statement,
)
from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from repository_generator_user_execution_candidate_presentation import (
  RepositoryGeneratorUserExecutionCandidateListPresentation,
)


def _render_candidate_statement(
  statement,
) -> str:
  try:
    latex = (
      render_repository_conclusion_latex(
        statement
      )
    )
  except (
    TypeError,
    ValueError,
  ):
    return format_statement(
      statement
    )

  return (
    "$"
    + latex
    + "$"
  )


def render_repository_generator_user_execution_candidate_list_markdown(
  presentation,
) -> str:
  if not isinstance(
    presentation,
    RepositoryGeneratorUserExecutionCandidateListPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "RepositoryGeneratorUserExecutionCandidateListPresentation"
    )

  lines = [
    "# Executable candidates",
    "",
  ]

  for candidate in presentation.candidates:
    lines.append(
      (
        str(
          candidate.candidate_number
        )
        + ". "
        + _render_candidate_statement(
          candidate.conclusion
        )
      )
    )

  lines.extend(
    (
      "",
      "Select a candidate number to execute.",
    )
  )

  return (
    "\n".join(
      lines
    )
    + "\n"
  )
