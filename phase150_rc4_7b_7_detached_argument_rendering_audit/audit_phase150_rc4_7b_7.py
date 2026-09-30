from collections import Counter, deque

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_argument_discourse import (
  TodaGroupProofNarrativeArgumentDiscourseRole,
  classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  _argument_direct_dependency_indices,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_transitions import (
  extract_toda_group_proof_narrative_transitions,
)


CASES = (
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)


def _root_argument_indices(arguments):
  return tuple(
    index
    for index, argument in enumerate(arguments)
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_GROUP_STRUCTURE
      and argument.conclusion_block.role
      is TodaGroupProofNarrativeMathematicalBlockRole.TARGET
    )
  )


def _child_reachable(arguments, roots):
  reachable = set()
  queue = deque(roots)
  while queue:
    index = queue.popleft()
    if index in reachable:
      continue
    reachable.add(index)
    queue.extend(arguments[index].child_argument_indices)
  return frozenset(reachable)


def _dependency_reaches(
  direct_dependencies,
  start_block_index,
  target_block_index,
):
  queue = deque((start_block_index,))
  visited = set()
  while queue:
    index = queue.popleft()
    if index in visited:
      continue
    visited.add(index)
    if index == target_block_index:
      return True
    queue.extend(direct_dependencies[index])
  return False


def _dependency_path(
  direct_dependencies,
  start_block_index,
  target_block_index,
):
  queue = deque(((start_block_index, (start_block_index,)),))
  visited = set()
  while queue:
    index, path = queue.popleft()
    if index in visited:
      continue
    visited.add(index)
    if index == target_block_index:
      return path
    for dependency_index in direct_dependencies[index]:
      queue.append(
        (
          dependency_index,
          path + (dependency_index,),
        )
      )
  return ()


def audit_case(label, n, k):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(n, k)

  ordered = order_toda_group_proof_narrative_arguments(arguments)
  discourse_roles = classify_toda_group_proof_narrative_argument_discourse_roles(
    arguments
  )
  source_index_by_identity = {
    id(argument): index
    for index, argument in enumerate(arguments)
  }
  block_index_by_identity = {
    id(block): index
    for index, block in enumerate(blocks)
  }
  direct_dependencies = _argument_direct_dependency_indices(
    presentation,
    blocks,
    sidecar,
  )
  roots = _root_argument_indices(arguments)
  child_reachable = _child_reachable(arguments, roots)
  transitions = extract_toda_group_proof_narrative_transitions(
    presentation,
    blocks,
    arguments,
  )
  transition_by_target_id = {
    id(transition.target_block): transition
    for transition in transitions
  }

  counts = Counter()

  print("=" * 112)
  print(label)
  print("=" * 112)
  print(f"blocks={len(blocks)}")
  print(f"arguments={len(arguments)}")
  print(f"root_argument_indices={roots}")
  print(f"child_reachable_indices={tuple(sorted(child_reachable))}")
  print()

  for ordered_position, argument in enumerate(ordered):
    argument_index = source_index_by_identity[id(argument)]
    discourse_role = discourse_roles[ordered_position]
    conclusion_block_index = block_index_by_identity[
      id(argument.conclusion_block)
    ]
    conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
    transition = transition_by_target_id.get(
      id(argument.conclusion_block)
    )
    local_body = extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )

    root_dependency_paths = []
    for root_index in roots:
      root_block_index = block_index_by_identity[
        id(arguments[root_index].conclusion_block)
      ]
      path = _dependency_path(
        direct_dependencies,
        root_block_index,
        conclusion_block_index,
      )
      if path:
        root_dependency_paths.append(
          (root_index, path)
        )

    if discourse_role is TodaGroupProofNarrativeArgumentDiscourseRole.DETACHED:
      if root_dependency_paths:
        classification = "DETACHED_BUT_ROOT_DEPENDENCY_REACHABLE"
      else:
        classification = "DETACHED_AND_ROOT_DEPENDENCY_UNREACHABLE"
    else:
      classification = "MAIN_ARGUMENT"

    counts[classification] += 1

    print(f"ARGUMENT A{argument_index:02d}")
    print(f"  ordered_position={ordered_position}")
    print(f"  role={argument.role.value}")
    print(f"  discourse_role={discourse_role.value}")
    print(f"  classification={classification}")
    print(f"  conclusion_block_index=B{conclusion_block_index:02d}")
    print(f"  conclusion_step_present={conclusion_step is not None}")
    print(f"  child_argument_indices={argument.child_argument_indices}")
    print(f"  child_reachable_from_root={argument_index in child_reachable}")
    print(
      "  transition_role="
      + (
        "NONE"
        if transition is None
        else transition.role.value
      )
    )
    print(
      "  transition_source_roles="
      + repr(
        ()
        if transition is None
        else tuple(
          block.role.value
          for block in transition.source_blocks
        )
      )
    )
    print(f"  local_body_count={len(local_body)}")
    print(
      "  local_body_roles="
      + repr(
        tuple(block.role.value for block in local_body)
      )
    )
    print(
      "  root_dependency_paths="
      + repr(root_dependency_paths)
    )

    for root_index, path in root_dependency_paths:
      print(
        f"    ROOT_PATH root=A{root_index:02d} "
        f"blocks={tuple('B%02d' % index for index in path)}"
      )

    print()

  print(f"CASE_CLASSIFICATION_COUNTS={dict(counts)}")
  print()
  return counts


def main():
  total = Counter()

  print("Phase 150 RC4-7B-7 Detached Argument Rendering Audit")
  print("Production changes: none")
  print(
    "Scope: discourse DETACHED classification, child reachability, "
    "and root block-dependency reachability."
  )
  print()

  for label, n, k in CASES:
    total.update(audit_case(label, n, k))

  print("=" * 112)
  print("CROSS-GROUP SUMMARY")
  print("=" * 112)
  print(f"CLASSIFICATION_COUNTS={dict(total)}")
  detached_reachable = total[
    "DETACHED_BUT_ROOT_DEPENDENCY_REACHABLE"
  ]
  detached_unreachable = total[
    "DETACHED_AND_ROOT_DEPENDENCY_UNREACHABLE"
  ]
  print(
    "DETACHED_BUT_ROOT_DEPENDENCY_REACHABLE_TOTAL="
    f"{detached_reachable}"
  )
  print(
    "DETACHED_AND_ROOT_DEPENDENCY_UNREACHABLE_TOTAL="
    f"{detached_unreachable}"
  )

  if detached_reachable:
    print(
      "AUDIT_DECISION="
      "DETACHED_POLICY_OR_ARGUMENT_HANDOFF_REPAIR_REQUIRED"
    )
  elif detached_unreachable:
    print(
      "AUDIT_DECISION="
      "DETACHED_ARGUMENTS_ARE_GRAPH_DISCONNECTED_REVIEW_OWNERSHIP"
    )
  else:
    print(
      "AUDIT_DECISION="
      "NO_DETACHED_ARGUMENT_RENDERING_GAP_FOUND"
    )


if __name__ == "__main__":
  main()
