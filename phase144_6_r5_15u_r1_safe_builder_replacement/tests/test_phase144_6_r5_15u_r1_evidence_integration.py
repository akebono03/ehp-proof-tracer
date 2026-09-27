from collections import defaultdict

import pytest

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
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_proof_dependency import (
  extract_toda_recursive_proof_provenance,
)
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


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
  aggregate_semantic_sidecar = (
    build_toda_group_proof_narrative_aggregate_semantic_sidecar(
      presentation
    )
  )
  contributions = (
    build_toda_group_proof_narrative_evidence_contribution_sidecar(
      presentation,
      blocks,
      aggregate_semantic_sidecar=aggregate_semantic_sidecar,
    )
  )
  return presentation, semantic_sidecar, blocks, arguments, contributions


def _edge_local_visible_unresolved_count(
  presentation,
  semantic_sidecar,
  blocks,
  arguments,
  contributions,
):
  visible_arguments_by_step_id = defaultdict(set)
  conclusion_arguments_by_step_id = defaultdict(set)

  for argument_index, argument in enumerate(arguments):
    for step in argument.conclusion_block.steps:
      conclusion_arguments_by_step_id[id(step)].add(argument_index)

    local_body = extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      argument_index,
    )
    hidden_step_ids = set(
      _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
        presentation,
        blocks,
        local_body,
        semantic_sidecar,
        argument,
      )
    )

    if argument.role is not TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION:
      hidden_step_ids.update(
        id(step)
        for block in local_body
        for step in block.steps
        if isinstance(step.conclusion, TodaEtaFamilyDefinitionStatement)
      )

    for block in local_body:
      for step in block.steps:
        if id(step) not in hidden_step_ids:
          visible_arguments_by_step_id[id(step)].add(argument_index)

  count = 0

  for semantic in contributions.edge_semantics:
    if (
      semantic.contribution
      is not TodaGroupProofNarrativeEvidenceContribution.UNRESOLVED
    ):
      continue

    premise_id = id(semantic.edge.premise_step)
    parent_id = id(semantic.edge.parent_step)

    if (
      visible_arguments_by_step_id[premise_id]
      & conclusion_arguments_by_step_id[parent_id]
    ):
      count += 1

  return count


def test_phase144_6_r5_15u_r1_resolves_all_edge_local_visible_contributions():
  unresolved = 0

  for n, k in TARGETS:
    unresolved += _edge_local_visible_unresolved_count(
      *_context(n, k)
    )

  assert unresolved == 0


def test_phase144_6_r5_15u_r1_preserves_old_mapper_without_aggregate_sidecar():
  presentation, semantic_sidecar, blocks, arguments, contributions = _context(
    5,
    3,
  )

  legacy_call = build_toda_group_proof_narrative_evidence_contribution_sidecar(
    presentation,
    blocks,
  )

  assert legacy_call.presentation is presentation
  assert legacy_call.edge_semantics


def test_phase144_6_r5_15u_r1_rejects_foreign_aggregate_sidecar():
  presentation, semantic_sidecar, blocks, arguments, contributions = _context(
    5,
    3,
  )
  foreign_presentation = _context(5, 7)[0]
  foreign_sidecar = (
    build_toda_group_proof_narrative_aggregate_semantic_sidecar(
      foreign_presentation
    )
  )

  with pytest.raises(
    ValueError,
    match="must belong to presentation",
  ):
    build_toda_group_proof_narrative_evidence_contribution_sidecar(
      presentation,
      blocks,
      aggregate_semantic_sidecar=foreign_sidecar,
    )
