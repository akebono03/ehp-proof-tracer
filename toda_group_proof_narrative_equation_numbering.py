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
    target_id = id(
      transition.target_step
    )
    current = sources_by_target.get(
      target_id,
      (),
    )

    if any(
      step is transition.source_step
      for step in current
    ):
      continue

    sources_by_target[
      target_id
    ] = (
      *current,
      transition.source_step,
    )

  step_by_id = {
    id(
      proof_step
    ): proof_step
    for block in blocks
    for proof_step in block.steps
  }
  lines = markdown.splitlines()
  plain_by_id = {
    step_id: _render_generic_narrative_step(
      proof_step
    )
    for step_id, proof_step in step_by_id.items()
  }

  reference_plans = []
  line_index_by_id = {}

  for target_id, source_steps in sources_by_target.items():
    target_plain = plain_by_id.get(
      target_id
    )

    if not target_plain:
      continue

    target_index = next(
      (
        index
        for index, line in enumerate(
          lines
        )
        if line == target_plain
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
        if lines[index] == "これらより, "
      ),
      None,
    )

    if connector_index is None:
      continue

    visible_source_ids = []

    for source_step in source_steps:
      source_id = id(
        source_step
      )
      source_plain = plain_by_id.get(
        source_id
      )

      if not source_plain:
        continue

      source_index = next(
        (
          index
          for index in range(
            connector_index - 1,
            -1,
            -1,
          )
          if lines[index] == source_plain
        ),
        None,
      )

      if source_index is None:
        continue

      visible_source_ids.append(
        source_id
      )
      current_index = line_index_by_id.get(
        source_id
      )

      if (
        current_index is None
        or source_index < current_index
      ):
        line_index_by_id[
          source_id
        ] = source_index

    if not visible_source_ids:
      continue

    current_target_index = line_index_by_id.get(
      target_id
    )

    if (
      current_target_index is None
      or target_index < current_target_index
    ):
      line_index_by_id[
        target_id
      ] = target_index

    reference_plans.append(
      (
        connector_index,
        tuple(
          visible_source_ids
        ),
      )
    )

  ordered_step_ids = tuple(
    step_id
    for step_id, _line_index in sorted(
      line_index_by_id.items(),
      key=lambda item: item[1],
    )
  )
  number_by_id = {
    step_id: number
    for number, step_id in enumerate(
      ordered_step_ids,
      start=1,
    )
  }

  occupied_line_indices = set()

  for step_id in ordered_step_ids:
    line_index = line_index_by_id[
      step_id
    ]

    if line_index in occupied_line_indices:
      continue

    proof_step = step_by_id.get(
      step_id
    )

    if proof_step is None:
      continue

    tagged_line = _numbered_step_line(
      proof_step,
      number_by_id[
        step_id
      ],
    )

    if tagged_line == lines[
      line_index
    ]:
      continue

    lines[
      line_index
    ] = tagged_line
    occupied_line_indices.add(
      line_index
    )

  for connector_index, source_ids in reference_plans:
    references = tuple(
      toda_group_proof_narrative_equation_reference(
        number_by_id[
          source_id
        ]
      )
      for source_id in source_ids
      if (
        source_id in number_by_id
        and line_index_by_id[
          source_id
        ] < connector_index
      )
    )

    if not references:
      continue

    if len(
      references
    ) == 1:
      reference_text = references[
        0
      ]
    else:
      reference_text = (
        ", ".join(
          references[
            :-1
          ]
        )
        + " と "
        + references[
          -1
        ]
      )

    lines[
      connector_index
    ] = (
      reference_text
      + " より, "
    )

  return "\n".join(
    lines
  )


