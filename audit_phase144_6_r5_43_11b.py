from collections import Counter

from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
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
)


def build_boundary_inventory():
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
    insertion_indices = _contribution_insertion_indices(
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
    discourse_by_argument_id = {
      id(
        argument
      ): discourse_roles[
        ordered_position
      ]
      for ordered_position, argument in enumerate(
        ordered_arguments
      )
    }

    for argument_index, contributions in enumerate(
      ordered
    ):
      if not contributions:
        continue

      indices = insertion_indices[
        argument_index
      ]
      insertable = sum(
        index is not None
        for index in indices
      )
      role = discourse_by_argument_id[
        id(
          arguments[
            argument_index
          ]
        )
      ]

      rows.append(
        (
          n,
          k,
          argument_index,
          arguments[
            argument_index
          ].role.value,
          role.value,
          len(
            contributions
          ),
          insertable,
        )
      )

  return tuple(
    rows
  )


def print_boundary_inventory():
  rows = build_boundary_inventory()

  print("=" * 78)
  print(
    "Phase 144-6-R5-43-11B detached-Argument boundary audit"
  )
  print("production changes: none")
  print("=" * 78)
  print()
  print("A. Populated Argument boundary")
  print("-" * 78)

  for (
    n,
    k,
    argument_index,
    argument_role,
    discourse_role,
    selected,
    insertable,
  ) in rows:
    print(
      f"pi_{n + k}^{n} "
      f"arg={argument_index} "
      f"argument_role={argument_role} "
      f"discourse={discourse_role} "
      f"selected={selected} "
      f"insertable={insertable}"
    )

  print()
  print("B. Aggregate by discourse role")
  print("-" * 78)

  argument_counts = Counter(
    discourse_role
    for (
      n,
      k,
      argument_index,
      argument_role,
      discourse_role,
      selected,
      insertable,
    ) in rows
  )
  selected_counts = Counter()
  insertable_counts = Counter()

  for (
    n,
    k,
    argument_index,
    argument_role,
    discourse_role,
    selected,
    insertable,
  ) in rows:
    selected_counts[
      discourse_role
    ] += selected
    insertable_counts[
      discourse_role
    ] += insertable

  for discourse_role in sorted(
    argument_counts
  ):
    print(
      f"{discourse_role}: "
      f"arguments={argument_counts[discourse_role]} "
      f"selected={selected_counts[discourse_role]} "
      f"insertable={insertable_counts[discourse_role]}"
    )

  non_insertable_rows = tuple(
    row
    for row in rows
    if row[
      6
    ] < row[
      5
    ]
  )
  non_insertable_detached = all(
    row[
      4
    ]
    == TodaGroupProofNarrativeArgumentDiscourseRole
    .DETACHED.value
    for row in non_insertable_rows
  )

  print()
  print("C. Boundary decision")
  print("-" * 78)
  print(
    "all non-insertable populated Arguments are DETACHED: "
    + str(
      non_insertable_detached
    )
  )
  print(
    "non-insertable selected contributions="
    + str(
      sum(
        row[
          5
        ] - row[
          6
        ]
        for row in rows
      )
    )
  )


if __name__ == "__main__":
  print_boundary_inventory()
