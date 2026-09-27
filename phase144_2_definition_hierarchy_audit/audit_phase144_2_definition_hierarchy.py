from collections import deque
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  _argument_dependency_closure_indices,
  _argument_direct_dependency_indices,
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_blocks import build_toda_group_proof_narrative_blocks
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_sidecar
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay

TARGETS = ((3, 3, "nu-prime"), (5, 7, "sigma triple-prime / nu_n"), (9, 7, "sigma_9 / sigma triple-prime"))

def _shortest_block_path(direct, start, goal):
  queue = deque(((start, (start,)),))
  visited = {start}
  while queue:
    current, path = queue.popleft()
    if current == goal:
      return path
    for dependency in direct[current]:
      if dependency in visited:
        continue
      visited.add(dependency)
      queue.append((dependency, path + (dependency,)))
  return None

def main():
  for n, k, label in TARGETS:
    report = build_standard_toda_report(n=n, k=k)
    group_result = report.candidates[0].source_candidate.group_result
    replay = build_toda_group_result_proof_replay(group_result, max_depth=3)
    presentation = build_toda_group_proof_presentation(replay)
    sidecar = build_toda_group_proof_narrative_semantic_sidecar(presentation)
    blocks = build_toda_group_proof_narrative_blocks(presentation, semantic_sidecar=sidecar)
    arguments = build_toda_group_proof_narrative_arguments(presentation, blocks, semantic_sidecar=sidecar)
    direct = _argument_direct_dependency_indices(presentation, blocks, sidecar)
    block_index_by_identity = {id(block): index for index, block in enumerate(blocks)}
    argument_index_by_block_index = {
      block_index_by_identity[id(argument.conclusion_block)]: index
      for index, argument in enumerate(arguments)
    }
    print("=" * 100)
    print(f"n={n}, k={k}, target=pi_{n + k}^{n}, label={label}")
    for definition_index, definition_argument in enumerate(arguments):
      if definition_argument.role is not TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION:
        continue
      definition_block_index = block_index_by_identity[id(definition_argument.conclusion_block)]
      subject = extract_toda_group_proof_narrative_argument_purpose_subject(definition_argument)
      print("-" * 100)
      print(f"definition_argument_index={definition_index}")
      print(f"subject={getattr(subject, 'name', subject)!r}")
      print(f"definition_block_index={definition_block_index}")
      print("consuming_arguments:")
      found = False
      for consumer_index, consumer_argument in enumerate(arguments):
        if consumer_index == definition_index:
          continue
        consumer_block_index = block_index_by_identity[id(consumer_argument.conclusion_block)]
        closure = _argument_dependency_closure_indices(direct, consumer_block_index)
        if definition_block_index not in closure:
          continue
        found = True
        path = _shortest_block_path(direct, consumer_block_index, definition_block_index)
        intermediate = tuple(
          argument_index_by_block_index[block_index]
          for block_index in path[1:-1]
          if block_index in argument_index_by_block_index
        )
        print(
          f"  consumer_argument_index={consumer_index}, "
          f"role={consumer_argument.role.value}, "
          f"direct_child={definition_index in consumer_argument.child_argument_indices}, "
          f"block_path={path}, "
          f"intermediate_argument_indices={intermediate}"
        )
      if not found:
        print("  <NONE>")
    print()

if __name__ == "__main__":
  main()
