from __future__ import annotations

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
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


def build_state(n, k, depth):
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
  depth_by_step_id = {
    id(replay_step.proof_step): replay_step.depth
    for replay_step in replay.steps
  }

  rows = []
  all_visible_ids = set()

  for argument_index, argument in enumerate(arguments):
    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )
    hidden_ids = (
      _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
        presentation,
        blocks,
        local_body_blocks,
        sidecar,
        argument,
      )
    )
    local_step_ids = {
      id(step)
      for block in local_body_blocks
      for step in block.steps
    }
    visible_ids = local_step_ids - set(hidden_ids)
    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )
    if conclusion_step is not None:
      visible_ids.add(id(conclusion_step))

    visible_depths = tuple(
      sorted(
        {
          depth_by_step_id[step_id]
          for step_id in visible_ids
          if step_id in depth_by_step_id
        }
      )
    )
    required_depth = (
      max(visible_depths)
      if visible_depths
      else None
    )
    all_visible_ids.update(visible_ids)

    rows.append(
      {
        "index": argument_index,
        "role": argument.role.value,
        "local_steps": len(local_step_ids),
        "visible_steps": len(visible_ids),
        "visible_depths": visible_depths,
        "required_depth": required_depth,
      }
    )

  narrative_required_depth = (
    max(
      depth_by_step_id[step_id]
      for step_id in all_visible_ids
      if step_id in depth_by_step_id
    )
    if all_visible_ids
    else 0
  )

  signature = tuple(
    (
      row["role"],
      row["visible_steps"],
      row["visible_depths"],
      row["required_depth"],
    )
    for row in rows
  )

  return {
    "replay": replay,
    "presentation": presentation,
    "arguments": arguments,
    "rows": rows,
    "required_depth": narrative_required_depth,
    "signature": signature,
  }


print("=" * 118)
print("Phase 144-6-R5-2 Narrative frontier required-depth audit")
print("=" * 118)
print(
  "NOTE: visible frontier is computed by the CURRENT local R4 helper; "
  "this audit does not define a second filtering policy."
)

for n, k in TARGETS:
  print()
  print("-" * 118)
  print(f"TARGET n={n}, k={k}")
  print("-" * 118)

  states = []
  for depth in range(0, 7):
    try:
      state = build_state(n, k, depth)
    except Exception as exc:
      print(
        f"depth={depth}: ERROR "
        f"{type(exc).__name__}: {exc}"
      )
      states.append(None)
      continue

    states.append(state)
    next_signature_changed = None
    print(
      f"depth={depth}: "
      f"replay_steps={len(state['replay'].steps)} "
      f"arguments={len(state['arguments'])} "
      f"frontier_required_depth={state['required_depth']}"
    )
    for row in state["rows"]:
      print(
        "  "
        f"A{row['index']:02d} "
        f"role={row['role']} "
        f"local={row['local_steps']} "
        f"visible={row['visible_steps']} "
        f"visible_depths={row['visible_depths']} "
        f"required={row['required_depth']}"
      )

  print()
  print("successive frontier-signature changes:")
  for depth in range(0, len(states) - 1):
    current = states[depth]
    following = states[depth + 1]
    if current is None or following is None:
      print(f"  {depth}->{depth + 1}: unavailable")
      continue
    print(
      f"  {depth}->{depth + 1}: "
      f"{current['signature'] != following['signature']}"
    )

print()
print("=" * 118)
print("Interpretation aid")
print("=" * 118)
print(
  "A fixed max_depth is justified only if the same value works "
  "structurally across targets. Otherwise the next design must derive "
  "Narrative depth from visible frontier/completeness, not n/k."
)
print(
  "If frontier signatures keep changing after the first apparently "
  "readable depth, required-depth alone is not yet a stopping criterion; "
  "a completeness/stability condition is also needed."
)
