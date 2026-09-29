from toda_calculation_facade import build_standard_toda_report
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


TARGETS = ((3, 3), (5, 3), (4, 6), (5, 7), (8, 7), (9, 7))

ROLE_TO_CONTRIBUTION = {
  TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS:
  TodaGroupProofNarrativeEvidenceContribution.ESTABLISH_EXACTNESS,
  TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION:
  TodaGroupProofNarrativeEvidenceContribution.ESTABLISH_DEFINITION,
  TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP:
  TodaGroupProofNarrativeEvidenceContribution.ESTABLISH_MEMBERSHIP,
}


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
  contribution_sidecar = (
    build_toda_group_proof_narrative_evidence_contribution_sidecar(
      presentation,
      blocks,
    )
  )
  return presentation, blocks, contribution_sidecar


def _role_by_step_id(blocks):
  return {
    id(step): block.role
    for block in blocks
    for step in block.steps
  }


def test_phase144_6_r5_15p_maps_generic_roles_to_typed_contributions():
  observed = {
    role: 0
    for role in ROLE_TO_CONTRIBUTION
  }

  for n, k in TARGETS:
    presentation, blocks, sidecar = _context(n, k)
    role_by_step_id = _role_by_step_id(blocks)

    assert len(sidecar.edge_semantics) == len(presentation.edges)

    for semantic in sidecar.edge_semantics:
      role = role_by_step_id[id(semantic.edge.premise_step)]
      if role not in ROLE_TO_CONTRIBUTION:
        continue
      assert semantic.contribution is ROLE_TO_CONTRIBUTION[role]
      observed[role] += 1

  assert all(count > 0 for count in observed.values())


def test_phase144_6_r5_15p_keeps_new_contributions_typed():
  expected = {
    TodaGroupProofNarrativeEvidenceContribution.ESTABLISH_EXACTNESS,
    TodaGroupProofNarrativeEvidenceContribution.ESTABLISH_DEFINITION,
    TodaGroupProofNarrativeEvidenceContribution.ESTABLISH_MEMBERSHIP,
  }
  observed = set()

  for n, k in TARGETS:
    _presentation, _blocks, sidecar = _context(n, k)
    for semantic in sidecar.edge_semantics:
      if semantic.contribution in expected:
        observed.add(semantic.contribution)

  assert observed == expected
