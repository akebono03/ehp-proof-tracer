from proof import (
  ProofStep,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
)
from toda_group_proof_narrative_step_transitions import (
  extract_toda_group_proof_narrative_step_transitions,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)


def toda_group_proof_narrative_equation_reference(
  equation_number: int,
) -> str:
  if (
    not isinstance(
      equation_number,
      int,
    )
    or isinstance(
      equation_number,
      bool,
    )
    or equation_number <= 0
  ):
    raise ValueError(
      "equation_number must be a positive integer"
    )

  return "(" + str(equation_number) + ")"


def _numbered_step_line(
  proof_step: ProofStep,
  equation_number: int,
) -> str:
  rendered = _render_generic_narrative_step(
    proof_step
  )
  closing = rendered.rfind("$")

  if (
    not rendered.startswith("$")
    or closing <= 0
  ):
    return rendered

  return (
    rendered[:closing]
    + r"\tag{"
    + str(equation_number)
    + "}"
    + rendered[closing:]
  )


def number_toda_group_proof_narrative_equations(
  markdown: str,
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
) -> str:
  if not isinstance(markdown, str):
    raise TypeError("markdown must be a string")

  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(blocks, tuple):
    raise TypeError("blocks must be a tuple")

  transitions = (
    extract_toda_group_proof_narrative_step_transitions(
      presentation,
      blocks,
    )
  )
  sources_by_target = {}

  for transition in transitions:
    target_id = id(transition.target_step)
    current = sources_by_target.get(
      target_id,
      (),
    )
    if any(
      step is transition.source_step
      for step in current
    ):
      continue
    sources_by_target[target_id] = (
      *current,
      transition.source_step,
    )

  ordered_steps = []
  seen_ids = set()

  for block in blocks:
    for target_step in block.steps:
      source_steps = sources_by_target.get(
        id(target_step),
        (),
      )
      for source_step in source_steps:
        source_id = id(source_step)
        if source_id in seen_ids:
          continue
        ordered_steps.append(source_step)
        seen_ids.add(source_id)

      if (
        source_steps
        and id(target_step) not in seen_ids
      ):
        ordered_steps.append(target_step)
        seen_ids.add(id(target_step))

  number_by_id = {
    id(step): number
    for number, step in enumerate(
      ordered_steps,
      start=1,
    )
  }
  plain_by_id = {
    id(step): _render_generic_narrative_step(step)
    for step in ordered_steps
  }
  tagged_by_id = {
    id(step): _numbered_step_line(
      step,
      number_by_id[id(step)],
    )
    for step in ordered_steps
  }

  lines = markdown.splitlines()

  for index, line in enumerate(lines):
    matching_id = next(
      (
        step_id
        for step_id, plain in plain_by_id.items()
        if line == plain
      ),
      None,
    )
    if matching_id is not None:
      lines[index] = tagged_by_id[matching_id]

  for target_id, source_steps in sources_by_target.items():
    target_line = tagged_by_id.get(target_id)
    if target_line is None:
      continue

    target_index = next(
      (
        index
        for index, line in enumerate(lines)
        if line == target_line
      ),
      None,
    )
    if target_index is None:
      continue

    connector_index = next(
      (
        index
        for index in range(
          target_index - 1,
          -1,
          -1,
        )
        if lines[index] == "これらより、"
      ),
      None,
    )
    if connector_index is None:
      continue

    references = tuple(
      toda_group_proof_narrative_equation_reference(
        number_by_id[id(source_step)]
      )
      for source_step in source_steps
      if id(source_step) in number_by_id
    )
    if not references:
      continue

    if len(references) == 1:
      reference_text = references[0]
    else:
      reference_text = (
        ", ".join(references[:-1])
        + " と "
        + references[-1]
      )

    lines[connector_index] = (
      reference_text + " より、"
    )

  return "\n".join(lines)
