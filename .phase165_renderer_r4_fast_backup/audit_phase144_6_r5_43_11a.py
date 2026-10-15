from collections import Counter
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
  TodaGroupProofNarrativeContributionPlacement,
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  _contribution_insertion_indices,
  _provider_anchor_index,
)


def _normalized(
  text: str,
) -> str:
  return "".join(
    text.split()
  )


@dataclass(frozen=True)
class FailureRow:
  n: int
  k: int
  argument_index: int
  argument_role: str
  contribution_count: int
  insertable_count: int
  failure_reason: str
  conclusion_line: str
  exact_conclusion_visible: bool
  normalized_conclusion_visible: bool
  placement_counts: tuple[
    tuple[str, int],
    ...,
  ]
  provider_anchor_resolved: int
  provider_anchor_unresolved: int


def _failure_reason(
  conclusion_step,
  conclusion_line: str,
  exact_conclusion_visible: bool,
  normalized_conclusion_visible: bool,
  contribution_count: int,
  insertable_count: int,
) -> str:
  if conclusion_step is None:
    return "no_conclusion_step"
  if not conclusion_line:
    return "empty_conclusion_rendering"
  if not exact_conclusion_visible:
    if normalized_conclusion_visible:
      return "conclusion_format_mismatch"
    return "conclusion_not_in_base_markdown"
  if insertable_count < contribution_count:
    return "placement_resolution_failure"
  return "resolved"


def build_failure_inventory():
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
    normalized_base = _normalized(
      base
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

    for argument_index, contributions in enumerate(
      ordered
    ):
      if not contributions:
        continue

      conclusion_step = (
        extract_toda_group_proof_narrative_argument_conclusion_step(
          arguments[
            argument_index
          ]
        )
      )
      conclusion_line = (
        ""
        if conclusion_step is None
        else _render_generic_narrative_step(
          conclusion_step
        )
      )
      exact_visible = bool(
        conclusion_line
      ) and conclusion_line in base
      normalized_visible = bool(
        conclusion_line
      ) and _normalized(
        conclusion_line
      ) in normalized_base

      indices = insertion_indices[
        argument_index
      ]
      insertable_count = sum(
        index is not None
        for index in indices
      )
      placement_counts = Counter(
        contribution.placement.value
        for contribution in contributions
      )

      provider_anchor_resolved = 0
      provider_anchor_unresolved = 0

      for contribution in contributions:
        if (
          contribution.placement
          is not TodaGroupProofNarrativeContributionPlacement
          .AT_PROVIDER_ANCHOR
        ):
          continue

        anchor_index = _provider_anchor_index(
          base,
          blocks,
          contribution.provider_keys,
        )

        if anchor_index is None:
          provider_anchor_unresolved += 1
        else:
          provider_anchor_resolved += 1

      rows.append(
        FailureRow(
          n=n,
          k=k,
          argument_index=argument_index,
          argument_role=arguments[
            argument_index
          ].role.value,
          contribution_count=len(
            contributions
          ),
          insertable_count=insertable_count,
          failure_reason=_failure_reason(
            conclusion_step,
            conclusion_line,
            exact_visible,
            normalized_visible,
            len(
              contributions
            ),
            insertable_count,
          ),
          conclusion_line=conclusion_line,
          exact_conclusion_visible=exact_visible,
          normalized_conclusion_visible=normalized_visible,
          placement_counts=tuple(
            sorted(
              placement_counts.items()
            )
          ),
          provider_anchor_resolved=provider_anchor_resolved,
          provider_anchor_unresolved=provider_anchor_unresolved,
        )
      )

  return tuple(
    rows
  )


def print_failure_inventory():
  rows = build_failure_inventory()
  reason_counts = Counter()
  contribution_reason_counts = Counter()

  for row in rows:
    reason_counts[
      row.failure_reason
    ] += 1
    contribution_reason_counts[
      row.failure_reason
    ] += (
      row.contribution_count
      - row.insertable_count
    )

  print("=" * 78)
  print(
    "Phase 144-6-R5-43-11A insertion-index failure classification audit"
  )
  print("production changes: none")
  print("=" * 78)
  print()
  print("A. Failure classification by populated Argument")
  print("-" * 78)

  for row in rows:
    print(
      f"pi_{row.n + row.k}^{row.n} "
      f"arg={row.argument_index} "
      f"role={row.argument_role} "
      f"selected={row.contribution_count} "
      f"insertable={row.insertable_count} "
      f"reason={row.failure_reason} "
      f"conclusion_exact={row.exact_conclusion_visible} "
      f"conclusion_normalized={row.normalized_conclusion_visible} "
      f"placements={dict(row.placement_counts)} "
      f"provider_anchor_resolved={row.provider_anchor_resolved} "
      f"provider_anchor_unresolved={row.provider_anchor_unresolved}"
    )
    if row.failure_reason != "resolved":
      preview = row.conclusion_line.replace(
        "\n",
        "\\n",
      )
      print(
        "  conclusion="
        + repr(
          preview[:240]
        )
      )

  print()
  print("B. Failure reason totals")
  print("-" * 78)
  print(
    "populated arguments="
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
        row.contribution_count
        for row in rows
      )
    )
  )
  print(
    "insertable contributions="
    + str(
      sum(
        row.insertable_count
        for row in rows
      )
    )
  )
  print(
    "non-insertable contributions="
    + str(
      sum(
        row.contribution_count
        - row.insertable_count
        for row in rows
      )
    )
  )

  for reason in sorted(
    reason_counts
  ):
    print(
      f"{reason}: "
      f"arguments={reason_counts[reason]} "
      f"non_insertable_contributions="
      f"{contribution_reason_counts[reason]}"
    )

  print()
  print("C. Placement inventory")
  print("-" * 78)
  placement_totals = Counter(
    contribution.placement.value
    for n, k in TARGETS
    for contribution_group in (
      _ordered_for_target(
        n,
        k,
      ),
    )
    for contributions in contribution_group
    for contribution in contributions
  )
  for placement, count in sorted(
    placement_totals.items()
  ):
    print(
      f"{placement}: {count}"
    )


def _ordered_for_target(
  n: int,
  k: int,
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
  return build_toda_group_proof_narrative_ordered_contributions(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
    current_markdown=base,
  )


if __name__ == "__main__":
  print_failure_inventory()
