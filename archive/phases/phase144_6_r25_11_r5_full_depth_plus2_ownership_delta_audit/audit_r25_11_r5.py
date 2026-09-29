from dataclasses import dataclass
import importlib.util
from pathlib import Path
import sys

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
  _contribution_insertion_indices,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)

EXPECTED_TOTAL = 190
EXPECTED_PI6 = 5
EXPECTED_PARTICIPATING = 33
EXPECTED_DETACHED = 157
EXPECTED_DETACHED_INSERTABLE = 0


def load_test_module(filename: str):
  path = Path("tests") / filename
  name = "_r25_11_r5_" + path.stem
  if name in sys.modules:
    return sys.modules[name]
  spec = importlib.util.spec_from_file_location(
    name,
    path,
  )
  if spec is None or spec.loader is None:
    raise ImportError(
      f"cannot load {path}"
    )
  module = importlib.util.module_from_spec(
    spec
  )
  sys.modules[name] = module
  spec.loader.exec_module(module)
  return module


foundation = load_test_module(
  "test_phase144_6_r5_18_production_generic_proof_chain_foundation.py"
)


@dataclass(frozen=True)
class Row:
  n: int
  k: int
  argument_index: int
  argument_role: str
  discourse_role: str
  statement_type: str
  rule_name: str
  rendered: str
  provider_anchor: bool
  placement: str
  provider_key_count: int
  distance: int | None
  insertable: bool


def discourse_by_argument_id(
  arguments,
):
  ordered_arguments = (
    order_toda_group_proof_narrative_arguments(
      arguments
    )
  )
  discourse_roles = (
    classify_toda_group_proof_narrative_argument_discourse_roles(
      arguments
    )
  )
  return {
    id(argument): discourse_roles[position]
    for position, argument in enumerate(
      ordered_arguments
    )
  }


def build_inventory():
  rows = []

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      _aggregate,
      proof_chains,
    ) = foundation._context(
      n,
      k,
    )

    base_markdown = (
      render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )
    ordered = (
      build_toda_group_proof_narrative_ordered_contributions(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        proof_chains,
        current_markdown=base_markdown,
      )
    )
    insertion_indices = (
      _contribution_insertion_indices(
        base_markdown,
        blocks,
        arguments,
        ordered,
      )
    )
    discourse = discourse_by_argument_id(
      arguments
    )

    for argument_index, contributions in enumerate(
      ordered
    ):
      argument = arguments[
        argument_index
      ]
      discourse_role = discourse[
        id(argument)
      ]

      for contribution_index, contribution in enumerate(
        contributions
      ):
        step = contribution.proof_step
        rule = step.inference_rule
        rows.append(
          Row(
            n=n,
            k=k,
            argument_index=argument_index,
            argument_role=argument.role.value,
            discourse_role=discourse_role.value,
            statement_type=type(
              step.conclusion
            ).__name__,
            rule_name=(
              "<none>"
              if rule is None
              else rule.name
            ),
            rendered=(
              _render_generic_narrative_step(
                step
              )
            ),
            provider_anchor=(
              contribution.provider_anchor
            ),
            placement=(
              contribution.placement.value
            ),
            provider_key_count=len(
              contribution.provider_keys
            ),
            distance=(
              contribution.distance_to_conclusion
            ),
            insertable=(
              insertion_indices[
                argument_index
              ][
                contribution_index
              ]
              is not None
            ),
          )
        )

  return tuple(
    rows
  )


def group_name(row):
  return (
    f"pi_{row.n + row.k}^{row.n}"
  )


def print_row(prefix, row):
  print(prefix)
  print(
    f"  group={group_name(row)} "
    f"argument[{row.argument_index}] "
    f"argument_role={row.argument_role} "
    f"discourse={row.discourse_role}"
  )
  print(
    f"  type={row.statement_type}"
  )
  print(
    f"  rule={row.rule_name}"
  )
  print(
    f"  provider_anchor={row.provider_anchor} "
    f"placement={row.placement} "
    f"provider_key_count={row.provider_key_count} "
    f"distance={row.distance} "
    f"insertable={row.insertable}"
  )
  print(
    f"  rendered={row.rendered}"
  )


def audit_population(rows):
  print("=" * 78)
  print("A. Full-depth selected population delta")
  print("=" * 78)

  total = 0
  for n, k in TARGETS:
    group_rows = tuple(
      row
      for row in rows
      if (
        row.n,
        row.k,
      ) == (
        n,
        k,
      )
    )
    total += len(
      group_rows
    )
    expected_note = (
      " expected=5 delta="
      + f"{len(group_rows) - EXPECTED_PI6:+d}"
      if (
        n,
        k,
      ) == (
        3,
        3,
      )
      else ""
    )
    print(
      f"pi_{n + k}^{n}: "
      f"selected={len(group_rows)}"
      + expected_note
    )

  print(
    f"TOTAL_SELECTED={total}"
  )
  print(
    f"EXPECTED_TOTAL={EXPECTED_TOTAL}"
  )
  print(
    f"TOTAL_DELTA={total - EXPECTED_TOTAL:+d}"
  )


def audit_participation(rows):
  print()
  print("=" * 78)
  print("B. Participation and insertion-boundary delta")
  print("=" * 78)

  participating = tuple(
    row
    for row in rows
    if (
      row.discourse_role
      != TodaGroupProofNarrativeArgumentDiscourseRole
      .DETACHED.value
    )
  )
  detached = tuple(
    row
    for row in rows
    if (
      row.discourse_role
      == TodaGroupProofNarrativeArgumentDiscourseRole
      .DETACHED.value
    )
  )
  detached_insertable = tuple(
    row
    for row in detached
    if row.insertable
  )
  participating_not_insertable = tuple(
    row
    for row in participating
    if not row.insertable
  )

  print(
    f"participating_selected={len(participating)} "
    f"expected={EXPECTED_PARTICIPATING} "
    f"delta={len(participating) - EXPECTED_PARTICIPATING:+d}"
  )
  print(
    f"detached_selected={len(detached)} "
    f"expected={EXPECTED_DETACHED} "
    f"delta={len(detached) - EXPECTED_DETACHED:+d}"
  )
  print(
    f"detached_insertable={len(detached_insertable)} "
    f"expected={EXPECTED_DETACHED_INSERTABLE} "
    f"delta={len(detached_insertable) - EXPECTED_DETACHED_INSERTABLE:+d}"
  )
  print(
    "participating_not_insertable="
    + str(
      len(
        participating_not_insertable
      )
    )
  )

  print()
  print("Detached contributions that became insertable:")
  if not detached_insertable:
    print("  <none>")
  for index, row in enumerate(
    detached_insertable
  ):
    print_row(
      f"detached_insertable[{index}]",
      row,
    )

  print()
  print("Participating contributions that are not insertable:")
  if not participating_not_insertable:
    print("  <none>")
  for index, row in enumerate(
    participating_not_insertable
  ):
    print_row(
      f"participating_not_insertable[{index}]",
      row,
    )


def audit_pi6(rows):
  print()
  print("=" * 78)
  print("C. pi_6^3 selected ownership inventory")
  print("=" * 78)

  pi6 = tuple(
    row
    for row in rows
    if (
      row.n,
      row.k,
    ) == (
      3,
      3,
    )
  )
  print(
    f"selected={len(pi6)} "
    f"expected={EXPECTED_PI6} "
    f"delta={len(pi6) - EXPECTED_PI6:+d}"
  )
  for index, row in enumerate(
    pi6
  ):
    print_row(
      f"pi6_selected[{index}]",
      row,
    )


def audit_anomaly_summary(rows):
  print()
  print("=" * 78)
  print("D. Candidate +2 ownership-delta summary")
  print("=" * 78)

  participating = tuple(
    row
    for row in rows
    if (
      row.discourse_role
      != TodaGroupProofNarrativeArgumentDiscourseRole
      .DETACHED.value
    )
  )
  detached_insertable = tuple(
    row
    for row in rows
    if (
      row.discourse_role
      == TodaGroupProofNarrativeArgumentDiscourseRole
      .DETACHED.value
      and row.insertable
    )
  )

  participating_by_group = {}
  for n, k in TARGETS:
    participating_by_group[
      (
        n,
        k,
      )
    ] = tuple(
      row
      for row in participating
      if (
        row.n,
        row.k,
      ) == (
        n,
        k,
      )
    )

  print("Participating selected by group:")
  for n, k in TARGETS:
    group_rows = participating_by_group[
      (
        n,
        k,
      )
    ]
    print(
      f"  pi_{n + k}^{n}: "
      f"{len(group_rows)}"
    )

  print()
  print("Detached-insertable by group:")
  for n, k in TARGETS:
    group_rows = tuple(
      row
      for row in detached_insertable
      if (
        row.n,
        row.k,
      ) == (
        n,
        k,
      )
    )
    print(
      f"  pi_{n + k}^{n}: "
      f"{len(group_rows)}"
    )

  print()
  print(
    "Interpretation guard: this audit reports structural "
    "candidates only. It does not assume that every "
    "detached-insertable row is one of the +2 selected rows."
  )


def main():
  rows = build_inventory()
  audit_population(
    rows
  )
  audit_participation(
    rows
  )
  audit_pi6(
    rows
  )
  audit_anomaly_summary(
    rows
  )

  print()
  print("=" * 78)
  print("R25-11-R5 full-depth +2 ownership delta audit complete.")
  print("Production changes: none.")
  print("Existing test changes: none.")
  print("Full pytest: not run.")
  print("=" * 78)


if __name__ == "__main__":
  main()
