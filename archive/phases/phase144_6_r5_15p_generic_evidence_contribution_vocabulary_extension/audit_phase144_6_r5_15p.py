from collections import Counter

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
)
from toda_group_proof_narrative_blocks import build_toda_group_proof_narrative_blocks
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
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=max_depth,
  )
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
  contributions = build_toda_group_proof_narrative_evidence_contribution_sidecar(
    presentation,
    blocks,
  )
  return presentation, semantic_sidecar, blocks, arguments, contributions


def _visibility(presentation, semantic_sidecar, blocks, arguments):
  visible = set()
  hidden = set()

  for argument_index, argument in enumerate(arguments):
    local_body = extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      argument_index,
    )
    hidden_ids = set(
      _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
        presentation,
        blocks,
        local_body,
        semantic_sidecar,
        argument,
      )
    )
    if argument.role is not TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION:
      hidden_ids.update(
        id(step)
        for block in local_body
        for step in block.steps
        if isinstance(step.conclusion, TodaEtaFamilyDefinitionStatement)
      )
    for block in local_body:
      for step in block.steps:
        if id(step) in hidden_ids:
          hidden.add(id(step))
        else:
          visible.add(id(step))

  result = {}
  for node in presentation.nodes:
    step_id = id(node.proof_step)
    if step_id in visible:
      result[step_id] = "VISIBLE"
    elif step_id in hidden:
      result[step_id] = "HIDDEN"
    else:
      result[step_id] = "OUTSIDE"
  return result


def main():
  print("=" * 96)
  print("Phase 144-6-R5-15P generic EvidenceContribution vocabulary audit")
  print("=" * 96)

  visible = Counter()
  all_contributions = Counter()

  for n, k in TARGETS:
    presentation, semantic_sidecar, blocks, arguments, contributions = _context(n, k)
    visibility = _visibility(
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
    )
    target_visible = Counter()

    for semantic in contributions.edge_semantics:
      contribution = semantic.contribution.value
      all_contributions[contribution] += 1
      if visibility[id(semantic.edge.premise_step)] == "VISIBLE":
        visible[contribution] += 1
        target_visible[contribution] += 1

    total = sum(target_visible.values())
    unresolved = target_visible[
      TodaGroupProofNarrativeEvidenceContribution.UNRESOLVED.value
    ]
    print(
      f"target=({n}, {k}) visible={total} "
      f"visible_unresolved={unresolved} "
      f"visible_resolution_ratio={(total - unresolved) / total:.6f}"
    )

  print()
  print("VISIBLE CONTRIBUTIONS")
  print("-" * 96)
  for contribution, count in visible.most_common():
    print(f"{contribution:<32} {count:6d}")

  total = sum(visible.values())
  unresolved = visible[
    TodaGroupProofNarrativeEvidenceContribution.UNRESOLVED.value
  ]
  resolved = total - unresolved
  print()
  print(f"visible_edges={total}")
  print(f"visible_resolved_edges={resolved}")
  print(f"visible_unresolved_edges={unresolved}")
  print(f"visible_resolution_ratio={resolved / total:.6f}")

  print()
  print("ALL CONTRIBUTIONS")
  print("-" * 96)
  for contribution, count in all_contributions.most_common():
    print(f"{contribution:<32} {count:6d}")


if __name__ == "__main__":
  main()
