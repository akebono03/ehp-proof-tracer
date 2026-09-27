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


class Layer(Enum):
  ATOMIC = "atomic"
  TRANSPORT = "transport"
  INTEGRATION = "integration"


@dataclass(frozen=True)
class Component:
  kind: str
  target_group: object
  generator: object | None = None
  order: int | None = None


@dataclass(frozen=True)
class Evidence:
  layer: Layer
  source: str
  depth: int | None
  components: tuple[Component, ...]
  note: str


def _group_result(n, k):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  return report.candidates[0].source_candidate.group_result


def _state(n, k):
  group_result = _group_result(
    n,
    k,
  )
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
    arguments,
  )


def _components_for_group(
  target_group,
  structure,
):
  result = []

  if isinstance(
    structure,
    FreeCyclicGroup,
  ):
    result.append(
      Component(
        "generator",
        target_group,
        structure.generator,
        None,
      )
    )
    return tuple(
      result
    )

  if isinstance(
    structure,
    FiniteCyclicGroup,
  ):
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
    return tuple(
      result
    )

  if isinstance(
    structure,
    DirectSumGroup,
  ):
    for index, summand in enumerate(
      structure.summands
    ):
      if isinstance(
        summand,
        FreeCyclicGroup,
      ):
        result.append(
          Component(
            f"summand[{index}].generator",
            target_group,
            summand.generator,
            None,
          )
        )
      elif isinstance(
        summand,
        FiniteCyclicGroup,
      ):
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

  return tuple(
    result
  )


def _root_claim(
  presentation,
):
  statement = presentation.root_step.conclusion
  if not isinstance(
    statement,
    Relation,
  ):
    return None
  if (
    statement.relation_type
    is not RelationType.EQUALITY
  ):
    return None
  if not isinstance(
    statement.lhs,
    TodaPrimaryGroup,
  ):
    return None
  return statement


def _depth_by_step_id(
  provenance,
):
  return {
    id(
      node.proof_step
    ): node.shortest_depth
    for node in provenance.nodes
  }


def _atomic_argument_evidence(
  arguments,
  root_components,
  depth_by_id,
):
  result = []

  for index, argument in enumerate(
    arguments
  ):
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_GROUP_STRUCTURE
    ):
      continue

    subject = extract_toda_group_proof_narrative_argument_purpose_subject(
      argument
    )
    conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
    if (
      subject is None
      or conclusion_step is None
    ):
      continue

    matched = []

    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_DEFINITION
    ):
      matched.extend(
        component
        for component in root_components
        if component.generator == subject
      )

    elif (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_ORDER
    ):
      statement = conclusion_step.conclusion
      if (
        isinstance(
          statement,
          Relation,
        )
        and statement.relation_type
        is RelationType.ORDER
      ):
        matched.extend(
          component
          for component in root_components
          if (
            component.kind.endswith(
              "order"
            )
            and component.generator
            == subject
            and component.order
            == statement.rhs
          )
      )

    if matched:
      result.append(
        Evidence(
          layer=Layer.ATOMIC,
          source=(
            f"A{index:02d}:"
            f"{argument.role.value}"
          ),
          depth=depth_by_id.get(
            id(
              conclusion_step
            )
          ),
          components=tuple(
            matched
          ),
          note=(
            "Narrative Argument purpose subject "
            "matches final claim component"
          ),
        )
      )

  return tuple(
    result
  )


def _typed_transport_evidence(
  provenance,
  root_components,
  depth_by_id,
):
  result = []

  for node in provenance.nodes:
    step = node.proof_step
    statement = step.conclusion
    supplied = []
    note = None

    if isinstance(
      statement,
      TodaProp515Pi12_5HopfIsomorphismStatement,
    ):
      source_group = statement.map.source_group
      source_structure = FiniteCyclicGroup(
        order=statement.image_group.order,
        generator=statement.source_generator,
      )
      candidates = _components_for_group(
        source_group,
        source_structure,
      )
      supplied.extend(
        component
        for component in root_components
        if component in candidates
      )
      note = (
        "Hopf isomorphism transports typed "
        "image_group order to source_generator"
      )

    elif isinstance(
      statement,
      Toda515Sigma8TransportedDecompositionStatement,
    ):
      target_group = (
        statement.prop44_isomorphism.map.target_group
      )
      candidates = _components_for_group(
        target_group,
        statement.transported_group,
      )
      supplied.extend(
        component
        for component in root_components
        if component in candidates
      )
      note = (
        "transported_group supplies typed "
        "direct-sum components"
      )

    elif isinstance(
      statement,
      Toda48Pi16_9OrderAndE4InjectiveStatement,
    ):
      for component in root_components:
        if (
          component.kind.endswith(
            "order"
          )
          and component.target_group
          == statement.target_group
          and component.order
          == statement.target_order
        ):
          supplied.append(
            component
          )
      note = (
        "target_group + target_order supply "
        "the final order component"
      )

    if supplied:
      result.append(
        Evidence(
          layer=Layer.TRANSPORT,
          source=type(
            statement
          ).__name__,
          depth=depth_by_id.get(
            id(
              step
            )
          ),
          components=tuple(
            supplied
          ),
          note=note,
        )
      )

  return tuple(
    result
  )


def _root_direct_premise_inventory(
  presentation,
  depth_by_id,
):
  result = []

  for index, premise in enumerate(
    presentation.root_step.premises
  ):
    result.append(
      (
        index,
        depth_by_id.get(
          id(
            premise
          )
        ),
        type(
          premise.conclusion
        ).__name__,
        premise.conclusion,
      )
    )

  return tuple(
    result
  )


def _integration_evidence(
  presentation,
  root_components,
  depth_by_id,
):
  root = presentation.root_step
  structural_premises = tuple(
    premise
    for premise in root.premises
    if isinstance(
      premise.conclusion,
      Toda56Nu4DecompositionStatement,
    )
  )

  if structural_premises:
    return (
      Evidence(
        layer=Layer.INTEGRATION,
        source=(
          "root + "
          "Toda56Nu4DecompositionStatement"
        ),
        depth=depth_by_id.get(
          id(
            root
          )
        ),
        components=root_components,
        note=(
          "final components are introduced by "
          "root integration from direct typed premises; "
          "no synthetic Composition is constructed"
        ),
      ),
    )

  return (
    Evidence(
      layer=Layer.INTEGRATION,
      source="root inference",
      depth=depth_by_id.get(
        id(
          root
        )
      ),
      components=root_components,
      note=(
        "root integrates provider evidence into "
        "the final group claim"
      ),
    ),
  )


def _component_key(
  component,
):
  return (
    component.kind,
    repr(
      component.target_group
    ),
    repr(
      component.generator
    ),
    component.order,
  )


def main():
  print(
    "=" * 120
  )
  print(
    "Phase 144-6-R5-13 atomic / transport / integration provider audit"
  )
  print(
    "=" * 120
  )
  print(
    "Audit only. No production code, tests, or project documents are modified."
  )
  print(
    "No rule-name parsing and no target-specific n/k checks are used for provider matching."
  )
  print()

  total_components = 0
  atomic_covered = 0
  transport_covered = 0
  preintegration_covered = 0
  integration_only = 0

  for n, k in TARGETS:
    (
      provenance,
      full_depth,
      presentation,
      arguments,
    ) = _state(
      n,
      k,
    )
    relation = _root_claim(
      presentation
    )

    print(
      "-" * 120
    )
    print(
      f"TARGET n={n}, k={k} "
      f"full_depth={full_depth} "
      f"arguments={len(arguments)}"
    )
    print(
      "-" * 120
    )

    if relation is None:
      print(
        "root_status=UNSUPPORTED"
      )
      print()
      continue

    root_components = _components_for_group(
      relation.lhs,
      relation.rhs,
    )
    depth_by_id = _depth_by_step_id(
      provenance
    )

    atomic = _atomic_argument_evidence(
      arguments,
      root_components,
      depth_by_id,
    )
    transport = _typed_transport_evidence(
      provenance,
      root_components,
      depth_by_id,
    )
    integration = _integration_evidence(
      presentation,
      root_components,
      depth_by_id,
    )

    atomic_keys = {
      _component_key(
        component
      )
      for evidence in atomic
      for component in evidence.components
    }
    transport_keys = {
      _component_key(
        component
      )
      for evidence in transport
      for component in evidence.components
    }

    print(
      f"root_claim={relation!r}"
    )
    print(
      f"root_component_count={len(root_components)}"
    )

    for index, component in enumerate(
      root_components,
      start=1,
    ):
      key = _component_key(
        component
      )
      layers = []
      if key in atomic_keys:
        layers.append(
          "ATOMIC"
        )
      if key in transport_keys:
        layers.append(
          "TRANSPORT"
        )
      if not layers:
        layers.append(
          "INTEGRATION_ONLY"
        )

      total_components += 1
      if key in atomic_keys:
        atomic_covered += 1
      if key in transport_keys:
        transport_covered += 1
      if (
        key in atomic_keys
        or key in transport_keys
      ):
        preintegration_covered += 1
      else:
        integration_only += 1

      print(
        f"C{index:02d} "
        f"kind={component.kind} "
        f"generator={component.generator!r} "
        f"order={component.order!r} "
        f"layers={'+'.join(layers)}"
      )

    print(
      "ATOMIC EVIDENCE"
    )
    if not atomic:
      print(
        "  NONE"
      )
    for evidence in atomic:
      print(
        f"  {evidence.source} "
        f"depth={evidence.depth} "
        f"components={tuple(c.kind for c in evidence.components)}"
      )
      print(
        f"    {evidence.note}"
      )

    print(
      "TRANSPORT EVIDENCE"
    )
    if not transport:
      print(
        "  NONE"
      )
    for evidence in transport:
      print(
        f"  {evidence.source} "
        f"depth={evidence.depth} "
        f"components={tuple(c.kind for c in evidence.components)}"
      )
      print(
        f"    {evidence.note}"
      )

    print(
      "ROOT DIRECT PREMISES"
    )
    for (
      premise_index,
      premise_depth,
      statement_type,
      statement,
    ) in _root_direct_premise_inventory(
      presentation,
      depth_by_id,
    ):
      print(
        f"  P{premise_index:02d} "
        f"depth={premise_depth} "
        f"type={statement_type}"
      )
      print(
        f"    {statement!r}"
      )

    print(
      "INTEGRATION EVIDENCE"
    )
    for evidence in integration:
      print(
        f"  {evidence.source} "
        f"depth={evidence.depth} "
        f"components={tuple(c.kind for c in evidence.components)}"
      )
      print(
        f"    {evidence.note}"
      )

    required_depth_candidates = [
      evidence.depth
      for evidence in (
        atomic
        + transport
      )
      if evidence.depth is not None
    ]
    provider_depth = (
      max(
        required_depth_candidates
      )
      if required_depth_candidates
      else 0
    )
    print(
      f"preintegration_provider_depth={provider_depth}"
    )
    print()

  print(
    "=" * 120
  )
  print(
    "SUMMARY"
  )
  print(
    "=" * 120
  )
  print(
    f"total_final_components={total_components}"
  )
  print(
    f"atomic_covered_components={atomic_covered}"
  )
  print(
    f"transport_covered_components={transport_covered}"
  )
  print(
    f"preintegration_covered_components={preintegration_covered}"
  )
  print(
    f"integration_only_components={integration_only}"
  )
  print()
  print(
    "=" * 120
  )
  print(
    "INTERPRETATION"
  )
  print(
    "=" * 120
  )
  print(
    "1. ATOMIC means an existing Definition/Order Narrative Argument directly establishes a final component."
  )
  print(
    "2. TRANSPORT means a typed structural statement transfers enough typed information to establish a final component."
  )
  print(
    "3. INTEGRATION_ONLY does not automatically mean missing proof data. It means the final component is first assembled at the root from direct premises."
  )
  print(
    "4. For pi_10^4, inspect ROOT DIRECT PREMISES. The important question is whether Toda56Nu4DecompositionStatement is a direct integration premise alongside the source-group fact, rather than whether the audit can synthesize nu_4 o nu_7 by hand."
  )
  print(
    "5. The next depth policy should be based on the closure needed to justify ATOMIC/TRANSPORT evidence plus the root integration premises, not on matching every final component to a standalone non-root statement."
  )


if __name__ == "__main__":
  main()
