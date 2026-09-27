from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"


def main() -> int:
  source = TARGET.read_text(encoding="utf-8-sig")

  import_anchor = """from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
"""
  import_replacement = """from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_step_transitions import (
  extract_toda_group_proof_narrative_step_transitions,
)
"""
  if "extract_toda_group_proof_narrative_step_transitions" not in source:
    if import_anchor not in source:
      raise RuntimeError("step-transition import anchor not found")
    source = source.replace(import_anchor, import_replacement, 1)

  helper = """def _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
  presentation: TodaGroupProofPresentation,
  local_body_blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  argument: TodaGroupProofNarrativeArgument,
) -> frozenset[
  int
]:
  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )

  if conclusion_step is None:
    return frozenset()

  direct_premise_ids = {
    id(
      premise_step
    )
    for premise_step in conclusion_step.premises
  }
  transition_step_ids = {
    id(
      step
    )
    for transition in (
      extract_toda_group_proof_narrative_step_transitions(
        presentation,
        tuple(
          local_body_blocks
        ),
      )
    )
    for step in (
      transition.source_step,
      transition.target_step,
    )
  }

  protected_step_ids = (
    direct_premise_ids
    | transition_step_ids
    | {
      id(
        conclusion_step
      )
    }
  )

  if (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION
  ):
    for proof_step in tuple(
      premise_step
      for block in local_body_blocks
      for premise_step in block.steps
      if id(
        premise_step
      ) in direct_premise_ids
    ):
      protected_step_ids.update(
        id(
          premise_step
        )
        for premise_step in proof_step.premises
      )

  return frozenset(
    id(
      proof_step
    )
    for block in local_body_blocks
    for proof_step in block.steps
    if (
      id(
        proof_step
      ) not in protected_step_ids
      and block.role
      not in (
        TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS,
        TodaGroupProofNarrativeMathematicalBlockRole
        .REFERENCE,
      )
    )
  )
"""

  marker = "\ndef render_toda_group_proof_narrative_multi_argument_markdown("
  if helper.splitlines()[0] not in source:
    if marker not in source:
      raise RuntimeError("renderer insertion marker not found")
    source = source.replace(marker, "\n\n" + helper + marker, 1)

  anchor = """    context_hidden_step_ids = frozenset(
      id(
        proof_step
      )
      for block in local_body_blocks
      for proof_step in block.steps
      if (
        argument.role
        is not TodaGroupProofNarrativeArgumentRole
        .ESTABLISH_DEFINITION
        and isinstance(
          proof_step.conclusion,
          TodaEtaFamilyDefinitionStatement,
        )
      )
    )
"""
  addition = """    context_hidden_step_ids = (
      context_hidden_step_ids
      | _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
        presentation,
        local_body_blocks,
        argument,
      )
    )
"""
  if addition not in source:
    count = source.count(anchor)
    if count == 0:
      raise RuntimeError("context-hidden anchor not found")
    source = source.replace(anchor, anchor + addition)

  ast.parse(source)
  TARGET.write_text(source, encoding="utf-8")
  print("Phase 144-6-R4 frontier filter applied.")
  print("Changed only: toda_group_proof_narrative_argument_multi_renderer.py")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
