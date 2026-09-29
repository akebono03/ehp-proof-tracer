from collections import Counter, deque

from proof import Relation
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
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)


def _children_by_step_id(presentation):
  children = {}
  step_by_id = {
    id(node.proof_step): node.proof_step
    for node in presentation.nodes
  }

  for edge in presentation.edges:
    children.setdefault(
      id(edge.premise_step),
      [],
    ).append(
      edge.parent_step
    )

  return children, step_by_id


def _one_shortest_path(
  presentation,
  source_step,
  target_step,
):
  children, step_by_id = _children_by_step_id(
    presentation
  )
  source_id = id(source_step)
  target_id = id(target_step)

  distance = {
    source_id: 0
  }
  predecessor = {}
  queue = deque(
    [
      source_id,
    ]
  )

  while queue:
    current_id = queue.popleft()

    if current_id == target_id:
      break

    for child in children.get(
      current_id,
      (),
    ):
      child_id = id(
        child
      )

      if child_id in distance:
        continue

      distance[
        child_id
      ] = distance[
        current_id
      ] + 1
      predecessor[
        child_id
      ] = current_id
      queue.append(
        child_id
      )

  if target_id not in distance:
    return ()

  path_ids = [
    target_id,
  ]
  current_id = target_id

  while current_id != source_id:
    current_id = predecessor[
      current_id
    ]
    path_ids.append(
      current_id
    )

  path_ids.reverse()

  return tuple(
    step_by_id[
      step_id
    ]
    for step_id in path_ids
  )


def _is_visible(
  markdown,
  proof_step,
):
  line = _render_generic_narrative_step(
    proof_step
  )
  return bool(
    line
    and line in markdown
  )


def _candidate_classification(
  proof_step,
):
  statement = proof_step.conclusion
  rule = (
    proof_step.inference_rule.name
    if proof_step.inference_rule is not None
    else ""
  )
  lowered = rule.lower()

  if isinstance(
    statement,
    Relation,
  ):
    if (
      "transport" in lowered
      or "bridge" in lowered
    ):
      return "transport_candidate"

    return "mathematical_relation_candidate"

  if (
    "integration" in lowered
  ):
    return "integration_provenance_candidate"

  return "structured_mathematical_candidate"


def _context_inventory(
  n,
  k,
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
  rows = []

  for argument_index, contributions in enumerate(
    ordered
  ):
    if len(
      contributions
    ) < 2:
      continue

    for source_index in range(
      len(
        contributions
      ) - 1
    ):
      source = contributions[
        source_index
      ].proof_step
      target = contributions[
        source_index + 1
      ].proof_step
      path = _one_shortest_path(
        presentation,
        source,
        target,
      )

      if len(
        path
      ) <= 2:
        continue

      hidden_steps = tuple(
        proof_step
        for proof_step in path[
          1:-1
        ]
        if not _is_visible(
          connected,
          proof_step,
        )
      )

      if not hidden_steps:
        continue

      for path_index, proof_step in enumerate(
        path[
          1:-1
        ],
        start=1,
      ):
        if _is_visible(
          connected,
          proof_step,
        ):
          continue

        rule_name = (
          proof_step.inference_rule.name
          if proof_step.inference_rule is not None
          else None
        )
        rows.append(
          {
            "n": n,
            "k": k,
            "argument_index": argument_index,
            "source_index": source_index,
            "path_index": path_index,
            "path_distance": len(
              path
            ) - 1,
            "statement_type": type(
              proof_step.conclusion
            ).__name__,
            "rule_name": rule_name,
            "rendered": _render_generic_narrative_step(
              proof_step
            ),
            "classification": _candidate_classification(
              proof_step
            ),
            "is_relation": isinstance(
              proof_step.conclusion,
              Relation,
            ),
          }
        )

  return tuple(
    rows
  )


def build_hidden_bridge_inventory():
  return tuple(
    row
    for n, k in TARGETS
    for row in _context_inventory(
      n,
      k,
    )
  )


def main():
  rows = build_hidden_bridge_inventory()

  print("=" * 78)
  print("Phase 144-6-R5-43-6 hidden bridge classification audit")
  print("production changes: none")
  print("=" * 78)
  print()

  print("A. Population")
  print("-" * 78)
  print(
    f"representative groups={len(TARGETS)}"
  )
  print(
    f"hidden bridge occurrences={len(rows)}"
  )
  print()

  print("B. Candidate classification counts")
  print("-" * 78)
  for classification, count in sorted(
    Counter(
      row[
        "classification"
      ]
      for row in rows
    ).items()
  ):
    print(
      f"{classification}: {count}"
    )
  print()

  print("C. Statement type / inference rule inventory")
  print("-" * 78)
  signatures = Counter(
    (
      row[
        "classification"
      ],
      row[
        "statement_type"
      ],
      row[
        "rule_name"
      ],
    )
    for row in rows
  )

  for (
    classification,
    statement_type,
    rule_name,
  ), count in sorted(
    signatures.items(),
    key=lambda item: (
      item[
        0
      ][
        0
      ],
      item[
        0
      ][
        1
      ],
      str(
        item[
          0
        ][
          2
        ]
      ),
    ),
  ):
    print(
      f"{count:3d} x "
      f"class={classification} "
      f"type={statement_type} "
      f"rule={rule_name!r}"
    )
  print()

  print("D. Per-group hidden bridges")
  print("-" * 78)
  for n, k in TARGETS:
    group_rows = tuple(
      row
      for row in rows
      if (
        row[
          "n"
        ],
        row[
          "k"
        ],
      ) == (
        n,
        k,
      )
    )
    print(
      f"pi_{n + k}^{n}: "
      f"hidden_bridges={len(group_rows)}"
    )

    for index, row in enumerate(
      group_rows,
      start=1,
    ):
      print(
        f"  H{index}: "
        f"arg={row['argument_index']} "
        f"segment={row['source_index'] + 1}->"
        f"{row['source_index'] + 2} "
        f"path_index={row['path_index']}/"
        f"{row['path_distance'] - 1} "
        f"class={row['classification']}"
      )
      print(
        f"    type={row['statement_type']}"
      )
      print(
        f"    rule={row['rule_name']!r}"
      )
      print(
        f"    {row['rendered']}"
      )
  print()

  print("E. Structural observations for the next phase")
  print("-" * 78)
  relation_count = sum(
    1
    for row in rows
    if row[
      "is_relation"
    ]
  )
  print(
    f"Relation occurrences: "
    f"{relation_count}/{len(rows)}"
  )
  print(
    "Candidate labels are audit-only. "
    "No semantic enum or prose behavior is added."
  )


if __name__ == "__main__":
  main()
