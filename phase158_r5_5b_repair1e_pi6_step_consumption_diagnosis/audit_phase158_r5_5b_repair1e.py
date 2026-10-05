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
  render_toda_group_proof_narrative_argument_body_markdown,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_exposure import (
  classify_toda_group_proof_narrative_exactness_component_exposure,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
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

  block_index_by_identity = {
    id(
      block
    ): index
    for index, block in enumerate(
      blocks
    )
  }

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

  transitions = (
    extract_toda_group_proof_narrative_step_transitions(
      presentation,
      blocks,
    )
  )
  transition_step_ids = {
    id(
      transition.source_step
    )
    for transition in transitions
  } | {
    id(
      transition.target_step
    )
    for transition in transitions
  }

  lines = [
    "=" * 100,
    "Phase 158-R5-5b repair1e - pi6 step-consumption diagnosis",
    "=" * 100,
    "",
    "A. CALCULATION BLOCK INVENTORY",
    "-" * 100,
  ]

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
      f"B{block_index} role=calculation"
    )

    for step_index, proof_step in enumerate(
      block.steps
    ):
      lines.append(
        (
          f"  S{step_index} "
          f"id={id(proof_step)} "
          f"transition_participant="
          f"{id(proof_step) in transition_step_ids} "
          f"type={type(proof_step.conclusion).__name__}"
        )
      )
      lines.append(
        "    "
        + _render_generic_narrative_step(
          proof_step
        )
      )

  lines.extend(
    (
      "",
      "B. ARGUMENT-BY-ARGUMENT CONSUMPTION",
      "-" * 100,
    )
  )

  seen_non_exact_block_ids = set()
  seen_non_exact_step_ids = set()

  for ordered_position, argument in enumerate(
    ordered_arguments
  ):
    argument_index = source_index_by_identity[
      id(
        argument
      )
    ]
    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
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
    components = (
      build_toda_group_proof_narrative_exactness_method_components(
        evidence
      )
    )
    relevant_groups = (
      extract_toda_group_proof_narrative_argument_relevant_groups(
        presentation,
        blocks,
        argument,
      )
    )
    exactness_exposure_by_block_id = {}

    for component in components:
      exposure = (
        classify_toda_group_proof_narrative_exactness_component_exposure(
          relevant_groups,
          components,
          component,
        )
      )

      for evidence_block in component.evidence_blocks:
        exactness_exposure_by_block_id[
          id(
            evidence_block
          )
        ] = exposure

    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )
    local_body_block_ids = {
      id(
        block
      )
      for block in local_body_blocks
    }
    evidence_block_ids = {
      id(
        block
      )
      for block in evidence
    }

    if (
      argument.conclusion_block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .TARGET
    ):
      missing_evidence_blocks = tuple(
        block
        for block in blocks
        if (
          id(
            block
          ) in evidence_block_ids
          and id(
            block
          ) not in local_body_block_ids
        )
      )

      if missing_evidence_blocks:
        conclusion_position = next(
          (
            index
            for index, block in enumerate(
              local_body_blocks
            )
            if block is argument.conclusion_block
          ),
          len(
            local_body_blocks
          ),
        )
        local_body_blocks = (
          local_body_blocks[
            :conclusion_position
          ]
          + missing_evidence_blocks
          + local_body_blocks[
            conclusion_position:
          ]
        )
    else:
      local_body_blocks = tuple(
        block
        for block in blocks
        if (
          id(
            block
          ) in local_body_block_ids
          or id(
            block
          ) in evidence_block_ids
        )
      )

    lines.append(
      (
        f"A{argument_index} "
        f"ordered_position={ordered_position} "
        f"role={role_value(argument.role)} "
        f"conclusion_block="
        f"{block_index_by_identity[id(argument.conclusion_block)]}"
      )
    )
    lines.append(
      "  seen_before="
      + repr(
        tuple(
          sorted(
            seen_non_exact_step_ids
          )
        )
      )
    )
    lines.append(
      (
        "  local_blocks="
        + repr(
          tuple(
            block_index_by_identity[
              id(
                block
              )
            ]
            for block in local_body_blocks
          )
        )
      )
    )

    for block in local_body_blocks:
      block_index = block_index_by_identity[
        id(
          block
        )
      ]

      if (
        block.role
        is TodaGroupProofNarrativeMathematicalBlockRole
        .CALCULATION
      ):
        lines.append(
          f"  calculation B{block_index}:"
        )

        for proof_step in block.steps:
          lines.append(
            (
              "    "
              + (
                "EXCLUDED"
                if id(
                  proof_step
                ) in seen_non_exact_step_ids
                else "VISIBLE"
              )
              + " id="
              + str(
                id(
                  proof_step
                )
              )
              + " :: "
              + _render_generic_narrative_step(
                proof_step
              )
            )
          )

    body = (
      render_toda_group_proof_narrative_argument_body_markdown(
        presentation,
        blocks,
        local_body_blocks,
        None,
        exactness_exposure_by_block_id=exactness_exposure_by_block_id,
        excluded_non_exact_block_ids=frozenset(
          seen_non_exact_block_ids
        ),
        excluded_non_exact_step_ids=frozenset(
          seen_non_exact_step_ids
        ),
        excluded_exactness_contribution_keys=frozenset(),
        connector_before_block_id=None,
        connector_text=None,
        conclusion_step=None,
        direct_derivation_premises=(),
        direct_derivation_support_steps=(),
        context_hidden_step_ids=frozenset(),
        preserve_provenance_block_ids=frozenset(),
      )
    )

    lines.append(
      "  BODY:"
    )

    for body_line in body.splitlines():
      lines.append(
        "    "
        + body_line
      )

    for block in local_body_blocks:
      if (
        block.role
        is TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      ):
        continue

      visible_step_ids = {
        id(
          proof_step
        )
        for proof_step in block.steps
        if id(
          proof_step
        ) not in seen_non_exact_step_ids
      }

      seen_non_exact_step_ids.update(
        visible_step_ids
      )

      if (
        len(
          visible_step_ids
        )
        == len(
          block.steps
        )
      ):
        seen_non_exact_block_ids.add(
          id(
            block
          )
        )

    lines.append(
      "  seen_after="
      + repr(
        tuple(
          sorted(
            seen_non_exact_step_ids
          )
        )
      )
    )
    lines.append(
      ""
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
    / "pi6_3_step_consumption.txt"
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
