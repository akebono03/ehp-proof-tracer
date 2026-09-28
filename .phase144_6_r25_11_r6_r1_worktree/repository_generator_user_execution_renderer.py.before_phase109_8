from formatter import (
  format_statement,
)
from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from repository_generator_user_execution_presentation import (
  RepositoryGeneratorUserExecutionPresentation,
)


def _render_user_execution_statement(
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


def render_repository_generator_user_execution_markdown(
  presentation,
) -> str:
  if not isinstance(
    presentation,
    RepositoryGeneratorUserExecutionPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "RepositoryGeneratorUserExecutionPresentation"
    )

  result_statement = (
    _render_user_execution_statement(
      presentation.conclusion
    )
  )

  lines = [
    "# Result",
    "",
    result_statement,
    "",
    "## Proof",
    "",
  ]

  if presentation.premises:
    lines.append(
      "Premises:"
    )

    for index, premise in enumerate(
      presentation.premises,
      start=1,
    ):
      lines.append(
        (
          f"{index}. "
          + _render_user_execution_statement(
            premise.conclusion
          )
        )
      )
  else:
    lines.append(
      "Premises: none"
    )

  lines.extend(
    (
      "",
      (
        "Rule: "
        + presentation.rule_name
      ),
      "",
      "Conclusion:",
      result_statement,
    )
  )

  return (
    "\n".join(
      lines
    )
    + "\n"
  )
