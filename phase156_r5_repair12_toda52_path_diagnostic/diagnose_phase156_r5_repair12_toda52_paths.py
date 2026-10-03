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
  _toda_group_proof_narrative_reference_frontier_step_ids,
  _toda_group_proof_narrative_reference_internal_step_ids,
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
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  return raw, closure


def _ref(
  step,
):
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


def _all_paths_to_root(
  presentation,
  source_step,
  max_paths: int = 20,
):
  children = _children_by_step_id(
    presentation
  )
  root = presentation.root_step
  result = []
  stack = [
    (
      source_step,
      (
        source_step,
      ),
    )
  ]

  while (
    stack
    and len(
      result
    )
    < max_paths
  ):
    current, path = stack.pop()

    if current is root:
      result.append(
        path
      )
      continue

    path_ids = {
      id(
        step
      )
      for step in path
    }

    for child in children.get(
      id(
        current
      ),
      (),
    ):
      if id(
        child
      ) in path_ids:
        continue

      stack.append(
        (
          child,
          (
            *path,
            child,
          ),
        )
      )

  return tuple(
    result
  )


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
    entries, _ = exclude_toda_group_proof_narrative_root_reference(
      entries,
      empty_lines,
      presentation.root_step,
    )

    frontier_step_ids = (
      _toda_group_proof_narrative_reference_frontier_step_ids(
        presentation,
        entries,
      )
    )
    internal_step_ids = (
      _toda_group_proof_narrative_reference_internal_step_ids(
        presentation,
        entries,
      )
    )

    toda52_entries = tuple(
      entry
      for entry in entries
      if entry.reference.locator == "(5.2)"
    )

    lines.append(
      "=" * 94
    )
    lines.append(
      "DEPTH "
      + str(
        depth
      )
    )
    lines.append(
      "=" * 94
    )
    lines.append(
      "(5.2) entries: "
      + str(
        len(
          toda52_entries
        )
      )
    )

    for entry_index, entry in enumerate(
      toda52_entries,
      start=1,
    ):
      lines.append(
        ""
      )
      lines.append(
        "ENTRY "
        + str(
          entry_index
        )
        + " number="
        + str(
          entry.number
        )
      )

      for step_index, step in enumerate(
        entry.proof_steps,
        start=1,
      ):
        lines.append(
          "  STEP "
          + str(
            step_index
          )
        )
        lines.append(
          "    id="
          + str(
            id(
              step
            )
          )
        )
        lines.append(
          "    rule="
          + str(
            (
              step.inference_rule.name
              if step.inference_rule is not None
              else None
            )
          )
        )
        lines.append(
          "    rendered="
          + str(
            _render_generic_narrative_step(
              step
            )
          )
        )
        lines.append(
          "    frontier="
          + str(
            id(
              step
            )
            in frontier_step_ids
          )
        )
        lines.append(
          "    internal="
          + str(
            id(
              step
            )
            in internal_step_ids
          )
        )

        consumers = tuple(
          edge.parent_step
          for edge in presentation.edges
          if edge.premise_step is step
        )

        lines.append(
          "    direct_consumers="
          + str(
            len(
              consumers
            )
          )
        )

        for consumer_index, consumer in enumerate(
          consumers,
          start=1,
        ):
          lines.append(
            "      consumer "
            + str(
              consumer_index
            )
            + ": ref="
            + str(
              _ref(
                consumer
              )
            )
            + " rule="
            + str(
              (
                consumer.inference_rule.name
                if consumer.inference_rule is not None
                else None
              )
            )
            + " rendered="
            + str(
              _render_generic_narrative_step(
                consumer
              )
            )
          )

        paths = _all_paths_to_root(
          presentation,
          step,
        )

        lines.append(
          "    root_paths="
          + str(
            len(
              paths
            )
          )
        )

        for path_index, path in enumerate(
          paths,
          start=1,
        ):
          lines.append(
            "      PATH "
            + str(
              path_index
            )
          )
          for path_step_index, path_step in enumerate(
            path,
            start=1,
          ):
            lines.append(
              "        ["
              + str(
                path_step_index
              )
              + "] ref="
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

  output_path = Path(
    "phase156_r5_repair12_toda52_path_diagnostic.txt"
  )
  output_path.write_text(
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
