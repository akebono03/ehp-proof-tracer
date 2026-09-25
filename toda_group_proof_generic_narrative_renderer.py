from proof import (
  ProofStep,
)
from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


_BLOCK_ROLE_LABELS = {
  TodaGroupProofNarrativeMathematicalBlockRole.TARGET:
    "証明対象",
  TodaGroupProofNarrativeMathematicalBlockRole.REFERENCE:
    "参照結果",
  TodaGroupProofNarrativeMathematicalBlockRole.PRECONDITION:
    "適用条件",
  TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION:
    "定義",
  TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP:
    "所属",
  TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION:
    "計算",
  TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS:
    "完全性",
  TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY:
    "写像の性質",
  TodaGroupProofNarrativeMathematicalBlockRole.ORDER:
    "位数",
  TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE:
    "群構造",
  TodaGroupProofNarrativeMathematicalBlockRole.CONCLUSION:
    "結論",
  TodaGroupProofNarrativeMathematicalBlockRole.OTHER:
    "その他",
}


def _render_generic_narrative_step(
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
    latex = None

  if latex is None:
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


def _validate_generic_narrative_blocks(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
) -> None:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    blocks,
    tuple,
  ):
    raise TypeError(
      "blocks must be a tuple"
    )

  selected_step_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }

  seen_step_ids = set()

  for block in blocks:
    if not isinstance(
      block,
      TodaGroupProofNarrativeBlock,
    ):
      raise TypeError(
        "blocks must contain only "
        "TodaGroupProofNarrativeBlock objects"
      )

    for proof_step in block.steps:
      step_id = id(
        proof_step
      )

      if step_id not in selected_step_ids:
        raise ValueError(
          "block proof steps must appear "
          "in presentation nodes"
        )

      if step_id in seen_step_ids:
        raise ValueError(
          "blocks must not contain duplicate "
          "ProofStep objects"
        )

      seen_step_ids.add(
        step_id
      )

  if seen_step_ids != selected_step_ids:
    raise ValueError(
      "blocks must cover presentation nodes "
      "exactly once"
    )


def _generic_narrative_dependency_indices(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  block_index: int,
) -> tuple[
  int,
  ...,
]:
  step_block_index = {
    id(
      proof_step
    ): index
    for index, block in enumerate(
      blocks
    )
    for proof_step in block.steps
  }

  block = blocks[
    block_index
  ]
  block_step_ids = {
    id(
      proof_step
    )
    for proof_step in block.steps
  }

  dependency_indices = []

  for edge in presentation.edges:
    if id(
      edge.parent_step
    ) not in block_step_ids:
      continue

    dependency_index = (
      step_block_index[
        id(
          edge.premise_step
        )
      ]
    )

    if dependency_index == block_index:
      continue

    if dependency_index in dependency_indices:
      continue

    dependency_indices.append(
      dependency_index
    )

  return tuple(
    dependency_indices
  )


def render_toda_group_proof_generic_narrative_markdown(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
) -> str:
  _validate_generic_narrative_blocks(
    presentation,
    blocks,
  )

  lines = [
    "# Generic group proof narrative",
    "",
  ]

  for block_index, block in enumerate(
    blocks
  ):
    block_number = (
      block_index
      + 1
    )
    role_label = (
      _BLOCK_ROLE_LABELS[
        block.role
      ]
    )

    lines.append(
      "## [B"
      + f"{block_number:02d}"
      + "] "
      + role_label
    )
    lines.append(
      ""
    )

    dependency_indices = (
      _generic_narrative_dependency_indices(
        presentation,
        blocks,
        block_index,
      )
    )

    if dependency_indices:
      dependency_labels = ", ".join(
        "[B"
        + f"{dependency_index + 1:02d}"
        + "]"
        for dependency_index
        in dependency_indices
      )

      lines.append(
        "依存: "
        + dependency_labels
      )
      lines.append(
        ""
      )

    for proof_step in block.steps:
      lines.append(
        "- "
        + _render_generic_narrative_step(
          proof_step
        )
      )

    lines.append(
      ""
    )

  return (
    "\n".join(
      lines
    ).rstrip()
    + "\n"
  )
