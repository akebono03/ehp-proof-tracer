from collections import Counter, defaultdict
from dataclasses import dataclass
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
from toda_group_proof_narrative_blocks import build_toda_group_proof_narrative_blocks
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


class Ownership(Enum):
  CLAIM_EVIDENCE = "CLAIM_EVIDENCE"
  PROVIDER_EVIDENCE = "PROVIDER_EVIDENCE"
  NESTED_PROOF = "NESTED_PROOF"
  UNRELATED_SUPPORT = "UNRELATED_SUPPORT"


@dataclass(frozen=True)
class Owner:
  kind: str
  label: str
  step: object


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
  return provenance, full_depth, presentation, sidecar, blocks, arguments


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


def owner_label(prefix, step):
  return f"{prefix}:{type(step.conclusion).__name__}"


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


def visible_step_ids_for_argument(
  presentation, blocks, sidecar, arguments, argument_index
):
  argument = arguments[argument_index]
  local = extract_toda_group_proof_narrative_argument_local_body_blocks(
    presentation, blocks, sidecar, arguments, argument_index
  )
  hidden = _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
    presentation, blocks, local, sidecar, argument
  )
  return {
    id(step)
    for block in local
    for step in block.steps
    if id(step) not in hidden
  }


def statement_text(step):
  text = repr(step.conclusion)
  if len(text) > 180:
    text = text[:177] + "..."
  return text


def main():
  print("=" * 124)
  print("Phase 144-6-R5-15E supporting-evidence ownership / relevance audit")
  print("=" * 124)
  print("Audit only. No production code, tests, or project documents are modified.")
  print("Ownership uses proof edges and selected claim/provider boundaries; no n/k-specific rule and no rule-name parsing.")
  print()
  total_counts = Counter()
  total_visible = Counter()

  for n, k in TARGETS:
    result = group_result(n, k)
    provenance, full_depth, presentation, sidecar, blocks, arguments = full_state(result)
    depth_by_id = {id(node.proof_step): node.shortest_depth for node in provenance.nodes}
    comps = final_components(presentation)
    claim_arguments = required_claim_arguments(arguments, comps)
    providers = provider_steps(presentation, provenance, comps)
    children = children_by_parent(provenance)

    owners = []
    claim_owner_ids = set()
    provider_owner_ids = set()
    visible_by_owner = {}

    for index, argument in claim_arguments:
      step = extract_toda_group_proof_narrative_argument_conclusion_step(argument)
      if step is None:
        continue
      owner = Owner("claim", owner_label(argument.role.value, step), step)
      owners.append(owner)
      claim_owner_ids.add(id(step))
      visible_by_owner[id(step)] = visible_step_ids_for_argument(
        presentation, blocks, sidecar, arguments, index
      )

    for step in providers:
      owner = Owner("provider", owner_label("provider", step), step)
      owners.append(owner)
      provider_owner_ids.add(id(step))
      visible_by_owner[id(step)] = set()

    direct_claim = set()
    direct_provider = set()
    nested_claim = set()
    nested_provider = set()

    for owner in owners:
      direct = {id(step) for step in children.get(id(owner.step), ())}
      nested = descendants(owner.step, children) - direct
      if owner.kind == "claim":
        direct_claim |= direct
        nested_claim |= nested
      else:
        direct_provider |= direct
        nested_provider |= nested

    selected_owner_ids = claim_owner_ids | provider_owner_ids
    node_ids = {id(node.proof_step) for node in provenance.nodes}
    evidence_ids = node_ids - selected_owner_ids

    classifications = {}
    for step_id in evidence_ids:
      if step_id in direct_claim:
        classifications[step_id] = Ownership.CLAIM_EVIDENCE
      elif step_id in direct_provider:
        classifications[step_id] = Ownership.PROVIDER_EVIDENCE
      elif step_id in nested_claim or step_id in nested_provider:
        classifications[step_id] = Ownership.NESTED_PROOF
      else:
        classifications[step_id] = Ownership.UNRELATED_SUPPORT

    visible_union = set().union(*visible_by_owner.values()) if visible_by_owner else set()

    counts = Counter(classifications.values())
    visible_counts = Counter(
      classifications[step_id]
      for step_id in visible_union
      if step_id in classifications
    )
    total_counts.update(counts)
    total_visible.update(visible_counts)

    print("-" * 124)
    print(f"TARGET n={n}, k={k} full_depth={full_depth}")
    print("SELECTED OWNERS")
    for owner in owners:
      print(
        f"  kind={owner.kind:<8} depth={depth_by_id.get(id(owner.step))} "
        f"label={owner.label}"
      )
    print("OWNERSHIP COUNTS")
    for role in Ownership:
      print(
        f"  {role.value:<18} total={counts[role]:3d} "
        f"r4_visible={visible_counts[role]:3d}"
      )

    print("DIRECT EVIDENCE")
    for role in (Ownership.CLAIM_EVIDENCE, Ownership.PROVIDER_EVIDENCE):
      print(f"  [{role.value}]")
      rows = [
        node for node in provenance.nodes
        if classifications.get(id(node.proof_step)) is role
      ]
      if not rows:
        print("    NONE")
      for node in rows:
        sid = id(node.proof_step)
        print(
          f"    depth={node.shortest_depth:<2} "
          f"r4_visible={'Y' if sid in visible_union else 'N'} "
          f"type={type(node.proof_step.conclusion).__name__} "
          f"statement={statement_text(node.proof_step)}"
        )

    nested_rows = [
      node for node in provenance.nodes
      if classifications.get(id(node.proof_step)) is Ownership.NESTED_PROOF
    ]
    print("NESTED PROOF SAMPLE")
    if not nested_rows:
      print("  NONE")
    for node in nested_rows[:12]:
      sid = id(node.proof_step)
      print(
        f"  depth={node.shortest_depth:<2} "
        f"r4_visible={'Y' if sid in visible_union else 'N'} "
        f"type={type(node.proof_step.conclusion).__name__}"
      )

    unrelated_rows = [
      node for node in provenance.nodes
      if classifications.get(id(node.proof_step)) is Ownership.UNRELATED_SUPPORT
    ]
    print("UNRELATED SUPPORT SAMPLE")
    if not unrelated_rows:
      print("  NONE")
    for node in unrelated_rows[:8]:
      print(
        f"  depth={node.shortest_depth:<2} "
        f"type={type(node.proof_step.conclusion).__name__}"
      )

    print("BOUNDARY DIAGNOSTICS")
    print(f"  selected_owner_count={len(owners)}")
    print(f"  direct_evidence_count={counts[Ownership.CLAIM_EVIDENCE] + counts[Ownership.PROVIDER_EVIDENCE]}")
    print(f"  nested_proof_count={counts[Ownership.NESTED_PROOF]}")
    print(f"  unrelated_support_count={counts[Ownership.UNRELATED_SUPPORT]}")
    print(f"  r4_visible_direct_count={visible_counts[Ownership.CLAIM_EVIDENCE] + visible_counts[Ownership.PROVIDER_EVIDENCE]}")
    print(f"  r4_visible_nested_count={visible_counts[Ownership.NESTED_PROOF]}")
    print()

  print("=" * 124)
  print("SUMMARY")
  print("=" * 124)
  for role in Ownership:
    print(
      f"{role.value:<18} total={total_counts[role]:4d} "
      f"r4_visible={total_visible[role]:4d}"
    )
  print()
  print("INTERPRETATION")
  print("1. CLAIM_EVIDENCE is a direct proof premise of a selected final-claim Argument conclusion.")
  print("2. PROVIDER_EVIDENCE is a direct proof premise of a selected typed provider.")
  print("3. NESTED_PROOF lies below those direct premises and represents recursive proof expansion.")
  print("4. UNRELATED_SUPPORT is outside the selected claim/provider ownership closure.")
  print("5. R4-visible overlap checks whether the current Argument-local frontier already approximates this ownership boundary.")
  print("6. If useful explanatory steps are mostly direct evidence while deep noise is mostly NESTED_PROOF, ownership is a viable Narrative boundary.")
  print("7. If required explanatory steps appear in NESTED_PROOF, the next audit must identify a generic semantic promotion rule rather than increase global depth.")

if __name__ == "__main__":
  main()
