from __future__ import annotations

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_narrative_step_transitions import (
  extract_toda_group_proof_narrative_step_transitions,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)

TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


def group_result(n, k):
  report = build_standard_toda_report(n=n, k=k)
  return report.candidates[0].source_candidate.group_result


def summarize(n, k, depth):
  result = group_result(n, k)
  replay = build_toda_group_result_proof_replay(
    result,
    max_depth=depth,
  )
  presentation = build_toda_group_proof_presentation(replay)
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    presentation
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
  )
  transitions = extract_toda_group_proof_narrative_step_transitions(
    presentation,
    blocks,
  )

  roles = tuple(argument.role.value for argument in arguments)
  block_roles = tuple(block.role.value for block in blocks)

  return {
    "nodes": len(presentation.nodes),
    "edges": len(presentation.edges),
    "blocks": len(blocks),
    "arguments": len(arguments),
    "argument_roles": roles,
    "block_roles": block_roles,
    "semantic_dependencies": len(sidecar.dependency_semantics),
    "step_transitions": len(transitions),
  }


print("=" * 120)
print("Phase 144-6-R5 Narrative depth policy audit")
print("=" * 120)

for n, k in TARGETS:
  print()
  print("-" * 120)
  print(f"TARGET n={n}, k={k}")
  print("-" * 120)

  previous = None
  for depth in range(0, 6):
    try:
      data = summarize(n, k, depth)
    except Exception as exc:
      print(
        f"depth={depth}: ERROR "
        f"{type(exc).__name__}: {exc}"
      )
      continue

    changed = (
      previous is None
      or data != previous
    )
    print(
      f"depth={depth}: "
      f"nodes={data['nodes']} "
      f"edges={data['edges']} "
      f"blocks={data['blocks']} "
      f"arguments={data['arguments']} "
      f"semantic_dependencies={data['semantic_dependencies']} "
      f"step_transitions={data['step_transitions']} "
      f"changed={changed}"
    )
    print(
      "  argument_roles="
      + repr(data["argument_roles"])
    )

    role_counts = {}
    for role in data["block_roles"]:
      role_counts[role] = role_counts.get(role, 0) + 1
    print(
      "  block_role_counts="
      + repr(role_counts)
    )

    previous = data

print()
print("=" * 120)
print("pi_6^3 replay node depths")
print("=" * 120)

result = group_result(3, 3)
replay = build_toda_group_result_proof_replay(
  result,
  max_depth=8,
)
for index, node in enumerate(replay.steps):
  print(
    f"S{index:02d} depth={node.depth} "
    f"role={node.role.value} "
    f"statement={node.proof_step.conclusion!r}"
  )
