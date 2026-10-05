from pathlib import Path
import shutil

REPO_ROOT = Path(__file__).resolve().parents[1]
TARGET = REPO_ROOT / "toda_group_proof_narrative_equation_numbering.py"

OLD = r"""def number_toda_group_proof_narrative_equations(
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
        if lines[index] == "これらより, "
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
      reference_text + " より, "
    )

  return "\n".join(lines)
"""
NEW = r"""def number_toda_group_proof_narrative_equations(
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
  source_line_index_by_id = {}

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
      current_index = (
        source_line_index_by_id.get(
          source_id
        )
      )
      if (
        current_index is None
        or source_index < current_index
      ):
        source_line_index_by_id[
          source_id
        ] = source_index

    if not visible_source_ids:
      continue

    reference_plans.append(
      (
        connector_index,
        tuple(
          visible_source_ids
        ),
      )
    )

  ordered_source_ids = tuple(
    source_id
    for source_id, _line_index in sorted(
      source_line_index_by_id.items(),
      key=lambda item: item[1],
    )
  )
  number_by_id = {
    source_id: number
    for number, source_id in enumerate(
      ordered_source_ids,
      start=1,
    )
  }

  occupied_line_indices = set()

  for source_id in ordered_source_ids:
    line_index = (
      source_line_index_by_id[
        source_id
      ]
    )
    if line_index in occupied_line_indices:
      continue

    proof_step = step_by_id.get(
      source_id
    )
    if proof_step is None:
      continue

    tagged_line = _numbered_step_line(
      proof_step,
      number_by_id[
        source_id
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
        and source_line_index_by_id[
          source_id
        ] < connector_index
      )
    )
    if not references:
      continue

    if len(references) == 1:
      reference_text = references[0]
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
"""

def main() -> int:
    if not TARGET.exists():
        raise FileNotFoundError(
            f"target file not found: {TARGET}"
        )

    raw = TARGET.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8")
    normalized = text.replace("\r\n", "\n")

    count = normalized.count(OLD)
    if count != 1:
        raise RuntimeError(
            "expected exactly one current equation-numbering function; "
            f"found {count}. Repository may not match the audited HEAD."
        )

    updated = normalized.replace(
        OLD,
        NEW,
        1,
    )

    backup = TARGET.with_suffix(
        TARGET.suffix
        + ".phase158_r5_4_repair_backup"
    )
    if not backup.exists():
        shutil.copy2(
            TARGET,
            backup,
        )

    if newline == "\r\n":
        updated = updated.replace(
            "\n",
            "\r\n",
        )

    TARGET.write_bytes(
        updated.encode(
            "utf-8"
        )
    )

    print("Phase 158-R5-4 repair applied.")
    print("Production code:")
    print("  toda_group_proof_narrative_equation_numbering.py")
    print("Changed function:")
    print("  number_toda_group_proof_narrative_equations")
    print("Rule:")
    print("  number only source equations visibly preceding a later connector")
    return 0

if __name__ == "__main__":
    raise SystemExit(
        main()
    )
