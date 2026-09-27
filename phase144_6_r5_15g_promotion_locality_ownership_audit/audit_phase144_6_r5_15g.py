from collections import Counter, defaultdict, deque
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

ELIGIBLE_ROLES = {
  TodaGroupProofNarrativeMathematicalBlockRole.PRECONDITION,
  TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION,
  TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP,
  TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION,
  TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS,
  TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY,
  TodaGroupProofNarrativeMathematicalBlockRole.ORDER,
  TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
}

class Candidate(Enum):
  REFERENCE = "REFERENCE"
  SEMANTIC = "SEMANTIC"
  OTHER = "OTHER"

def group_result(n, k):
  return build_standard_toda_report(n=n, k=k).candidates[0].source_candidate.group_result

def full_state(result):
  provenance = extract_toda_recursive_proof_provenance(result)
  full_depth = max(node.shortest_depth for node in provenance.nodes)
  replay = build_toda_group_result_proof_replay(result, max_depth=full_depth)
  presentation = build_toda_group_proof_presentation(replay)
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(presentation)
  blocks = build_toda_group_proof_narrative_blocks(presentation, semantic_sidecar=sidecar)
  arguments = build_toda_group_proof_narrative_arguments(presentation, blocks, semantic_sidecar=sidecar)
  return provenance, full_depth, presentation, sidecar, blocks, arguments

def final_components(presentation):
  s = presentation.root_step.conclusion
  if not (isinstance(s, Relation) and s.relation_type is RelationType.EQUALITY and isinstance(s.lhs, TodaPrimaryGroup)):
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
    if isinstance(step.conclusion, (
      Toda56Nu4DecompositionStatement,
      Toda515Sigma8TransportedDecompositionStatement,
      TodaProp515Pi12_5HopfIsomorphismStatement,
      Toda48Pi16_9OrderAndE4InjectiveStatement,
    )):
      out.append(step)
  unique, seen = [], set()
  for step in out:
    key = (type(step.conclusion).__name__, repr(step.conclusion))
    if key not in seen:
      seen.add(key)
      unique.append(step)
  return tuple(unique)

def role_by_step_id(blocks):
  return {id(step): block.role for block in blocks for step in block.steps}

def children_by_parent(provenance):
  out = defaultdict(list)
  for edge in provenance.edges:
    out[id(edge.parent_step)].append(edge.premise_step)
  return out

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

def candidate_kind(step, role):
  if extract_toda_group_proof_step_literature_reference(step) is not None:
    return Candidate.REFERENCE
  if role in ELIGIBLE_ROLES:
    return Candidate.SEMANTIC
  return Candidate.OTHER

def locality_from_owners(owners, children, boundary_ids):
  best = {}
  queue = deque()
  for owner_label, owner_step in owners:
    for child in children.get(id(owner_step), ()):
      queue.append((child, owner_label, 1, False))
  while queue:
    step, owner_label, distance, crossed = queue.popleft()
    sid = id(step)
    previous = best.get((sid, owner_label))
    if previous is not None and previous <= (distance, crossed):
      continue
    best[(sid, owner_label)] = (distance, crossed)
    next_crossed = crossed or sid in boundary_ids
    for child in children.get(sid, ()):
      queue.append((child, owner_label, distance + 1, next_crossed))
  return best

def main():
  print("=" * 132)
  print("Phase 144-6-R5-15G promotion locality / ownership audit")
  print("=" * 132)
  print("Audit only. No production code, tests, or project documents are modified.")
  print("Locality = shortest selected-owner premise distance + whether another Argument/provider boundary is crossed.")
  print("No n/k-specific visibility rule and no inference-rule-name parsing are used.")
  print()

  grand = Counter()

  for n, k in TARGETS:
    result = group_result(n, k)
    provenance, full_depth, presentation, sidecar, blocks, arguments = full_state(result)
    comps = final_components(presentation)
    claims = required_claim_arguments(arguments, comps)
    providers = provider_steps(presentation, provenance, comps)
    roles = role_by_step_id(blocks)
    children = children_by_parent(provenance)
    visible = r4_visible_ids(presentation, blocks, sidecar, arguments, claims)

    owners = []
    selected_owner_ids = set()
    for index, argument in claims:
      step = extract_toda_group_proof_narrative_argument_conclusion_step(argument)
      if step is not None:
        label = f"claim:{argument.role.value}:{type(step.conclusion).__name__}"
        owners.append((label, step))
        selected_owner_ids.add(id(step))
    for step in providers:
      label = f"provider:{type(step.conclusion).__name__}"
      owners.append((label, step))
      selected_owner_ids.add(id(step))

    all_argument_conclusion_ids = {
      id(step)
      for argument in arguments
      for step in (extract_toda_group_proof_narrative_argument_conclusion_step(argument),)
      if step is not None
    }
    provider_ids = {id(step) for step in providers}
    boundary_ids = (all_argument_conclusion_ids | provider_ids) - selected_owner_ids
    locality = locality_from_owners(owners, children, boundary_ids)

    rows = []
    for node in provenance.nodes:
      step = node.proof_step
      sid = id(step)
      if sid in selected_owner_ids:
        continue
      matches = [
        (owner_label, distance, crossed)
        for (step_id, owner_label), (distance, crossed) in locality.items()
        if step_id == sid
      ]
      if not matches:
        continue
      owner_label, distance, crossed = min(matches, key=lambda x: (x[1], x[2], x[0]))
      role = roles.get(sid, TodaGroupProofNarrativeMathematicalBlockRole.OTHER)
      kind = candidate_kind(step, role)
      is_visible = sid in visible
      rows.append((node, kind, role, owner_label, distance, crossed, is_visible))

    counts = Counter()
    for _, kind, role, _, distance, crossed, is_visible in rows:
      bucket = "1" if distance == 1 else "2" if distance == 2 else "3+"
      counts[(kind.value, bucket, crossed, is_visible)] += 1
      grand[(kind.value, bucket, crossed, is_visible)] += 1

    print("-" * 132)
    print(f"TARGET n={n}, k={k} full_depth={full_depth} selected_owners={len(owners)}")
    print("SELECTED OWNERS")
    for label, step in owners:
      print(f"  {label}")
    print("LOCALITY MATRIX: kind distance crossed_boundary visible count")
    for key, count in sorted(counts.items()):
      kind, bucket, crossed, is_visible = key
      print(f"  {kind:<10} d={bucket:<2} crossed={'Y' if crossed else 'N'} visible={'Y' if is_visible else 'N'} count={count:4d}")

    print("VISIBLE SEMANTIC/REFERENCE BY LOCALITY")
    visible_rows = [
      row for row in rows
      if row[6] and row[1] in (Candidate.SEMANTIC, Candidate.REFERENCE)
    ]
    for node, kind, role, owner_label, distance, crossed, _ in visible_rows[:32]:
      print(
        f"  depth={node.shortest_depth:<2} owner_distance={distance:<2} "
        f"crossed={'Y' if crossed else 'N'} kind={kind.value:<9} "
        f"role={role.value:<15} type={type(node.proof_step.conclusion).__name__:<48} "
        f"owner={owner_label}"
      )

    print("HIDDEN ELIGIBLE NEAR-OWNER SAMPLES")
    near_hidden = [
      row for row in rows
      if not row[6]
      and row[1] in (Candidate.SEMANTIC, Candidate.REFERENCE)
      and row[4] <= 2
      and not row[5]
    ][:20]
    if not near_hidden:
      print("  NONE")
    for node, kind, role, owner_label, distance, crossed, _ in near_hidden:
      print(
        f"  depth={node.shortest_depth:<2} owner_distance={distance:<2} "
        f"kind={kind.value:<9} role={role.value:<15} "
        f"type={type(node.proof_step.conclusion).__name__:<48} owner={owner_label}"
      )

    print("VISIBLE DEEP/CROSSED ELIGIBLE SAMPLES")
    deep_visible = [
      row for row in rows
      if row[6]
      and row[1] in (Candidate.SEMANTIC, Candidate.REFERENCE)
      and (row[4] >= 3 or row[5])
    ][:20]
    if not deep_visible:
      print("  NONE")
    for node, kind, role, owner_label, distance, crossed, _ in deep_visible:
      print(
        f"  depth={node.shortest_depth:<2} owner_distance={distance:<2} "
        f"crossed={'Y' if crossed else 'N'} kind={kind.value:<9} "
        f"role={role.value:<15} type={type(node.proof_step.conclusion).__name__:<48} "
        f"owner={owner_label}"
      )
    print()

  print("=" * 132)
  print("SUMMARY")
  print("=" * 132)
  print("kind distance crossed_boundary visible count")
  for key, count in sorted(grand.items()):
    kind, bucket, crossed, is_visible = key
    print(f"{kind:<10} d={bucket:<2} crossed={'Y' if crossed else 'N'} visible={'Y' if is_visible else 'N'} count={count:5d}")
  print()
  print("INTERPRETATION")
  print("1. Distance 1 is direct evidence of a selected claim/provider.")
  print("2. Distance 2 is one supporting layer below direct evidence.")
  print("3. Distance 3+ is recursive expansion and should require a stronger reason than semantic role alone.")
  print("4. crossed_boundary=Y means the path passed through another non-selected Argument/provider conclusion.")
  print("5. A strong locality rule would retain most useful visible semantic/reference evidence at small distance without crossing a boundary.")
  print("6. Hidden eligible evidence at d<=2/no-crossing indicates that locality alone may still over-promote.")
  print("7. Visible eligible evidence at d>=3 or after crossing a boundary identifies cases needing semantic promotion exceptions or ownership reassignment.")
  print("8. Do not turn a numeric distance threshold into production policy unless the six representative groups support the same structural interpretation.")

if __name__ == "__main__":
  main()
