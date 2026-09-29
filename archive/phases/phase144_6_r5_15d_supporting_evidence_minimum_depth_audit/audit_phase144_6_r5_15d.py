from collections import Counter
import re

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from proof import Relation, RelationType
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_argument_multi_renderer import render_toda_group_proof_narrative_multi_argument_markdown
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
  extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_blocks import build_toda_group_proof_narrative_blocks
from toda_group_proof_narrative_references import build_toda_group_proof_narrative_reference_entries
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


def group_result(n, k):
  return build_standard_toda_report(n=n, k=k).candidates[0].source_candidate.group_result


def state(result, depth):
  replay = build_toda_group_result_proof_replay(result, max_depth=depth)
  presentation = build_toda_group_proof_presentation(replay)
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(presentation)
  blocks = build_toda_group_proof_narrative_blocks(presentation, semantic_sidecar=sidecar)
  arguments = build_toda_group_proof_narrative_arguments(presentation, blocks, semantic_sidecar=sidecar)
  transitions = extract_toda_group_proof_narrative_transitions(presentation, blocks, arguments)
  references = build_toda_group_proof_narrative_reference_entries(presentation)
  markdown = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation, blocks, sidecar, arguments
  )
  return replay, presentation, arguments, transitions, references, markdown


def final_components(presentation):
  s = presentation.root_step.conclusion
  if not (isinstance(s, Relation) and s.relation_type is RelationType.EQUALITY and isinstance(s.lhs, TodaPrimaryGroup)):
    return ()
  target, structure = s.lhs, s.rhs
  out = []
  summands = structure.summands if isinstance(structure, DirectSumGroup) else (structure,)
  for summand in summands:
    if isinstance(summand, FreeCyclicGroup):
      out.append(("generator", target, summand.generator, None))
    elif isinstance(summand, FiniteCyclicGroup):
      out.append(("generator", target, summand.generator, None))
      out.append(("order", target, summand.generator, summand.order))
  return tuple(out)


def required_claims(arguments, comps):
  out = []
  for a in arguments:
    subject = extract_toda_group_proof_narrative_argument_purpose_subject(a)
    include = a.role is TodaGroupProofNarrativeArgumentRole.ESTABLISH_GROUP_STRUCTURE
    if a.role is TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION:
      include = any(c[2] == subject for c in comps)
    if a.role is TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER:
      step = extract_toda_group_proof_narrative_argument_conclusion_step(a)
      s = None if step is None else step.conclusion
      include = (
        isinstance(s, Relation)
        and s.relation_type is RelationType.ORDER
        and any(c[0] == "order" and c[2] == subject and c[3] == s.rhs for c in comps)
      )
    if include:
      out.append(a)
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


def claim_sig(a):
  return (a.role.value, repr(extract_toda_group_proof_narrative_argument_purpose_subject(a)))


def provider_sig(step):
  return (type(step.conclusion).__name__, repr(step.conclusion))


def snapshot(result, depth, provenance, comps, full_claims, full_providers):
  replay, presentation, arguments, transitions, references, markdown = state(result, depth)
  claims = {claim_sig(a) for a in required_claims(arguments, comps)}
  replay_ids = {id(item.proof_step) for item in replay.steps}
  providers = {
    provider_sig(step)
    for step in provider_steps(presentation, provenance, comps)
    if id(step) in replay_ids
  }
  tc = Counter(t.role for t in transitions)
  roles = tuple(sorted(Counter(a.role.value for a in arguments).items()))
  return {
    "depth": depth,
    "struct": full_claims <= claims and full_providers <= providers,
    "roles": roles,
    "refs": len(references),
    "calc": tc[TodaGroupProofNarrativeTransitionRole.CALCULATION_CHAIN],
    "support": tc[TodaGroupProofNarrativeTransitionRole.SUPPORT],
    "deriv": tc[TodaGroupProofNarrativeTransitionRole.DERIVATION],
    "tags": len(re.findall(r"\\tag\{\d+\}", markdown)),
    "chars": len(markdown),
    "markdown": markdown,
  }


def first_depth(rows, key):
  for row in rows:
    if row[key] > 0:
      return row["depth"]
  return None


def main():
  print("=" * 120)
  print("Phase 144-6-R5-15D supporting-evidence minimum depth audit")
  print("=" * 120)
  print("Audit only. No production code, tests, or project documents are modified.")
  print("Full-depth reference/equation counts are diagnostics, not completion criteria.")
  print()

  summary = []
  for n, k in TARGETS:
    result = group_result(n, k)
    provenance = extract_toda_recursive_proof_provenance(result)
    full_depth = max(node.shortest_depth for node in provenance.nodes)
    depth_by_id = {id(node.proof_step): node.shortest_depth for node in provenance.nodes}

    _, full_presentation, full_arguments, _, _, _ = state(result, full_depth)
    comps = final_components(full_presentation)
    claims = required_claims(full_arguments, comps)
    providers = provider_steps(full_presentation, provenance, comps)
    full_claim_sigs = {claim_sig(a) for a in claims}
    full_provider_sigs = {provider_sig(s) for s in providers}

    depths = [0]
    for a in claims:
      step = extract_toda_group_proof_narrative_argument_conclusion_step(a)
      if step is not None:
        depths.append(depth_by_id.get(id(step), 0))
    depths.extend(depth_by_id.get(id(step), 0) for step in providers)
    d_claim = max(depths)

    rows = [
      snapshot(result, d, provenance, comps, full_claim_sigs, full_provider_sigs)
      for d in range(d_claim, full_depth + 1)
    ]

    print("-" * 120)
    print(f"TARGET n={n}, k={k} D_claim={d_claim} full_depth={full_depth}")
    print("d struct refs calc support deriv tags chars roles event")
    previous = None
    events = []
    for row in rows:
      key = (
        row["struct"], row["roles"], row["refs"], row["calc"],
        row["support"], row["deriv"], row["tags"]
      )
      event = key != previous
      if event:
        events.append(row["depth"])
      roles = ",".join(f"{name}:{count}" for name, count in row["roles"])
      print(
        f'{row["depth"]:2d} {"Y" if row["struct"] else "N":>6} '
        f'{row["refs"]:4d} {row["calc"]:4d} {row["support"]:7d} '
        f'{row["deriv"]:5d} {row["tags"]:4d} {row["chars"]:5d} '
        f'{roles} {"*" if event else ""}'
      )
      previous = key

    milestones = {
      "first_ref": first_depth(rows, "refs"),
      "first_calc": first_depth(rows, "calc"),
      "first_deriv": first_depth(rows, "deriv"),
      "first_tag": first_depth(rows, "tags"),
    }
    print("MILESTONES " + " ".join(f"{k}={v}" for k, v in milestones.items()))
    print(f"event_depths={events}")

    preview_depths = []
    for d in (d_claim, *milestones.values()):
      if d is not None and d not in preview_depths:
        preview_depths.append(d)
    print("EVENT PREVIEWS")
    for d in preview_depths:
      md = next(row["markdown"] for row in rows if row["depth"] == d)
      print(f"--- depth={d} ---")
      print(md if len(md) <= 1800 else md[:1800] + f"\n... [truncated; total chars={len(md)}]")
      print(f"--- end depth={d} ---")

    summary.append((n, k, d_claim, full_depth, milestones["first_ref"], milestones["first_calc"], milestones["first_deriv"], milestones["first_tag"], ",".join(map(str, events))))
    print()

  print("=" * 120)
  print("SUMMARY")
  print("n k D_claim full first_ref first_calc first_deriv first_tag event_depths")
  for row in summary:
    print(" ".join(str(value) for value in row))
  print()
  print("INTERPRETATION")
  print("1. '*' means the semantic evidence signature changed at that depth.")
  print("2. First Reference/calculation/derivation/tag depths are evidence milestones, not universal pass criteria.")
  print("3. Do not select full depth merely because counts keep increasing; later evidence may belong to recursively expanded support proofs.")
  print("4. Inspect previews to find the first depth that explains the final claim rather than merely states it.")
  print("5. A common generic milestone across the six groups can become the R5-16 minimum-depth policy.")
  print("6. If no common milestone exists, supporting evidence must be selected by semantic relation to the final claim/provider.")

if __name__ == "__main__":
  main()
