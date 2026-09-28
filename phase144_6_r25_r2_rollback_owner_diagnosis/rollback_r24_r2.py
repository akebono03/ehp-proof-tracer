from pathlib import Path

ROOT = Path.cwd()

main_path = ROOT / "main.py"
main_text = main_path.read_text(encoding="utf-8-sig")

r24_main = """    if (
      mode == "narrative"
      and max_depth is not None
    ):
      narrative_replay = (
        build_toda_group_result_proof_replay(
          group_result
        )
      )
      presentation = (
        build_toda_group_proof_presentation(
          narrative_replay
        )
      )
    else:
      presentation = (
        build_toda_group_proof_presentation(
          replay
        )
      )
"""

pre_r24_main = """    presentation = (
      build_toda_group_proof_presentation(
        replay
      )
    )
"""

if r24_main in main_text:
  main_text = main_text.replace(r24_main, pre_r24_main, 1)
elif pre_r24_main not in main_text:
  raise RuntimeError(
    "main.py is neither expected R24 nor pre-R24 state"
  )

main_path.write_text(main_text, encoding="utf-8")
print("main.py: pre-R24 state confirmed.")

multi_path = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"
multi_text = multi_path.read_text(encoding="utf-8-sig")

function_name = (
  "def _toda_group_proof_narrative_argument_frontier_hidden_step_ids("
)
start = multi_text.find(function_name)
if start < 0:
  raise RuntimeError("frontier hidden-step function not found")

next_function = multi_text.find("\ndef ", start + len(function_name))
if next_function < 0:
  raise RuntimeError("next function boundary not found")

current_function = multi_text[start:next_function].rstrip("\r\n")
canonical_function = 'def _toda_group_proof_narrative_argument_frontier_hidden_step_ids(\n  presentation: TodaGroupProofPresentation,\n  blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  local_body_blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,\n  argument: TodaGroupProofNarrativeArgument,\n) -> frozenset[\n  int\n]:\n  conclusion_step = (\n    extract_toda_group_proof_narrative_argument_conclusion_step(\n      argument\n    )\n  )\n\n  if conclusion_step is None:\n    return frozenset()\n\n  direct_premise_steps = list(\n    conclusion_step.premises\n  )\n\n  if (\n    argument.role\n    is TodaGroupProofNarrativeArgumentRole\n    .ESTABLISH_DEFINITION\n  ):\n    direct_premise_steps.extend(\n      semantic.prerequisite_step\n      for semantic in semantic_sidecar.dependency_semantics\n      if (\n        semantic.dependent_step\n        is conclusion_step\n      )\n    )\n\n  direct_premise_ids = {\n    id(\n      premise_step\n    )\n    for premise_step in direct_premise_steps\n  }\n  transition_step_ids = {\n    id(\n      step\n    )\n    for transition in (\n      extract_toda_group_proof_narrative_step_transitions(\n        presentation,\n        blocks,\n      )\n    )\n    for step in (\n      transition.source_step,\n      transition.target_step,\n    )\n  }\n\n  protected_step_ids = (\n    direct_premise_ids\n    | transition_step_ids\n    | {\n      id(\n        conclusion_step\n      )\n    }\n  )\n\n  for proof_step in direct_premise_steps:\n    protected_step_ids.update(\n      id(\n        premise_step\n      )\n      for premise_step in proof_step.premises\n    )\n\n  return frozenset(\n    id(\n      proof_step\n    )\n    for block in local_body_blocks\n    for proof_step in block.steps\n    if (\n      id(\n        proof_step\n      ) not in protected_step_ids\n      and not is_toda_group_proof_aggregate_statement(\n        proof_step.conclusion\n      )\n      and block.role\n      not in (\n        TodaGroupProofNarrativeMathematicalBlockRole\n        .EXACTNESS,\n        TodaGroupProofNarrativeMathematicalBlockRole\n        .REFERENCE,\n      )\n    )\n  )\n'.rstrip("\r\n")

if current_function != canonical_function:
  multi_text = (
    multi_text[:start]
    + canonical_function
    + multi_text[next_function:]
  )
  multi_path.write_text(multi_text, encoding="utf-8")
  print("multi renderer: restored complete pre-R24 function.")
else:
  print("multi renderer: pre-R24 function already present.")

print("No other production change was made.")
