from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
  build_toda_group_result_proof_replay,
)


EQUATION_FRAGMENTS = (
  r"2\nu' = \eta_{3}E\eta_{3}\eta_{5}",
  (
    r"\eta_{3}E\eta_{3}\eta_{5} = "
    r"\eta_{3}^{3}"
  ),
  r"2\nu' = \eta_{3}^{3}",
)


def _group_result():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  return (
    report.candidates[
      0
    ].source_candidate.group_result
  )


def _presentation(
  max_depth,
):
  group_result = (
    _group_result()
  )

  if max_depth is None:
    replay = (
      build_complete_toda_group_result_proof_replay(
        group_result
      )
    )
  else:
    replay = (
      build_toda_group_result_proof_replay(
        group_result,
        max_depth=max_depth,
      )
    )

  return (
    build_toda_group_proof_presentation(
      replay
    )
  )


def _contains_equation(
  presentation,
  fragment,
):
  return any(
    fragment
    in _render_generic_narrative_step(
      node.proof_step
    )
    for node in presentation.nodes
  )


def test_phase148_rc2_4_repair_r4_1_audit_complete_replay_contains_numbered_equation_sources():
  presentation = (
    _presentation(
      None
    )
  )

  for fragment in EQUATION_FRAGMENTS:
    assert _contains_equation(
      presentation,
      fragment,
    )


def test_phase148_rc2_4_repair_r4_1_audit_records_depth2_semantic_closure_state():
  presentation = (
    _presentation(
      2
    )
  )
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  assert len(
    closure.nodes
  ) >= len(
    presentation.nodes
  )

  for node in presentation.nodes:
    assert any(
      closure_node.proof_step
      is node.proof_step
      for closure_node in closure.nodes
    )


def test_phase148_rc2_4_repair_r4_1_audit_depth3_is_strictly_richer_than_depth2():
  depth2 = (
    _presentation(
      2
    )
  )
  depth3 = (
    _presentation(
      3
    )
  )

  assert len(
    depth3.nodes
  ) > len(
    depth2.nodes
  )
