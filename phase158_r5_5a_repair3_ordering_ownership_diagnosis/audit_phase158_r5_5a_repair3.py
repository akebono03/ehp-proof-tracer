from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _generic_narrative_dependency_indices,
  _generic_narrative_proof_order_indices,
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from web_group_proof import (
  WebGroupProofRenderedLineView,
  build_standard_web_group_proof_view,
)


MAX_DEPTH = 2

TARGETS = (
  (
    "pi7_4",
    4,
    3,
  ),
  (
    "pi15_8",
    8,
    7,
  ),
)


def render_web_line(
  line: WebGroupProofRenderedLineView,
) -> str:
  if line.kind == "heading":
    return "## " + line.prefix

  if line.kind == "separator":
    return "---"

  if line.segments:
    parts = []

    for segment in line.segments:
      if segment.kind == "text":
        parts.append(
          segment.value
        )
      elif segment.kind == "strong":
        parts.append(
          "**"
          + segment.value
          + "**"
        )
      elif segment.kind in (
        "inline_math",
        "display_math",
      ):
        parts.append(
          "$"
          + segment.value
          + "$"
        )
      else:
        parts.append(
          repr(
            segment
          )
        )

    return "".join(
      parts
    )

  if line.statement_latex is not None:
    return (
      line.prefix
      + "$"
      + line.statement_latex
      + "$"
      + line.suffix
    )

  return (
    line.prefix
    + line.suffix
  )


def proof_body_lines(
  view,
) -> tuple[
  str,
  ...,
]:
  in_proof = False
  result = []

  for line in view.rendered_lines:
    if (
      line.kind == "heading"
      and line.prefix == "証明"
    ):
      in_proof = True
      continue

    if not in_proof:
      continue

    rendered = render_web_line(
      line
    )

    if rendered.strip():
      result.append(
        rendered
      )

  return tuple(
    result
  )


def safe_role_value(
  value,
) -> str:
  return getattr(
    value,
    "value",
    str(
      value
    ),
  )


def diagnose_target(
  label: str,
  n: int,
  k: int,
) -> str:
  view = (
    build_standard_web_group_proof_view(
      n,
      k,
      max_depth=MAX_DEPTH,
      mode="narrative",
    )
  )

  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=MAX_DEPTH,
    )
  )

  raw_presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw_presentation
    )
  )

  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=semantic_sidecar,
    )
  )

  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=semantic_sidecar,
    )
  )

  proof_order = (
    _generic_narrative_proof_order_indices(
      presentation,
      blocks,
      semantic_sidecar=semantic_sidecar,
    )
  )

  body = proof_body_lines(
    view
  )

  lines = [
    "=" * 100,
    (
      "Phase 158-R5-5a repair3 ordering ownership diagnosis: "
      + label
    ),
    "=" * 100,
    (
      f"group=pi_{n + k}^{n} "
      f"web_mode={view.mode} "
      f"web_max_depth={view.max_depth}"
    ),
    (
      f"replay_steps={len(replay.steps)} "
      f"presentation_nodes={len(presentation.nodes)} "
      f"blocks={len(blocks)} "
      f"arguments={len(arguments)}"
    ),
    "",
    "PUBLIC BODY",
    "-" * 100,
  ]

  for index, text in enumerate(
    body
  ):
    lines.append(
      f"P{index:03d} {text}"
    )

  lines.extend(
    (
      "",
      "DEPTH-2 REPLAY STEPS",
      "-" * 100,
    )
  )

  for index, replay_step in enumerate(
    replay.steps
  ):
    rendered = (
      _render_generic_narrative_step(
        replay_step.proof_step
      )
    )

    lines.extend(
      (
        (
          f"S{index:03d} "
          f"depth={replay_step.depth} "
          f"role={safe_role_value(replay_step.role)} "
          f"type={type(replay_step.proof_step.conclusion).__name__}"
        ),
        (
          "  rendered="
          + rendered
        ),
        (
          "  premise_count="
          + str(
            len(
              replay_step.proof_step.premises
            )
          )
        ),
      )
    )

  lines.extend(
    (
      "",
      "SEMANTIC BLOCKS",
      "-" * 100,
    )
  )

  step_to_block = {}

  for block_index, block in enumerate(
    blocks
  ):
    dependency_indices = (
      _generic_narrative_dependency_indices(
        presentation,
        blocks,
        block_index,
        semantic_sidecar=semantic_sidecar,
      )
    )

    lines.append(
      (
        f"B{block_index:03d} "
        f"role={safe_role_value(block.role)} "
        f"dependencies={dependency_indices} "
        f"step_count={len(block.steps)}"
      )
    )

    for step_index, proof_step in enumerate(
      block.steps
    ):
      step_to_block[
        id(
          proof_step
        )
      ] = block_index

      lines.append(
        (
          f"  B{block_index:03d}.S{step_index:02d} "
          f"type={type(proof_step.conclusion).__name__} "
          f"text={_render_generic_narrative_step(proof_step)}"
        )
      )

  lines.extend(
    (
      "",
      "GENERIC BLOCK PROOF ORDER",
      "-" * 100,
      "order="
      + repr(
        proof_order
      ),
    )
  )

  for order_index, block_index in enumerate(
    proof_order
  ):
    block = blocks[
      block_index
    ]

    lines.append(
      (
        f"O{order_index:03d} -> B{block_index:03d} "
        f"role={safe_role_value(block.role)}"
      )
    )

  lines.extend(
    (
      "",
      "NARRATIVE ARGUMENTS",
      "-" * 100,
    )
  )

  for argument_index, argument in enumerate(
    arguments
  ):
    lines.append(
      (
        f"A{argument_index:03d} "
        f"type={type(argument).__name__}"
      )
    )

    lines.append(
      (
        "  repr="
        + repr(
          argument
        )
      )
    )

  lines.extend(
    (
      "",
      "PRESENTATION EDGES WITH BLOCK OWNERSHIP",
      "-" * 100,
    )
  )

  for edge_index, edge in enumerate(
    presentation.edges
  ):
    premise_block = step_to_block.get(
      id(
        edge.premise_step
      )
    )
    parent_block = step_to_block.get(
      id(
        edge.parent_step
      )
    )

    lines.extend(
      (
        (
          f"E{edge_index:03d} "
          f"B{premise_block} -> B{parent_block} "
          f"premise_index={edge.premise_index}"
        ),
        (
          "  premise="
          + _render_generic_narrative_step(
            edge.premise_step
          )
        ),
        (
          "  parent="
          + _render_generic_narrative_step(
            edge.parent_step
          )
        ),
      )
    )

  lines.append(
    ""
  )

  return "\n".join(
    lines
  )


def main() -> int:
  output_dir = (
    Path(__file__).resolve().parent
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  combined = []

  for label, n, k in TARGETS:
    report = diagnose_target(
      label,
      n,
      k,
    )

    (
      output_dir
      / f"{label}.txt"
    ).write_text(
      report
      + "\n",
      encoding="utf-8",
      newline="\n",
    )

    combined.append(
      report
    )

  summary = "\n\n".join(
    combined
  )

  (
    output_dir
    / "diagnosis.txt"
  ).write_text(
    summary
    + "\n",
    encoding="utf-8",
    newline="\n",
  )

  print(
    summary
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
