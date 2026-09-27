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


class Promotion(Enum):
  PROMOTE = "PROMOTE"
  COLLAPSE_TO_REFERENCE = "COLLAPSE_TO_REFERENCE"
  HIDE = "HIDE"


PROMOTE_ROLES = {
  TodaGroupProofNarrativeMathematicalBlockRole.PRECONDITION,
  TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION,
  TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP,
  TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION,
  TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS,
  TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY,
  TodaGroupProofNarrativeMathematicalBlockRole.ORDER,
  TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
}

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
    sig = (type(step.conclusion).__name__, repr(step.conclusion))
    if sig not in seen:
      seen.add(sig)
      unique.append(step)
  return tuple(unique)

def children_by_parent(provenance):
  out = defaultdict(list)
  for edge in provenance.edges:
    out[id(edge.parent_step)].append(edge.premise_step)
  return out

def descendants(seed, children):
  seen = set()
  queue = list(children.get(id(seed), ()))
  while queue:
    step = queue.pop(0)
    if id(step) in seen:
      continue
    seen.add(id(step))
    queue.extend(children.get(id(step), ()))
  return seen

def visible_ids(presentation, blocks, sidecar, arguments, claim_arguments):
  visible = set()
  for index, argument in claim_arguments:
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

def role_by_step_id(blocks):
  out = {}
  for block in blocks:
    for step in block.steps:
      out[id(step)] = block.role
  return out

def classify_promotion(step, role):
  if extract_toda_group_proof_step_literature_reference(step) is not None:
    return Promotion.COLLAPSE_TO_REFERENCE
  if role in PROMOTE_ROLES:
    return Promotion.PROMOTE
  return Promotion.HIDE

def main():
  print("=" * 126)
  print("Phase 144-6-R5-15F nested-evidence semantic promotion audit")
  print("=" * 126)
  print("Audit only. No production code, tests, or project documents are modified.")
  print("Promotion uses block role + structured LiteratureReference + claim/provider ownership.")
  print("No n/k-specific rule and no inference-rule-name parsing are used.")
  print()

  grand_roles = Counter()
  grand_actions = Counter()
  grand_visible_actions = Counter()

  for n, k in TARGETS:
    result = group_result(n, k)
    provenance, full_depth, presentation, sidecar, blocks, arguments = full_state(result)
    comps = final_components(presentation)
    claims = required_claim_arguments(arguments, comps)
    providers = provider_steps(presentation, provenance, comps)
    children = children_by_parent(provenance)
    roles = role_by_step_id(blocks)
    visible = visible_ids(presentation, blocks, sidecar, arguments, claims)

    owner_steps = []
    for _, argument in claims:
      step = extract_toda_group_proof_narrative_argument_conclusion_step(argument)
      if step is not None:
        owner_steps.append(step)
    owner_steps.extend(providers)

    direct = set()
    nested = set()
    for owner in owner_steps:
      d = {id(step) for step in children.get(id(owner), ())}
      direct |= d
      nested |= descendants(owner, children) - d
    nested -= {id(step) for step in owner_steps}
    nested -= direct

    nested_nodes = [node for node in provenance.nodes if id(node.proof_step) in nested]
    role_counts = Counter()
    action_counts = Counter()
    visible_action_counts = Counter()
    action_role_counts = Counter()

    for node in nested_nodes:
      step = node.proof_step
      role = roles.get(id(step), TodaGroupProofNarrativeMathematicalBlockRole.OTHER)
      action = classify_promotion(step, role)
      role_counts[role.value] += 1
      action_counts[action.value] += 1
      action_role_counts[(action.value, role.value)] += 1
      if id(step) in visible:
        visible_action_counts[action.value] += 1

    grand_roles.update(role_counts)
    grand_actions.update(action_counts)
    grand_visible_actions.update(visible_action_counts)

    print("-" * 126)
    print(f"TARGET n={n}, k={k} full_depth={full_depth} nested={len(nested_nodes)} r4_visible_nested={sum(1 for node in nested_nodes if id(node.proof_step) in visible)}")
    print("NESTED BLOCK ROLE COUNTS")
    for role, count in sorted(role_counts.items()):
      print(f"  {role:<16} {count:4d}")
    print("PROMOTION CANDIDATE COUNTS")
    for action in Promotion:
      print(
        f"  {action.value:<22} total={action_counts[action.value]:4d} "
        f"r4_visible={visible_action_counts[action.value]:4d}"
      )
    print("ACTION x ROLE")
    for (action, role), count in sorted(action_role_counts.items()):
      if count:
        print(f"  {action:<22} {role:<16} {count:4d}")

    print("VISIBLE NESTED SAMPLES")
    samples = [
      node for node in nested_nodes
      if id(node.proof_step) in visible
    ][:24]
    if not samples:
      print("  NONE")
    for node in samples:
      step = node.proof_step
      role = roles.get(id(step), TodaGroupProofNarrativeMathematicalBlockRole.OTHER)
      action = classify_promotion(step, role)
      ref = extract_toda_group_proof_step_literature_reference(step)
      ref_text = "-" if ref is None else (ref.locator or ref.label)
      print(
        f"  depth={node.shortest_depth:<2} "
        f"action={action.value:<21} role={role.value:<15} "
        f"type={type(step.conclusion).__name__:<48} ref={ref_text}"
      )

    print("HIDDEN PROMOTION CANDIDATE SAMPLES")
    hidden_promote = [
      node for node in nested_nodes
      if id(node.proof_step) not in visible
      and classify_promotion(
        node.proof_step,
        roles.get(id(node.proof_step), TodaGroupProofNarrativeMathematicalBlockRole.OTHER),
      ) is Promotion.PROMOTE
    ][:16]
    if not hidden_promote:
      print("  NONE")
    for node in hidden_promote:
      step = node.proof_step
      role = roles.get(id(step), TodaGroupProofNarrativeMathematicalBlockRole.OTHER)
      print(
        f"  depth={node.shortest_depth:<2} role={role.value:<15} "
        f"type={type(step.conclusion).__name__}"
      )
    print()

  print("=" * 126)
  print("SUMMARY")
  print("=" * 126)
  print("NESTED ROLE TOTALS")
  for role, count in sorted(grand_roles.items()):
    print(f"{role:<16} {count:5d}")
  print("PROMOTION TOTALS")
  for action in Promotion:
    print(
      f"{action.value:<22} total={grand_actions[action.value]:5d} "
      f"r4_visible={grand_visible_actions[action.value]:5d}"
    )
  print()
  print("INTERPRETATION")
  print("1. COLLAPSE_TO_REFERENCE means the nested step already has structured LiteratureReference provenance.")
  print("2. PROMOTE means its existing generic mathematical block role is reader-facing evidence.")
  print("3. HIDE currently consists of nested OTHER material without structured literature provenance.")
  print("4. This is a candidate classification audit, not a production visibility policy.")
  print("5. If R4-visible nested evidence is mostly PROMOTE or COLLAPSE_TO_REFERENCE, the semantic promotion model explains current useful visibility.")
  print("6. If many R4-visible nested OTHER/HIDE steps are mathematically necessary, OTHER must be structurally refined before production filtering.")
  print("7. Hidden PROMOTE samples show the opposite risk: semantic role alone may over-promote recursively nested proofs.")
  print("8. The next step should test promotion locality/ownership so only evidence attached to the selected claim/provider is promoted.")

if __name__ == "__main__":
  main()
