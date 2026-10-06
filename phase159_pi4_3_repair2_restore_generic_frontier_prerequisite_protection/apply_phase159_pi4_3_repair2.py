from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = (
  ROOT
  / "toda_group_proof_narrative_argument_multi_renderer.py"
)
TEST = (
  ROOT
  / "tests"
  / "test_phase159_pi4_3_repair2_frontier_prerequisite_protection.py"
)

NEW_FUNCTION = 'def _toda_group_proof_narrative_argument_frontier_hidden_step_ids(\n  presentation: TodaGroupProofPresentation,\n  blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  local_body_blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,\n  argument: TodaGroupProofNarrativeArgument,\n) -> frozenset[\n  int\n]:\n  conclusion_step = (\n    extract_toda_group_proof_narrative_argument_conclusion_step(\n      argument\n    )\n  )\n\n  if conclusion_step is None:\n    return frozenset()\n\n  direct_premise_steps = list(\n    conclusion_step.premises\n  )\n\n  if (\n    argument.role\n    is TodaGroupProofNarrativeArgumentRole\n    .ESTABLISH_DEFINITION\n  ):\n    direct_premise_steps.extend(\n      semantic.prerequisite_step\n      for semantic in semantic_sidecar.dependency_semantics\n      if (\n        semantic.dependent_step\n        is conclusion_step\n      )\n    )\n\n  direct_premise_ids = {\n    id(\n      premise_step\n    )\n    for premise_step in direct_premise_steps\n  }\n  transition_step_ids = {\n    id(\n      step\n    )\n    for transition in (\n      extract_toda_group_proof_narrative_step_transitions(\n        presentation,\n        blocks,\n      )\n    )\n    for step in (\n      transition.source_step,\n      transition.target_step,\n    )\n  }\n\n  protected_step_ids = (\n    direct_premise_ids\n    | transition_step_ids\n    | {\n      id(\n        conclusion_step\n      )\n    }\n  )\n\n  for proof_step in direct_premise_steps:\n    protected_step_ids.update(\n      id(\n        premise_step\n      )\n      for premise_step in proof_step.premises\n    )\n\n  return frozenset(\n    id(\n      proof_step\n    )\n    for block in local_body_blocks\n    for proof_step in block.steps\n    if (\n      id(\n        proof_step\n      ) not in protected_step_ids\n      and not is_toda_group_proof_aggregate_statement(\n        proof_step.conclusion\n      )\n      and block.role\n      not in (\n        TodaGroupProofNarrativeMathematicalBlockRole\n        .EXACTNESS,\n        TodaGroupProofNarrativeMathematicalBlockRole\n        .REFERENCE,\n      )\n    )\n  )\n'
TEST_TEXT = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_argument_local_body import (\n  extract_toda_group_proof_narrative_argument_local_body_blocks,\n)\nfrom toda_group_proof_narrative_argument_multi_renderer import (\n  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,\n  render_toda_group_proof_narrative_multi_argument_markdown,\n)\nfrom toda_group_proof_narrative_arguments import (\n  build_toda_group_proof_narrative_arguments,\n)\nfrom toda_group_proof_narrative_blocks import (\n  build_toda_group_proof_narrative_blocks,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n  build_toda_group_proof_narrative_semantic_sidecar,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\nfrom toda_rules import (\n  TodaEtaFamilyDefinitionStatement,\n  TodaSuspensionKernelFreeCyclicStatement,\n  TodaSuspensionSurjectiveStatement,\n)\n\n\ndef _phase159_repair2_pi4_3_narrative_data():\n  report = build_standard_toda_report(\n    n=3,\n    k=1,\n  )\n\n  group_result = (\n    report.candidates[0]\n    .source_candidate\n    .group_result\n  )\n\n  replay = (\n    build_toda_group_result_proof_replay(\n      group_result,\n      max_depth=2,\n    )\n  )\n\n  presentation = (\n    build_toda_group_proof_presentation(\n      replay\n    )\n  )\n\n  presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      presentation\n    )\n  )\n\n  sidecar = (\n    build_toda_group_proof_narrative_semantic_sidecar(\n      presentation\n    )\n  )\n\n  blocks = (\n    build_toda_group_proof_narrative_blocks(\n      presentation,\n      sidecar,\n    )\n  )\n\n  arguments = (\n    build_toda_group_proof_narrative_arguments(\n      presentation,\n      blocks,\n      sidecar,\n    )\n  )\n\n  assert len(arguments) == 1\n\n  local_body_blocks = (\n    extract_toda_group_proof_narrative_argument_local_body_blocks(\n      presentation,\n      blocks,\n      sidecar,\n      arguments,\n      0,\n    )\n  )\n\n  hidden_ids = (\n    _toda_group_proof_narrative_argument_frontier_hidden_step_ids(\n      presentation,\n      blocks,\n      local_body_blocks,\n      sidecar,\n      arguments[0],\n    )\n  )\n\n  return (\n    presentation,\n    blocks,\n    sidecar,\n    arguments,\n    local_body_blocks,\n    hidden_ids,\n  )\n\n\ndef test_phase159_repair2_protects_group_structure_direct_premise_prerequisites():\n  (\n    presentation,\n    blocks,\n    sidecar,\n    arguments,\n    local_body_blocks,\n    hidden_ids,\n  ) = _phase159_repair2_pi4_3_narrative_data()\n\n  protected_steps = tuple(\n    step\n    for block in local_body_blocks\n    for step in block.steps\n    if (\n      isinstance(\n        step.conclusion,\n        TodaSuspensionKernelFreeCyclicStatement,\n      )\n      or isinstance(\n        step.conclusion,\n        TodaSuspensionSurjectiveStatement,\n      )\n    )\n  )\n\n  assert protected_steps\n  assert all(\n    id(step) not in hidden_ids\n    for step in protected_steps\n  )\n\n\ndef test_phase159_repair2_keeps_internal_eta_definition_hidden():\n  (\n    presentation,\n    blocks,\n    sidecar,\n    arguments,\n    local_body_blocks,\n    hidden_ids,\n  ) = _phase159_repair2_pi4_3_narrative_data()\n\n  eta_definition_steps = tuple(\n    step\n    for block in local_body_blocks\n    for step in block.steps\n    if isinstance(\n      step.conclusion,\n      TodaEtaFamilyDefinitionStatement,\n    )\n  )\n\n  assert eta_definition_steps\n  assert all(\n    id(step) in hidden_ids\n    for step in eta_definition_steps\n  )\n\n\ndef test_phase159_repair2_pi4_3_markdown_exposes_kernel_and_surjectivity():\n  (\n    presentation,\n    blocks,\n    sidecar,\n    arguments,\n    local_body_blocks,\n    hidden_ids,\n  ) = _phase159_repair2_pi4_3_narrative_data()\n\n  rendered = (\n    render_toda_group_proof_narrative_multi_argument_markdown(\n      presentation,\n      blocks,\n      sidecar,\n      arguments,\n    )\n  )\n\n  assert (\n    "Toda pi_4^3 exactness "\n    "Delta image equals E kernel"\n    in rendered\n  )\n  assert (\n    r"E: \\pi_{3}^{2} \\to "\n    r"\\pi_{4}^{3}"\n    in rendered\n  )\n  assert (\n    r"\\pi_{3}^{2} = "\n    r"\\mathbb{Z}\\{\\eta_{2}\\}"\n    in rendered\n  )\n  assert (\n    "TodaEtaFamilyDefinitionStatement"\n    not in rendered\n  )\n'


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

  if TEST.exists():
    raise RuntimeError(
      "repair2 test already exists"
    )

  updated = (
    source[:start]
    + NEW_FUNCTION
    + source[end:]
  )

  TARGET.write_text(
    updated,
    encoding="utf-8",
    newline="\n",
  )

  TEST.write_text(
    TEST_TEXT,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159 pi_4^3 repair2 applied."
  )
  print(
    "Changed: "
    "toda_group_proof_narrative_argument_multi_renderer.py"
  )
  print(
    "Changed helper: "
    "_toda_group_proof_narrative_argument_frontier_hidden_step_ids()"
  )
  print(
    "Added: tests/"
    "test_phase159_pi4_3_repair2_frontier_prerequisite_protection.py"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
