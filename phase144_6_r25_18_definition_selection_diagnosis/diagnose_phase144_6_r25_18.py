from toda_calculation_facade import build_standard_toda_report
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_narrative_blocks import build_toda_group_proof_narrative_blocks
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)


def describe(label, presentation):
  closure = build_toda_group_proof_narrative_semantic_closure_presentation(
    presentation
  )
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    closure
  )
  blocks = build_toda_group_proof_narrative_blocks(
    closure,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    closure,
    blocks,
    semantic_sidecar=sidecar,
  )

  print("=" * 78)
  print(label)
  print("=" * 78)
  print("input max_depth:", presentation.max_depth)
  print("input nodes:", len(presentation.nodes))
  print("closure max_depth:", closure.max_depth)
  print("closure nodes:", len(closure.nodes))
  print("blocks:", len(blocks))
  print("step semantics:")
  for semantic in sidecar.step_semantics:
    print(
      "  ",
      semantic.role.value,
      type(semantic.proof_step.conclusion).__name__,
      repr(semantic.proof_step.conclusion),
    )
  print("dependency semantics:")
  for semantic in sidecar.dependency_semantics:
    print(
      "  ",
      semantic.role.value,
      "prerequisite=",
      type(semantic.prerequisite_step.conclusion).__name__,
      "dependent=",
      type(semantic.dependent_step.conclusion).__name__,
    )
  print("arguments:")
  for index, argument in enumerate(arguments):
    conclusion = extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
    print(
      f"  [{index}] role={argument.role.value}",
      f"children={argument.child_argument_indices}",
      "conclusion=",
      None if conclusion is None else type(conclusion.conclusion).__name__,
    )

  return closure, sidecar, blocks, arguments


report = build_standard_toda_report(n=3, k=3)
group_result = report.candidates[0].source_candidate.group_result

depth2 = build_toda_group_proof_presentation(
  build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
)
full = build_toda_group_proof_presentation(
  build_toda_group_result_proof_replay(
    group_result
  )
)

describe("DEPTH=2 + SEMANTIC CLOSURE", depth2)
describe("FULL + SEMANTIC CLOSURE", full)
