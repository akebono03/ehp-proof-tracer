from collections import deque

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


def _shortest_paths(
  presentation,
  source_step,
  target_step,
):
  children, step_by_id = _children_by_step_id(
    presentation
  )
  source_id = id(source_step)
  target_id = id(target_step)

  if source_id == target_id:
    return (
      (
        source_step,
      ),
    )

  distance = {
    source_id: 0
  }
  predecessors = {
    source_id: []
  }
  queue = deque(
    [
      source_id,
    ]
  )

  while queue:
    current_id = queue.popleft()
    next_distance = distance[
      current_id
    ] + 1

    for child in children.get(
      current_id,
      (),
    ):
      child_id = id(
        child
      )

      if child_id not in distance:
        distance[
          child_id
        ] = next_distance
        predecessors[
          child_id
        ] = [
          current_id,
        ]
        queue.append(
          child_id
        )
        continue

      if distance[
        child_id
      ] == next_distance:
        predecessors[
          child_id
        ].append(
          current_id
        )

  if target_id not in distance:
    return ()

  paths = []

  def build(
    current_id,
    reversed_ids,
  ):
    if current_id == source_id:
      path_ids = tuple(
        reversed(
          (
            current_id,
            *reversed_ids,
          )
        )
      )
      paths.append(
        tuple(
          step_by_id[
            step_id
          ]
          for step_id in path_ids
        )
      )
      return

    for predecessor_id in predecessors[
      current_id
    ]:
      build(
        predecessor_id,
        (
          current_id,
          *reversed_ids,
        ),
      )

  build(
    target_id,
    (),
  )

  return tuple(
    paths
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


def _next_reachable_visible_step(
  presentation,
  connected,
  source_step,
  excluded_step_ids,
):
  candidates = []

  for node in presentation.nodes:
    proof_step = node.proof_step
    step_id = id(
      proof_step
    )

    if step_id in excluded_step_ids:
      continue

    line = _render_generic_narrative_step(
      proof_step
    )
    if not line:
      continue

    position = connected.find(
      line
    )
    if position < 0:
      continue

    paths = _shortest_paths(
      presentation,
      source_step,
      proof_step,
    )
    if not paths:
      continue

    candidates.append(
      (
        position,
        len(
          paths[0]
        ) - 1,
        proof_step,
        paths,
      )
    )

  if not candidates:
    return None

  source_line = _render_generic_narrative_step(
    source_step
  )
  source_position = connected.find(
    source_line
  )

  later = tuple(
    candidate
    for candidate in candidates
    if candidate[
      0
    ] > source_position
  )
  if not later:
    return None

  return min(
    later,
    key=lambda row: (
      row[0],
      row[1],
    ),
  )


def build_chain_audit():
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
  contributions = next(
    rows
    for rows in ordered
    if rows
  )
  contribution_step_ids = {
    id(
      contribution.proof_step
    )
    for contribution in contributions
  }

  segments = []

  for source_index in range(
    3
  ):
    source = contributions[
      source_index
    ].proof_step

    if source_index < 2:
      target = contributions[
        source_index + 1
      ].proof_step
      paths = _shortest_paths(
        presentation,
        source,
        target,
      )
      target_kind = (
        "next_contribution"
      )
    else:
      target_row = (
        _next_reachable_visible_step(
          presentation,
          connected,
          source,
          contribution_step_ids,
        )
      )
      if target_row is None:
        target = None
        paths = ()
      else:
        target = target_row[
          2
        ]
        paths = target_row[
          3
        ]
      target_kind = (
        "next_reachable_visible"
      )

    segments.append(
      {
        "source_index": source_index,
        "source": source,
        "target": target,
        "target_kind": target_kind,
        "paths": paths,
      }
    )

  return (
    presentation,
    connected,
    contributions,
    tuple(
      segments
    ),
  )


def _rule_name(
  proof_step,
):
  if proof_step.inference_rule is None:
    return None
  return proof_step.inference_rule.name


def main():
  (
    presentation,
    connected,
    contributions,
    segments,
  ) = build_chain_audit()

  print("=" * 78)
  print("Phase 144-6-R5-43-5 transitive contribution chain audit")
  print("production changes: none")
  print("=" * 78)
  print()

  for segment_index, segment in enumerate(
    segments,
    start=1,
  ):
    source = segment[
      "source"
    ]
    target = segment[
      "target"
    ]
    paths = segment[
      "paths"
    ]

    print(
      f"Segment {segment_index}: "
      f"C{segment['source_index'] + 1} -> "
      f"{segment['target_kind']}"
    )
    print(
      "  source: "
      + _render_generic_narrative_step(
        source
      )
    )

    if target is None:
      print(
        "  target: none"
      )
      print(
        "  shortest paths: 0"
      )
      print()
      continue

    print(
      "  target: "
      + _render_generic_narrative_step(
        target
      )
    )
    print(
      f"  shortest distance: "
      f"{len(paths[0]) - 1}"
    )
    print(
      f"  shortest paths: "
      f"{len(paths)}"
    )

    for path_index, path in enumerate(
      paths,
      start=1,
    ):
      print(
        f"  Path {path_index}:"
      )

      for step_index, proof_step in enumerate(
        path
      ):
        if step_index == 0:
          status = "SOURCE"
        elif step_index == len(
          path
        ) - 1:
          status = "TARGET"
        else:
          status = (
            "VISIBLE"
            if _is_visible(
              connected,
              proof_step,
            )
            else "HIDDEN"
          )

        print(
          f"    [{step_index}] "
          f"{status} "
          f"type={type(proof_step.conclusion).__name__} "
          f"rule={_rule_name(proof_step)!r}"
        )
        print(
          "        "
          + _render_generic_narrative_step(
            proof_step
          )
        )

    hidden_counts = tuple(
      sum(
        1
        for proof_step in path[
          1:-1
        ]
        if not _is_visible(
          connected,
          proof_step,
        )
      )
      for path in paths
    )
    print(
      "  hidden intermediate counts: "
      + ", ".join(
        str(
          count
        )
        for count in hidden_counts
      )
    )
    print()

  print("Summary")
  print("-" * 78)
  for segment_index, segment in enumerate(
    segments,
    start=1,
  ):
    paths = segment[
      "paths"
    ]
    if not paths:
      print(
        f"Segment {segment_index}: unreachable"
      )
      continue

    minimum_hidden = min(
      sum(
        1
        for proof_step in path[
          1:-1
        ]
        if not _is_visible(
          connected,
          proof_step,
        )
      )
      for path in paths
    )
    print(
      f"Segment {segment_index}: "
      f"distance={len(paths[0]) - 1} "
      f"shortest_paths={len(paths)} "
      f"minimum_hidden_intermediates={minimum_hidden}"
    )

  print()
  print(
    "No transitive prose connector is added in R5-43-5."
  )


if __name__ == "__main__":
  main()
