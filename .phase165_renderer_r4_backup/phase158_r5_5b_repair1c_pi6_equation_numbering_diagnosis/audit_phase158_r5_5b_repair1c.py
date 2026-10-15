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

import toda_group_proof_narrative_argument_multi_renderer as multi_renderer
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_equation_numbering import (
  number_toda_group_proof_narrative_equations,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_step_transitions import (
  extract_toda_group_proof_narrative_step_transitions,
)


def role_value(
  value,
) -> str:
  return getattr(
    value,
    "value",
    str(
      value
    ),
  )


def main() -> int:
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  captured = {}

  original_numbering = (
    multi_renderer
    .number_toda_group_proof_narrative_equations
  )

  def capture_numbering(
    markdown,
    captured_presentation,
    captured_blocks,
  ):
    captured[
      "raw_markdown"
    ] = markdown

    return original_numbering(
      markdown,
      captured_presentation,
      captured_blocks,
    )

  multi_renderer.number_toda_group_proof_narrative_equations = (
    capture_numbering
  )

  try:
    final_markdown = (
      multi_renderer
      .render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        sidecar,
        arguments,
      )
    )
  finally:
    multi_renderer.number_toda_group_proof_narrative_equations = (
      original_numbering
    )

  raw_markdown = captured.get(
    "raw_markdown",
    "",
  )

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
      proof_step is transition.source_step
      for proof_step in current
    ):
      continue

    sources_by_target[
      target_id
    ] = (
      *current,
      transition.source_step,
    )

  ordered_steps = []
  seen_ids = set()

  for block in blocks:
    for target_step in block.steps:
      source_steps = sources_by_target.get(
        id(
          target_step
        ),
        (),
      )

      for source_step in source_steps:
        source_id = id(
          source_step
        )

        if source_id in seen_ids:
          continue

        ordered_steps.append(
          source_step
        )
        seen_ids.add(
          source_id
        )

      if (
        source_steps
        and id(
          target_step
        ) not in seen_ids
      ):
        ordered_steps.append(
          target_step
        )
        seen_ids.add(
          id(
            target_step
          )
        )

  lines = [
    "=" * 100,
    "Phase 158-R5-5b repair1c - pi6 equation numbering diagnosis",
    "=" * 100,
    "",
    "A. NUMBERING CANDIDATES",
    "-" * 100,
  ]

  for number, proof_step in enumerate(
    ordered_steps,
    start=1,
  ):
    plain = (
      _render_generic_narrative_step(
        proof_step
      )
    )
    tag = (
      r"\tag{"
      + str(
        number
      )
      + "}"
    )

    lines.append(
      (
        f"N{number}: "
        f"type={type(proof_step.conclusion).__name__} "
        f"raw_plain={plain in raw_markdown} "
        f"final_plain={plain in final_markdown} "
        f"final_tag={tag in final_markdown}"
      )
    )
    lines.append(
      "  "
      + plain
    )

  lines.extend(
    (
      "",
      "B. ARGUMENT LOCAL BODY / METHOD EVIDENCE",
      "-" * 100,
    )
  )

  ordered_arguments = (
    order_toda_group_proof_narrative_arguments(
      arguments
    )
  )
  source_index_by_identity = {
    id(
      argument
    ): index
    for index, argument in enumerate(
      arguments
    )
  }
  block_index_by_identity = {
    id(
      block
    ): index
    for index, block in enumerate(
      blocks
    )
  }

  for ordered_position, argument in enumerate(
    ordered_arguments
  ):
    argument_index = source_index_by_identity[
      id(
        argument
      )
    ]

    local_body = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )
    evidence = (
      extract_toda_group_proof_narrative_argument_method_evidence(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )

    lines.append(
      (
        f"A{argument_index} "
        f"ordered_position={ordered_position} "
        f"role={role_value(argument.role)} "
        f"local_blocks="
        f"{tuple(block_index_by_identity[id(block)] for block in local_body)} "
        f"evidence_blocks="
        f"{tuple(block_index_by_identity[id(block)] for block in evidence)} "
        f"conclusion_block="
        f"{block_index_by_identity[id(argument.conclusion_block)]}"
      )
    )

    for block in local_body:
      block_index = block_index_by_identity[
        id(
          block
        )
      ]
      lines.append(
        (
          f"  B{block_index} "
          f"role={role_value(block.role)}"
        )
      )

      for proof_step in block.steps:
        rendered = (
          _render_generic_narrative_step(
            proof_step
          )
        )
        lines.append(
          (
            "    "
            + type(
              proof_step.conclusion
            ).__name__
            + " :: "
            + rendered
          )
        )

  lines.extend(
    (
      "",
      "C. RAW MARKDOWN BEFORE NUMBERING",
      "-" * 100,
      raw_markdown,
      "",
      "D. FINAL MARKDOWN AFTER NUMBERING",
      "-" * 100,
      final_markdown,
      "",
      "=" * 100,
    )
  )

  output_dir = (
    Path(__file__).resolve().parent
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )
  output_path = (
    output_dir
    / "pi6_3_equation_numbering.txt"
  )
  output_path.write_text(
    "\n".join(
      lines
    )
    + "\n",
    encoding="utf-8",
    newline="\n",
  )

  print(
    "\n".join(
      lines
    )
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
