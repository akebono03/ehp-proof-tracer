from proof import ProofStep
from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def _render_group_proof_outline_statement(
  proof_step: ProofStep,
) -> str:
  if not isinstance(
    proof_step,
    ProofStep,
  ):
    raise TypeError(
      "proof_step must be a ProofStep"
    )

  statement = proof_step.conclusion

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

  if latex is not None:
    return (
      "$"
      + latex
      + "$"
    )

  if proof_step.inference_rule is not None:
    return proof_step.inference_rule.name

  return (
    "`"
    + type(
      statement
    ).__name__
    + "`"
  )


def _outline_edges_for_parent(
  presentation: TodaGroupProofPresentation,
  parent_step: ProofStep,
):
  return tuple(
    sorted(
      (
        edge
        for edge in presentation.edges
        if edge.parent_step is parent_step
      ),
      key=lambda edge: edge.premise_index,
    )
  )


def _append_outline_children(
  lines: list[str],
  presentation: TodaGroupProofPresentation,
  parent_step: ProofStep,
  indent_level: int,
  active_step_ids: set[int],
) -> None:
  parent_id = id(
    parent_step
  )

  if parent_id in active_step_ids:
    return

  active_step_ids.add(
    parent_id
  )

  for edge in _outline_edges_for_parent(
    presentation,
    parent_step,
  ):
    premise_step = edge.premise_step

    lines.append(
      (
        "  " * indent_level
        + "- Premise "
        + str(
          edge.premise_index + 1
        )
        + ": "
        + _render_group_proof_outline_statement(
          premise_step
        )
      )
    )

    _append_outline_children(
      lines,
      presentation,
      premise_step,
      indent_level + 1,
      active_step_ids,
    )

  active_step_ids.remove(
    parent_id
  )


def render_toda_group_proof_outline_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  source_entry = presentation.source_entry

  lines = [
    "# Group proof outline",
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
    (
      "- Repository key: `"
      + source_entry.key
      + "`"
    ),
    "",
    "## Conclusion",
    "",
    (
      _render_group_proof_outline_statement(
        presentation.root_step
      )
    ),
    "",
    "## Outline",
    "",
    (
      "- Conclusion: "
      + _render_group_proof_outline_statement(
        presentation.root_step
      )
    ),
  ]

  _append_outline_children(
    lines,
    presentation,
    presentation.root_step,
    1,
    set(),
  )

  return (
    "\n".join(
      lines
    )
    + "\n"
  )
