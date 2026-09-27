from collections import Counter, defaultdict
from enum import Enum

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from proof import Relation, RelationType
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_aggregate_statement_catalog import is_toda_group_proof_aggregate_statement
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


class SupportRelation(Enum):
  CLAIM_INPUT = "CLAIM_INPUT"
  PROVIDER_INPUT = "PROVIDER_INPUT"
  REFERENCE_INPUT = "REFERENCE_INPUT"
  DEFINITION_INPUT = "DEFINITION_INPUT"
  STRUCTURAL_INPUT = "STRUCTURAL_INPUT"
  COMPUTATION_INPUT = "COMPUTATION_INPUT"
  PRECONDITION_INPUT = "PRECONDITION_INPUT"
  MAP_INPUT = "MAP_INPUT"
  AGGREGATE_INPUT = "AGGREGATE_INPUT"
  RESIDUAL_SUPPORT = "RESIDUAL_SUPPORT"


def group_result(n, k):
  return build_standard_toda_report(n=n, k=k).candidates[0].source_candidate.group_result


def full_state(result):
  provenance = extract_toda_recursive_proof_provenance(result)
  full_depth = max(node.shortest_depth for node in provenance.nodes)
  replay = build_toda_group_result_proof_replay(result, max_depth=full_depth)
  presentation = build_toda_group_proof_presentation(replay)
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(presentation)
  blocks = build_toda_group_proof_narrative_blocks(presentation, semantic_sidecar=sidecar)
  arguments = build_toda_group_proof_narrative_arguments(
    presentation, blocks, semantic_sidecar=sidecar
  )
  transitions = extract_toda_group_proof_narrative_transitions(
    presentation, blocks, arguments
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
  return {id(step): block for block in blocks for step in block.steps}


def r4_visible_ids(presentation, blocks, sidecar, arguments, claims):
  visible = set()
  for index, argument in claims:
    local = extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation, blocks, sidecar, arguments, index
    )
    hidden = _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation, blocks, local, sidecar, argument
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
  edge_roles = transition_roles.get((id(premise_block), id(parent_block)), set())
  if (
    TodaGroupProofNarrativeTransitionRole.CALCULATION_CHAIN in edge_roles
    or (
      premise_block.role is TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION
      and parent_block.role is TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION
    )
  ):
    return EvidenceFunction.COMPUTE
  if (
    premise_block.role is TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
    or parent_block.role is TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
  ):
    return EvidenceFunction.EXACTNESS
  if (
    premise_block.role is TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY
    and parent_block.role in (
      TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
      TodaGroupProofNarrativeMathematicalBlockRole.ORDER,
      TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP,
    )
  ):
    return EvidenceFunction.TRANSPORT
  if (
    TodaGroupProofNarrativeTransitionRole.DERIVATION in edge_roles
    or parent_block.role in (
      TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION,
      TodaGroupProofNarrativeMathematicalBlockRole.ORDER,
      TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
      TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP,
    )
  ):
    return EvidenceFunction.ESTABLISH
  return EvidenceFunction.SUPPORT_ONLY


def classify_support_relation(
  premise_block,
  parent_block,
  parent_is_claim,
  parent_is_provider,
):
  if parent_is_provider:
    return SupportRelation.PROVIDER_INPUT
  if parent_is_claim:
    return SupportRelation.CLAIM_INPUT
  if parent_block.role is TodaGroupProofNarrativeMathematicalBlockRole.REFERENCE:
    return SupportRelation.REFERENCE_INPUT
  if parent_block.role is TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION:
    return SupportRelation.DEFINITION_INPUT
  if parent_block.role in (
    TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
    TodaGroupProofNarrativeMathematicalBlockRole.ORDER,
    TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP,
  ):
    return SupportRelation.STRUCTURAL_INPUT
  if parent_block.role is TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION:
    return SupportRelation.COMPUTATION_INPUT
  if parent_block.role is TodaGroupProofNarrativeMathematicalBlockRole.PRECONDITION:
    return SupportRelation.PRECONDITION_INPUT
  if parent_block.role is TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY:
    return SupportRelation.MAP_INPUT
  if (
    any(is_toda_group_proof_aggregate_statement(step.conclusion) for step in parent_block.steps)
    or any(is_toda_group_proof_aggregate_statement(step.conclusion) for step in premise_block.steps)
  ):
    return SupportRelation.AGGREGATE_INPUT
  return SupportRelation.RESIDUAL_SUPPORT


def main():
  print("=" * 136)
  print("Phase 144-6-R5-15I SUPPORT_ONLY relation decomposition audit")
  print("=" * 136)
  print("Audit only. No production code, tests, or project documents are modified.")
  print("R5-15H SUPPORT_ONLY edges are decomposed by consumer relation, not by rule-name parsing.")
  print("Priority: direct selected-owner support, then visible nested support, then hidden nested support.")
  print()

  grand = Counter()
  direct_grand = Counter()

  for n, k in TARGETS:
    result = group_result(n, k)
    provenance, full_depth, presentation, sidecar, blocks, arguments, transitions = full_state(result)
    comps = final_components(presentation)
    claims = required_claim_arguments(arguments, comps)
    providers = provider_steps(presentation, provenance, comps)
    visible = r4_visible_ids(presentation, blocks, sidecar, arguments, claims)
    blocks_by_step = block_by_step_id(blocks)
    transition_roles = transition_roles_by_edge(transitions)

    claim_steps = {
      id(step)
      for _, argument in claims
      for step in (extract_toda_group_proof_narrative_argument_conclusion_step(argument),)
      if step is not None
    }
    provider_ids = {id(step) for step in providers}
    selected_owner_ids = claim_steps | provider_ids

    rows = []
    for edge in provenance.edges:
      premise = edge.premise_step
      parent = edge.parent_step
      premise_block = blocks_by_step.get(id(premise))
      parent_block = blocks_by_step.get(id(parent))
      if premise_block is None or parent_block is None:
        continue
      function = classify_evidence_function(
        premise, parent, premise_block, parent_block, transition_roles
      )
      if function is not EvidenceFunction.SUPPORT_ONLY:
        continue
      relation = classify_support_relation(
        premise_block,
        parent_block,
        id(parent) in claim_steps,
        id(parent) in provider_ids,
      )
      direct_owner = id(parent) in selected_owner_ids
      is_visible = id(premise) in visible
      rows.append(
        (edge, relation, premise_block.role, parent_block.role, direct_owner, is_visible)
      )
      key = (relation.value, direct_owner, is_visible)
      grand[key] += 1
      if direct_owner:
        direct_grand[(relation.value, is_visible)] += 1

    counts = Counter(
      (relation.value, direct_owner, is_visible)
      for _, relation, _, _, direct_owner, is_visible in rows
    )

    print("-" * 136)
    print(
      f"TARGET n={n}, k={k} full_depth={full_depth} "
      f"claims={len(claims)} providers={len(providers)} support_only_edges={len(rows)}"
    )
    print("RELATION MATRIX: relation direct_selected_owner visible count")
    for key, count in sorted(counts.items()):
      relation, direct_owner, is_visible = key
      print(
        f"  {relation:<20} direct_owner={'Y' if direct_owner else 'N'} "
        f"visible={'Y' if is_visible else 'N'} count={count:4d}"
      )

    print("DIRECT SELECTED-OWNER SUPPORT_ONLY")
    direct_rows = [row for row in rows if row[4]]
    if not direct_rows:
      print("  NONE")
    for edge, relation, premise_role, parent_role, _, is_visible in direct_rows:
      print(
        f"  relation={relation.value:<20} visible={'Y' if is_visible else 'N'} "
        f"premise_role={premise_role.value:<15} parent_role={parent_role.value:<15} "
        f"premise={type(edge.premise_step.conclusion).__name__:<52} "
        f"parent={type(edge.parent_step.conclusion).__name__}"
      )

    print("VISIBLE NESTED SUPPORT_ONLY BY RELATION")
    visible_nested = [row for row in rows if not row[4] and row[5]]
    relation_counts = Counter(row[1].value for row in visible_nested)
    if not relation_counts:
      print("  NONE")
    for relation, count in sorted(relation_counts.items()):
      print(f"  {relation:<20} count={count:4d}")

    print("VISIBLE NESTED RESIDUAL SAMPLES")
    residual = [
      row for row in visible_nested
      if row[1] is SupportRelation.RESIDUAL_SUPPORT
    ][:28]
    if not residual:
      print("  NONE")
    for edge, relation, premise_role, parent_role, _, _ in residual:
      print(
        f"  premise_role={premise_role.value:<15} parent_role={parent_role.value:<15} "
        f"premise={type(edge.premise_step.conclusion).__name__:<52} "
        f"parent={type(edge.parent_step.conclusion).__name__}"
      )

    print("HIDDEN NESTED SUPPORT_ONLY BY RELATION")
    hidden_nested = [row for row in rows if not row[4] and not row[5]]
    hidden_counts = Counter(row[1].value for row in hidden_nested)
    for relation, count in sorted(hidden_counts.items()):
      print(f"  {relation:<20} count={count:4d}")
    print()

  print("=" * 136)
  print("SUMMARY")
  print("=" * 136)
  print("relation direct_selected_owner visible count")
  for key, count in sorted(grand.items()):
    relation, direct_owner, is_visible = key
    print(
      f"{relation:<20} direct_owner={'Y' if direct_owner else 'N'} "
      f"visible={'Y' if is_visible else 'N'} count={count:5d}"
    )

  print()
  print("DIRECT-OWNER SUMMARY")
  print("relation visible count")
  for key, count in sorted(direct_grand.items()):
    relation, is_visible = key
    print(f"{relation:<20} visible={'Y' if is_visible else 'N'} count={count:4d}")

  print()
  print("INTERPRETATION")
  print("1. CLAIM_INPUT and PROVIDER_INPUT are ownership relations, not mathematical statement categories.")
  print("2. REFERENCE_INPUT, DEFINITION_INPUT, STRUCTURAL_INPUT, COMPUTATION_INPUT, PRECONDITION_INPUT, and MAP_INPUT describe the consumer function of residual support.")
  print("3. AGGREGATE_INPUT detects generic aggregate-statement participation without parsing inference-rule names.")
  print("4. RESIDUAL_SUPPORT is the remaining gap after consumer-side decomposition.")
  print("5. The 17 direct-owner SUPPORT_ONLY edges from R5-15H should fall primarily into CLAIM_INPUT or PROVIDER_INPUT.")
  print("6. If the four hidden direct-owner edges are PROVIDER_INPUT while analogous visible direct-owner evidence is also PROVIDER_INPUT, ownership relation alone still cannot decide visibility.")
  print("7. Visible nested SUPPORT_ONLY should be inspected by relation; a small RESIDUAL_SUPPORT count would mean consumer-side relation semantics explain most of the gap.")
  print("8. A large visible RESIDUAL_SUPPORT count means the next audit must inspect structural statement shape or typed provider semantics, not replay depth.")
  print("9. This audit does not change the production visibility policy.")

if __name__ == "__main__":
  main()
