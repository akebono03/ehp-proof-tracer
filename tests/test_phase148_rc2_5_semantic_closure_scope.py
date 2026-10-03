from proof import (
  Relation,
  RelationType,
)
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
  build_toda_group_result_proof_replay,
)


EQ1 = r"2\nu' = \eta_{3}\eta_{4}\eta_{5}"
EQ2 = (
  r"\eta_{3}\eta_{4}\eta_{5} = "
  r"\eta_{3}^{3}"
)
UNRELATED_GROUP = (
  r"\pi_{4}^{2} = "
  r"\mathbb{Z}/2\{\eta_{2}\eta_{3}\}"
)
UNRELATED_HOPF_1 = (
  r"H\left(\nu'\right) = E^{2}\eta_{3}"
)
UNRELATED_HOPF_2 = (
  r"E^{2}\eta_{3} = \eta_{5}"
)


def _presentation(
  n,
  k,
  depth,
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
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=depth,
    )
  )
  return build_toda_group_proof_presentation(
    replay
  )


def test_phase148_rc2_5_depth_zero_semantic_closure_is_identity():
  presentation = _presentation(
    9,
    7,
    0,
  )
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  assert closure is presentation
  assert closure.max_depth == 0
  assert len(
    closure.nodes
  ) == 1


def test_phase148_rc2_5_order_calculation_closure_adds_only_required_chain_and_definition():
  presentation = _presentation(
    3,
    3,
    2,
  )
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )
  original_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }
  added_nodes = tuple(
    node
    for node in closure.nodes
    if id(
      node.proof_step
    ) not in original_ids
  )
  rendered = tuple(
    _render_generic_narrative_step(
      node.proof_step
    )
    for node in added_nodes
  )
  added_equalities = tuple(
    node
    for node in added_nodes
    if (
      isinstance(
        node.proof_step.conclusion,
        Relation,
      )
      and node.proof_step.conclusion.relation_type
      is RelationType.EQUALITY
    )
  )

  assert len(
    added_nodes
  ) == 3
  assert len(
    added_equalities
  ) == 2
  assert any(
    EQ1 in value
    for value in rendered
  )
  assert any(
    EQ2 in value
    for value in rendered
  )
  assert all(
    UNRELATED_GROUP not in value
    for value in rendered
  )
  assert all(
    UNRELATED_HOPF_1 not in value
    for value in rendered
  )
  assert all(
    UNRELATED_HOPF_2 not in value
    for value in rendered
  )
