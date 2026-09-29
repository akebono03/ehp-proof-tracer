from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def replace_once(
  path: Path,
  old: str,
  new: str,
) -> None:
  text = path.read_text(
    encoding="utf-8"
  )

  count = text.count(
    old
  )

  if count != 1:
    raise RuntimeError(
      f"{path}: expected exactly one replacement anchor, found {count}"
    )

  path.write_text(
    text.replace(
      old,
      new,
      1,
    ),
    encoding="utf-8",
  )

  print(
    f"updated {path}"
  )


def main() -> None:
  multi = (
    ROOT
    / "toda_group_proof_narrative_argument_multi_renderer.py"
  )
  body = (
    ROOT
    / "toda_group_proof_narrative_argument_body_renderer.py"
  )

  replace_once(
    multi,
    """from toda_group_proof_narrative_argument_discourse import (
""",
    """from toda_group_proof_narrative_argument_direct_premises import (
  extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises,
)
from toda_group_proof_narrative_argument_discourse import (
""",
  )

  replace_once(
    multi,
    """    conclusion_step = (
      None
      if connector is None
      else extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )

    body = (
""",
    """    conclusion_step = (
      None
      if connector is None
      else extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )
    direct_derivation_premises = (
      ()
      if conclusion_step is None
      else (
        extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
          argument,
          arguments,
        )
      )
    )

    body = (
""",
  )

  replace_once(
    multi,
    """        connector_text=connector,
        conclusion_step=conclusion_step,
      )
""",
    """        connector_text=connector,
        conclusion_step=conclusion_step,
        direct_derivation_premises=direct_derivation_premises,
      )
""",
  )

  replace_once(
    body,
    """def _insert_toda_group_proof_narrative_connector_before_conclusion_step(
""",
    """def _relocatable_toda_group_proof_narrative_direct_derivation_premises(
  direct_derivation_premises: tuple[
    ProofStep,
    ...,
  ],
  sources_by_target_id: dict[
    int,
    tuple[
      ProofStep,
      ...,
    ],
  ],
  conclusion_block: TodaGroupProofNarrativeBlock,
) -> tuple[
  ProofStep,
  ...,
]:
  return tuple(
    premise_step
    for premise_step in direct_derivation_premises
    if (
      premise_step not in conclusion_block.steps
      and not sources_by_target_id.get(
        id(
          premise_step
        ),
        (),
      )
    )
  )


def _insert_toda_group_proof_narrative_relocated_direct_premises(
  block_lines: tuple[
    str,
    ...,
  ],
  block: TodaGroupProofNarrativeBlock,
  conclusion_step: ProofStep,
  direct_derivation_premises: tuple[
    ProofStep,
    ...,
  ],
  relocated_direct_premises: tuple[
    ProofStep,
    ...,
  ],
) -> tuple[
  str,
  ...,
]:
  if not relocated_direct_premises:
    return block_lines

  anchor_steps = tuple(
    premise_step
    for premise_step in direct_derivation_premises
    if premise_step in block.steps
  ) + (
    conclusion_step,
  )

  anchor_lines = tuple(
    _render_generic_narrative_step(
      proof_step
    )
    for proof_step in anchor_steps
  )

  anchor_index = next(
    (
      index
      for index, line in enumerate(
        block_lines
      )
      if line in anchor_lines
    ),
    None,
  )

  if anchor_index is None:
    return block_lines

  relocated_lines = []

  for premise_step in relocated_direct_premises:
    relocated_lines.append(
      _render_generic_narrative_step(
        premise_step
      )
    )
    relocated_lines.append(
      ""
    )

  return (
    block_lines[
      :anchor_index
    ]
    + tuple(
      relocated_lines
    )
    + block_lines[
      anchor_index:
    ]
  )


def _insert_toda_group_proof_narrative_connector_before_conclusion_step(
""",
  )

  replace_once(
    body,
    """  connector_text: str | None = None,
  conclusion_step: ProofStep | None = None,
) -> str:
""",
    """  connector_text: str | None = None,
  conclusion_step: ProofStep | None = None,
  direct_derivation_premises: tuple[
    ProofStep,
    ...,
  ] = (),
) -> str:
""",
  )

  replace_once(
    body,
    """  if (
    conclusion_step is not None
    and connector_before_block_id is None
  ):
    raise ValueError(
      "conclusion_step requires connector placement"
    )

  block_index_by_identity = {
""",
    """  if (
    conclusion_step is not None
    and connector_before_block_id is None
  ):
    raise ValueError(
      "conclusion_step requires connector placement"
    )

  if not isinstance(
    direct_derivation_premises,
    tuple,
  ):
    raise TypeError(
      "direct_derivation_premises must be a tuple"
    )

  for premise_step in direct_derivation_premises:
    if not isinstance(
      premise_step,
      ProofStep,
    ):
      raise TypeError(
        "direct_derivation_premises must contain only "
        "ProofStep objects"
      )

  block_index_by_identity = {
""",
  )

  replace_once(
    body,
    """  redundant_direct_premise_step_ids = (
    frozenset()
    if conclusion_step is None
    else (
      extract_toda_group_structure_narrative_redundant_direct_premise_step_ids(
        conclusion_step
      )
    )
  )

  lines = []
""",
    """  redundant_direct_premise_step_ids = (
    frozenset()
    if conclusion_step is None
    else (
      extract_toda_group_structure_narrative_redundant_direct_premise_step_ids(
        conclusion_step
      )
    )
  )
  relocated_direct_premises = (
    ()
    if conclusion_step is None
    else (
      _relocatable_toda_group_proof_narrative_direct_derivation_premises(
        direct_derivation_premises,
        step_derivation_sources_by_target_id,
        next(
          block
          for block in blocks
          if conclusion_step in block.steps
        ),
      )
    )
  )
  relocated_direct_premise_ids = {
    id(
      premise_step
    )
    for premise_step in relocated_direct_premises
  }

  lines = []
""",
  )

  replace_once(
    body,
    """      display_steps = tuple(
        proof_step
        for proof_step in block.steps
        if id(
          proof_step
        ) not in redundant_direct_premise_step_ids
      )
""",
    """      display_steps = tuple(
        proof_step
        for proof_step in block.steps
        if (
          id(
            proof_step
          ) not in redundant_direct_premise_step_ids
          and (
            id(
              proof_step
            ) not in relocated_direct_premise_ids
            or (
              conclusion_step is not None
              and conclusion_step in block.steps
            )
          )
        )
      )
""",
  )

  replace_once(
    body,
    """      block_lines = (
        _insert_toda_group_proof_narrative_step_derivation_connectors(
          block_lines,
          reordered_block,
          step_derivation_sources_by_target_id,
        )
      )

    if not block_lines:
""",
    """      block_lines = (
        _insert_toda_group_proof_narrative_step_derivation_connectors(
          block_lines,
          reordered_block,
          step_derivation_sources_by_target_id,
        )
      )

      if (
        conclusion_step is not None
        and conclusion_step in reordered_block.steps
      ):
        block_lines = (
          _insert_toda_group_proof_narrative_relocated_direct_premises(
            block_lines,
            reordered_block,
            conclusion_step,
            direct_derivation_premises,
            relocated_direct_premises,
          )
        )

    if not block_lines:
""",
  )


if __name__ == "__main__":
  main()
