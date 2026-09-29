from dataclasses import dataclass

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

@dataclass(frozen=True)
class Component:
  kind: str
  target_group: object
  generator: object | None = None
  order: int | None = None

def group_result(n, k):
  return build_standard_toda_report(n=n, k=k).candidates[0].source_candidate.group_result

def state(result, depth):
  replay = build_toda_group_result_proof_replay(result, max_depth=depth)
  presentation = build_toda_group_proof_presentation(replay)
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(presentation)
  blocks = build_toda_group_proof_narrative_blocks(presentation, semantic_sidecar=sidecar)
  arguments = build_toda_group_proof_narrative_arguments(
    presentation, blocks, semantic_sidecar=sidecar
  )
  markdown = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation, blocks, sidecar, arguments
  )
  return replay, presentation, blocks, arguments, markdown

def components(presentation):
  statement = presentation.root_step.conclusion
  if not (
    isinstance(statement, Relation)
    and statement.relation_type is RelationType.EQUALITY
    and isinstance(statement.lhs, TodaPrimaryGroup)
  ):
    return ()
  target = statement.lhs
  structure = statement.rhs
  result = []
  if isinstance(structure, FreeCyclicGroup):
    result.append(Component("generator", target, structure.generator))
  elif isinstance(structure, FiniteCyclicGroup):
    result.append(Component("generator", target, structure.generator))
    result.append(Component("order", target, structure.generator, structure.order))
  elif isinstance(structure, DirectSumGroup):
    for index, summand in enumerate(structure.summands):
      if isinstance(summand, FreeCyclicGroup):
        result.append(Component(f"summand[{index}].generator", target, summand.generator))
      elif isinstance(summand, FiniteCyclicGroup):
        result.append(Component(f"summand[{index}].generator", target, summand.generator))
        result.append(Component(f"summand[{index}].order", target, summand.generator, summand.order))
  return tuple(result)

def required_claims(arguments, comps):
  result = []
  for argument in arguments:
    subject = extract_toda_group_proof_narrative_argument_purpose_subject(argument)
    include = argument.role is TodaGroupProofNarrativeArgumentRole.ESTABLISH_GROUP_STRUCTURE
    if argument.role is TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION:
      include = subject is not None and any(c.generator == subject for c in comps)
    if argument.role is TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER:
      step = extract_toda_group_proof_narrative_argument_conclusion_step(argument)
      s = None if step is None else step.conclusion
      include = (
        subject is not None
        and isinstance(s, Relation)
        and s.relation_type is RelationType.ORDER
        and any(
          c.kind.endswith("order") and c.generator == subject and c.order == s.rhs
          for c in comps
        )
      )
    if include:
      result.append(argument)
  return tuple(result)

def provider_steps(presentation, provenance, comps):
  result = []
  for node in provenance.nodes:
    step = node.proof_step
    s = step.conclusion
    if isinstance(s, TodaProp515Pi12_5HopfIsomorphismStatement):
      if any(c.target_group == s.map.source_group for c in comps):
        result.append(step)
    elif isinstance(s, Toda515Sigma8TransportedDecompositionStatement):
      target = s.prop44_isomorphism.map.target_group
      if any(c.target_group == target for c in comps):
        result.append(step)
    elif isinstance(s, Toda48Pi16_9OrderAndE4InjectiveStatement):
      if any(
        c.kind.endswith("order") and c.target_group == s.target_group and c.order == s.target_order
        for c in comps
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
    sig = (type(step.conclusion).__name__, repr(step.conclusion))
    if sig not in seen:
      seen.add(sig)
      unique.append(step)
  return tuple(unique)

def claim_sig(argument):
  return (
    argument.role.value,
    repr(extract_toda_group_proof_narrative_argument_purpose_subject(argument)),
  )

def provider_sig(step):
  return (type(step.conclusion).__name__, repr(step.conclusion))

def count_refs(markdown):
  return sum(markdown.count(f"[R{i}]") for i in range(1, 100))

def count_tags(markdown):
  return sum(markdown.count(f"\\tag{{{i}}}") for i in range(1, 100))

def main():
  print("=" * 110)
  print("Phase 144-6-R5-15C claim-provider conclusion depth sufficiency audit")
  print("=" * 110)
  print("Audit only. No production code, tests, or project documents are modified.")
  print("No n/k-specific depth rule and no inference-rule-name parsing are used.")
  print()
  rows = []
  for n, k in TARGETS:
    result = group_result(n, k)
    provenance = extract_toda_recursive_proof_provenance(result)
    full_depth = max(node.shortest_depth for node in provenance.nodes)
    depth_by_id = {id(node.proof_step): node.shortest_depth for node in provenance.nodes}

    _, full_presentation, _, full_arguments, full_markdown = state(result, full_depth)
    comps = components(full_presentation)
    claims = required_claims(full_arguments, comps)
    providers = provider_steps(full_presentation, provenance, comps)

    depths = [0]
    for argument in claims:
      step = extract_toda_group_proof_narrative_argument_conclusion_step(argument)
      if step is not None:
        depths.append(depth_by_id.get(id(step), 0))
    for step in providers:
      depths.append(depth_by_id.get(id(step), 0))
    candidate_depth = max(depths)

    replay, cand_presentation, cand_blocks, cand_arguments, cand_markdown = state(
      result, candidate_depth
    )
    cand_claims = required_claims(cand_arguments, comps)
    replay_ids = {id(item.proof_step) for item in replay.steps}
    cand_providers = tuple(
      step for step in provider_steps(cand_presentation, provenance, comps)
      if id(step) in replay_ids
    )

    missing_claims = {claim_sig(a) for a in claims} - {claim_sig(a) for a in cand_claims}
    missing_providers = {provider_sig(s) for s in providers} - {provider_sig(s) for s in cand_providers}

    full_refs, cand_refs = count_refs(full_markdown), count_refs(cand_markdown)
    full_tags, cand_tags = count_tags(full_markdown), count_tags(cand_markdown)

    print("-" * 110)
    print(f"TARGET n={n}, k={k} full_depth={full_depth} candidate_depth={candidate_depth} saving={full_depth-candidate_depth}")
    print("FULL REQUIRED CLAIMS")
    for a in claims:
      step = extract_toda_group_proof_narrative_argument_conclusion_step(a)
      print(
        f"  depth={None if step is None else depth_by_id.get(id(step))} "
        f"role={a.role.value} "
        f"subject={extract_toda_group_proof_narrative_argument_purpose_subject(a)!r}"
      )
    print("FULL REQUIRED PROVIDERS")
    if not providers:
      print("  NONE")
    for step in providers:
      print(f"  depth={depth_by_id.get(id(step))} type={type(step.conclusion).__name__}")

    print(
      f"candidate_arguments={len(cand_arguments)} "
      f"candidate_required_claims={len(cand_claims)} candidate_blocks={len(cand_blocks)}"
    )
    print(f"claims_preserved={not missing_claims} providers_preserved={not missing_providers}")
    if missing_claims:
      print("MISSING CLAIMS")
      for role, subject in sorted(missing_claims):
        print(f"  role={role} subject={subject}")
    if missing_providers:
      print("MISSING PROVIDERS")
      for statement_type, _ in sorted(missing_providers):
        print(f"  type={statement_type}")

    print(f"full_reference_count={full_refs} candidate_reference_count={cand_refs}")
    print(f"full_equation_tag_count={full_tags} candidate_equation_tag_count={cand_tags}")
    print(f"candidate_markdown_chars={len(cand_markdown)}")

    if (n, k) == (3, 3):
      print("PI6 BENCHMARK CHECKS")
      print(f"  candidate_depth_is_3={candidate_depth == 3}")
      print(f"  has_references={cand_refs > 0}")
      print(f"  has_equation_tags={cand_tags > 0}")
      print("PI6 CANDIDATE MARKDOWN")
      print(cand_markdown)
      print("END PI6 CANDIDATE MARKDOWN")

    sufficient = (
      not missing_claims
      and not missing_providers
      and bool(cand_markdown.strip())
      and ((n, k) != (3, 3) or candidate_depth == 3)
    )
    status = "SUFFICIENT" if sufficient else "INSUFFICIENT"
    print(f"status={status}")
    print()
    rows.append(
      (n, k, full_depth, candidate_depth, len(claims), len(providers),
       len(missing_claims), len(missing_providers), full_refs, cand_refs,
       full_tags, cand_tags, status)
    )

  print("=" * 110)
  print("SUMMARY")
  print("=" * 110)
  print("n k full candidate claims providers missing_claims missing_providers full_refs candidate_refs full_tags candidate_tags status")
  for row in rows:
    print(" ".join(str(value) for value in row))
  print()
  print("INTERPRETATION")
  print("1. Candidate depth is the maximum conclusion depth of required claims/providers.")
  print("2. The complete generic Narrative pipeline is rebuilt at candidate depth.")
  print("3. pi_6^3 succeeds only if candidate depth is 3 and required claims/providers survive.")
  print("4. Reference/equation counts are diagnostics: losses identify missing supporting evidence.")
  print("5. If claims/providers survive but text quality drops, the remaining problem is supporting-evidence selection, not claim-provider selection.")
  print("6. Production depth-policy validation should wait until all six representatives are structurally sufficient.")

if __name__ == "__main__":
  main()
