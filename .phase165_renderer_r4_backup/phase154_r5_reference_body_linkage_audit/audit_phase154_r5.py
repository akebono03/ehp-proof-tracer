from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  extract_toda_group_proof_step_literature_reference,
  select_toda_group_proof_narrative_reference_statement_steps,
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


def build_pi11_4():
  report = build_standard_toda_report(
    n=4,
    k=7,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  raw_presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw_presentation
    )
  )

  return (
    raw_presentation,
    presentation,
  )


def reference_label(
  reference,
) -> str:
  if reference is None:
    return "None"

  for attribute in (
    "label",
    "title",
    "name",
  ):
    value = getattr(
      reference,
      attribute,
      None,
    )
    if isinstance(
      value,
      str,
    ) and value:
      return value

  return str(
    reference
  )


def selected_steps_for_entry(
  presentation,
  entry,
):
  candidate_steps = []
  seen = set()

  for proof_step in entry.proof_steps:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered:
      continue

    if rendered in seen:
      continue

    seen.add(
      rendered
    )
    candidate_steps.append(
      proof_step
    )

  return (
    select_toda_group_proof_narrative_reference_statement_steps(
      entry,
      tuple(
        candidate_steps
      ),
      presentation.edges,
      root_step=presentation.root_step,
    )
  )


def direct_consumers(
  presentation,
  proof_step,
):
  return tuple(
    edge.parent_step
    for edge in presentation.edges
    if edge.premise_step is proof_step
  )


def reaches_root(
  presentation,
  start_step,
) -> bool:
  children = defaultdict(
    list
  )

  for edge in presentation.edges:
    children[
      id(
        edge.premise_step
      )
    ].append(
      edge.parent_step
    )

  root_id = id(
    presentation.root_step
  )
  queue = deque(
    [
      start_step,
    ]
  )
  visited = set()

  while queue:
    current = queue.popleft()
    current_id = id(
      current
    )

    if current_id in visited:
      continue

    visited.add(
      current_id
    )

    if current_id == root_id:
      return True

    queue.extend(
      children.get(
        current_id,
        (),
      )
    )

  return False


def shortest_path_to_root(
  presentation,
  start_step,
):
  children = defaultdict(
    list
  )

  for edge in presentation.edges:
    children[
      id(
        edge.premise_step
      )
    ].append(
      edge.parent_step
    )

  root = presentation.root_step
  root_id = id(
    root
  )
  queue = deque(
    [
      (
        start_step,
        (
          start_step,
        ),
      ),
    ]
  )
  visited = set()

  while queue:
    current, path = queue.popleft()
    current_id = id(
      current
    )

    if current_id in visited:
      continue

    visited.add(
      current_id
    )

    if current_id == root_id:
      return path

    for child in children.get(
      current_id,
      (),
    ):
      queue.append(
        (
          child,
          (
            *path,
            child,
          ),
        )
      )

  return ()


def render_step_record(
  proof_step,
) -> tuple[
  str,
  str,
  str,
]:
  rendered = (
    _render_generic_narrative_step(
      proof_step
    )
  )
  statement_type = type(
    proof_step.conclusion
  ).__name__
  reference = (
    extract_toda_group_proof_step_literature_reference(
      proof_step
    )
  )

  return (
    statement_type,
    rendered,
    reference_label(
      reference
    ),
  )


def main() -> int:
  (
    raw_presentation,
    presentation,
  ) = build_pi11_4()

  rendered_public = (
    render_toda_group_proof_narrative_markdown(
      raw_presentation
    )
  )
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  statement_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      entries,
    )
  )
  (
    entries,
    statement_lines,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      entries,
      statement_lines,
      presentation.root_step,
    )
  )

  output_dir = (
    Path(__file__).resolve().parent
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  lines = [
    "# Phase 154-R5 — Reference ↔ proof body linkage audit",
    "",
    "Production changes: none.",
    "",
    "Target:",
    "- group: $\\pi_{11}^{4}$",
    "- view: Narrative",
    "- depth: 2",
    "",
    "## Public Narrative",
    "",
    rendered_public.rstrip(),
    "",
    "## Reference graph audit",
    "",
  ]

  for entry in entries:
    marker = (
      "[R"
      + str(
        entry.number
      )
      + "]"
    )
    lines.extend(
      (
        f"### {marker}",
        "",
        (
          "- literature reference: `"
          + reference_label(
            entry.reference
          )
          + "`"
        ),
        "- selected reference statements:",
        "",
      )
    )

    selected_steps = selected_steps_for_entry(
      presentation,
      entry,
    )

    for selected_index, selected_step in enumerate(
      selected_steps,
      start=1,
    ):
      (
        statement_type,
        rendered_statement,
        step_reference,
      ) = render_step_record(
        selected_step
      )
      consumers = direct_consumers(
        presentation,
        selected_step,
      )
      path = shortest_path_to_root(
        presentation,
        selected_step,
      )

      lines.extend(
        (
          f"#### selected step {selected_index}",
          "",
          f"- statement type: `{statement_type}`",
          (
            "- rendered statement: `"
            + rendered_statement.replace(
              "`",
              r"\`",
            )
            + "`"
          ),
          f"- own reference: `{step_reference}`",
          f"- direct consumer count: {len(consumers)}",
          f"- reaches root: {reaches_root(presentation, selected_step)}",
          "",
          "Direct consumers:",
          "",
        )
      )

      if not consumers:
        lines.append(
          "- none"
        )

      for consumer_index, consumer in enumerate(
        consumers,
        start=1,
      ):
        (
          consumer_type,
          consumer_rendered,
          consumer_reference,
        ) = render_step_record(
          consumer
        )
        lines.extend(
          (
            (
              "- "
              + str(
                consumer_index
              )
              + ". "
              + consumer_type
            ),
            (
              "  - rendered: `"
              + consumer_rendered.replace(
                "`",
                r"\`",
              )
              + "`"
            ),
            (
              "  - literature reference: `"
              + consumer_reference
              + "`"
            ),
          )
        )

      lines.extend(
        (
          "",
          "Shortest selected-step → root path:",
          "",
        )
      )

      if not path:
        lines.append(
          "- none"
        )

      for path_index, path_step in enumerate(
        path,
        start=1,
      ):
        (
          path_type,
          path_rendered,
          path_reference,
        ) = render_step_record(
          path_step
        )
        lines.extend(
          (
            (
              "- "
              + str(
                path_index
              )
              + ". `"
              + path_type
              + "`"
            ),
            (
              "  - rendered: `"
              + path_rendered.replace(
                "`",
                r"\`",
              )
              + "`"
            ),
            (
              "  - literature reference: `"
              + path_reference
              + "`"
            ),
          )
        )

      lines.append("")

  lines.extend(
    (
      "## Statement lines used in the public Reference section",
      "",
    )
  )

  for number, reference_lines in statement_lines.items():
    lines.append(
      f"### [R{number}]"
    )
    lines.append("")

    for reference_line in reference_lines:
      lines.append(
        "- `"
        + reference_line.replace(
          "`",
          r"\`",
        )
        + "`"
      )

    lines.append("")

  lines.extend(
    (
      "## Decision rule for R5 implementation",
      "",
      (
        "- Do not generate linkage from line adjacency alone."
      ),
      (
        "- Use the selected reference step and its graph consumer/path "
        "to identify the mathematical fact that the Reference supports."
      ),
      (
        "- If the selected step has a unique proof path to a visible "
        "consumer, render the Reference marker as support for that fact."
      ),
      (
        "- If graph ownership is ambiguous, keep the existing neutral "
        "`[R#]を用いる。` form rather than inventing a relation."
      ),
      (
        "- R5 must remain generic; no pi11_4-specific branch."
      ),
      "",
    )
  )

  report_path = (
    output_dir
    / "phase154_r5_reference_body_linkage_audit.md"
  )
  report_path.write_text(
    "\n".join(
      lines
    ),
    encoding="utf-8",
  )

  print(
    "# Phase 154-R5 Reference linkage audit"
  )
  print(
    "references:",
    len(
      entries
    ),
  )

  for entry in entries:
    selected_steps = selected_steps_for_entry(
      presentation,
      entry,
    )
    print(
      "[R"
      + str(
        entry.number
      )
      + "]",
      "selected_steps=",
      len(
        selected_steps
      ),
    )

    for selected_step in selected_steps:
      print(
        "  selected:",
        _render_generic_narrative_step(
          selected_step
        ),
      )
      print(
        "  direct_consumers:",
        len(
          direct_consumers(
            presentation,
            selected_step,
          )
        ),
      )
      path = shortest_path_to_root(
        presentation,
        selected_step,
      )
      print(
        "  path_to_root_length:",
        len(
          path
        ),
      )

      for path_step in path:
        print(
          "    ->",
          type(
            path_step.conclusion
          ).__name__,
          ":",
          _render_generic_narrative_step(
            path_step
          ),
        )

  print(
    "Report:",
    report_path,
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
