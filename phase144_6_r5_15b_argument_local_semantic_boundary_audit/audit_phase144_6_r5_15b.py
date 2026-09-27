from collections import Counter
from dataclasses import dataclass

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
from toda_group_proof_narrative_argument_discourse import (
  TodaGroupProofNarrativeArgumentDiscourseRole,
  classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
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


@dataclass(frozen=True)
class Component:
  kind: str
  target_group: object
  generator: object | None = None
  order: int | None = None


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
    sidecar,
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


def _depth_by_step_id(provenance):
  return {
    id(node.proof_step): node.shortest_depth
    for node in provenance.nodes
  }


def _required_argument_indices(arguments, components):
  required = set()

  for index, argument in enumerate(arguments):
    subject = extract_toda_group_proof_narrative_argument_purpose_subject(
      argument
    )

    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_GROUP_STRUCTURE
    ):
      required.add(index)
      continue

    if subject is None:
      continue

    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION
      and any(
        component.generator == subject
        for component in components
      )
    ):
      required.add(index)
      continue

    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER
    ):
      conclusion_step = (
        extract_toda_group_proof_narrative_argument_conclusion_step(
          argument
        )
      )
      if conclusion_step is None:
        continue
      statement = conclusion_step.conclusion
      if not (
        isinstance(statement, Relation)
        and statement.relation_type is RelationType.ORDER
      ):
        continue
      if any(
        component.kind.endswith("order")
        and component.generator == subject
        and component.order == statement.rhs
        for component in components
      ):
        required.add(index)

  return frozenset(required)


def _structural_provider_steps(
  presentation,
  provenance,
  components,
):
  result = []

  for node in provenance.nodes:
    step = node.proof_step
    statement = step.conclusion

    if isinstance(
      statement,
      TodaProp515Pi12_5HopfIsomorphismStatement,
    ):
      if any(
        component.target_group == statement.map.source_group
        for component in components
      ):
        result.append(step)

    elif isinstance(
      statement,
      Toda515Sigma8TransportedDecompositionStatement,
    ):
      target_group = statement.prop44_isomorphism.map.target_group
      if any(
        component.target_group == target_group
        for component in components
      ):
        result.append(step)

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
        result.append(step)

  for premise in presentation.root_step.premises:
    if isinstance(
      premise.conclusion,
      (
        Toda56Nu4DecompositionStatement,
        Toda515Sigma8TransportedDecompositionStatement,
        TodaProp515Pi12_5HopfIsomorphismStatement,
        Toda48Pi16_9OrderAndE4InjectiveStatement,
      ),
    ):
      result.append(premise)

  unique = []
  seen = set()
  for step in result:
    if id(step) in seen:
      continue
    seen.add(id(step))
    unique.append(step)
  return tuple(unique)


def _production_frontier_visible_step_ids(
  presentation,
  sidecar,
  blocks,
  arguments,
  argument_index,
):
  argument = arguments[argument_index]
  local_body_blocks = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )
  hidden = (
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      local_body_blocks,
      sidecar,
      argument,
    )
  )

  visible = {
    id(step)
    for block in local_body_blocks
    for step in block.steps
    if id(step) not in hidden
  }

  return (
    local_body_blocks,
    hidden,
    frozenset(visible),
  )


def main():
  print("=" * 120)
  print("Phase 144-6-R5-15B Argument-local semantic boundary audit")
  print("=" * 120)
  print(
    "Audit only. No production code, tests, or project documents are modified."
  )
  print(
    "No n/k-specific boundary rule and no inference-rule-name parsing are used."
  )
  print(
    "The audit reuses the production Argument local-body extractor and the R4 production frontier filter."
  )
  print()

  summary = []

  for n, k in TARGETS:
    (
      provenance,
      full_depth,
      presentation,
      sidecar,
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
    required_indices = _required_argument_indices(
      arguments,
      components,
    )
    structural_steps = _structural_provider_steps(
      presentation,
      provenance,
      components,
    )
    depth_by_id = _depth_by_step_id(provenance)
    discourse = (
      classify_toda_group_proof_narrative_argument_discourse_roles(
        arguments
      )
    )

    required_visible_ids = set()
    local_body_ids = set()
    hidden_ids = set()

    print("-" * 120)
    print(
      f"TARGET n={n}, k={k} "
      f"full_depth={full_depth} "
      f"arguments={len(arguments)} "
      f"required_arguments={len(required_indices)} "
      f"structural_providers={len(structural_steps)}"
    )
    print("-" * 120)

    for argument_index in sorted(required_indices):
      argument = arguments[argument_index]
      (
        local_body_blocks,
        hidden,
        visible,
      ) = _production_frontier_visible_step_ids(
        presentation,
        sidecar,
        blocks,
        arguments,
        argument_index,
      )

      local_steps = tuple(
        step
        for block in local_body_blocks
        for step in block.steps
      )
      local_ids = {
        id(step)
        for step in local_steps
      }

      local_body_ids.update(local_ids)
      hidden_ids.update(hidden)
      required_visible_ids.update(visible)

      local_depth = max(
        (
          depth_by_id.get(id(step), 0)
          for step in local_steps
        ),
        default=0,
      )
      visible_depth = max(
        (
          depth_by_id.get(step_id, 0)
          for step_id in visible
        ),
        default=0,
      )

      role_counts = Counter(
        block.role.value
        for block in local_body_blocks
      )

      subject = (
        extract_toda_group_proof_narrative_argument_purpose_subject(
          argument
        )
      )

      print(
        f"ARG[{argument_index:02d}] "
        f"role={argument.role.value} "
        f"discourse={discourse[argument_index].value} "
        f"subject={subject!r}"
      )
      print(
        f"  local_blocks={len(local_body_blocks)} "
        f"local_steps={len(local_steps)} "
        f"local_depth={local_depth} "
        f"frontier_visible={len(visible)} "
        f"frontier_depth={visible_depth} "
        f"hidden={len(hidden)}"
      )
      print(
        "  block_roles="
        + ",".join(
          f"{name}:{count}"
          for name, count in sorted(role_counts.items())
        )
      )

      deepest_visible = sorted(
        (
          (
            depth_by_id.get(step_id, 0),
            type(
              next(
                node.proof_step
                for node in provenance.nodes
                if id(node.proof_step) == step_id
              ).conclusion
            ).__name__,
          )
          for step_id in visible
        ),
        reverse=True,
      )[:8]

      print("  deepest_frontier_visible")
      for depth, statement_type in deepest_visible:
        print(
          f"    depth={depth} type={statement_type}"
        )

    structural_ids = {
      id(step)
      for step in structural_steps
    }
    required_visible_ids.update(structural_ids)

    print("STRUCTURAL PROVIDERS")
    if not structural_steps:
      print("  NONE")
    for step in structural_steps:
      print(
        f"  depth={depth_by_id.get(id(step))} "
        f"type={type(step.conclusion).__name__}"
      )

    required_depth = max(
      (
        depth_by_id.get(step_id, 0)
        for step_id in required_visible_ids
      ),
      default=0,
    )

    print(
      f"required_visible_steps={len(required_visible_ids)}"
    )
    print(
      f"argument_local_union_steps={len(local_body_ids)}"
    )
    print(
      f"frontier_hidden_union_steps={len(hidden_ids)}"
    )
    print(
      f"argument_local_required_depth={required_depth}"
    )
    print(
      f"depth_saving_vs_full={full_depth - required_depth}"
    )

    deepest_required = sorted(
      (
        (
          depth_by_id.get(step_id, 0),
          type(
            next(
              node.proof_step
              for node in provenance.nodes
              if id(node.proof_step) == step_id
            ).conclusion
          ).__name__,
        )
        for step_id in required_visible_ids
      ),
      reverse=True,
    )[:12]

    print("DEEPEST_REQUIRED_VISIBLE")
    for depth, statement_type in deepest_required:
      print(
        f"  depth={depth} type={statement_type}"
      )

    if (n, k) == (3, 3):
      status = (
        "TARGET_PI6_DEPTH3"
        if required_depth == 3
        else "PI6_NOT_DEPTH3"
      )
    else:
      status = (
        "BOUNDED"
        if required_depth < full_depth
        else "REACHES_FULL_DEPTH"
      )

    print(f"status={status}")
    print()

    summary.append(
      (
        n,
        k,
        full_depth,
        required_depth,
        full_depth - required_depth,
        len(required_indices),
        len(structural_steps),
        status,
      )
    )

  print("=" * 120)
  print("SUMMARY")
  print("=" * 120)
  print(
    "n k full_depth required_depth saving "
    "required_arguments structural_providers status"
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
    "1. The benchmark succeeds only if pi_6^3 reaches required_depth=3 without a target-specific boundary condition."
  )
  print(
    "2. Unlike R5-15, ordinary CALCULATION/GROUP_STRUCTURE blocks are not globally expanded. They are retained only when they survive the production Argument-local R4 frontier."
  )
  print(
    "3. Required structural providers are added explicitly as provider facts, but their own premise closures are not recursively expanded."
  )
  print(
    "4. A shallow depth is still not sufficient by itself. Inspect each required Argument's deepest_frontier_visible list."
  )
  print(
    "5. If pi_10^4 or pi_15^8 loses a mathematically necessary aggregate/decomposition fact, provider selection must be refined before depth-policy validation."
  )
  print(
    "6. If all six representatives retain their required Arguments/providers and pi_6^3 reaches depth 3, the next step can be R5-16 depth-policy validation."
  )


if __name__ == "__main__":
  main()
