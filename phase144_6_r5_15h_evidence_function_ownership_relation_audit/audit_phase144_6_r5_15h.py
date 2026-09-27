from collections import Counter, defaultdict
from enum import Enum

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from proof import Relation, RelationType
from toda_calculation_facade import build_standard_toda_report
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
from toda_group_proof_narrative_references import (
  extract_toda_group_proof_step_literature_reference,
)
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_sidecar
from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransitionRole,
  extract_toda_group_proof_narrative_transitions,
)
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_proof_dependency import extract_toda_recursive_proof_provenance
from toda_rules import (
  Toda48Pi16_9OrderAndE4InjectiveStatement,
  Toda515Sigma8TransportedDecompositionStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  Toda56Nu4DecompositionStatement,
)

TARGETS = ((3, 3), (5, 3), (4, 6), (5, 7), (8, 7), (9, 7))


class EvidenceFunction(Enum):
  ESTABLISH = "ESTABLISH"
  COMPUTE = "COMPUTE"
  EXACTNESS = "EXACTNESS"
  TRANSPORT = "TRANSPORT"
  REFERENCE = "REFERENCE"
  SUPPORT_ONLY = "SUPPORT_ONLY"


def group_result(n, k):
  return build_standard_toda_report(n=n, k=k).candidates[0].source_candidate.group_result


def full_state(result):
  provenance = extract_toda_recursive_proof_provenance(result)
  full_depth = max(node.shortest_depth for node in provenance.nodes)
  replay = build_toda_group_result_proof_replay(result, max_depth=full_depth)
  presentation = build_toda_group_proof_presentation(replay)
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(presentation)
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
  )
  transitions = extract_toda_group_proof_narrative_transitions(
    presentation,
    blocks,
    arguments,
  )
  return provenance, full_depth, presentation, sidecar, blocks, arguments, transitions


def final_components(presentation):
  s = presentation.root_step.conclusion
  if not (
    isinstance(s, Relation)
    and s.relation_type is RelationType.EQUALITY
    and isinstance(s.lhs, TodaPrimaryGroup)
  ):
    return ()
  target, structure = s.lhs, s.rhs
  summands = structure.summands if isinstance(structure, DirectSumGroup) else (structure,)
  out = []
  for summand in summands:
    if isinstance(summand, FreeCyclicGroup):
      out.append(("generator", target, summand.generator, None))
    elif isinstance(summand, FiniteCyclicGroup):
      out.append(("generator", target, summand.generator, None))
      out.append(("order", target, summand.generator, summand.order))
  return tuple(out)


def required_claim_arguments(arguments, comps):
  out = []
  for index, argument in enumerate(arguments):
    subject = extract_toda_group_proof_narrative_argument_purpose_subject(argument)
    include = argument.role is TodaGroupProofNarrativeArgumentRole.ESTABLISH_GROUP_STRUCTURE
    if argument.role is TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION:
      include = any(c[2] == subject for c in comps)
    if argument.role is TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER:
      step = extract_toda_group_proof_narrative_argument_conclusion_step(argument)
      s = None if step is None else step.conclusion
      include = (
        isinstance(s, Relation)
        and s.relation_type is RelationType.ORDER
        and any(c[0] == "order" and c[2] == subject and c[3] == s.rhs for c in comps)
      )
    if include:
      out.append((index, argument))
  return tuple(out)


def provider_steps(presentation, provenance, comps):
  out = []
  for node in provenance.nodes:
    step, s = node.proof_step, node.proof_step.conclusion
    if isinstance(s, TodaProp515Pi12_5HopfIsomorphismStatement):
      if any(c[1] == s.map.source_group for c in comps):
        out.append(step)
    elif isinstance(s, Toda515Sigma8TransportedDecompositionStatement):
      if any(c[1] == s.prop44_isomorphism.map.target_group for c in comps):
        out.append(step)
    elif isinstance(s, Toda48Pi16_9OrderAndE4InjectiveStatement):
      if any(c[0] == "order" and c[1] == s.target_group and c[3] == s.target_order for c in comps):
        out.append(step)
  for step in presentation.root_step.premises:
    if isinstance(
      step.conclusion,
      (
        Toda56Nu4DecompositionStatement,
        Toda515Sigma8TransportedDecompositionStatement,
        TodaProp515Pi12_5HopfIsomorphismStatement,
        Toda48Pi16_9OrderAndE4InjectiveStatement,
      ),
    ):
      out.append(step)
  unique, seen = [], set()
  for step in out:
    key = (type(step.conclusion).__name__, repr(step.conclusion))
    if key not in seen:
      seen.add(key)
      unique.append(step)
  return tuple(unique)


def block_by_step_id(blocks):
  return {
    id(step): block
    for block in blocks
    for step in block.steps
  }


def r4_visible_ids(presentation, blocks, sidecar, arguments, claims):
  visible = set()
  for index, argument in claims:
    local = extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      index,
    )
    hidden = _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      local,
      sidecar,
      argument,
    )
    visible.update(
      id(step)
      for block in local
      for step in block.steps
      if id(step) not in hidden
    )
  return visible


def transition_roles_by_edge(transitions):
  roles = defaultdict(set)
  for transition in transitions:
    for source in transition.source_blocks:
      roles[(id(source), id(transition.target_block))].add(transition.role)
  return roles


def classify_evidence_function(premise_step, parent_step, premise_block, parent_block, transition_roles):
  if extract_toda_group_proof_step_literature_reference(premise_step) is not None:
    return EvidenceFunction.REFERENCE

  edge_transition_roles = transition_roles.get(
    (id(premise_block), id(parent_block)),
    set(),
  )

  if (
    TodaGroupProofNarrativeTransitionRole.CALCULATION_CHAIN
    in edge_transition_roles
    or (
      premise_block.role
      is TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION
      and parent_block.role
      is TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION
    )
  ):
    return EvidenceFunction.COMPUTE

  if (
    premise_block.role
    is TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
    or parent_block.role
    is TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
  ):
    return EvidenceFunction.EXACTNESS

  if (
    premise_block.role
    is TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY
    and parent_block.role
    in (
      TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
      TodaGroupProofNarrativeMathematicalBlockRole.ORDER,
      TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP,
    )
  ):
    return EvidenceFunction.TRANSPORT

  if (
    TodaGroupProofNarrativeTransitionRole.DERIVATION
    in edge_transition_roles
    or parent_block.role
    in (
      TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION,
      TodaGroupProofNarrativeMathematicalBlockRole.ORDER,
      TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
      TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP,
    )
  ):
    return EvidenceFunction.ESTABLISH

  return EvidenceFunction.SUPPORT_ONLY


def main():
  print("=" * 132)
  print("Phase 144-6-R5-15H evidence function / ownership relation audit")
  print("=" * 132)
  print("Audit only. No production code, tests, or project documents are modified.")
  print("Evidence function is inferred from existing block roles, structured LiteratureReference, and Narrative transitions.")
  print("No n/k-specific rule and no inference-rule-name parsing are used.")
  print()

  grand = Counter()

  for n, k in TARGETS:
    result = group_result(n, k)
    (
      provenance,
      full_depth,
      presentation,
      sidecar,
      blocks,
      arguments,
      transitions,
    ) = full_state(result)
    comps = final_components(presentation)
    claims = required_claim_arguments(arguments, comps)
    providers = provider_steps(presentation, provenance, comps)
    visible = r4_visible_ids(presentation, blocks, sidecar, arguments, claims)
    blocks_by_step = block_by_step_id(blocks)
    transition_roles = transition_roles_by_edge(transitions)

    selected_owner_ids = {
      id(step)
      for _, argument in claims
      for step in (extract_toda_group_proof_narrative_argument_conclusion_step(argument),)
      if step is not None
    } | {id(step) for step in providers}

    rows = []
    for edge in provenance.edges:
      premise = edge.premise_step
      parent = edge.parent_step
      premise_block = blocks_by_step.get(id(premise))
      parent_block = blocks_by_step.get(id(parent))
      if premise_block is None or parent_block is None:
        continue
      function = classify_evidence_function(
        premise,
        parent,
        premise_block,
        parent_block,
        transition_roles,
      )
      owner_direct = id(parent) in selected_owner_ids
      is_visible = id(premise) in visible
      rows.append(
        (
          edge,
          function,
          premise_block.role,
          parent_block.role,
          owner_direct,
          is_visible,
        )
      )
      grand[
        (
          function.value,
          owner_direct,
          is_visible,
        )
      ] += 1

    counts = Counter(
      (
        function.value,
        owner_direct,
        is_visible,
      )
      for _, function, _, _, owner_direct, is_visible in rows
    )

    print("-" * 132)
    print(
      f"TARGET n={n}, k={k} full_depth={full_depth} "
      f"selected_claim_arguments={len(claims)} providers={len(providers)} edges={len(rows)}"
    )
    print("FUNCTION MATRIX: function direct_selected_owner visible count")
    for key, count in sorted(counts.items()):
      function, owner_direct, is_visible = key
      print(
        f"  {function:<13} direct_owner={'Y' if owner_direct else 'N'} "
        f"visible={'Y' if is_visible else 'N'} count={count:4d}"
      )

    print("DIRECT SELECTED-OWNER EVIDENCE")
    direct_rows = [row for row in rows if row[4]]
    if not direct_rows:
      print("  NONE")
    for edge, function, premise_role, parent_role, _, is_visible in direct_rows[:32]:
      print(
        f"  function={function.value:<13} visible={'Y' if is_visible else 'N'} "
        f"premise_role={premise_role.value:<15} parent_role={parent_role.value:<15} "
        f"premise={type(edge.premise_step.conclusion).__name__:<48} "
        f"parent={type(edge.parent_step.conclusion).__name__}"
      )

    print("VISIBLE NON-DIRECT FUNCTION SAMPLES")
    samples = [row for row in rows if not row[4] and row[5]][:32]
    if not samples:
      print("  NONE")
    for edge, function, premise_role, parent_role, _, _ in samples:
      print(
        f"  function={function.value:<13} "
        f"premise_role={premise_role.value:<15} parent_role={parent_role.value:<15} "
        f"premise={type(edge.premise_step.conclusion).__name__:<48} "
        f"parent={type(edge.parent_step.conclusion).__name__}"
      )

    print("HIDDEN DIRECT EVIDENCE")
    hidden_direct = [row for row in rows if row[4] and not row[5]]
    if not hidden_direct:
      print("  NONE")
    for edge, function, premise_role, parent_role, _, _ in hidden_direct[:24]:
      print(
        f"  function={function.value:<13} "
        f"premise_role={premise_role.value:<15} parent_role={parent_role.value:<15} "
        f"premise={type(edge.premise_step.conclusion).__name__:<48} "
        f"parent={type(edge.parent_step.conclusion).__name__}"
      )

    print("VISIBLE SUPPORT_ONLY SAMPLES")
    support_only = [
      row for row in rows
      if row[1] is EvidenceFunction.SUPPORT_ONLY and row[5]
    ][:24]
    if not support_only:
      print("  NONE")
    for edge, function, premise_role, parent_role, owner_direct, _ in support_only:
      print(
        f"  direct_owner={'Y' if owner_direct else 'N'} "
        f"premise_role={premise_role.value:<15} parent_role={parent_role.value:<15} "
        f"premise={type(edge.premise_step.conclusion).__name__:<48} "
        f"parent={type(edge.parent_step.conclusion).__name__}"
      )
    print()

  print("=" * 132)
  print("SUMMARY")
  print("=" * 132)
  print("function direct_selected_owner visible count")
  for key, count in sorted(grand.items()):
    function, owner_direct, is_visible = key
    print(
      f"{function:<13} direct_owner={'Y' if owner_direct else 'N'} "
      f"visible={'Y' if is_visible else 'N'} count={count:5d}"
    )
  print()
  print("INTERPRETATION")
  print("1. ESTABLISH means the premise participates in deriving a definition/order/group/membership claim or a DERIVATION transition.")
  print("2. COMPUTE means the edge is a calculation-chain relation.")
  print("3. EXACTNESS means exactness is structurally involved on the edge.")
  print("4. TRANSPORT means a map-property premise is used toward a group/order/membership claim.")
  print("5. REFERENCE means the premise has structured LiteratureReference provenance.")
  print("6. SUPPORT_ONLY is the residual category; it is the main place to look for missing typed evidence-function semantics.")
  print("7. direct_owner=Y is evidence immediately consumed by a selected final-claim Argument/provider.")
  print("8. If useful visible evidence is concentrated in named functions while SUPPORT_ONLY is mostly hidden, evidence-function semantics are promising.")
  print("9. If visible SUPPORT_ONLY remains large or mathematically essential, existing block/transition semantics are insufficient and must be refined before filtering.")
  print("10. This audit does not propose a production visibility policy.")

if __name__ == "__main__":
  main()
