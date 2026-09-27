from collections import Counter, defaultdict, deque

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_aggregate_semantics import (
  build_toda_group_proof_narrative_aggregate_semantic_sidecar,
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
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_evidence_contributions import (
  TodaGroupProofNarrativeEvidenceContribution,
  build_toda_group_proof_narrative_evidence_contribution_sidecar,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_proof_dependency import extract_toda_recursive_proof_provenance
from toda_rules import TodaEtaFamilyDefinitionStatement


TARGETS = ((3, 3), (5, 3), (4, 6), (5, 7), (8, 7), (9, 7))


def _context(n, k):
  report = build_standard_toda_report(n=n, k=k)
  group_result = report.candidates[0].source_candidate.group_result
  provenance = extract_toda_recursive_proof_provenance(group_result)
  max_depth = max(node.shortest_depth for node in provenance.nodes)
  replay = build_toda_group_result_proof_replay(group_result, max_depth=max_depth)
  presentation = build_toda_group_proof_presentation(replay)
  semantic_sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    presentation
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=semantic_sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=semantic_sidecar,
  )
  aggregate = build_toda_group_proof_narrative_aggregate_semantic_sidecar(
    presentation
  )
  contributions = build_toda_group_proof_narrative_evidence_contribution_sidecar(
    presentation,
    blocks,
    aggregate_semantic_sidecar=aggregate,
  )
  return presentation, semantic_sidecar, blocks, arguments, contributions


def _r4_visible_step_ids(
  presentation,
  semantic_sidecar,
  blocks,
  arguments,
  argument_index,
):
  argument = arguments[argument_index]
  local_body = extract_toda_group_proof_narrative_argument_local_body_blocks(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    argument_index,
  )
  hidden = set(
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      local_body,
      semantic_sidecar,
      argument,
    )
  )
  if argument.role is not TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION:
    hidden.update(
      id(step)
      for block in local_body
      for step in block.steps
      if isinstance(step.conclusion, TodaEtaFamilyDefinitionStatement)
    )
  return {
    id(step)
    for block in local_body
    for step in block.steps
    if id(step) not in hidden
  }


def _edges_by_parent(contributions):
  result = defaultdict(list)
  for semantic in contributions.edge_semantics:
    result[id(semantic.edge.parent_step)].append(semantic)
  return result


def _typed_premises(parent_step_ids, by_parent):
  result = set()
  contribution_counts = Counter()
  for parent_id in parent_step_ids:
    for semantic in by_parent[parent_id]:
      if (
        semantic.contribution
        is TodaGroupProofNarrativeEvidenceContribution.UNRESOLVED
      ):
        continue
      premise_id = id(semantic.edge.premise_step)
      result.add(premise_id)
      contribution_counts[semantic.contribution.value] += 1
  return result, contribution_counts


def main():
  print("=" * 118)
  print("Phase 144-6-R5-16 Narrative evidence relevance policy audit")
  print("=" * 118)
  print("Audit only. No production visibility or depth rule is changed.")
  print()

  global_counts = Counter()
  missing_l2_examples = []
  recursive_gain_examples = []

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      contributions,
    ) = _context(n, k)

    by_parent = _edges_by_parent(contributions)
    step_by_id = {
      id(node.proof_step): node.proof_step
      for node in presentation.nodes
    }

    print("-" * 118)
    print(f"TARGET ({n},{k}) arguments={len(arguments)}")

    for argument_index, argument in enumerate(arguments):
      conclusion_ids = {
        id(step)
        for step in argument.conclusion_block.steps
      }
      visible = _r4_visible_step_ids(
        presentation,
        semantic_sidecar,
        blocks,
        arguments,
        argument_index,
      )

      l1, l1_counts = _typed_premises(conclusion_ids, by_parent)
      l2, l2_counts = _typed_premises(l1, by_parent)
      l2_union = l1 | l2

      recursive = set(l1)
      frontier = set(l1)
      for _ in range(8):
        new, _ = _typed_premises(frontier, by_parent)
        new -= recursive
        if not new:
          break
        recursive |= new
        frontier = new

      visible_l1 = visible & l1
      visible_l2 = visible & l2_union
      visible_recursive = visible & recursive
      visible_not_l2 = visible - l2_union - conclusion_ids
      recursive_gain = visible_recursive - visible_l2

      global_counts["arguments"] += 1
      global_counts["visible"] += len(visible)
      global_counts["l1"] += len(l1)
      global_counts["l2_union"] += len(l2_union)
      global_counts["recursive"] += len(recursive)
      global_counts["visible_l1"] += len(visible_l1)
      global_counts["visible_l2"] += len(visible_l2)
      global_counts["visible_recursive"] += len(visible_recursive)
      global_counts["visible_not_l2"] += len(visible_not_l2)
      global_counts["recursive_gain"] += len(recursive_gain)

      print(
        f"A{argument_index:02d} role={argument.role.value:<28} "
        f"visible={len(visible):3d} "
        f"L1={len(l1):3d} "
        f"L1+L2={len(l2_union):3d} "
        f"recursive={len(recursive):3d} "
        f"visible∩L1={len(visible_l1):3d} "
        f"visible∩L1+L2={len(visible_l2):3d} "
        f"visible∩recursive={len(visible_recursive):3d} "
        f"visible_not_L2={len(visible_not_l2):3d}"
      )

      if visible_not_l2 and len(missing_l2_examples) < 24:
        roles = Counter()
        types = Counter()
        for step_id in visible_not_l2:
          block = next(
            block
            for block in blocks
            if any(id(step) == step_id for step in block.steps)
          )
          roles[block.role.value] += 1
          types[type(step_by_id[step_id].conclusion).__name__] += 1
        missing_l2_examples.append(
          (
            (n, k),
            argument_index,
            argument.role.value,
            tuple(roles.most_common()),
            tuple(types.most_common(8)),
          )
        )

      if recursive_gain and len(recursive_gain_examples) < 24:
        roles = Counter()
        for step_id in recursive_gain:
          block = next(
            block
            for block in blocks
            if any(id(step) == step_id for step in block.steps)
          )
          roles[block.role.value] += 1
        recursive_gain_examples.append(
          (
            (n, k),
            argument_index,
            argument.role.value,
            tuple(roles.most_common()),
          )
        )

  print()
  print("=" * 118)
  print("GLOBAL SUMMARY")
  print("=" * 118)
  for key in (
    "arguments",
    "visible",
    "l1",
    "l2_union",
    "recursive",
    "visible_l1",
    "visible_l2",
    "visible_recursive",
    "visible_not_l2",
    "recursive_gain",
  ):
    print(f"{key:<28} {global_counts[key]}")

  visible = global_counts["visible"]
  if visible:
    print(
      "visible_coverage_L1="
      f"{global_counts['visible_l1'] / visible:.6f}"
    )
    print(
      "visible_coverage_L1_L2="
      f"{global_counts['visible_l2'] / visible:.6f}"
    )
    print(
      "visible_coverage_recursive="
      f"{global_counts['visible_recursive'] / visible:.6f}"
    )

  print()
  print("VISIBLE EVIDENCE NOT EXPLAINED BY L1+L2")
  print("-" * 118)
  for item in missing_l2_examples:
    print(item)

  print()
  print("VISIBLE EVIDENCE GAINED ONLY BY RECURSIVE TYPED CLOSURE")
  print("-" * 118)
  for item in recursive_gain_examples:
    print(item)

  print()
  print("INTERPRETATION GUIDE")
  print("-" * 118)
  print(
    "1. If L1+L2 covers nearly all R4-visible evidence and recursive closure "
    "adds little, a two-level evidence boundary is promising."
  )
  print(
    "2. If recursive closure adds many visible steps but also grows far beyond "
    "R4, typed contribution alone still needs a stopping function."
  )
  print(
    "3. Inspect visible_not_L2 by block role/type. Repeated REFERENCE, "
    "EXACTNESS, CALCULATION, or DEFINITION patterns may define explicit "
    "promotion rules."
  )
  print(
    "4. Do not treat all_edge_unresolved as a relevance failure; this audit "
    "measures only evidence owned by Narrative Arguments."
  )


if __name__ == "__main__":
  main()
