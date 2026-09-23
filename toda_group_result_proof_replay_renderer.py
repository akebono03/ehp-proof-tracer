from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from toda_group_result_proof_replay import (
  TodaGroupResultProofReplayResult,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def _render_group_result_proof_replay_statement(
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
      return (
        "`"
        + type(
          statement
        ).__name__
        + "`"
      )

  return (
    "$"
    + latex
    + "$"
  )


def _group_result_proof_replay_rule_name(
  proof_step,
) -> str:
  if proof_step.inference_rule is not None:
    return proof_step.inference_rule.name

  return proof_step.rule.value


def render_toda_group_result_proof_replay_markdown(
  result,
) -> str:
  if not isinstance(
    result,
    TodaGroupResultProofReplayResult,
  ):
    raise TypeError(
      "result must be a "
      "TodaGroupResultProofReplayResult"
    )

  source_entry = result.source_entry

  lines = [
    "# Group result",
    "",
    _render_group_result_proof_replay_statement(
      result.root_step.conclusion
    ),
    "",
    "## Source",
    "",
    (
      "- Theorem: "
      + (
        source_entry.theorem
        if source_entry.theorem is not None
        else "unknown"
      )
    ),
    (
      "- Phase: "
      + (
        source_entry.phase
        if source_entry.phase is not None
        else "unknown"
      )
    ),
    "- Repository key: `" + source_entry.key + "`",
    "",
    "## Proof",
    "",
  ]

  for index, replay_step in enumerate(
    result.steps,
    start=1,
  ):
    proof_step = replay_step.proof_step

    lines.extend(
      (
        (
          f"{index}. Depth {replay_step.depth}: "
          + _render_group_result_proof_replay_statement(
            proof_step.conclusion
          )
        ),
        (
          "   Role: "
          + replay_step.role.value
        ),
        (
          "   Rule: "
          + _group_result_proof_replay_rule_name(
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
