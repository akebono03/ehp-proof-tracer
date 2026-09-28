from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  _context,
)
from toda_group_proof_narrative_argument_discourse import (
  TodaGroupProofNarrativeArgumentDiscourseRole,
  classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  _contribution_insertion_indices,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


def _inventory():
  rows = []

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      aggregate_semantic_sidecar,
      proof_chains,
    ) = _context(
      n,
      k,
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
    indices = _contribution_insertion_indices(
      base,
      blocks,
      arguments,
      ordered,
    )
    ordered_arguments = order_toda_group_proof_narrative_arguments(
      arguments
    )
    discourse_roles = classify_toda_group_proof_narrative_argument_discourse_roles(
      arguments
    )
    discourse_by_id = {
      id(
        argument
      ): discourse_roles[
        position
      ]
      for position, argument in enumerate(
        ordered_arguments
      )
    }

    for argument_index, contributions in enumerate(
      ordered
    ):
      if not contributions:
        continue

      rows.append(
        (
          discourse_by_id[
            id(
              arguments[
                argument_index
              ]
            )
          ],
          len(
            contributions
          ),
          sum(
            index is not None
            for index in indices[
              argument_index
            ]
          ),
        )
      )

  return tuple(
    rows
  )


def test_phase144_6_r5_43_11c_connects_all_non_detached_selected_contributions():
  rows = _inventory()
  non_detached = tuple(
    row
    for row in rows
    if row[
      0
    ] is not TodaGroupProofNarrativeArgumentDiscourseRole.DETACHED
  )

  assert sum(
    row[
      1
    ]
    for row in non_detached
  ) == 33
  assert sum(
    row[
      2
    ]
    for row in non_detached
  ) == 33


def test_phase144_6_r5_43_11c_keeps_detached_contributions_uninserted():
  rows = _inventory()
  detached = tuple(
    row
    for row in rows
    if row[
      0
    ] is TodaGroupProofNarrativeArgumentDiscourseRole.DETACHED
  )

  assert sum(
    row[
      1
    ]
    for row in detached
  ) == 157
  assert sum(
    row[
      2
    ]
    for row in detached
  ) == 0


def test_phase144_6_r5_43_11c_definition_groups_gain_connected_output_without_public_route_change():
  for n, k in (
    (8, 7),
    (9, 7),
  ):
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      aggregate_semantic_sidecar,
      proof_chains,
    ) = _context(
      n,
      k,
    )
    base = render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
    connected = render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )

    assert connected != base
    assert len(
      connected
    ) > len(
      base
    )


def test_phase144_6_r5_43_11c_has_no_target_specific_branch():
  import inspect
  import toda_group_proof_narrative_contribution_renderer as module

  source = inspect.getsource(
    module
  )

  assert "n == 3" not in source
  assert "k == 3" not in source
  assert "n == 8" not in source
  assert "n == 9" not in source
  assert "sigma" not in source.lower()
  assert "_pi6" not in source.lower()
