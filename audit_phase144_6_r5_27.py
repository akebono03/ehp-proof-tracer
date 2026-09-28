from collections import deque
from dataclasses import dataclass

from audit_phase144_6_r5_23 import (
  _canonical_fact_targets,
  _step_contains_target,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
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


REQUIRED_FRONTIER_KEYS = (
  "pi5_3_group",
  "pi7_5_group",
  "hopf_pi7_surjective",
  "delta_zero",
)


@dataclass(frozen=True)
class ReleasedStep:
  n: int
  k: int
  argument_index: int
  block_role: str
  statement_type: str
  rendered: str


@dataclass(frozen=True)
class BoundedPathImpact:
  n: int
  k: int
  argument_count: int
  hidden_local_steps: int
  hidden_path_steps: int
  max_hidden_path_distance: int | None
  roles: tuple[str, ...]


@dataclass(frozen=True)
class RequiredFactCoverage:
  key: str
  argument_index: int
  distance: int | None
  selected_by_bounded_path: bool


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


def build_step_dedup_released_steps():
  released = []

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

        displayable = tuple(
          step for step in block.steps if id(step) not in hidden
        )

        if id(block) in seen_blocks:
          for step in displayable:
            if id(step) in seen_steps:
              continue
            released.append(
              ReleasedStep(
                n=n,
                k=k,
                argument_index=argument_index,
                block_role=block.role.value,
                statement_type=type(step.conclusion).__name__,
                rendered=_render_generic_narrative_step(step),
              )
            )

        seen_blocks.add(id(block))
        seen_steps.update(id(step) for step in displayable)

  return tuple(released)


def _reverse_raw_distances(presentation, conclusion_step):
  premises_by_parent = {}
  for edge in presentation.edges:
    premises_by_parent.setdefault(
      id(edge.parent_step), []
    ).append(edge.premise_step)

  distances = {id(conclusion_step): 0}
  queue = deque([conclusion_step])

  while queue:
    parent = queue.popleft()
    next_distance = distances[id(parent)] + 1
    for premise in premises_by_parent.get(id(parent), ()):
      premise_id = id(premise)
      if premise_id in distances:
        continue
      distances[premise_id] = next_distance
      queue.append(premise)

  return distances


def build_bounded_path_impacts():
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

    hidden_local_ids = set()
    hidden_path_ids = set()
    hidden_path_distances = []
    roles = []

    for argument_index, argument in enumerate(arguments):
      conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
      if conclusion_step is None:
        continue
      distances = _reverse_raw_distances(presentation, conclusion_step)
      hidden = _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
        presentation,
        blocks,
        local_bodies[argument_index],
        semantic_sidecar,
        argument,
      )
      hidden_local_ids.update(hidden)

      for block in local_bodies[argument_index]:
        for step in block.steps:
          step_id = id(step)
          if step_id not in hidden or step_id not in distances:
            continue
          hidden_path_ids.add(step_id)
          hidden_path_distances.append(distances[step_id])
          roles.append(block.role.value)

    impacts.append(
      BoundedPathImpact(
        n=n,
        k=k,
        argument_count=len(arguments),
        hidden_local_steps=len(hidden_local_ids),
        hidden_path_steps=len(hidden_path_ids),
        max_hidden_path_distance=(
          max(hidden_path_distances) if hidden_path_distances else None
        ),
        roles=tuple(dict.fromkeys(roles)),
      )
    )

  return tuple(impacts)


def build_required_fact_coverage():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)
  local_bodies = _local_bodies(
    presentation, blocks, semantic_sidecar, arguments
  )
  targets = _canonical_fact_targets()
  coverage = []

  for argument_index, argument in enumerate(arguments):
    conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
    if conclusion_step is None:
      continue
    distances = _reverse_raw_distances(presentation, conclusion_step)
    hidden = _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      local_bodies[argument_index],
      semantic_sidecar,
      argument,
    )
    local_ids = {
      id(step)
      for block in local_bodies[argument_index]
      for step in block.steps
    }

    for key in REQUIRED_FRONTIER_KEYS:
      matching = tuple(
        dict.fromkeys(
          step
          for block in blocks
          for step in block.steps
          if _step_contains_target(step, targets[key])
        )
      )
      selected = tuple(
        step
        for step in matching
        if (
          id(step) in local_ids
          and id(step) in hidden
          and id(step) in distances
        )
      )
      selected_distances = tuple(
        distances[id(step)] for step in selected
      )
      coverage.append(
        RequiredFactCoverage(
          key=key,
          argument_index=argument_index,
          distance=(
            min(selected_distances)
            if selected_distances
            else None
          ),
          selected_by_bounded_path=bool(selected),
        )
      )

  return tuple(coverage)


def print_audit():
  released = build_step_dedup_released_steps()
  impacts = build_bounded_path_impacts()
  coverage = build_required_fact_coverage()

  print("=" * 78)
  print("Phase 144-6-R5-27 bounded derivation visibility + step-dedup production readiness audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nA. All steps released by hypothetical step-level deduplication")
  print("-" * 78)
  print(f"released_step_occurrences={len(released)}")
  for item in released:
    print(
      f"pi_{item.n + item.k}^{item.n}: argument={item.argument_index} "
      f"block={item.block_role} statement={item.statement_type}"
    )
    print(f"  {item.rendered}")

  print("\\nB. Local-body-bounded hidden derivation-path impact")
  print("-" * 78)
  total_hidden = 0
  total_path = 0
  for impact in impacts:
    total_hidden += impact.hidden_local_steps
    total_path += impact.hidden_path_steps
    print(
      f"pi_{impact.n + impact.k}^{impact.n}: "
      f"arguments={impact.argument_count} "
      f"hidden_local={impact.hidden_local_steps} "
      f"hidden_on_path={impact.hidden_path_steps} "
      f"max_distance={impact.max_hidden_path_distance} "
      f"roles={','.join(impact.roles) or '-'}"
    )
  print(
    f"totals: hidden_local={total_hidden} "
    f"hidden_on_path={total_path}"
  )

  print("\\nC. Required pi_6^3 fact coverage")
  print("-" * 78)
  for item in coverage:
    print(
      f"{item.key}: argument={item.argument_index} "
      f"selected={item.selected_by_bounded_path} "
      f"distance={item.distance}"
    )

  print("\\nD. Production-readiness observations")
  print("-" * 78)
  pi6_released = tuple(
    item for item in released if (item.n, item.k) == (3, 3)
  )
  pi6_required_selected = {
    item.key
    for item in coverage
    if item.selected_by_bounded_path
  }
  print(f"pi6_step_dedup_released={len(pi6_released)}")
  print(
    "pi6_bounded_path_required_keys="
    + ",".join(sorted(pi6_required_selected))
  )
  print(
    "step_dedup_ready_for_implementation="
    + str(len(released) <= 12 and len(pi6_released) == 2)
  )
  print(
    "bounded_path_covers_all_required_frontier_facts="
    + str(pi6_required_selected == set(REQUIRED_FRONTIER_KEYS))
  )
  print(
    "No production change is made here. A bounded-path rule is acceptable "
    "only if its six-group impact is small enough to review explicitly."
  )
  print(
    "Embedded nu-prime eta_6 membership remains a separate generic rule."
  )


if __name__ == "__main__":
  print_audit()
