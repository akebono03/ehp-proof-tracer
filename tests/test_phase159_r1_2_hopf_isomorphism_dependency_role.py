from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_proof_dependency import (
  TodaProofDependencyRole,
  classify_toda_proof_step_role,
)
from toda_rules import (
  TodaHopfInvariantIsomorphismStatement,
)


def _phase159_r1_2_hopf_isomorphism_step():
  report = build_standard_toda_report(
    n=2,
    k=1,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  return next(
    node.proof_step
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaHopfInvariantIsomorphismStatement,
    )
  )


def test_phase159_r1_2_hopf_isomorphism_is_dependency_map_property():
  proof_step = (
    _phase159_r1_2_hopf_isomorphism_step()
  )

  assert (
    classify_toda_proof_step_role(
      proof_step
    )
    is TodaProofDependencyRole.MAP_PROPERTY
  )
