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


class SeedKind(Enum):
  ATOMIC = "atomic"
  TRANSPORT = "transport"
  INTEGRATION_DIRECT_PREMISE = "integration_direct_premise"


@dataclass(frozen=True)
class Component:
  kind: str
  target_group: object
  generator: object | None = None
  order: int | None = None


@dataclass(frozen=True)
class ProviderSeed:
  kind: SeedKind
  step: object
  reason: str


def _group_result(n, k):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  return report.candidates[0].source_candidate.group_result


def _full_state(n, k):
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
    group_result,
    provenance,
    full_depth,
    presentation,
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


def _components_for_group(target_group, structure):
  result = []

  if isinstance(structure, FreeCyclicGroup):
    result.append(
      Component(
        kind="generator",
        target_group=target_group,
        generator=structure.generator,
      )
    )
    return tuple(result)

  if isinstance(structure, FiniteCyclicGroup):
    result.extend(
      (
        Component(
          kind="generator",
          target_group=target_group,
          generator=structure.generator,
        ),
        Component(
          kind="order",
          target_group=target_group,
          generator=structure.generator,
          order=structure.order,
        ),
      )
    )
    return tuple(result)

  if isinstance(structure, DirectSumGroup):
    for index, summand in enumerate(structure.summands):
      if isinstance(summand, FreeCyclicGroup):
        result.append(
          Component(
            kind=f"summand[{index}].generator",
            target_group=target_group,
            generator=summand.generator,
          )
        )
      elif isinstance(summand, FiniteCyclicGroup):
        result.extend(
          (
            Component(
              kind=f"summand[{index}].generator",
              target_group=target_group,
              generator=summand.generator,
            ),
            Component(
              kind=f"summand[{index}].order",
              target_group=target_group,
              generator=summand.generator,
              order=summand.order,
            ),
          )
        )

  return tuple(result)


def _depth_by_step_id(provenance):
  return {
    id(node.proof_step): node.shortest_depth
    for node in provenance.nodes
  }


def _atomic_seeds(arguments, components):
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
    conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
    if subject is None or conclusion_step is None:
      continue

    matches = False

    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION
    ):
      matches = any(
        component.generator == subject
        for component in components
      )

    elif (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER
    ):
      statement = conclusion_step.conclusion
      matches = (
        isinstance(statement, Relation)
        and statement.relation_type is RelationType.ORDER
        and any(
          component.kind.endswith("order")
          and component.generator == subject
          and component.order == statement.rhs
          for component in components
        )
      )

    if matches:
      seeds.append(
        ProviderSeed(
          kind=SeedKind.ATOMIC,
          step=conclusion_step,
          reason=argument.role.value,
        )
      )

  return tuple(seeds)


def _transport_seeds(provenance, components):
  seeds = []

  for node in provenance.nodes:
    step = node.proof_step
    statement = step.conclusion
    matches = False

    if isinstance(
      statement,
      TodaProp515Pi12_5HopfIsomorphismStatement,
    ):
      matches = any(
        component.target_group == statement.map.source_group
        and (
          component.generator == statement.source_generator
          or (
            component.kind.endswith("order")
            and component.order == statement.image_group.order
          )
        )
        for component in components
      )

    elif isinstance(
      statement,
      Toda515Sigma8TransportedDecompositionStatement,
    ):
      target_group = statement.prop44_isomorphism.map.target_group
      matches = any(
        component.target_group == target_group
        for component in components
      )

    elif isinstance(
      statement,
      Toda48Pi16_9OrderAndE4InjectiveStatement,
    ):
      matches = any(
        component.kind.endswith("order")
        and component.target_group == statement.target_group
        and component.order == statement.target_order
        for component in components
      )

    if matches:
      seeds.append(
        ProviderSeed(
          kind=SeedKind.TRANSPORT,
          step=step,
          reason=type(statement).__name__,
        )
      )

  return tuple(seeds)


def _integration_direct_premise_seeds(
  presentation,
  components,
  atomic_seeds,
  transport_seeds,
):
  covered_step_ids = {
    id(seed.step)
    for seed in atomic_seeds + transport_seeds
  }

  root = presentation.root_step
  structural_types = (
    Toda56Nu4DecompositionStatement,
    Toda515Sigma8TransportedDecompositionStatement,
    TodaProp515Pi12_5HopfIsomorphismStatement,
    Toda48Pi16_9OrderAndE4InjectiveStatement,
  )

  seeds = []

  for premise in root.premises:
    if id(premise) in covered_step_ids:
      continue

    statement = premise.conclusion

    include = False
    reason = ""

    if isinstance(statement, structural_types):
      include = True
      reason = f"structural direct premise: {type(statement).__name__}"

    elif (
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
      include = True
      reason = "group-structure direct premise"

    elif (
      isinstance(statement, Relation)
      and statement.relation_type is RelationType.ORDER
      and any(
        component.generator == statement.lhs
        and component.order == statement.rhs
        for component in components
        if component.kind.endswith("order")
      )
    ):
      include = True
      reason = "final-order direct premise"

    if include:
      seeds.append(
        ProviderSeed(
          kind=SeedKind.INTEGRATION_DIRECT_PREMISE,
          step=premise,
          reason=reason,
        )
      )

  return tuple(seeds)


def _children_by_parent_id(provenance):
  result = {}
  for edge in provenance.edges:
    result.setdefault(
      id(edge.parent_step),
      [],
    ).append(edge.premise_step)
  return result


def _closure_step_ids(seed_steps, provenance):
  children = _children_by_parent_id(provenance)
  queue = list(seed_steps)
  seen = set()

  while queue:
    step = queue.pop(0)
    step_id = id(step)
    if step_id in seen:
      continue
    seen.add(step_id)
    queue.extend(
      children.get(step_id, ())
    )

  return seen


def _required_depth(step_ids, depth_by_id):
  depths = [
    depth_by_id[step_id]
    for step_id in step_ids
    if step_id in depth_by_id
  ]
  return max(depths) if depths else 0


def _closure_summary(
  label,
  seeds,
  provenance,
  depth_by_id,
):
  seed_steps = tuple(seed.step for seed in seeds)
  closure_ids = _closure_step_ids(
    seed_steps,
    provenance,
  )
  print(
    f"{label}_seed_count={len(seeds)} "
    f"{label}_closure_nodes={len(closure_ids)} "
    f"{label}_closure_depth="
    f"{_required_depth(closure_ids, depth_by_id)}"
  )
  for index, seed in enumerate(seeds, start=1):
    print(
      f"  {label}_SEED[{index:02d}] "
      f"depth={depth_by_id.get(id(seed.step))} "
      f"kind={seed.kind.value} "
      f"type={type(seed.step.conclusion).__name__} "
      f"reason={seed.reason}"
    )
  return closure_ids


def main():
  print("=" * 120)
  print("Phase 144-6-R5-14 provider closure -> required depth audit")
  print("=" * 120)
  print(
    "Audit only. No production code, tests, or project documents are modified."
  )
  print(
    "The audit compares seed depth, unrestricted premise closure depth, "
    "and full proof depth."
  )
  print()

  rows = []

  for n, k in TARGETS:
    (
      group_result,
      provenance,
      full_depth,
      presentation,
      arguments,
    ) = _full_state(n, k)

    relation = _root_relation(presentation)
    if relation is None:
      print(f"TARGET n={n}, k={k}: unsupported root")
      continue

    components = _components_for_group(
      relation.lhs,
      relation.rhs,
    )
    depth_by_id = _depth_by_step_id(provenance)

    atomic = _atomic_seeds(
      arguments,
      components,
    )
    transport = _transport_seeds(
      provenance,
      components,
    )
    integration = _integration_direct_premise_seeds(
      presentation,
      components,
      atomic,
      transport,
    )

    all_seeds = atomic + transport + integration

    print("-" * 120)
    print(
      f"TARGET n={n}, k={k} "
      f"full_depth={full_depth} "
      f"components={len(components)} "
      f"arguments={len(arguments)}"
    )
    print("-" * 120)

    seed_depth = max(
      (
        depth_by_id.get(id(seed.step), 0)
        for seed in all_seeds
      ),
      default=0,
    )
    print(f"provider_seed_depth={seed_depth}")

    atomic_ids = _closure_summary(
      "ATOMIC",
      atomic,
      provenance,
      depth_by_id,
    )
    transport_ids = _closure_summary(
      "TRANSPORT",
      transport,
      provenance,
      depth_by_id,
    )
    integration_ids = _closure_summary(
      "INTEGRATION",
      integration,
      provenance,
      depth_by_id,
    )

    combined_ids = (
      atomic_ids
      | transport_ids
      | integration_ids
    )
    combined_depth = _required_depth(
      combined_ids,
      depth_by_id,
    )

    print(
      f"COMBINED_closure_nodes={len(combined_ids)} "
      f"COMBINED_required_depth={combined_depth}"
    )
    print(
      f"depth_saving_vs_full={full_depth - combined_depth}"
    )

    if combined_depth == full_depth:
      status = "REACHES_FULL_DEPTH"
    elif combined_depth > seed_depth:
      status = "BOUNDED_CLOSURE"
    else:
      status = "SEED_DEPTH_SUFFICIENT"

    print(f"closure_status={status}")

    deepest = sorted(
      (
        (
          depth_by_id[step_id],
          type(
            next(
              node.proof_step
              for node in provenance.nodes
              if id(node.proof_step) == step_id
            ).conclusion
          ).__name__,
        )
        for step_id in combined_ids
        if step_id in depth_by_id
      ),
      reverse=True,
    )[:8]

    print("DEEPEST_REQUIRED_CLOSURE_NODES")
    for depth, statement_type in deepest:
      print(
        f"  depth={depth} type={statement_type}"
      )

    rows.append(
      (
        n,
        k,
        full_depth,
        seed_depth,
        combined_depth,
        status,
        len(combined_ids),
      )
    )
    print()

  print("=" * 120)
  print("SUMMARY")
  print("=" * 120)
  print(
    "n k full_depth seed_depth closure_depth saving status closure_nodes"
  )
  for (
    n,
    k,
    full_depth,
    seed_depth,
    closure_depth,
    status,
    closure_nodes,
  ) in rows:
    print(
      f"{n} {k} {full_depth} {seed_depth} "
      f"{closure_depth} {full_depth - closure_depth} "
      f"{status} {closure_nodes}"
    )

  print()
  print("=" * 120)
  print("INTERPRETATION")
  print("=" * 120)
  print(
    "1. If unrestricted provider premise closure reaches full_depth, "
    "provider discovery is not the remaining problem; closure needs a "
    "Narrative boundary rule."
  )
  print(
    "2. If closure_depth is substantially below full_depth, the provider "
    "closure itself is a viable required-depth candidate."
  )
  print(
    "3. pi_6^3 should not be accepted merely because seed_depth=3; "
    "compare its closure_depth with full_depth=10."
  )
  print(
    "4. pi_10^4 and pi_15^8 must not collapse to depth 0. Their root "
    "integration direct premises must appear as seeds and their premise "
    "closures must be measured."
  )
  print(
    "5. This audit deliberately uses unrestricted premise closure so that "
    "we can detect whether the next step needs a semantic stop boundary "
    "rather than hiding that problem in the prototype."
  )


if __name__ == "__main__":
  main()
