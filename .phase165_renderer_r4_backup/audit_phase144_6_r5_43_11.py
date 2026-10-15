from dataclasses import dataclass

from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
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
  _contribution_connector_lines,
  _contribution_insertion_indices,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)


_TRANSPORT_CONNECTOR = (
  "Proposition 5.3 を順次適用し、"
  "suspension による安定化を用いると、"
)


@dataclass(frozen=True)
class CompletionAuditRow:
  n: int
  k: int
  argument_count: int
  contribution_count: int
  populated_argument_count: int
  insertable_count: int
  transport_connector_count: int
  direct_connector_count: int
  missing_rendered_count: int
  duplicate_violations: int
  order_violations: int
  conclusion_placement_violations: int
  connected_chars: int


def _group_label(
  n: int,
  k: int,
) -> str:
  return f"pi_{n + k}^{n}"


def _build_row(
  n: int,
  k: int,
) -> CompletionAuditRow:
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

  insertable_count = 0
  missing_rendered_count = 0
  duplicate_violations = 0
  order_violations = 0
  conclusion_placement_violations = 0

  for argument_index, contributions in enumerate(
    ordered
  ):
    if not contributions:
      continue

    visible_positions = []

    for contribution_index, contribution in enumerate(
      contributions
    ):
      line = _render_generic_narrative_step(
        contribution.proof_step
      )
      insertion_index = insertion_indices[
        argument_index
      ][
        contribution_index
      ]

      if not line or insertion_index is None:
        continue

      insertable_count += 1
      count = connected.count(
        line
      )

      if count == 0:
        missing_rendered_count += 1
        continue

      if count != 1:
        duplicate_violations += 1
        continue

      visible_positions.append(
        connected.index(
          line
        )
      )

    if visible_positions != sorted(
      visible_positions
    ):
      order_violations += 1

    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        arguments[
          argument_index
        ]
      )
    )

    if conclusion_step is None:
      continue

    conclusion_line = (
      _render_generic_narrative_step(
        conclusion_step
      )
    )

    if not conclusion_line:
      continue

    conclusion_index = connected.find(
      conclusion_line
    )

    if conclusion_index < 0:
      continue

    conclusion_placement_violations += sum(
      1
      for position in visible_positions
      if position > conclusion_index
    )

  return CompletionAuditRow(
    n=n,
    k=k,
    argument_count=len(
      arguments
    ),
    contribution_count=sum(
      len(
        contributions
      )
      for contributions in ordered
    ),
    populated_argument_count=sum(
      1
      for contributions in ordered
      if contributions
    ),
    insertable_count=insertable_count,
    transport_connector_count=sum(
      1
      for connector in connectors.values()
      if connector == _TRANSPORT_CONNECTOR
    ),
    direct_connector_count=sum(
      1
      for connector in connectors.values()
      if connector == "これより、"
    ),
    missing_rendered_count=missing_rendered_count,
    duplicate_violations=duplicate_violations,
    order_violations=order_violations,
    conclusion_placement_violations=(
      conclusion_placement_violations
    ),
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


def print_completion_audit():
  rows = build_completion_inventory()

  print("=" * 78)
  print(
    "Phase 144-6-R5-43-11-R2 visibility-aware completion cross-group Narrative audit"
  )
  print("production changes: none")
  print("=" * 78)
  print()
  print("A. Six-group connected Narrative summary")
  print("-" * 78)

  for row in rows:
    print(
      f"{_group_label(row.n, row.k)}: "
      f"arguments={row.argument_count} "
      f"populated={row.populated_argument_count} "
      f"selected={row.contribution_count} "
      f"insertable={row.insertable_count} "
      f"transport={row.transport_connector_count} "
      f"direct={row.direct_connector_count} "
      f"missing={row.missing_rendered_count} "
      f"duplicates={row.duplicate_violations} "
      f"order={row.order_violations} "
      f"after_conclusion={row.conclusion_placement_violations} "
      f"chars={row.connected_chars}"
    )

  selected = sum(
    row.contribution_count
    for row in rows
  )
  insertable = sum(
    row.insertable_count
    for row in rows
  )
  transport = sum(
    row.transport_connector_count
    for row in rows
  )
  direct = sum(
    row.direct_connector_count
    for row in rows
  )
  missing = sum(
    row.missing_rendered_count
    for row in rows
  )
  duplicates = sum(
    row.duplicate_violations
    for row in rows
  )
  order = sum(
    row.order_violations
    for row in rows
  )
  after_conclusion = sum(
    row.conclusion_placement_violations
    for row in rows
  )

  print()
  print("B. Aggregate completion invariants")
  print("-" * 78)
  print(f"groups={len(rows)}")
  print(f"selected contributions={selected}")
  print(f"insertable contributions={insertable}")
  print(f"transport connectors={transport}")
  print(f"direct connectors={direct}")
  print(f"missing rendered contributions={missing}")
  print(f"duplicate violations={duplicates}")
  print(f"order violations={order}")
  print(
    "conclusion-placement violations="
    + str(
      after_conclusion
    )
  )

  complete = (
    len(
      rows
    ) == 6
    and selected == 190
    and insertable == 190
    and transport == 16
    and missing == 0
    and duplicates == 0
    and order == 0
    and after_conclusion == 0
  )

  print()
  print("C. R5-43 completion decision")
  print("-" * 78)
  print(
    "R5-43 completion invariants: "
    + (
      "PASS"
      if complete
      else "FAIL"
    )
  )
  print("Public CLI/Web renderer route: unchanged")
  print("Full-suite status: not run in R5-43-11")


if __name__ == "__main__":
  print_completion_audit()
