from collections import Counter, defaultdict, deque
from dataclasses import dataclass

from audit_phase144_6_r5_23 import (
  _canonical_fact_targets,
  _step_contains_target,
)
from audit_phase144_6_r5_29 import (
  _anchored_chain_step_ids,
  _local_body,
  _provider_anchor_step_ids,
)
from audit_phase144_6_r5_34 import (
  VISIBILITY_GAP_KEYS,
  _effective_hidden_ids,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)


@dataclass(frozen=True)
class NecessityRecord:
  n: int
  k: int
  argument_index: int
  argument_role: str
  block_role: str
  statement_type: str
  provider_anchor: bool
  distance_to_conclusion: int | None
  on_any_anchor_path: bool
  necessary_for_any_anchor: bool
  necessary_anchor_count: int
  reachable_anchor_count: int


@dataclass(frozen=True)
class Pi6NecessityPlacement:
  key: str
  argument_index: int
  argument_role: str
  in_chain: bool
  hidden: bool
  provider_anchor: bool
  necessary_for_any_anchor: bool
  necessary_anchor_count: int
  reachable_anchor_count: int
  block_role: str | None
  statement_type: str | None
  distance_to_conclusion: int | None


def _forward_parents(presentation):
  result = defaultdict(list)
  for edge in presentation.edges:
    result[id(edge.premise_step)].append(edge.parent_step)
  return result


def _can_reach_conclusion(
  start_id,
  conclusion_id,
  parents,
  allowed_ids,
  removed_id=None,
):
  if start_id == removed_id:
    return False
  if start_id == conclusion_id:
    return True
  queue = deque([start_id])
  visited = {start_id}
  while queue:
    current = queue.popleft()
    for parent in parents.get(current, ()):
      parent_id = id(parent)
      if parent_id == removed_id:
        continue
      if parent_id not in allowed_ids:
        continue
      if parent_id == conclusion_id:
        return True
      if parent_id in visited:
        continue
      visited.add(parent_id)
      queue.append(parent_id)
  return False


def _necessity_for_chain(
  presentation,
  local_body,
  proof_chain,
  conclusion_step,
):
  chain_ids, anchors, distances = _anchored_chain_step_ids(
    presentation,
    local_body,
    proof_chain,
    conclusion_step,
  )
  parents = _forward_parents(presentation)
  conclusion_id = id(conclusion_step)
  allowed_ids = frozenset(chain_ids)
  reachable_anchors = tuple(
    anchor_id
    for anchor_id in anchors
    if _can_reach_conclusion(
      anchor_id,
      conclusion_id,
      parents,
      allowed_ids,
    )
  )
  necessity = {}
  for step_id in chain_ids:
    affected = tuple(
      anchor_id
      for anchor_id in reachable_anchors
      if (
        step_id != anchor_id
        and not _can_reach_conclusion(
          anchor_id,
          conclusion_id,
          parents,
          allowed_ids,
          removed_id=step_id,
        )
      )
    )
    necessity[step_id] = affected
  return chain_ids, anchors, distances, reachable_anchors, necessity


def build_hidden_anchored_necessity_inventory():
  rows = []
  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      aggregate_semantic_sidecar,
      proof_chains,
    ) = _context(n, k)
    for argument_index, argument in enumerate(arguments):
      conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
      if conclusion_step is None:
        continue
      body = _local_body(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
      hidden_ids = _effective_hidden_ids(
        presentation,
        blocks,
        body,
        semantic_sidecar,
        argument,
      )
      chain_ids, anchors, distances, reachable_anchors, necessity = (
        _necessity_for_chain(
          presentation,
          body,
          proof_chains[argument_index],
          conclusion_step,
        )
      )
      block_by_id = {
        id(step): block
        for block in body
        for step in block.steps
      }
      step_by_id = {
        id(step): step
        for block in body
        for step in block.steps
      }
      for step_id in chain_ids & hidden_ids:
        step = step_by_id.get(step_id)
        block = block_by_id.get(step_id)
        if step is None or block is None:
          continue
        affected = necessity.get(step_id, ())
        rows.append(
          NecessityRecord(
            n=n,
            k=k,
            argument_index=argument_index,
            argument_role=argument.role.value,
            block_role=block.role.value,
            statement_type=type(step.conclusion).__name__,
            provider_anchor=step_id in anchors,
            distance_to_conclusion=distances.get(step_id),
            on_any_anchor_path=bool(reachable_anchors),
            necessary_for_any_anchor=bool(affected),
            necessary_anchor_count=len(affected),
            reachable_anchor_count=len(reachable_anchors),
          )
        )
  return tuple(rows)


def build_pi6_gap_necessity():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)
  targets = _canonical_fact_targets()
  rows = []
  for argument_index, argument in enumerate(arguments):
    conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
    if conclusion_step is None:
      continue
    body = _local_body(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      argument_index,
    )
    hidden_ids = _effective_hidden_ids(
      presentation,
      blocks,
      body,
      semantic_sidecar,
      argument,
    )
    chain_ids, anchors, distances, reachable_anchors, necessity = (
      _necessity_for_chain(
        presentation,
        body,
        proof_chains[argument_index],
        conclusion_step,
      )
    )
    block_by_id = {
      id(step): block
      for block in body
      for step in block.steps
    }
    for key in VISIBILITY_GAP_KEYS:
      matches = tuple(
        dict.fromkeys(
          step
          for block in blocks
          for step in block.steps
          if _step_contains_target(step, targets[key])
        )
      )
      selected = next(
        (step for step in matches if id(step) in chain_ids),
        matches[0] if matches else None,
      )
      if selected is None:
        continue
      step_id = id(selected)
      block = block_by_id.get(step_id)
      affected = necessity.get(step_id, ())
      rows.append(
        Pi6NecessityPlacement(
          key=key,
          argument_index=argument_index,
          argument_role=argument.role.value,
          in_chain=step_id in chain_ids,
          hidden=step_id in hidden_ids,
          provider_anchor=step_id in anchors,
          necessary_for_any_anchor=bool(affected),
          necessary_anchor_count=len(affected),
          reachable_anchor_count=len(reachable_anchors),
          block_role=None if block is None else block.role.value,
          statement_type=type(selected.conclusion).__name__,
          distance_to_conclusion=distances.get(step_id),
        )
      )
  return tuple(rows)


def _top(counter, limit=40):
  return counter.most_common(limit)


def print_audit():
  inventory = build_hidden_anchored_necessity_inventory()
  pi6 = build_pi6_gap_necessity()

  print("=" * 78)
  print("Phase 144-6-R5-35 hidden anchored contribution necessity audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nA. pi_6^3 genuine visibility gaps: graph necessity")
  print("-" * 78)
  for row in pi6:
    print(
      f"{row.key}: argument={row.argument_index} role={row.argument_role} "
      f"in_chain={row.in_chain} hidden={row.hidden} anchor={row.provider_anchor} "
      f"necessary={row.necessary_for_any_anchor} "
      f"necessary_anchors={row.necessary_anchor_count}/"
      f"{row.reachable_anchor_count} block_role={row.block_role} "
      f"type={row.statement_type} distance={row.distance_to_conclusion}"
    )

  print("\\nB. Six-group necessity population")
  print("-" * 78)
  total_necessary = 0
  for n, k in TARGETS:
    rows = tuple(row for row in inventory if (row.n, row.k) == (n, k))
    necessary = sum(row.necessary_for_any_anchor for row in rows)
    total_necessary += necessary
    print(
      f"pi_{n + k}^{n}: hidden_anchored={len(rows)} "
      f"necessary={necessary} nonnecessary={len(rows)-necessary} "
      f"anchors={sum(row.provider_anchor for row in rows)}"
    )
  print(
    f"totals: hidden_anchored={len(inventory)} "
    f"necessary={total_necessary} "
    f"nonnecessary={len(inventory)-total_necessary}"
  )

  necessary_rows = tuple(
    row for row in inventory if row.necessary_for_any_anchor
  )
  print("\\nC. Necessary hidden contribution semantics")
  print("-" * 78)
  print("Block roles")
  for name, count in _top(Counter(row.block_role for row in necessary_rows)):
    print(f"{count:4d}  {name}")
  print("\\nStatement types")
  for name, count in _top(Counter(row.statement_type for row in necessary_rows)):
    print(f"{count:4d}  {name}")
  print("\\nArgument roles")
  for name, count in _top(Counter(row.argument_role for row in necessary_rows)):
    print(f"{count:4d}  {name}")
  print("\\nNecessary anchor counts")
  for count_value, count in sorted(
    Counter(row.necessary_anchor_count for row in necessary_rows).items()
  ):
    print(f"{count:4d}  {count_value}")

  print("\\nD. Necessary cross classification")
  print("-" * 78)
  cross = Counter(
    (
      row.argument_role,
      row.block_role,
      row.statement_type,
      "anchor" if row.provider_anchor else "chain",
    )
    for row in necessary_rows
  )
  for key, count in _top(cross):
    print(f"{count:4d}  {key}")

  print("\\nDecision boundary")
  print("-" * 78)
  print(
    "Graph necessity means: removing this hidden anchored step breaks every "
    "remaining provider-to-conclusion path for at least one currently "
    "reachable direct SUPPORTING_BLOCK provider anchor."
  )
  print(
    "This is a structural diagnostic, not yet a Narrative display rule. "
    "Direct provider anchors themselves are not marked necessary merely "
    "because removing the anchor removes its own path."
  )
  print(
    "No production frontier, renderer, ProofChain, ownership, deduplication, "
    "membership, parity matcher, or public route is changed."
  )


if __name__ == "__main__":
  print_audit()
