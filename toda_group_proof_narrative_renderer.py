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


def _render_group_proof_narrative_fact(
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


def _narrative_edges_for_parent(
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


def _premise_lead(
  premise_number: int,
  premise_count: int,
) -> str:
  if premise_count <= 0:
    raise ValueError(
      "premise_count must be positive"
    )

  if (
    premise_number < 0
    or premise_number >= premise_count
  ):
    raise ValueError(
      "premise_number must be within "
      "the premise range"
    )

  if premise_number == 0:
    return "まず"

  if premise_number == premise_count - 1:
    return "さらに"

  return "また"


def _append_narrative_for_step(
  lines: list[str],
  presentation: TodaGroupProofPresentation,
  parent_step: ProofStep,
  active_step_ids: set[int],
  expanded_step_ids: set[int],
) -> None:
  parent_id = id(
    parent_step
  )

  if parent_id in active_step_ids:
    return

  active_step_ids.add(
    parent_id
  )

  edges = (
    _narrative_edges_for_parent(
      presentation,
      parent_step,
    )
  )

  for index, edge in enumerate(
    edges
  ):
    premise_step = edge.premise_step
    premise_id = id(
      premise_step
    )
    premise_fact = (
      _render_group_proof_narrative_fact(
        premise_step
      )
    )
    lead = (
      _premise_lead(
        index,
        len(
          edges
        ),
      )
    )

    if premise_id in expanded_step_ids:
      lines.append(
        (
          lead
          + "、既出の"
          + premise_fact
          + "を用いる。"
        )
      )
      continue

    premise_edges = (
      _narrative_edges_for_parent(
        presentation,
        premise_step,
      )
    )

    if premise_edges:
      _append_narrative_for_step(
        lines,
        presentation,
        premise_step,
        active_step_ids,
        expanded_step_ids,
      )

      lines.append(
        (
          "これらから、"
          + premise_fact
          + "を得る。"
        )
      )
    else:
      lines.append(
        (
          lead
          + "、"
          + premise_fact
          + "を用いる。"
        )
      )

    expanded_step_ids.add(
      premise_id
    )

  active_step_ids.remove(
    parent_id
  )


def render_toda_group_proof_narrative_markdown(
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

  theorem = (
    source_entry.theorem
    if source_entry.theorem is not None
    else "出典不明の結果"
  )

  lines = [
    "# Group proof narrative",
    "",
    theorem + "を用いる。",
    "",
  ]

  root_edges = (
    _narrative_edges_for_parent(
      presentation,
      presentation.root_step,
    )
  )

  if root_edges:
    _append_narrative_for_step(
      lines,
      presentation,
      presentation.root_step,
      set(),
      set(),
    )

    lines.extend(
      (
        "",
        (
          "したがって、"
          + _render_group_proof_narrative_fact(
            presentation.root_step
          )
          + "を得る。"
        ),
      )
    )
  else:
    lines.append(
      (
        "したがって、"
        + _render_group_proof_narrative_fact(
          presentation.root_step
        )
        + "である。"
      )
    )

  return (
    "\n".join(
      lines
    )
    + "\n"
  )
