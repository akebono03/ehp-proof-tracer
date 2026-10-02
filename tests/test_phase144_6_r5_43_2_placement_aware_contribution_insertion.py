from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  _context,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_contribution_ordering import (
  TodaGroupProofNarrativeContributionPlacement,
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  _contribution_insertion_indices,
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
  return base, connected, blocks, arguments, ordered


def test_phase144_6_r5_43_2_pi6_uses_provider_anchor_indices():
  base, connected, blocks, arguments, ordered = _pi6_data()
  populated_index, rows = next(
    (index, rows)
    for index, rows in enumerate(ordered)
    if rows
  )
  indices = _contribution_insertion_indices(
    base,
    blocks,
    arguments,
    ordered,
  )[populated_index]

  assert len(rows) == 5
  assert all(
    row.placement
    is TodaGroupProofNarrativeContributionPlacement.AT_PROVIDER_ANCHOR
    for row in rows
  )
  assert all(index is not None for index in indices)


def test_phase144_6_r5_43_2_pi6_contributions_are_not_dumped_after_final_connector():
  base, connected, blocks, arguments, ordered = _pi6_data()
  rows = next(rows for rows in ordered if rows)
  contribution_lines = tuple(
    _render_generic_narrative_step(row.proof_step)
    for row in rows
  )
  conclusion_argument_index = next(
    index
    for index, rows in enumerate(ordered)
    if rows
  )
  conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
    arguments[conclusion_argument_index]
  )
  conclusion_line = _render_generic_narrative_step(conclusion_step)
  conclusion_index = connected.index(conclusion_line)
  final_connector_index = connected.rfind(
    "以上より、",
    0,
    conclusion_index,
  )

  assert final_connector_index >= 0
  assert all(
    connected.index(line) < final_connector_index
    for line in contribution_lines
  )


def test_phase144_6_r5_43_2_pi6_contributions_remain_unique_and_topologically_ordered():
  base, connected, blocks, arguments, ordered = _pi6_data()
  rows = next(rows for rows in ordered if rows)
  lines = tuple(
    _render_generic_narrative_step(row.proof_step)
    for row in rows
  )
  positions = tuple(
    connected.index(line)
    for line in lines
  )

  assert positions == tuple(sorted(positions))
  assert all(connected.count(line) == 1 for line in lines)


def test_phase144_6_r5_43_2_base_renderer_remains_unchanged():
  base, connected, blocks, arguments, ordered = _pi6_data()
  (
    presentation,
    semantic_sidecar,
    fresh_blocks,
    fresh_arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)
  fresh_base = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    fresh_blocks,
    semantic_sidecar,
    fresh_arguments,
  )

  assert base == fresh_base
  assert connected != base


