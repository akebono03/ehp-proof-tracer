import pytest

from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  _context,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  _contribution_connector_lines,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)


def _pi6_data():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)
  base = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )
  ordered = build_toda_group_proof_narrative_ordered_contributions(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
    current_markdown=base,
  )
  connected = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  contributions = next(
    rows
    for rows in ordered
    if rows
  )
  return (
    presentation,
    base,
    connected,
    ordered,
    contributions,
  )


@pytest.fixture(
  scope="module",
)
def pi6_data():
  return _pi6_data()


def test_phase144_6_r5_43_4_only_direct_contribution_dependency_gets_direct_connector(
  pi6_data,
):
  (
    presentation,
    base,
    connected,
    ordered,
    contributions,
  ) = pi6_data
  connector_by_target_step_id = (
    _contribution_connector_lines(
      presentation,
      ordered,
    )
  )
  direct_connector_targets = {
    step_id
    for step_id, connector
    in connector_by_target_step_id.items()
    if connector == "これより、"
  }

  assert direct_connector_targets == {
    id(
      contributions[4].proof_step
    ),
  }


def test_phase144_6_r5_43_4_c4_to_c5_has_connector(
  pi6_data,
):
  (
    presentation,
    base,
    connected,
    ordered,
    contributions,
  ) = pi6_data
  c4 = _render_generic_narrative_step(
    contributions[3].proof_step
  )
  c5 = _render_generic_narrative_step(
    contributions[4].proof_step
  )
  expected = (
    c4
    + "\n\nこれより、\n\n"
    + c5
  )

  assert expected in connected


def test_phase144_6_r5_43_4_transitive_c1_c2_c3_do_not_get_false_direct_connectors(
  pi6_data,
):
  (
    presentation,
    base,
    connected,
    ordered,
    contributions,
  ) = pi6_data
  c1 = _render_generic_narrative_step(
    contributions[0].proof_step
  )
  c2 = _render_generic_narrative_step(
    contributions[1].proof_step
  )
  c3 = _render_generic_narrative_step(
    contributions[2].proof_step
  )

  assert (
    c1
    + "\n\nこれより、\n\n"
    + c2
  ) not in connected
  assert (
    c2
    + "\n\nこれより、\n\n"
    + c3
  ) not in connected


def test_phase144_6_r5_43_4_no_connector_is_inferred_from_visual_adjacency_after_c5(
  pi6_data,
):
  (
    presentation,
    base,
    connected,
    ordered,
    contributions,
  ) = pi6_data
  c5 = _render_generic_narrative_step(
    contributions[4].proof_step
  )
  h_surjective = (
    "$H: \\pi_{6}^{3} \\to \\pi_{6}^{5}$ "
    "は全射である."
  )

  assert (
    c5
    + "\n\nこれより、\n\n"
    + h_surjective
  ) not in connected


def test_phase144_6_r5_43_4_preserves_r5_43_2_placement_and_uniqueness(
  pi6_data,
):
  (
    presentation,
    base,
    connected,
    ordered,
    contributions,
  ) = pi6_data
  lines = tuple(
    _render_generic_narrative_step(
      contribution.proof_step
    )
    for contribution in contributions
  )
  positions = tuple(
    connected.index(
      line
    )
    for line in lines
  )
  conclusion = (
    "$\\pi_{6}^{3} = "
    "\\mathbb{Z}/4\\{\\nu'\\}$"
  )
  final_connector_index = connected.rfind(
    "以上より、",
    0,
    connected.index(
      conclusion
    ),
  )

  assert positions == tuple(
    sorted(
      positions
    )
  )
  assert all(
    connected.count(
      line
    ) == 1
    for line in lines
  )
  assert all(
    position < final_connector_index
    for position in positions
  )


def test_phase144_6_r5_43_4_has_no_pi6_specific_branch():
  import inspect
  import toda_group_proof_narrative_contribution_renderer as module

  source = inspect.getsource(
    module
  )

  assert "n == 3" not in source
  assert "k == 3" not in source
  assert "_pi6" not in source.lower()
