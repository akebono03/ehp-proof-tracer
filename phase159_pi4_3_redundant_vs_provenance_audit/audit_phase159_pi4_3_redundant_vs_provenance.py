from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_argument_direct_premises import (
  extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_transition_by_conclusion_id,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_group_structure_semantics import (
  extract_toda_group_structure_narrative_redundant_direct_premise_step_ids,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransitionRole,
  extract_toda_group_proof_narrative_transitions,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGET_RULE = (
  "Toda pi_4^3 finite cyclic quotient calculation"
)


def build_data():
  report = build_standard_toda_report(
    n=3,
    k=1,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
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

  return (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
  )


def rule_name(
  proof_step,
) -> str:
  if proof_step.inference_rule is not None:
    return proof_step.inference_rule.name

  if hasattr(
    proof_step.rule,
    "value",
  ):
    return proof_step.rule.value

  return str(
    proof_step.rule
  )


def main() -> int:
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
  ) = build_data()

  argument = next(
    argument
    for argument in arguments
    if (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
      is presentation.root_step
    )
  )
  argument_index = arguments.index(
    argument
  )
  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )
  direct_derivation_premises = (
    extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
      argument,
      arguments,
    )
  )
  redundant_ids = (
    extract_toda_group_structure_narrative_redundant_direct_premise_step_ids(
      conclusion_step
    )
  )

  transitions = (
    extract_toda_group_proof_narrative_transitions(
      presentation,
      blocks,
      arguments,
    )
  )
  transition_by_conclusion_id = (
    _toda_group_proof_narrative_argument_transition_by_conclusion_id(
      presentation,
      blocks,
      arguments,
    )
  )
  root_transition = (
    transition_by_conclusion_id.get(
      id(
        argument.conclusion_block
      )
    )
  )

  derivation_source_block_ids = (
    frozenset()
    if (
      root_transition is None
      or root_transition.role
      is not TodaGroupProofNarrativeTransitionRole.DERIVATION
    )
    else frozenset(
      id(
        source_block
      )
      for source_block in root_transition.source_blocks
    )
  )

  block_by_step_id = {
    id(
      proof_step
    ): block
    for block in blocks
    for proof_step in block.steps
  }
  block_index_by_id = {
    id(
      block
    ): index
    for index, block in enumerate(
      blocks
    )
  }

  target_step = next(
    proof_step
    for proof_step in direct_derivation_premises
    if rule_name(
      proof_step
    )
    == TARGET_RULE
  )
  target_block = block_by_step_id[
    id(
      target_step
    )
  ]

  local_body_blocks = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      argument_index,
    )
  )

  lines = [
    "# Phase 159 pi4_3 redundant-vs-provenance audit",
    "",
    "target_rule: "
    + TARGET_RULE,
    "",
    "## Target step",
    "",
    "step_id: "
    + str(
      id(
        target_step
      )
    ),
    "block_index: "
    + str(
      block_index_by_id[
        id(
          target_block
        )
      ]
    ),
    "block_role: "
    + str(
      getattr(
        target_block.role,
        "value",
        target_block.role,
      )
    ),
    "is_redundant_direct_premise: "
    + str(
      id(
        target_step
      )
      in redundant_ids
    ),
    "block_is_preserve_provenance: "
    + str(
      id(
        target_block
      )
      in derivation_source_block_ids
    ),
    "block_is_local_body: "
    + str(
      target_block
      in local_body_blocks
    ),
    "",
    "## Root transition",
    "",
    "transition_exists: "
    + str(
      root_transition is not None
    ),
  ]

  if root_transition is not None:
    lines.extend(
      (
        "transition_role: "
        + str(
          getattr(
            root_transition.role,
            "value",
            root_transition.role,
          )
        ),
        "source_block_indices: "
        + repr(
          tuple(
            block_index_by_id[
              id(
                source_block
              )
            ]
            for source_block in root_transition.source_blocks
          )
        ),
        "target_block_index: "
        + str(
          block_index_by_id[
            id(
              root_transition.target_block
            )
          ]
        ),
      )
    )

  lines.extend(
    (
      "",
      "## Derivation-source blocks",
      "",
    )
  )

  for source_block_id in derivation_source_block_ids:
    source_block = next(
      block
      for block in blocks
      if id(
        block
      )
      == source_block_id
    )
    lines.append(
      "block "
      + str(
        block_index_by_id[
          source_block_id
        ]
      )
      + ": role="
      + str(
        getattr(
          source_block.role,
          "value",
          source_block.role,
        )
      )
    )

    for proof_step in source_block.steps:
      lines.append(
        "  step: "
        + rule_name(
          proof_step
        )
        + " | redundant="
        + str(
          id(
            proof_step
          )
          in redundant_ids
        )
      )

  lines.extend(
    (
      "",
      "## All direct derivation premises",
      "",
    )
  )

  for proof_step in direct_derivation_premises:
    block = block_by_step_id[
      id(
        proof_step
      )
    ]
    lines.append(
      rule_name(
        proof_step
      )
      + " | block="
      + str(
        block_index_by_id[
          id(
            block
          )
        ]
      )
      + " | redundant="
      + str(
        id(
          proof_step
        )
        in redundant_ids
      )
      + " | preserve="
      + str(
        id(
          block
        )
        in derivation_source_block_ids
      )
    )

  lines.extend(
    (
      "",
      "## Interpretation",
      "",
      "If target step is redundant=True and preserve=True, "
      "the duplicate survives because the provenance-preservation "
      "exception overrides redundant-direct-premise suppression.",
      "",
      "If redundant=True and preserve=False, the remaining duplicate "
      "must come from another body path and this audit is not sufficient.",
      "",
    )
  )

  report = "\n".join(
    lines
  )

  output_path = (
    Path(__file__).resolve().parent
    / "phase159_pi4_3_redundant_vs_provenance_audit.txt"
  )
  output_path.write_text(
    report,
    encoding="utf-8",
  )

  print(
    report
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
