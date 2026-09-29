from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  _context,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  _contribution_insertion_indices,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)


def _children_by_step_id(presentation):
  children = {}
  for edge in presentation.edges:
    children.setdefault(
      id(edge.premise_step),
      [],
    ).append(
      edge.parent_step
    )
  return children


def _reachable(children, source_step, target_step):
  target_id = id(target_step)
  stack = list(
    children.get(
      id(source_step),
      (),
    )
  )
  seen = set()

  while stack:
    current = stack.pop()
    current_id = id(current)
    if current_id == target_id:
      return True
    if current_id in seen:
      continue
    seen.add(current_id)
    stack.extend(
      children.get(
        current_id,
        (),
      )
    )

  return False


def _direct_parent_steps(presentation, proof_step):
  return tuple(
    edge.parent_step
    for edge in presentation.edges
    if edge.premise_step is proof_step
  )


def _visible_step_positions(markdown, presentation):
  rows = []
  seen_lines = set()

  for node in presentation.nodes:
    proof_step = node.proof_step
    line = _render_generic_narrative_step(
      proof_step
    )
    if not line:
      continue
    if line in seen_lines:
      continue
    position = markdown.find(line)
    if position < 0:
      continue
    seen_lines.add(line)
    rows.append(
      (
        position,
        proof_step,
        line,
      )
    )

  return tuple(
    sorted(
      rows,
      key=lambda row: row[0],
    )
  )


def _next_visible_step(
  visible_rows,
  contribution_line,
):
  contribution_position = next(
    position
    for position, proof_step, line in visible_rows
    if line == contribution_line
  )
  return next(
    (
      (position, proof_step, line)
      for position, proof_step, line in visible_rows
      if position > contribution_position
    ),
    None,
  )


def _nearest_reachable_visible_step(
  visible_rows,
  children,
  contribution_step,
):
  contribution_line = _render_generic_narrative_step(
    contribution_step
  )
  contribution_position = next(
    position
    for position, proof_step, line in visible_rows
    if line == contribution_line
  )

  for position, proof_step, line in visible_rows:
    if position <= contribution_position:
      continue
    if _reachable(
      children,
      contribution_step,
      proof_step,
    ):
      return (
        position,
        proof_step,
        line,
      )

  return None


def build_transition_inventory():
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
  insertion_indices = _contribution_insertion_indices(
    base,
    blocks,
    arguments,
    ordered,
  )
  children = _children_by_step_id(
    presentation
  )
  visible_rows = _visible_step_positions(
    connected,
    presentation,
  )

  inventory = []

  for argument_index, contributions in enumerate(
    ordered
  ):
    for contribution_index, contribution in enumerate(
      contributions
    ):
      contribution_line = _render_generic_narrative_step(
        contribution.proof_step
      )
      direct_parents = _direct_parent_steps(
        presentation,
        contribution.proof_step,
      )
      next_visible = _next_visible_step(
        visible_rows,
        contribution_line,
      )
      nearest_reachable = _nearest_reachable_visible_step(
        visible_rows,
        children,
        contribution.proof_step,
      )

      inventory.append(
        {
          "argument_index": argument_index,
          "contribution_index": contribution_index,
          "line": contribution_line,
          "placement": contribution.placement.value,
          "insertion_index": insertion_indices[
            argument_index
          ][
            contribution_index
          ],
          "direct_parent_lines": tuple(
            _render_generic_narrative_step(step)
            for step in direct_parents
          ),
          "next_visible_line": (
            None
            if next_visible is None
            else next_visible[2]
          ),
          "next_visible_is_direct_parent": (
            False
            if next_visible is None
            else any(
              next_visible[1] is step
              for step in direct_parents
            )
          ),
          "next_visible_is_reachable": (
            False
            if next_visible is None
            else _reachable(
              children,
              contribution.proof_step,
              next_visible[1],
            )
          ),
          "nearest_reachable_visible_line": (
            None
            if nearest_reachable is None
            else nearest_reachable[2]
          ),
        }
      )

  return (
    connected,
    tuple(
      inventory
    ),
  )


def main():
  connected, inventory = build_transition_inventory()

  print("=" * 78)
  print("Phase 144-6-R5-43-3 contribution transition prose audit")
  print("production changes: none")
  print("=" * 78)
  print()
  print("A. Contribution transition inventory")
  print("-" * 78)

  for row in inventory:
    number = row[
      "contribution_index"
    ] + 1
    print(
      f"C{number}: placement={row['placement']} "
      f"insertion_index={row['insertion_index']}"
    )
    print(f"  contribution: {row['line']}")
    print(
      "  direct parents:"
    )
    if row["direct_parent_lines"]:
      for parent_line in row[
        "direct_parent_lines"
      ]:
        print(
          f"    - {parent_line}"
        )
    else:
      print("    - none")
    print(
      "  next visible: "
      f"{row['next_visible_line']}"
    )
    print(
      "  next visible direct parent: "
      f"{row['next_visible_is_direct_parent']}"
    )
    print(
      "  next visible reachable: "
      f"{row['next_visible_is_reachable']}"
    )
    print(
      "  nearest reachable visible: "
      f"{row['nearest_reachable_visible_line']}"
    )
    print()

  print("B. Grouped insertion anchors")
  print("-" * 78)
  groups = {}
  for row in inventory:
    groups.setdefault(
      row["insertion_index"],
      [],
    ).append(
      row
    )

  for insertion_index, rows in sorted(
    groups.items()
  ):
    labels = ", ".join(
      f"C{row['contribution_index'] + 1}"
      for row in rows
    )
    targets = []
    for row in rows:
      target = row[
        "nearest_reachable_visible_line"
      ]
      if target is None:
        continue
      if target not in targets:
        targets.append(
          target
        )
    print(
      f"anchor={insertion_index}: {labels}"
    )
    if targets:
      for target in targets:
        print(
          f"  reachable target: {target}"
        )
    else:
      print(
        "  reachable target: none"
      )
  print()

  print("C. Interpretation inputs")
  print("-" * 78)
  direct_count = sum(
    1
    for row in inventory
    if row[
      "next_visible_is_direct_parent"
    ]
  )
  reachable_count = sum(
    1
    for row in inventory
    if row[
      "next_visible_is_reachable"
    ]
  )
  target_count = sum(
    1
    for row in inventory
    if row[
      "nearest_reachable_visible_line"
    ] is not None
  )
  print(
    f"next-visible direct-parent relations: "
    f"{direct_count}/{len(inventory)}"
  )
  print(
    f"next-visible reachable relations: "
    f"{reachable_count}/{len(inventory)}"
  )
  print(
    f"nearest reachable visible targets: "
    f"{target_count}/{len(inventory)}"
  )
  print()
  print(
    "No prose connector is added in R5-43-3. "
    "These facts are the input for the next implementation decision."
  )


if __name__ == "__main__":
  main()
