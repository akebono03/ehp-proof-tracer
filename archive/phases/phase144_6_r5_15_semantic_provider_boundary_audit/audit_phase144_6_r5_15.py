from dataclasses import dataclass
from enum import Enum

from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  Relation,
  RelationType,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
  extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
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
from toda_proof_dependency import (
  extract_toda_recursive_proof_provenance,
)
from toda_rules import (
  Toda48Pi16_9OrderAndE4InjectiveStatement,
  Toda515Sigma8TransportedDecompositionStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  Toda56Nu4DecompositionStatement,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


class BoundaryAction(Enum):
  EXPAND = "expand"
  REFERENCE = "reference"
  STRUCTURAL = "structural"
  INTERNAL = "internal"


@dataclass(frozen=True)
class Component:
  kind: str
  target_group: object
  generator: object | None = None
  order: int | None = None


@dataclass(frozen=True)
class Seed:
  step: object
  reason: str


def _group_result(n, k):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  return report.candidates[0].source_candidate.group_result


def _state(n, k):
  group_result = _group_result(n, k)
  provenance = extract_toda_recursive_proof_provenance(
    group_result
  )
  full_depth = max(
    node.shortest_depth
    for node in provenance.nodes
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=full_depth,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
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
  return (
    provenance,
    full_depth,
    presentation,
    blocks,
    arguments,
  )


def _root_relation(presentation):
  statement = presentation.root_step.conclusion
  if not isinstance(statement, Relation):
    return None
  if statement.relation_type is not RelationType.EQUALITY:
    return None
  if not isinstance(statement.lhs, TodaPrimaryGroup):
    return None
  return statement


def _components(target_group, structure):
  result = []

  if isinstance(structure, FreeCyclicGroup):
    result.append(
      Component(
        "generator",
        target_group,
        structure.generator,
        None,
      )
    )

  elif isinstance(structure, FiniteCyclicGroup):
    result.extend(
      (
        Component(
          "generator",
          target_group,
          structure.generator,
          None,
        ),
        Component(
          "order",
          target_group,
          structure.generator,
          structure.order,
        ),
      )
    )

  elif isinstance(structure, DirectSumGroup):
    for index, summand in enumerate(structure.summands):
      if isinstance(summand, FreeCyclicGroup):
        result.append(
          Component(
            f"summand[{index}].generator",
            target_group,
            summand.generator,
            None,
          )
        )
      elif isinstance(summand, FiniteCyclicGroup):
        result.extend(
          (
            Component(
              f"summand[{index}].generator",
              target_group,
              summand.generator,
              None,
            ),
            Component(
              f"summand[{index}].order",
              target_group,
              summand.generator,
              summand.order,
            ),
          )
        )

  return tuple(result)


def _depth_by_id(provenance):
  return {
    id(node.proof_step): node.shortest_depth
    for node in provenance.nodes
  }


def _block_role_by_step_id(blocks):
  return {
    id(step): block.role
    for block in blocks
    for step in block.steps
  }


def _argument_conclusion_by_step_id(arguments):
  result = {}
  for index, argument in enumerate(arguments):
    step = extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
    if step is not None:
      result[id(step)] = (
        index,
        argument.role,
      )
  return result


def _provider_seeds(
  presentation,
  provenance,
  arguments,
  components,
):
  seeds = []

  for argument in arguments:
    if argument.role not in (
      TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION,
      TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER,
    ):
      continue

    subject = extract_toda_group_proof_narrative_argument_purpose_subject(
      argument
    )
    step = extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
    if subject is None or step is None:
      continue

    matched = False

    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION
    ):
      matched = any(
        component.generator == subject
        for component in components
      )

    elif (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER
    ):
      statement = step.conclusion
      matched = (
        isinstance(statement, Relation)
        and statement.relation_type is RelationType.ORDER
        and any(
          component.kind.endswith("order")
          and component.generator == subject
          and component.order == statement.rhs
          for component in components
        )
      )

    if matched:
      seeds.append(
        Seed(
          step=step,
          reason=f"atomic:{argument.role.value}",
        )
      )

  for node in provenance.nodes:
    statement = node.proof_step.conclusion

    if isinstance(
      statement,
      TodaProp515Pi12_5HopfIsomorphismStatement,
    ):
      if any(
        component.target_group == statement.map.source_group
        for component in components
      ):
        seeds.append(
          Seed(
            step=node.proof_step,
            reason="transport:hopf_isomorphism",
          )
        )

    elif isinstance(
      statement,
      Toda515Sigma8TransportedDecompositionStatement,
    ):
      target_group = statement.prop44_isomorphism.map.target_group
      if any(
        component.target_group == target_group
        for component in components
      ):
        seeds.append(
          Seed(
            step=node.proof_step,
            reason="transport:transported_decomposition",
          )
        )

    elif isinstance(
      statement,
      Toda48Pi16_9OrderAndE4InjectiveStatement,
    ):
      if any(
        component.kind.endswith("order")
        and component.target_group == statement.target_group
        and component.order == statement.target_order
        for component in components
      ):
        seeds.append(
          Seed(
            step=node.proof_step,
            reason="transport:target_order",
          )
        )

  seed_ids = {
    id(seed.step)
    for seed in seeds
  }

  for premise in presentation.root_step.premises:
    if id(premise) in seed_ids:
      continue

    statement = premise.conclusion

    if isinstance(
      statement,
      (
        Toda56Nu4DecompositionStatement,
        Toda515Sigma8TransportedDecompositionStatement,
        TodaProp515Pi12_5HopfIsomorphismStatement,
        Toda48Pi16_9OrderAndE4InjectiveStatement,
      ),
    ):
      seeds.append(
        Seed(
          step=premise,
          reason="integration:structural_direct_premise",
        )
      )
      continue

    if (
      isinstance(statement, Relation)
      and statement.relation_type is RelationType.EQUALITY
      and isinstance(statement.lhs, TodaPrimaryGroup)
      and isinstance(
        statement.rhs,
        (
          FreeCyclicGroup,
          FiniteCyclicGroup,
          DirectSumGroup,
        ),
      )
    ):
      seeds.append(
        Seed(
          step=premise,
          reason="integration:group_structure_direct_premise",
        )
      )

  unique = []
  seen = set()
  for seed in seeds:
    key = id(seed.step)
    if key in seen:
      continue
    seen.add(key)
    unique.append(seed)

  return tuple(unique)


def _children_by_parent_id(provenance):
  result = {}
  for edge in provenance.edges:
    result.setdefault(
      id(edge.parent_step),
      [],
    ).append(edge.premise_step)
  return result


def _boundary_action(
  step,
  *,
  is_seed,
  block_role_by_step_id,
  argument_conclusion_by_step_id,
):
  step_id = id(step)
  block_role = block_role_by_step_id.get(step_id)
  argument_boundary = argument_conclusion_by_step_id.get(step_id)

  if is_seed:
    return BoundaryAction.EXPAND

  if block_role is TodaGroupProofNarrativeMathematicalBlockRole.REFERENCE:
    return BoundaryAction.REFERENCE

  if argument_boundary is not None:
    return BoundaryAction.REFERENCE

  if block_role in (
    TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS,
    TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY,
  ):
    return BoundaryAction.STRUCTURAL

  if block_role in (
    TodaGroupProofNarrativeMathematicalBlockRole.PRECONDITION,
    TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION,
    TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP,
    TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION,
    TodaGroupProofNarrativeMathematicalBlockRole.ORDER,
    TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
  ):
    return BoundaryAction.EXPAND

  return BoundaryAction.INTERNAL


def _bounded_closure(
  seeds,
  provenance,
  blocks,
  arguments,
):
  children = _children_by_parent_id(provenance)
  block_roles = _block_role_by_step_id(blocks)
  argument_boundaries = _argument_conclusion_by_step_id(arguments)
  seed_ids = {
    id(seed.step)
    for seed in seeds
  }

  queue = list(seed.step for seed in seeds)
  visited = set()
  action_by_step_id = {}

  while queue:
    step = queue.pop(0)
    step_id = id(step)

    if step_id in visited:
      continue

    visited.add(step_id)

    action = _boundary_action(
      step,
      is_seed=step_id in seed_ids,
      block_role_by_step_id=block_roles,
      argument_conclusion_by_step_id=argument_boundaries,
    )
    action_by_step_id[step_id] = action

    if (
      step_id not in seed_ids
      and action
      in (
        BoundaryAction.REFERENCE,
        BoundaryAction.STRUCTURAL,
        BoundaryAction.INTERNAL,
      )
    ):
      continue

    queue.extend(
      children.get(step_id, ())
    )

  return visited, action_by_step_id


def main():
  print("=" * 120)
  print("Phase 144-6-R5-15 semantic provider boundary audit")
  print("=" * 120)
  print(
    "Audit only. No production code, tests, or project documents are modified."
  )
  print(
    "No n/k-specific boundary rules and no inference-rule-name parsing are used."
  )
  print(
    "Boundary inputs: existing Narrative block roles and existing Argument conclusions."
  )
  print()

  summary = []

  for n, k in TARGETS:
    (
      provenance,
      full_depth,
      presentation,
      blocks,
      arguments,
    ) = _state(n, k)

    relation = _root_relation(presentation)
    if relation is None:
      continue

    components = _components(
      relation.lhs,
      relation.rhs,
    )
    seeds = _provider_seeds(
      presentation,
      provenance,
      arguments,
      components,
    )
    depth_by_id = _depth_by_id(provenance)

    visited, action_by_id = _bounded_closure(
      seeds,
      provenance,
      blocks,
      arguments,
    )

    bounded_depth = max(
      (
        depth_by_id[step_id]
        for step_id in visited
        if step_id in depth_by_id
      ),
      default=0,
    )

    counts = {
      action: sum(
        1
        for value in action_by_id.values()
        if value is action
      )
      for action in BoundaryAction
    }

    print("-" * 120)
    print(
      f"TARGET n={n}, k={k} "
      f"full_depth={full_depth} "
      f"bounded_depth={bounded_depth} "
      f"saving={full_depth - bounded_depth} "
      f"visited={len(visited)} "
      f"seeds={len(seeds)}"
    )
    print("-" * 120)

    for index, seed in enumerate(seeds, start=1):
      print(
        f"SEED[{index:02d}] "
        f"depth={depth_by_id.get(id(seed.step))} "
        f"type={type(seed.step.conclusion).__name__} "
        f"reason={seed.reason}"
      )

    print(
      "ACTIONS "
      + " ".join(
        f"{action.value}={counts[action]}"
        for action in BoundaryAction
      )
    )

    deepest = sorted(
      (
        (
          depth_by_id[step_id],
          action_by_id[step_id].value,
          type(
            next(
              node.proof_step
              for node in provenance.nodes
              if id(node.proof_step) == step_id
            ).conclusion
          ).__name__,
        )
        for step_id in visited
        if step_id in depth_by_id
      ),
      reverse=True,
    )[:12]

    print("DEEPEST_BOUNDED_NODES")
    for depth, action, statement_type in deepest:
      print(
        f"  depth={depth} "
        f"action={action} "
        f"type={statement_type}"
      )

    boundary_nodes = sorted(
      (
        (
          depth_by_id[step_id],
          action.value,
          type(
            next(
              node.proof_step
              for node in provenance.nodes
              if id(node.proof_step) == step_id
            ).conclusion
          ).__name__,
        )
        for step_id, action in action_by_id.items()
        if action in (
          BoundaryAction.REFERENCE,
          BoundaryAction.STRUCTURAL,
          BoundaryAction.INTERNAL,
        )
        and step_id in depth_by_id
      )
    )

    print("STOP_BOUNDARIES")
    for depth, action, statement_type in boundary_nodes[:24]:
      print(
        f"  depth={depth} "
        f"action={action} "
        f"type={statement_type}"
      )
    if len(boundary_nodes) > 24:
      print(
        f"  ... {len(boundary_nodes) - 24} more"
      )

    status = (
      "TARGET_PI6_DEPTH3"
      if (n, k) == (3, 3) and bounded_depth == 3
      else (
        "BOUNDED"
        if bounded_depth < full_depth
        else "REACHES_FULL_DEPTH"
      )
    )

    print(f"status={status}")
    print()

    summary.append(
      (
        n,
        k,
        full_depth,
        bounded_depth,
        full_depth - bounded_depth,
        len(visited),
        status,
      )
    )

  print("=" * 120)
  print("SUMMARY")
  print("=" * 120)
  print(
    "n k full_depth bounded_depth saving visited status"
  )
  for row in summary:
    print(
      " ".join(
        str(value)
        for value in row
      )
    )

  print()
  print("=" * 120)
  print("INTERPRETATION")
  print("=" * 120)
  print(
    "1. The primary benchmark is pi_6^3: bounded_depth should be 3 without an n/k-specific boundary rule."
  )
  print(
    "2. REFERENCE stops at an existing REFERENCE block or another Argument conclusion."
  )
  print(
    "3. STRUCTURAL stops below existing EXACTNESS/MAP_PROPERTY blocks; the structural fact remains available to Narrative, but its proof is not recursively expanded."
  )
  print(
    "4. INTERNAL stops at unclassified OTHER material. If required mathematical content is incorrectly stopped here, the boundary is too aggressive and must be refined before production use."
  )
  print(
    "5. A shallow depth is not sufficient by itself. Inspect DEEPEST_BOUNDED_NODES and STOP_BOUNDARIES for every representative group."
  )
  print(
    "6. If the same semantic rule bounds all six representatives while preserving their provider seeds, R5 can proceed to a depth-policy validation audit. Otherwise the next substep must refine the boundary semantics, not add target-specific exceptions."
  )


if __name__ == "__main__":
  main()
