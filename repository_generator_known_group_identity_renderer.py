from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from repository_generator_known_group_identity_presentation import (
  RepositoryGeneratorKnownGroupIdentityPresentation,
)
from toda_human_readable_renderer import (
  _render_generator_symbol_latex,
)


def render_repository_generator_known_group_identity_markdown(
  presentation,
) -> str:
  if not isinstance(
    presentation,
    RepositoryGeneratorKnownGroupIdentityPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "RepositoryGeneratorKnownGroupIdentityPresentation"
    )

  generator_latex = (
    _render_generator_symbol_latex(
      presentation.generator
    )
  )

  conclusion_latex = (
    render_repository_conclusion_latex(
      presentation.conclusion
    )
  )

  lines = [
    "# Generator",
    "",
    "$" + generator_latex + "$",
    "",
    "# Known group",
    "",
    "$" + conclusion_latex + "$",
  ]

  return (
    "\n".join(
      lines
    )
    + "\n"
  )
