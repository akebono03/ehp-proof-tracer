from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = (
  ROOT
  / "toda_group_proof_narrative_argument_multi_renderer.py"
)

ORIGINAL_FUNCTION = 'def _toda_group_proof_narrative_argument_frontier_hidden_step_ids(\n  presentation: TodaGroupProofPresentation,\n  blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  local_body_blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,\n  argument: TodaGroupProofNarrativeArgument,\n) -> frozenset[\n  int\n]:\n  conclusion_step = (\n    extract_toda_group_proof_narrative_argument_conclusion_step(\n      argument\n    )\n  )\n\n  if conclusion_step is None:\n    return frozenset()\n\n  direct_premise_steps = list(\n    conclusion_step.premises\n  )\n\n  if (\n    argument.role\n    is TodaGroupProofNarrativeArgumentRole\n    .ESTABLISH_DEFINITION\n  ):\n    direct_premise_steps.extend(\n      semantic.prerequisite_step\n      for semantic in semantic_sidecar.dependency_semantics\n      if (\n        semantic.dependent_step\n        is conclusion_step\n      )\n    )\n\n  direct_premise_ids = {\n    id(\n      premise_step\n    )\n    for premise_step in direct_premise_steps\n  }\n  transition_step_ids = {\n    id(\n      step\n    )\n    for transition in (\n      extract_toda_group_proof_narrative_step_transitions(\n        presentation,\n        blocks,\n      )\n    )\n    for step in (\n      transition.source_step,\n      transition.target_step,\n    )\n  }\n\n  protected_step_ids = (\n    direct_premise_ids\n    | transition_step_ids\n    | {\n      id(\n        conclusion_step\n      )\n    }\n  )\n\n  if (\n    argument.role\n    is TodaGroupProofNarrativeArgumentRole\n    .ESTABLISH_DEFINITION\n  ):\n    for proof_step in direct_premise_steps:\n      protected_step_ids.update(\n        id(\n          premise_step\n        )\n        for premise_step in proof_step.premises\n      )\n\n  return frozenset(\n    id(\n      proof_step\n    )\n    for block in local_body_blocks\n    for proof_step in block.steps\n    if (\n      id(\n        proof_step\n      ) not in protected_step_ids\n      and not is_toda_group_proof_aggregate_statement(\n        proof_step.conclusion\n      )\n      and block.role\n      not in (\n        TodaGroupProofNarrativeMathematicalBlockRole\n        .EXACTNESS,\n        TodaGroupProofNarrativeMathematicalBlockRole\n        .REFERENCE,\n      )\n    )\n  )\n'


def main() -> int:
  source = TARGET.read_text(
    encoding="utf-8"
  )

  start_marker = (
    "def _toda_group_proof_narrative_argument_frontier_hidden_step_ids("
  )
  end_marker = (
    "\ndef render_toda_group_proof_narrative_multi_argument_markdown("
  )

  start = source.find(
    start_marker
  )
  if start < 0:
    raise RuntimeError(
      "frontier hidden helper not found"
    )

  end = source.find(
    end_marker,
    start,
  )
  if end < 0:
    raise RuntimeError(
      "frontier hidden helper end boundary not found"
    )

  updated = (
    source[:start]
    + ORIGINAL_FUNCTION
    + source[end:]
  )

  TARGET.write_text(
    updated,
    encoding="utf-8",
    newline="\n",
  )

  failed_test = (
    ROOT
    / "tests"
    / "test_phase159_pi4_3_repair2_frontier_prerequisite_protection.py"
  )

  if failed_test.exists():
    failed_test.unlink()

  print(
    "Phase 159 pi_4^3 repair2a rollback applied."
  )
  print(
    "Restored current frontier contract in "
    "toda_group_proof_narrative_argument_multi_renderer.py"
  )
  print(
    "Removed failed repair2 test file if present."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
