from collections import Counter, defaultdict

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
  TodaGroupProofNarrativeMathematicalBlockRole,
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
  aggregate_semantics = (
    build_toda_group_proof_narrative_aggregate_semantic_sidecar(
      presentation
    )
  )
  return (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    contributions,
    aggregate_semantics,
  )


def _visible_argument_indices_by_step_id(
  presentation,
  semantic_sidecar,
  blocks,
  arguments,
):
  result = defaultdict(set)

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
        if id(step) not in hidden_ids:
          result[id(step)].add(argument_index)

  return result


def _candidate_contribution(
  aggregate_kind,
  consumer_block_role,
  argument_role,
):
  if (
    argument_role
    is TodaGroupProofNarrativeArgumentRole.ESTABLISH_GROUP_STRUCTURE
    and consumer_block_role
    is TodaGroupProofNarrativeMathematicalBlockRole.TARGET
  ):
    return "ESTABLISH_GROUP"

  if (
    argument_role
    is TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION
    and consumer_block_role
    is TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION
  ):
    return "ESTABLISH_DEFINITION"

  return None


def main():
  print("=" * 110)
  print("Phase 144-6-R5-15T aggregate semantic metadata prototype audit")
  print("=" * 110)
  print(
    "Contribution candidate classifier uses aggregate semantic kind, "
    "consumer block role, and Argument role only."
  )

  rows = []

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      contributions,
      aggregate_semantics,
    ) = _context(n, k)

    block_by_step_id = {
      id(step): block
      for block in blocks
      for step in block.steps
    }
    visible_args = _visible_argument_indices_by_step_id(
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
    )
    conclusion_args = defaultdict(set)
    for argument_index, argument in enumerate(arguments):
      for step in argument.conclusion_block.steps:
        conclusion_args[id(step)].add(argument_index)

    aggregate_kind_by_step_id = {
      id(semantic.proof_step): semantic.kind
      for semantic in aggregate_semantics.step_semantics
    }

    for semantic in contributions.edge_semantics:
      if (
        semantic.contribution
        is not TodaGroupProofNarrativeEvidenceContribution.UNRESOLVED
      ):
        continue

      premise_id = id(semantic.edge.premise_step)
      parent_id = id(semantic.edge.parent_step)
      consumer_argument_indices = conclusion_args[parent_id]
      edge_local_indices = (
        visible_args[premise_id]
        & consumer_argument_indices
      )

      if not edge_local_indices:
        continue

      aggregate_kind = aggregate_kind_by_step_id.get(premise_id)
      candidates = set()

      for argument_index in edge_local_indices:
        candidates.add(
          _candidate_contribution(
            aggregate_kind,
            block_by_step_id[parent_id].role,
            arguments[argument_index].role,
          )
        )

      candidates.discard(None)

      rows.append(
        (
          (n, k),
          aggregate_kind.value if aggregate_kind is not None else None,
          block_by_step_id[parent_id].role.value,
          tuple(
            sorted(
              arguments[index].role.value
              for index in edge_local_indices
            )
          ),
          tuple(sorted(candidates)),
        )
      )

  classified = sum(
    1
    for row in rows
    if len(row[4]) == 1
  )

  print()
  for index, row in enumerate(rows, start=1):
    print(
      f"{index:2d}. target={row[0]} "
      f"aggregate_semantic={row[1]} "
      f"consumer_role={row[2]} "
      f"argument_roles={row[3]} "
      f"candidate={row[4]}"
    )

  print()
  print(f"edge_local_visible_unresolved={len(rows)}")
  print(f"classified_by_metadata_and_consumer_purpose={classified}")
  print(f"unclassified={len(rows) - classified}")
  print(
    "classification_ratio="
    f"{classified / len(rows) if rows else 1.0:.6f}"
  )

  semantic_counts = Counter(row[1] for row in rows)
  print()
  print("SEMANTIC POPULATION")
  print("-" * 110)
  for key, count in semantic_counts.most_common():
    print(f"{str(key):<40} {count:5d}")

  if len(rows) != 9:
    raise AssertionError(
      f"expected 9 edge-local visible unresolved edges, got {len(rows)}"
    )

  if classified != 9:
    raise AssertionError(
      f"expected 9 metadata-classified edges, got {classified}"
    )

  if any(row[1] is None for row in rows):
    raise AssertionError(
      "every remaining edge must have aggregate semantic metadata"
    )

  print()
  print("PROTOTYPE RESULT: 9/9 classified without statement-class branching")
  print(
    "NOTE: statement classes are used only at the explicit metadata "
    "registration boundary, not by the contribution candidate classifier."
  )


if __name__ == "__main__":
  main()
