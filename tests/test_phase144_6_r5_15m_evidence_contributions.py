from toda_calculation_facade import (
  build_standard_toda_report,
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


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


def _presentation_and_blocks(
  n,
  k,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )

  provenance = (
    extract_toda_recursive_proof_provenance(
      group_result
    )
  )

  max_depth = max(
    node.shortest_depth
    for node in provenance.nodes
  )

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=max_depth,
    )
  )

  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=semantic_sidecar,
    )
  )

  return (
    presentation,
    blocks,
  )


def test_phase144_6_r5_15m_covers_every_presentation_edge_once():
  for n, k in TARGETS:
    presentation, blocks = (
      _presentation_and_blocks(
        n,
        k,
      )
    )

    sidecar = (
      build_toda_group_proof_narrative_evidence_contribution_sidecar(
        presentation,
        blocks,
      )
    )

    assert (
      sidecar.presentation
      is presentation
    )

    assert len(
      sidecar.edge_semantics
    ) == len(
      presentation.edges
    )

    assert len(
      {
        (
          id(
            semantic.edge.parent_step
          ),
          id(
            semantic.edge.premise_step
          ),
          semantic.edge.premise_index,
        )
        for semantic in sidecar.edge_semantics
      }
    ) == len(
      presentation.edges
    )


def test_phase144_6_r5_15m_uses_typed_contributions():
  for n, k in TARGETS:
    presentation, blocks = (
      _presentation_and_blocks(
        n,
        k,
      )
    )

    sidecar = (
      build_toda_group_proof_narrative_evidence_contribution_sidecar(
        presentation,
        blocks,
      )
    )

    assert sidecar.edge_semantics

    assert all(
      isinstance(
        semantic.contribution,
        TodaGroupProofNarrativeEvidenceContribution,
      )
      for semantic in sidecar.edge_semantics
    )


def test_phase144_6_r5_15m_resolves_multiple_generic_contribution_kinds():
  contributions = set()

  for n, k in TARGETS:
    presentation, blocks = (
      _presentation_and_blocks(
        n,
        k,
      )
    )

    sidecar = (
      build_toda_group_proof_narrative_evidence_contribution_sidecar(
        presentation,
        blocks,
      )
    )

    contributions.update(
      semantic.contribution
      for semantic in sidecar.edge_semantics
    )

  assert {
    TodaGroupProofNarrativeEvidenceContribution.ESTABLISH_GROUP,
    TodaGroupProofNarrativeEvidenceContribution.ESTABLISH_MAP,
    TodaGroupProofNarrativeEvidenceContribution.ESTABLISH_ZERO,
    TodaGroupProofNarrativeEvidenceContribution.ESTABLISH_ORDER,
    TodaGroupProofNarrativeEvidenceContribution.ESTABLISH_RELATION,
    TodaGroupProofNarrativeEvidenceContribution.PROVIDE_REFERENCE,
    TodaGroupProofNarrativeEvidenceContribution.PROVIDE_PRECONDITION,
    TodaGroupProofNarrativeEvidenceContribution.UNRESOLVED,
  }.issubset(
    contributions
  )


def test_phase144_6_r5_15m_does_not_change_existing_semantic_sidecar_contract():
  presentation, blocks = (
    _presentation_and_blocks(
      3,
      3,
    )
  )

  existing_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  before = tuple(
    (
      id(
        semantic.edge.parent_step
      ),
      id(
        semantic.edge.premise_step
      ),
      semantic.edge.premise_index,
      semantic.role,
    )
    for semantic in existing_sidecar.premise_semantics
  )

  build_toda_group_proof_narrative_evidence_contribution_sidecar(
    presentation,
    blocks,
  )

  after = tuple(
    (
      id(
        semantic.edge.parent_step
      ),
      id(
        semantic.edge.premise_step
      ),
      semantic.edge.premise_index,
      semantic.role,
    )
    for semantic in existing_sidecar.premise_semantics
  )

  assert after == before


def test_phase144_6_r5_15m_keeps_unresolved_edges_explicit():
  unresolved_count = 0

  for n, k in TARGETS:
    presentation, blocks = (
      _presentation_and_blocks(
        n,
        k,
      )
    )

    sidecar = (
      build_toda_group_proof_narrative_evidence_contribution_sidecar(
        presentation,
        blocks,
      )
    )

    unresolved_count += sum(
      semantic.contribution
      is TodaGroupProofNarrativeEvidenceContribution.UNRESOLVED
      for semantic in sidecar.edge_semantics
    )

  assert unresolved_count > 0
