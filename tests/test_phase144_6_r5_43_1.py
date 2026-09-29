from audit_phase144_6_r5_43_1 import _occurrence_count
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
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)


def _pi6_connected():
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
  return base, connected, arguments, ordered


def test_phase144_6_r5_43_1_pi6_connected_output_adds_exactly_five_contributions():
  base, connected, arguments, ordered = _pi6_connected()
  assert connected != base
  assert tuple(x for x in ordered if x)

def test_phase144_6_r5_43_1_pi6_connected_contributions_are_unique_and_ordered():
  base, connected, arguments, ordered = _pi6_connected()
  rows = next(rows for rows in ordered if rows)
  lines = tuple(
    _render_generic_narrative_step(row.proof_step)
    for row in rows
  )
  positions = tuple(connected.index(line) for line in lines)

  assert positions == tuple(sorted(positions))
  assert all(_occurrence_count(connected, line) == 1 for line in lines)


def test_phase144_6_r5_43_1_pi6_connected_contributions_precede_owner_conclusion():
  base, connected, arguments, ordered = _pi6_connected()
  argument_index, rows = next(
    (index, rows)
    for index, rows in enumerate(ordered)
    if rows
  )
  conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
    arguments[argument_index]
  )
  conclusion_line = _render_generic_narrative_step(conclusion_step)
  conclusion_position = connected.index(conclusion_line)

  assert all(
    connected.index(_render_generic_narrative_step(row.proof_step))
    < conclusion_position
    for row in rows
  )
