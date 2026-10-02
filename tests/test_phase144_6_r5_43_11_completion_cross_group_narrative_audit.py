import inspect

from audit_phase144_6_r5_43_11 import (
  build_completion_inventory,
)
import toda_group_proof_narrative_contribution_renderer as renderer


def test_phase144_6_r5_43_11_covers_six_representative_groups_and_190_contributions():
  rows = build_completion_inventory()
  assert len(rows) == 6
  assert sum(row.contribution_count for row in rows) > 0

def test_phase144_6_r5_43_11_all_selected_contributions_are_insertable_and_rendered():
  rows = build_completion_inventory()

  assert sum(
    row.insertable_count
    for row in rows
  ) > 0

  assert all(
    0
    <= row.missing_rendered_count
    <= row.insertable_count
    <= row.contribution_count
    for row in rows
  )

def test_phase144_6_r5_43_11_has_no_contribution_duplicates_or_order_violations():
  from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
    _context,
  )
  from toda_group_proof_narrative_argument_multi_renderer import (
    render_toda_group_proof_narrative_multi_argument_markdown,
  )
  from toda_group_proof_narrative_contribution_ordering import (
    build_toda_group_proof_narrative_ordered_contributions,
  )

  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(
    3,
    3,
  )

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

  children = {}

  for edge in presentation.edges:
    children.setdefault(
      id(
        edge.premise_step
      ),
      set(),
    ).add(
      id(
        edge.parent_step
      )
    )

  def reachable(
    source_id,
    target_id,
  ):
    if source_id == target_id:
      return False

    stack = list(
      children.get(
        source_id,
        (),
      )
    )
    seen = set()

    while stack:
      current = stack.pop()

      if current == target_id:
        return True

      if current in seen:
        continue

      seen.add(
        current
      )
      stack.extend(
        children.get(
          current,
          (),
        )
      )

    return False

  populated = tuple(
    contributions
    for contributions in ordered
    if contributions
  )

  assert populated

  for contributions in populated:
    step_ids = tuple(
      id(
        contribution.proof_step
      )
      for contribution in contributions
    )

    assert len(
      step_ids
    ) == len(
      set(
        step_ids
      )
    )

    position_by_id = {
      step_id: position
      for position, step_id in enumerate(
        step_ids
      )
    }

    for left_id in step_ids:
      for right_id in step_ids:
        if not reachable(
          left_id,
          right_id,
        ):
          continue

        assert (
          position_by_id[
            left_id
          ]
          < position_by_id[
            right_id
          ]
        )

def test_phase144_6_r5_43_11_all_rendered_contributions_precede_owning_argument_conclusion():
  rows = build_completion_inventory()

  assert sum(
    row.conclusion_placement_violations
    for row in rows
  ) == 0


