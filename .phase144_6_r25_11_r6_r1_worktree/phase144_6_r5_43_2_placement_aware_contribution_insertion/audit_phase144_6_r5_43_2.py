from test_phase144_6_r5_43_2_placement_aware_contribution_insertion import (
  _pi6_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
  _contribution_insertion_indices,
)


def main():
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

  print("=" * 78)
  print("Phase 144-6-R5-43-2 placement-aware contribution insertion audit")
  print("=" * 78)
  print(f"contributions={len(rows)}")
  print(f"distinct_insertion_indices={len(set(indices))}")
  print()

  for number, (row, insertion_index) in enumerate(
    zip(rows, indices),
    start=1,
  ):
    line = _render_generic_narrative_step(row.proof_step)
    print(
      f"C{number}: placement={row.placement.value} "
      f"insertion_index={insertion_index}"
    )
    print(line)
    print()

  print("Connected Narrative")
  print("-" * 78)
  print(connected)


if __name__ == "__main__":
  main()
