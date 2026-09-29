from dataclasses import dataclass
from collections import deque

from audit_phase144_6_r5_23 import (
  _canonical_fact_targets,
  _step_contains_target,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)


FRONTIER_KEYS = (
  "pi5_3_group",
  "pi7_5_group",
  "hopf_pi7_surjective",
  "delta_zero",
)


@dataclass(frozen=True)
class StepDedupImpact:
  n: int
  k: int
  shared_non_exact_block_occurrences: int
  block_policy_suppressed_steps: int
  step_policy_still_suppressed_steps: int
  step_policy_released_steps: int


@dataclass(frozen=True)
class DerivationPathTrace:
  key: str
  argument_index: int
  argument_role: str
  hidden_by_frontier: bool
  on_raw_premise_path_to_conclusion: bool
  raw_distance_to_conclusion: int | None
  on_semantic_augmented_path_to_conclusion: bool
  semantic_augmented_distance: int | None


def _local_bodies(presentation, blocks, semantic_sidecar, arguments):
  return tuple(
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      i,
    )
    for i in range(len(arguments))
  )


def build_step_dedup_impacts():
  impacts = []

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      aggregate_semantic_sidecar,
      proof_chains,
    ) = _context(n, k)

    local_bodies = _local_bodies(
      presentation, blocks, semantic_sidecar, arguments
    )
    ordered = order_toda_group_proof_narrative_arguments(arguments)
    source_index = {id(argument): i for i, argument in enumerate(arguments)}
    ordered_indices = tuple(source_index[id(a)] for a in ordered)

    seen_blocks = set()
    seen_steps = set()
    shared_occurrences = 0
    block_suppressed = 0
    step_suppressed = 0
    released = 0

    for argument_index in ordered_indices:
      body = local_bodies[argument_index]
      hidden = _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
        presentation,
        blocks,
        body,
        semantic_sidecar,
        arguments[argument_index],
      )

      for block in body:
        if block.role is TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS:
          continue

        displayable_step_ids = tuple(
          id(step)
          for step in block.steps
          if id(step) not in hidden
        )

        if id(block) in seen_blocks:
          shared_occurrences += 1
          block_suppressed += len(displayable_step_ids)
          already_seen = sum(
            step_id in seen_steps
            for step_id in displayable_step_ids
          )
          step_suppressed += already_seen
          released += len(displayable_step_ids) - already_seen

        seen_blocks.add(id(block))
        seen_steps.update(displayable_step_ids)

    impacts.append(
      StepDedupImpact(
        n=n,
        k=k,
        shared_non_exact_block_occurrences=shared_occurrences,
        block_policy_suppressed_steps=block_suppressed,
        step_policy_still_suppressed_steps=step_suppressed,
        step_policy_released_steps=released,
      )
    )

  return tuple(impacts)


def _reverse_distance_map(presentation, semantic_sidecar, conclusion_step, augmented):
  prerequisites_by_dependent = {}

  for edge in presentation.edges:
    prerequisites_by_dependent.setdefault(
      id(edge.parent_step), []
    ).append(edge.premise_step)

  if augmented:
    for semantic in semantic_sidecar.dependency_semantics:
      prerequisites_by_dependent.setdefault(
        id(semantic.dependent_step), []
      ).append(semantic.prerequisite_step)

  distance = {id(conclusion_step): 0}
  queue = deque([conclusion_step])

  while queue:
    dependent = queue.popleft()
    next_distance = distance[id(dependent)] + 1
    for prerequisite in prerequisites_by_dependent.get(id(dependent), ()):
      prerequisite_id = id(prerequisite)
      if prerequisite_id in distance:
        continue
      distance[prerequisite_id] = next_distance
      queue.append(prerequisite)

  return distance


def build_derivation_path_traces():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)
  targets = _canonical_fact_targets()
  local_bodies = _local_bodies(
    presentation, blocks, semantic_sidecar, arguments
  )

  traces = []

  for argument_index, argument in enumerate(arguments):
    conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
    if conclusion_step is None:
      continue

    raw_distances = _reverse_distance_map(
      presentation, semantic_sidecar, conclusion_step, False
    )
    augmented_distances = _reverse_distance_map(
      presentation, semantic_sidecar, conclusion_step, True
    )
    hidden = _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      local_bodies[argument_index],
      semantic_sidecar,
      argument,
    )

    for key in FRONTIER_KEYS:
      target = targets[key]
      matching_steps = tuple(
        dict.fromkeys(
          step
          for block in blocks
          for step in block.steps
          if _step_contains_target(step, target)
        )
      )
      if not matching_steps:
        continue

      raw_values = [
        raw_distances[id(step)]
        for step in matching_steps
        if id(step) in raw_distances
      ]
      augmented_values = [
        augmented_distances[id(step)]
        for step in matching_steps
        if id(step) in augmented_distances
      ]

      traces.append(
        DerivationPathTrace(
          key=key,
          argument_index=argument_index,
          argument_role=argument.role.value,
          hidden_by_frontier=any(id(step) in hidden for step in matching_steps),
          on_raw_premise_path_to_conclusion=bool(raw_values),
          raw_distance_to_conclusion=min(raw_values) if raw_values else None,
          on_semantic_augmented_path_to_conclusion=bool(augmented_values),
          semantic_augmented_distance=(
            min(augmented_values) if augmented_values else None
          ),
        )
      )

  return tuple(traces)


def print_audit():
  impacts = build_step_dedup_impacts()
  traces = build_derivation_path_traces()

  print("=" * 78)
  print("Phase 144-6-R5-26 step-level deduplication + derivation-path relevance audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nA. Hypothetical step-level deduplication impact")
  print("-" * 78)
  totals = [0, 0, 0, 0]
  for impact in impacts:
    totals[0] += impact.shared_non_exact_block_occurrences
    totals[1] += impact.block_policy_suppressed_steps
    totals[2] += impact.step_policy_still_suppressed_steps
    totals[3] += impact.step_policy_released_steps
    print(
      f"pi_{impact.n + impact.k}^{impact.n}: "
      f"shared_blocks={impact.shared_non_exact_block_occurrences} "
      f"block_suppressed={impact.block_policy_suppressed_steps} "
      f"step_still_suppressed={impact.step_policy_still_suppressed_steps} "
      f"step_released={impact.step_policy_released_steps}"
    )
  print(
    "totals: "
    f"shared_blocks={totals[0]} "
    f"block_suppressed={totals[1]} "
    f"step_still_suppressed={totals[2]} "
    f"step_released={totals[3]}"
  )

  print("\\nB. pi_6^3 frontier facts on derivation paths")
  print("-" * 78)
  for trace in traces:
    print(
      f"{trace.key}: argument={trace.argument_index} "
      f"role={trace.argument_role} hidden={trace.hidden_by_frontier} "
      f"raw_path={trace.on_raw_premise_path_to_conclusion} "
      f"raw_distance={trace.raw_distance_to_conclusion} "
      f"augmented_path={trace.on_semantic_augmented_path_to_conclusion} "
      f"augmented_distance={trace.semantic_augmented_distance}"
    )

  print("\\nC. Path classification summary")
  print("-" * 78)
  for key in FRONTIER_KEYS:
    key_traces = tuple(trace for trace in traces if trace.key == key)
    print(
      f"{key}: "
      f"raw_path_arguments="
      f"{sum(t.on_raw_premise_path_to_conclusion for t in key_traces)} "
      f"augmented_path_arguments="
      f"{sum(t.on_semantic_augmented_path_to_conclusion for t in key_traces)} "
      f"hidden_arguments={sum(t.hidden_by_frontier for t in key_traces)}"
    )

  print("\\nDecision boundary")
  print("-" * 78)
  print(
    "This audit does not replace block-level deduplication. It only measures "
    "the hypothetical difference between block identity and visible-step identity."
  )
  print(
    "This audit does not change frontier visibility. A derivation-path rule "
    "is production-ready only if it explains the required facts without "
    "opening broad unrelated closures."
  )
  print(
    "Embedded nu-prime eta_6 membership remains outside this audit."
  )


if __name__ == "__main__":
  print_audit()
