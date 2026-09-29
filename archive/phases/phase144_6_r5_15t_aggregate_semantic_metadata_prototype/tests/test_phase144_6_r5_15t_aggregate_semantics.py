import pytest

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_aggregate_semantics import (
  TodaGroupProofNarrativeAggregateSemanticKind,
  TodaGroupProofNarrativeAggregateSemanticSidecar,
  TodaGroupProofNarrativeAggregateStepSemantic,
  build_toda_group_proof_narrative_aggregate_semantic_sidecar,
)
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_proof_dependency import extract_toda_recursive_proof_provenance


TARGETS = (
  (5, 3),
  (5, 7),
  (8, 7),
  (9, 7),
)


def _presentation(n, k):
  report = build_standard_toda_report(n=n, k=k)
  group_result = report.candidates[0].source_candidate.group_result
  provenance = extract_toda_recursive_proof_provenance(group_result)
  max_depth = max(node.shortest_depth for node in provenance.nodes)
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=max_depth,
  )
  return build_toda_group_proof_presentation(replay)


def test_phase144_6_r5_15t_builds_typed_aggregate_semantics():
  observed = set()

  for n, k in TARGETS:
    sidecar = (
      build_toda_group_proof_narrative_aggregate_semantic_sidecar(
        _presentation(n, k)
      )
    )
    observed.update(
      semantic.kind
      for semantic in sidecar.step_semantics
    )

  assert observed == {
    TodaGroupProofNarrativeAggregateSemanticKind
    .GROUP_ORDER_TRANSPORT,
    TodaGroupProofNarrativeAggregateSemanticKind
    .MAP_TRANSPORT,
    TodaGroupProofNarrativeAggregateSemanticKind
    .GROUP_DECOMPOSITION_TRANSPORT,
    TodaGroupProofNarrativeAggregateSemanticKind
    .RELATION_AGGREGATE,
  }


def test_phase144_6_r5_15t_sidecar_rejects_duplicate_steps():
  presentation = _presentation(5, 3)
  sidecar = (
    build_toda_group_proof_narrative_aggregate_semantic_sidecar(
      presentation
    )
  )
  semantic = sidecar.step_semantics[0]

  with pytest.raises(
    ValueError,
    match="duplicate proof steps",
  ):
    TodaGroupProofNarrativeAggregateSemanticSidecar(
      presentation=presentation,
      step_semantics=(semantic, semantic),
    )


def test_phase144_6_r5_15t_sidecar_rejects_foreign_steps():
  presentation = _presentation(5, 3)
  foreign_presentation = _presentation(5, 7)
  foreign_step = foreign_presentation.root_step
  semantic = TodaGroupProofNarrativeAggregateStepSemantic(
    proof_step=foreign_step,
    kind=(
      TodaGroupProofNarrativeAggregateSemanticKind
      .MAP_TRANSPORT
    ),
  )

  with pytest.raises(
    ValueError,
    match="must appear in presentation nodes",
  ):
    TodaGroupProofNarrativeAggregateSemanticSidecar(
      presentation=presentation,
      step_semantics=(semantic,),
    )
