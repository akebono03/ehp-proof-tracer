from __future__ import annotations

from collections import deque
from pathlib import Path

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_internal_step_ids,
  _toda_group_proof_narrative_reference_owned_step_ids,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  extract_toda_group_proof_step_literature_reference,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _presentation(
  depth: int,
):
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=depth,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  return (
    raw,
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    ),
  )


def _ref(step):
  reference = extract_toda_group_proof_step_literature_reference(
    step
  )
  if reference is None:
    return None
  return (
    reference.label,
    reference.locator,
  )


def _children_by_step_id(
  presentation,
):
  result = {}
  for edge in presentation.edges:
    result.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )
  return result


def _shortest_path_to_root(
  presentation,
  source_step,
  blocked_step_ids,
):
  children = _children_by_step_id(
    presentation
  )
  root_id = id(
    presentation.root_step
  )

  queue = deque(
    [
      source_step,
    ]
  )
  predecessor = {
    id(
      source_step
    ): None,
  }
  step_by_id = {
    id(
      node.proof_step
    ): node.proof_step
    for node in presentation.nodes
  }

  while queue:
    current = queue.popleft()
    current_id = id(
      current
    )

    if current_id == root_id:
      path = []
      cursor_id = current_id

      while cursor_id is not None:
        path.append(
          step_by_id[
            cursor_id
          ]
        )
        cursor_id = predecessor[
          cursor_id
        ]

      return tuple(
        reversed(
          path
        )
      )

    for child in children.get(
      current_id,
      (),
    ):
      child_id = id(
        child
      )

      if (
        child_id in predecessor
        or child_id in blocked_step_ids
      ):
        continue

      predecessor[
        child_id
      ] = current_id
      queue.append(
        child
      )

  return ()


def main() -> int:
  lines = []

  for depth in (
    2,
    3,
  ):
    raw, presentation = _presentation(
      depth
    )
    entries = build_toda_group_proof_narrative_reference_entries(
      presentation
    )
    empty_lines = {
      entry.number: ()
      for entry in entries
    }
    (
      entries,
      _,
    ) = exclude_toda_group_proof_narrative_root_reference(
      entries,
      empty_lines,
      presentation.root_step,
    )

    internal_step_ids = (
      _toda_group_proof_narrative_reference_internal_step_ids(
        presentation,
        entries,
      )
    )
    owned_step_ids = (
      _toda_group_proof_narrative_reference_owned_step_ids(
        presentation,
        entries,
      )
    )

    prop51 = next(
      entry
      for entry in entries
      if entry.reference.locator == "Proposition 5.1"
    )

    lines.append(
      "=" * 90
    )
    lines.append(
      "DEPTH "
      + str(
        depth
      )
    )
    lines.append(
      "=" * 90
    )
    lines.append(
      "Proposition 5.1 steps: "
      + str(
        len(
          prop51.proof_steps
        )
      )
    )

    for index, step in enumerate(
      prop51.proof_steps,
      start=1,
    ):
      lines.append(
        ""
      )
      lines.append(
        "PROP51 STEP "
        + str(
          index
        )
      )
      lines.append(
        "id="
        + str(
          id(
            step
          )
        )
      )
      lines.append(
        "rule="
        + str(
          (
            step.inference_rule.name
            if step.inference_rule is not None
            else None
          )
        )
      )
      lines.append(
        "reference="
        + str(
          _ref(
            step
          )
        )
      )
      lines.append(
        "rendered="
        + str(
          _render_generic_narrative_step(
            step
          )
        )
      )
      lines.append(
        "internal="
        + str(
          id(
            step
          )
          in internal_step_ids
        )
      )
      lines.append(
        "owned="
        + str(
          id(
            step
          )
          in owned_step_ids
        )
      )

      direct_consumers = tuple(
        edge.parent_step
        for edge in presentation.edges
        if edge.premise_step is step
      )

      lines.append(
        "direct_consumers="
        + str(
          len(
            direct_consumers
          )
        )
      )

      for consumer_index, consumer in enumerate(
        direct_consumers,
        start=1,
      ):
        lines.append(
          "  consumer "
          + str(
            consumer_index
          )
          + ": id="
          + str(
            id(
              consumer
            )
          )
          + " ref="
          + str(
            _ref(
              consumer
            )
          )
          + " internal="
          + str(
            id(
              consumer
            )
            in internal_step_ids
          )
          + " rendered="
          + str(
            _render_generic_narrative_step(
              consumer
            )
          )
        )

      path = _shortest_path_to_root(
        presentation,
        step,
        internal_step_ids,
      )

      lines.append(
        "path_without_internal_steps="
        + str(
          bool(
            path
          )
        )
      )

      for path_index, path_step in enumerate(
        path,
        start=1,
      ):
        lines.append(
          "  path["
          + str(
            path_index
          )
          + "] id="
          + str(
            id(
              path_step
            )
          )
          + " ref="
          + str(
            _ref(
              path_step
            )
          )
          + " internal="
          + str(
            id(
              path_step
            )
            in internal_step_ids
          )
          + " rule="
          + str(
            (
              path_step.inference_rule.name
              if path_step.inference_rule is not None
              else None
            )
          )
          + " rendered="
          + str(
            _render_generic_narrative_step(
              path_step
            )
          )
        )

    rendered = render_toda_group_proof_narrative_markdown(
      raw
    )
    lines.append(
      ""
    )
    lines.append(
      "PUBLIC REFERENCE HEADERS"
    )
    for line in rendered.splitlines():
      if line.startswith(
        "**[R"
      ):
        lines.append(
          line
        )

  output = "\n".join(
    lines
  )
  print(
    output
  )

  path = Path(
    "phase156_r5_repair11_proposition51_path_diagnostic.txt"
  )
  path.write_text(
    output,
    encoding="utf-8",
  )

  print()
  print(
    "PASS: diagnostic completed."
  )
  print(
    "Production changes: none."
  )
  print(
    "Repository-wide pytest is intentionally NOT run."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
