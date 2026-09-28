from formatter import (
  format_statement,
)
from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from repository_generator_known_group_proof_replay_presentation import (
  RepositoryGeneratorKnownGroupProofReplayPresentation,
)
from toda_human_readable_renderer import (
  _render_generator_symbol_latex,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def _render_known_group_proof_replay_statement(
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
    latex = (
      render_toda_proof_statement_latex(
        statement
      )
    )

    if latex is None:
      return format_statement(
        statement
      )

  return (
    "$"
    + latex
    + "$"
  )


def _known_group_proof_replay_rule_name(
  proof_step,
) -> str:
  if proof_step.inference_rule is not None:
    return proof_step.inference_rule.name

  return proof_step.rule.value


def render_repository_generator_known_group_proof_replay_markdown(
  presentation,
) -> str:
  if not isinstance(
    presentation,
    RepositoryGeneratorKnownGroupProofReplayPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "RepositoryGeneratorKnownGroupProofReplayPresentation"
    )

  generator_latex = (
    _render_generator_symbol_latex(
      presentation.generator
    )
  )

  result_statement = (
    _render_known_group_proof_replay_statement(
      presentation.conclusion
    )
  )

  lines = [
    "# Generator",
    "",
    "$" + generator_latex + "$",
    "",
    "# Result",
    "",
    result_statement,
    "",
    "## Proof",
    "",
  ]

  for index, replay_step in enumerate(
    presentation.steps,
    start=1,
  ):
    proof_step = (
      replay_step.proof_step
    )

    lines.extend(
      (
        (
          f"{index}. Depth "
          f"{replay_step.depth}: "
          + _render_known_group_proof_replay_statement(
            proof_step.conclusion
          )
        ),
        (
          "   Rule: "
          + _known_group_proof_replay_rule_name(
            proof_step
          )
        ),
      )
    )

  return (
    "\n".join(
      lines
    )
    + "\n"
  )
