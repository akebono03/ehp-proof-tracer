from collections import Counter
from dataclasses import dataclass

from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
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
  _contribution_connector_lines,
  _contribution_insertion_indices,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)


_TRANSPORT_CONNECTOR = (
  "Proposition 5.3 を順次適用し、"
  "suspension による安定化を用いると、"
)


@dataclass(frozen=True)
class CompletionRow:
  n: int
  k: int
  selected: int
  participating_selected: int
  participating_insertable: int
  detached_selected: int
  detached_insertable: int
  transport_connectors: int
  direct_connectors: int
  missing_inserted_lines: int
  connected_chars: int


def _build_row(
  n: int,
  k: int,
) -> CompletionRow:
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
  connected = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  connectors = _contribution_connector_lines(
    presentation,
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

  participating_selected = 0
  participating_insertable = 0
  detached_selected = 0
  detached_insertable = 0
  missing_inserted_lines = 0

  for argument_index, contributions in enumerate(
    ordered
  ):
    if not contributions:
      continue

    discourse_role = discourse_by_id[
      id(
        arguments[
          argument_index
        ]
      )
    ]
    indices = insertion_indices[
      argument_index
    ]

    for contribution_index, contribution in enumerate(
      contributions
    ):
      insertion_index = indices[
        contribution_index
      ]

      if (
        discourse_role
        is TodaGroupProofNarrativeArgumentDiscourseRole
        .DETACHED
      ):
        detached_selected += 1
        if insertion_index is not None:
          detached_insertable += 1
        continue

      participating_selected += 1

      if insertion_index is None:
        continue

      participating_insertable += 1
      line = _render_generic_narrative_step(
        contribution.proof_step
      )

      if (
        line
        and line not in base
        and line not in connected
      ):
        missing_inserted_lines += 1

  return CompletionRow(
    n=n,
    k=k,
    selected=sum(
      len(
        contributions
      )
      for contributions in ordered
    ),
    participating_selected=participating_selected,
    participating_insertable=participating_insertable,
    detached_selected=detached_selected,
    detached_insertable=detached_insertable,
    transport_connectors=sum(
      connector == _TRANSPORT_CONNECTOR
      for connector in connectors.values()
    ),
    direct_connectors=sum(
      connector == "これより、"
      for connector in connectors.values()
    ),
    missing_inserted_lines=missing_inserted_lines,
    connected_chars=len(
      connected
    ),
  )


_CACHE = None


def build_completion_inventory():
  global _CACHE

  if _CACHE is None:
    _CACHE = tuple(
      _build_row(
        n,
        k,
      )
      for n, k in TARGETS
    )

  return _CACHE


def completion_invariants_pass(
  rows,
) -> bool:
  return (
    len(
      rows
    ) == 6
    and sum(
      row.selected
      for row in rows
    ) == 190
    and sum(
      row.participating_selected
      for row in rows
    ) == 33
    and sum(
      row.participating_insertable
      for row in rows
    ) == 33
    and sum(
      row.detached_selected
      for row in rows
    ) == 157
    and sum(
      row.detached_insertable
      for row in rows
    ) == 0
    and sum(
      row.transport_connectors
      for row in rows
    ) == 16
    and sum(
      row.missing_inserted_lines
      for row in rows
    ) == 0
  )


def print_completion_audit():
  rows = build_completion_inventory()

  print("=" * 78)
  print(
    "Phase 144-6-R5-43-11D final completion cross-group Narrative audit"
  )
  print("production changes: none")
  print("=" * 78)
  print()
  print("A. Six-group Narrative boundary")
  print("-" * 78)

  for row in rows:
    print(
      f"pi_{row.n + row.k}^{row.n}: "
      f"selected={row.selected} "
      f"participating={row.participating_selected}/"
      f"{row.participating_insertable} "
      f"detached={row.detached_selected}/"
      f"{row.detached_insertable} "
      f"transport={row.transport_connectors} "
      f"direct={row.direct_connectors} "
      f"missing={row.missing_inserted_lines} "
      f"chars={row.connected_chars}"
    )

  print()
  print("B. Aggregate completion invariants")
  print("-" * 78)
  print(
    "groups="
    + str(
      len(
        rows
      )
    )
  )
  print(
    "selected contributions="
    + str(
      sum(
        row.selected
        for row in rows
      )
    )
  )
  print(
    "Narrative-participating selected="
    + str(
      sum(
        row.participating_selected
        for row in rows
      )
    )
  )
  print(
    "Narrative-participating insertable="
    + str(
      sum(
        row.participating_insertable
        for row in rows
      )
    )
  )
  print(
    "DETACHED selected="
    + str(
      sum(
        row.detached_selected
        for row in rows
      )
    )
  )
  print(
    "DETACHED insertable="
    + str(
      sum(
        row.detached_insertable
        for row in rows
      )
    )
  )
  print(
    "transport connectors="
    + str(
      sum(
        row.transport_connectors
        for row in rows
      )
    )
  )
  print(
    "direct connectors="
    + str(
      sum(
        row.direct_connectors
        for row in rows
      )
    )
  )
  print(
    "missing inserted lines="
    + str(
      sum(
        row.missing_inserted_lines
        for row in rows
      )
    )
  )

  print()
  print("C. R5-43 completion decision")
  print("-" * 78)
  print(
    "R5-43 completion invariants: "
    + (
      "PASS"
      if completion_invariants_pass(
        rows
      )
      else "FAIL"
    )
  )
  print("Public CLI/Web renderer route: unchanged")
  print("Full-suite status: not run in R5-43-11D")


if __name__ == "__main__":
  print_completion_audit()
