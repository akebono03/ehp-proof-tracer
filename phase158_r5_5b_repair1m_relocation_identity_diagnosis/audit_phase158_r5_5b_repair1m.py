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

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_body_renderer import (
  _relocatable_toda_group_proof_narrative_direct_derivation_premises,
  _step_derivation_sources_by_target_id,
)
from toda_group_proof_narrative_argument_direct_premises import (
  extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)


def describe_step(
  prefix: str,
  proof_step,
) -> str:
  return (
    prefix
    + f"id={id(proof_step)} "
    + f"type={type(proof_step.conclusion).__name__} "
    + _render_generic_narrative_step(
      proof_step
    )
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

  order_argument_index = next(
    index
    for index, argument in enumerate(
      arguments
    )
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_ORDER
    )
  )
  argument = arguments[
    order_argument_index
  ]
  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )
  direct_premises = (
    extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
      argument,
      arguments,
    )
  )
  support_steps = tuple(
    support_step
    for premise_step in direct_premises
    for support_step in premise_step.premises
    if all(
      support_step is not existing_step
      for existing_step in direct_premises
    )
  )
  sources_by_target_id = (
    _step_derivation_sources_by_target_id(
      presentation,
      blocks,
    )
  )
  transition_source_ids = {
    id(
      source_step
    )
    for source_steps in sources_by_target_id.values()
    for source_step in source_steps
  }
  local_body_blocks = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      order_argument_index,
    )
  )
  conclusion_block = next(
    block
    for block in blocks
    if (
      conclusion_step is not None
      and conclusion_step in block.steps
    )
  )
  relocatable = (
    _relocatable_toda_group_proof_narrative_direct_derivation_premises(
      direct_premises + support_steps,
      sources_by_target_id,
      conclusion_block,
    )
  )
  relocatable_ids = {
    id(
      step
    )
    for step in relocatable
  }

  lines = [
    "=" * 100,
    "Phase 158-R5-5b repair1m - relocation identity diagnosis",
    "=" * 100,
    "",
    f"order_argument_index={order_argument_index}",
    f"conclusion_block_role={conclusion_block.role.value}",
    "",
    "A. ORDER CONCLUSION",
    "-" * 100,
  ]

  if conclusion_step is None:
    lines.append(
      "None"
    )
  else:
    lines.append(
      describe_step(
        "",
        conclusion_step,
      )
    )

  lines.extend(
    (
      "",
      "B. DIRECT PREMISES",
      "-" * 100,
    )
  )

  for index, step in enumerate(
    direct_premises
  ):
    lines.append(
      describe_step(
        f"P{index} ",
        step,
      )
    )
    lines.append(
      (
        "  transition_source="
        + str(
          id(
            step
          )
          in transition_source_ids
        )
        + " incoming_sources="
        + str(
          tuple(
            id(
              source
            )
            for source in sources_by_target_id.get(
              id(
                step
              ),
              (),
            )
          )
        )
        + " relocatable="
        + str(
          id(
            step
          )
          in relocatable_ids
        )
      )
    )

  lines.extend(
    (
      "",
      "C. SUPPORT STEPS",
      "-" * 100,
    )
  )

  for index, step in enumerate(
    support_steps
  ):
    lines.append(
      describe_step(
        f"S{index} ",
        step,
      )
    )
    lines.append(
      (
        "  transition_source="
        + str(
          id(
            step
          )
          in transition_source_ids
        )
        + " incoming_sources="
        + str(
          tuple(
            id(
              source
            )
            for source in sources_by_target_id.get(
              id(
                step
              ),
              (),
            )
          )
        )
        + " relocatable="
        + str(
          id(
            step
          )
          in relocatable_ids
        )
      )
    )

  lines.extend(
    (
      "",
      "D. CALCULATION TRANSITIONS",
      "-" * 100,
    )
  )

  for block_index, block in enumerate(
    blocks
  ):
    if (
      block.role
      is not TodaGroupProofNarrativeMathematicalBlockRole
      .CALCULATION
    ):
      continue

    lines.append(
      f"B{block_index}"
    )

    for step_index, target_step in enumerate(
      block.steps
    ):
      source_steps = sources_by_target_id.get(
        id(
          target_step
        ),
        (),
      )

      lines.append(
        describe_step(
          f"  T{step_index} ",
          target_step,
        )
      )
      lines.append(
        (
          "    sources="
          + str(
            tuple(
              id(
                source
              )
              for source in source_steps
            )
          )
        )
      )

      for source in source_steps:
        lines.append(
          describe_step(
            "      <- ",
            source,
          )
        )

  lines.extend(
    (
      "",
      "E. ORDER ARGUMENT LOCAL BLOCKS",
      "-" * 100,
    )
  )

  block_index_by_id = {
    id(
      block
    ): index
    for index, block in enumerate(
      blocks
    )
  }

  for block in local_body_blocks:
    block_index = block_index_by_id[
      id(
        block
      )
    ]
    lines.append(
      f"B{block_index} role={block.role.value}"
    )

    for step in block.steps:
      lines.append(
        describe_step(
          "  ",
          step,
        )
      )

  lines.extend(
    (
      "",
      "F. RELOCATABLE RESULT",
      "-" * 100,
    )
  )

  for index, step in enumerate(
    relocatable
  ):
    lines.append(
      describe_step(
        f"R{index} ",
        step,
      )
    )

  lines.extend(
    (
      "",
      "=" * 100,
      "Production changes: none",
      "Repository-wide pytest: not run",
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
  (
    output_dir
    / "pi6_relocation_identity.txt"
  ).write_text(
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
