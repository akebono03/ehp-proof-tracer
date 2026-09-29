from collections import Counter, deque

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
from toda_group_proof_narrative_hidden_bridge_semantics import (
  TodaGroupProofNarrativeHiddenBridgeSemanticRole,
  build_toda_group_proof_narrative_hidden_bridge_semantics,
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
  rendered = _render_generic_narrative_step(
    proof_step
  )

  return bool(
    rendered
    and rendered in markdown
  )


def _semantic_role_by_step_id(
  presentation,
):
  return {
    id(
      semantic.proof_step
    ): semantic.role
    for semantic in (
      build_toda_group_proof_narrative_hidden_bridge_semantics(
        presentation
      )
    )
  }


def _rule_name(
  proof_step,
):
  rule = proof_step.inference_rule

  if rule is None:
    return None

  return rule.name


def _signature(
  proof_step,
):
  return (
    type(
      proof_step.conclusion
    ).__name__,
    _rule_name(
      proof_step
    ),
  )


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
  role_by_step_id = _semantic_role_by_step_id(
    presentation
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

      hidden = tuple(
        proof_step
        for proof_step in path[
          1:-1
        ]
        if not _is_visible(
          connected,
          proof_step,
        )
      )
      hidden_roles = tuple(
        role_by_step_id.get(
          id(
            proof_step
          )
        )
        for proof_step in hidden
      )

      if not hidden:
        continue

      if not all(
        role
        is TodaGroupProofNarrativeHiddenBridgeSemanticRole.TRANSPORT
        for role in hidden_roles
      ):
        continue

      rows.append(
        {
          "n": n,
          "k": k,
          "argument_index": argument_index,
          "source_index": source_index,
          "source": source,
          "target": target,
          "path": path,
          "hidden": hidden,
          "hidden_roles": hidden_roles,
          "source_signature": _signature(
            source
          ),
          "target_signature": _signature(
            target
          ),
          "hidden_signatures": tuple(
            _signature(
              proof_step
            )
            for proof_step in hidden
          ),
          "hidden_rendered": tuple(
            _render_generic_narrative_step(
              proof_step
            )
            for proof_step in hidden
          ),
        }
      )

  return tuple(
    rows
  )


def build_transport_chain_inventory():
  return tuple(
    row
    for n, k in TARGETS
    for row in _context_inventory(
      n,
      k,
    )
  )


def main():
  rows = build_transport_chain_inventory()

  print("=" * 78)
  print(
    "Phase 144-6-R5-43-8 transport chain "
    "narrative compression audit"
  )
  print("production changes: none")
  print("=" * 78)
  print()

  print("A. Population")
  print("-" * 78)
  print(
    f"representative groups={len(TARGETS)}"
  )
  print(
    f"transport chains={len(rows)}"
  )
  print(
    "transport hidden steps="
    f"{sum(len(row['hidden']) for row in rows)}"
  )
  print()

  print("B. Chain-length distribution")
  print("-" * 78)
  for length, count in sorted(
    Counter(
      len(
        row[
          "hidden"
        ]
      )
      for row in rows
    ).items()
  ):
    print(
      f"hidden_length={length}: {count}"
    )
  print()

  print("C. Hidden signature sequence distribution")
  print("-" * 78)
  sequence_counts = Counter(
    row[
      "hidden_signatures"
    ]
    for row in rows
  )

  for sequence, count in sequence_counts.items():
    print(
      f"count={count}"
    )

    for index, signature in enumerate(
      sequence,
      start=1,
    ):
      print(
        f"  {index}: "
        f"type={signature[0]} "
        f"rule={signature[1]!r}"
      )
  print()

  print("D. Boundary signature distribution")
  print("-" * 78)
  boundary_counts = Counter(
    (
      row[
        "source_signature"
      ],
      row[
        "target_signature"
      ],
    )
    for row in rows
  )

  for (
    source_signature,
    target_signature,
  ), count in boundary_counts.items():
    print(
      f"count={count}"
    )
    print(
      "  source: "
      f"type={source_signature[0]} "
      f"rule={source_signature[1]!r}"
    )
    print(
      "  target: "
      f"type={target_signature[0]} "
      f"rule={target_signature[1]!r}"
    )
  print()

  print("E. Per-chain detail")
  print("-" * 78)
  for index, row in enumerate(
    rows,
    start=1,
  ):
    print(
      f"Chain {index}: "
      f"pi_{row['n'] + row['k']}^{row['n']} "
      f"arg={row['argument_index']} "
      f"segment={row['source_index'] + 1}->"
      f"{row['source_index'] + 2}"
    )
    print(
      "  source: "
      + _render_generic_narrative_step(
        row[
          "source"
        ]
      )
    )

    for hidden_index, rendered in enumerate(
      row[
        "hidden_rendered"
      ],
      start=1,
    ):
      print(
        f"  transport {hidden_index}: "
        f"{rendered}"
      )

    print(
      "  target: "
      + _render_generic_narrative_step(
        row[
          "target"
        ]
      )
    )
  print()

  print("F. Compression preconditions")
  print("-" * 78)
  print(
    "unique hidden signature sequences="
    f"{len(sequence_counts)}"
  )
  print(
    "unique boundary signature pairs="
    f"{len(boundary_counts)}"
  )
  print(
    "No compression prose is added in R5-43-8."
  )


if __name__ == "__main__":
  main()
