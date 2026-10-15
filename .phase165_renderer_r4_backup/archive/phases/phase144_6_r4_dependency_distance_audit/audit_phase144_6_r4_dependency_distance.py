from collections import deque

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
  _argument_direct_dependency_indices,
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import build_toda_group_proof_narrative_blocks
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_sidecar
from toda_group_proof_narrative_step_transitions import extract_toda_group_proof_narrative_step_transitions
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step


report = build_standard_toda_report(n=3, k=3)
group_result = report.candidates[0].source_candidate.group_result
replay = build_toda_group_result_proof_replay(group_result, max_depth=3)
presentation = build_toda_group_proof_presentation(replay)
sidecar = build_toda_group_proof_narrative_semantic_sidecar(presentation)
blocks = build_toda_group_proof_narrative_blocks(
  presentation,
  semantic_sidecar=sidecar,
)
arguments = build_toda_group_proof_narrative_arguments(
  presentation,
  blocks,
  semantic_sidecar=sidecar,
)
deps = _argument_direct_dependency_indices(presentation, blocks, sidecar)
block_index = {id(block): i for i, block in enumerate(blocks)}

transition_step_ids = {
  id(step)
  for transition in extract_toda_group_proof_narrative_step_transitions(
    presentation,
    blocks,
  )
  for step in (transition.source_step, transition.target_step)
}


def distances_from(conclusion_index):
  distances = {conclusion_index: 0}
  queue = deque((conclusion_index,))
  while queue:
    current = queue.popleft()
    for dependency in deps[current]:
      candidate = distances[current] + 1
      if dependency in distances and distances[dependency] <= candidate:
        continue
      distances[dependency] = candidate
      queue.append(dependency)
  return distances


print("=" * 100)
print("Phase 144-6-R4 dependency-distance audit")
print("=" * 100)

for argument_index, argument in enumerate(arguments):
  conclusion_index = block_index[id(argument.conclusion_block)]
  distances = distances_from(conclusion_index)
  print()
  print(
    f"ARGUMENT {argument_index}: {argument.role.name}; "
    f"conclusion_block={conclusion_index}"
  )
  for index, block in enumerate(blocks):
    if index not in distances:
      continue
    for step in block.steps:
      print(
        f"d={distances[index]} | block={index}:{block.role.name} | "
        f"transition={id(step) in transition_step_ids} | "
        f"{type(step.conclusion).__name__}"
      )
      print("  " + _render_generic_narrative_step(step))
