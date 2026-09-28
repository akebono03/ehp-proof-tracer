from collections import defaultdict, deque
from dataclasses import dataclass

from audit_phase144_6_r5_23 import (
  _canonical_fact_targets,
  _step_contains_target,
)
from audit_phase144_6_r5_28 import (
  MISSING_6_KEYS,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_proof_chains import (
  TodaGroupProofNarrativeProofChainProviderKind,
)


@dataclass(frozen=True)
class ContributionChainAudit:
  n: int
  k: int
  argument_index: int
  argument_role: str
  local_steps: int
  provider_anchor_steps: int
  chain_steps: int
  chain_blocks: int
  max_distance_to_conclusion: int | None


@dataclass(frozen=True)
class MissingFactChainPlacement:
  key: str
  argument_index: int
  argument_role: str
  in_chain: bool
  provider_anchor: bool
  distance_to_conclusion: int | None


def _local_body(
  presentation,
  blocks,
  semantic_sidecar,
  arguments,
  argument_index,
):
  return extract_toda_group_proof_narrative_argument_local_body_blocks(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    argument_index,
  )


def _premises_by_parent(presentation):
  result = defaultdict(list)
  for edge in presentation.edges:
    result[id(edge.parent_step)].append(edge.premise_step)
  return result


def _reverse_distances(presentation, conclusion_step):
  premises = _premises_by_parent(presentation)
  distances = {id(conclusion_step): 0}
  queue = deque([conclusion_step])

  while queue:
    parent = queue.popleft()
    distance = distances[id(parent)] + 1
    for premise in premises.get(id(parent), ()):
      premise_id = id(premise)
      if premise_id in distances:
        continue
      distances[premise_id] = distance
      queue.append(premise)

  return distances


def _provider_anchor_step_ids(proof_chain):
  return {
    id(step)
    for provider in proof_chain.providers
    if (
      provider.kind
      is TodaGroupProofNarrativeProofChainProviderKind.SUPPORTING_BLOCK
    )
    for step in provider.supporting_block.steps
  }


def _forward_parents(presentation):
  result = defaultdict(list)
  for edge in presentation.edges:
    result[id(edge.premise_step)].append(edge.parent_step)
  return result


def _anchored_chain_step_ids(
  presentation,
  local_body_blocks,
  proof_chain,
  conclusion_step,
):
  local_ids = {
    id(step)
    for block in local_body_blocks
    for step in block.steps
  }
  anchors = _provider_anchor_step_ids(proof_chain) & local_ids
  distances = _reverse_distances(presentation, conclusion_step)
  parents = _forward_parents(presentation)

  chain_ids = {id(conclusion_step)}
  queue = deque(
    step
    for block in local_body_blocks
    for step in block.steps
    if id(step) in anchors
  )
  visited = set(anchors)

  while queue:
    step = queue.popleft()
    step_id = id(step)
    if step_id not in distances:
      continue
    chain_ids.add(step_id)

    for parent in parents.get(step_id, ()):
      parent_id = id(parent)
      if parent_id not in local_ids:
        continue
      if parent_id not in distances:
        continue
      if distances[parent_id] >= distances[step_id]:
        continue
      chain_ids.add(parent_id)
      if parent_id in visited:
        continue
      visited.add(parent_id)
      queue.append(parent)

  return frozenset(chain_ids), frozenset(anchors), distances


def build_six_group_chain_inventory():
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
      chain_ids, anchors, distances = _anchored_chain_step_ids(
        presentation,
        body,
        proof_chains[argument_index],
        conclusion_step,
      )
      local_steps = tuple(
        step for block in body for step in block.steps
      )
      block_by_step_id = {
        id(step): block
        for block in body
        for step in block.steps
      }
      chain_distances = tuple(
        distances[step_id]
        for step_id in chain_ids
        if step_id in distances
      )
      rows.append(
        ContributionChainAudit(
          n=n,
          k=k,
          argument_index=argument_index,
          argument_role=argument.role.value,
          local_steps=len(local_steps),
          provider_anchor_steps=len(anchors),
          chain_steps=len(chain_ids),
          chain_blocks=len({
            id(block_by_step_id[step_id])
            for step_id in chain_ids
            if step_id in block_by_step_id
          }),
          max_distance_to_conclusion=(
            max(chain_distances) if chain_distances else None
          ),
        )
      )

  return tuple(rows)


def build_pi6_missing6_chain_placements():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)
  targets = _canonical_fact_targets()
  placements = []

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
    chain_ids, anchors, distances = _anchored_chain_step_ids(
      presentation,
      body,
      proof_chains[argument_index],
      conclusion_step,
    )

    for key in MISSING_6_KEYS:
      matching_steps = tuple(
        dict.fromkeys(
          step
          for block in blocks
          for step in block.steps
          if _step_contains_target(step, targets[key])
        )
      )
      matching_chain = tuple(
        step for step in matching_steps if id(step) in chain_ids
      )
      matching_anchor = tuple(
        step for step in matching_steps if id(step) in anchors
      )
      matching_distances = tuple(
        distances[id(step)]
        for step in matching_steps
        if id(step) in distances
      )
      placements.append(
        MissingFactChainPlacement(
          key=key,
          argument_index=argument_index,
          argument_role=argument.role.value,
          in_chain=bool(matching_chain),
          provider_anchor=bool(matching_anchor),
          distance_to_conclusion=(
            min(matching_distances)
            if matching_distances
            else None
          ),
        )
      )

  return tuple(placements)


def print_audit():
  inventory = build_six_group_chain_inventory()
  placements = build_pi6_missing6_chain_placements()

  print("=" * 78)
  print("Phase 144-6-R5-29 Narrative contribution-chain ownership audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nA. pi_6^3 missing-6 placement in provider-anchored chains")
  print("-" * 78)
  for row in placements:
    print(
      f"{row.key}: argument={row.argument_index} "
      f"role={row.argument_role} "
      f"in_chain={row.in_chain} "
      f"provider_anchor={row.provider_anchor} "
      f"distance={row.distance_to_conclusion}"
    )

  print("\\nB. Six-group provider-anchored chain inventory")
  print("-" * 78)
  totals = [0, 0, 0]
  for n, k in TARGETS:
    group_rows = tuple(
      row for row in inventory if (row.n, row.k) == (n, k)
    )
    local = sum(row.local_steps for row in group_rows)
    anchors = sum(row.provider_anchor_steps for row in group_rows)
    chains = sum(row.chain_steps for row in group_rows)
    totals[0] += local
    totals[1] += anchors
    totals[2] += chains
    max_distance = max(
      (
        row.max_distance_to_conclusion or 0
        for row in group_rows
      ),
      default=0,
    )
    print(
      f"pi_{n + k}^{n}: arguments={len(group_rows)} "
      f"local_step_occurrences={local} "
      f"provider_anchor_occurrences={anchors} "
      f"chain_step_occurrences={chains} "
      f"max_distance={max_distance}"
    )
  print(
    f"totals: local_step_occurrences={totals[0]} "
    f"provider_anchor_occurrences={totals[1]} "
    f"chain_step_occurrences={totals[2]}"
  )

  print("\\nC. pi_6^3 chain ownership summary")
  print("-" * 78)
  for argument_index in range(3):
    rows = tuple(
      row for row in placements if row.argument_index == argument_index
    )
    if not rows:
      continue
    print(
      f"argument={argument_index} role={rows[0].argument_role} "
      f"missing6_in_chain="
      f"{sum(row.in_chain for row in rows)}/6 "
      f"missing6_provider_anchors="
      f"{sum(row.provider_anchor for row in rows)}/6"
    )

  print("\\nDecision boundary")
  print("-" * 78)
  print(
    "A provider-anchored contribution chain is diagnostic only. "
    "It starts from direct SUPPORTING_BLOCK provider steps and follows "
    "existing presentation parent edges toward the Argument conclusion, "
    "without traversing outside the current local body."
  )
  print(
    "If missing internal facts lie on the same anchored chain while the "
    "six-group chain inventory stays substantially smaller than all local "
    "body occurrences, contribution-chain ownership is a viable next design."
  )
  print(
    "No production ownership, renderer, frontier, deduplication, ProofChain, "
    "or membership rule is changed."
  )


if __name__ == "__main__":
  print_audit()
