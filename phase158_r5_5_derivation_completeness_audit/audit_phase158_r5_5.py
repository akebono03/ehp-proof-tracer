from pathlib import Path
import csv
import re
import sys

AUDIT_DIR = Path(__file__).resolve().parent
REPO_ROOT = AUDIT_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(REPO_ROOT),
  )

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
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
  build_complete_toda_group_result_proof_replay,
)


AUDIT_TARGETS = (
  ("pi6_3_reference", 3, 3),
  ("pi8_5_former_dedicated", 5, 3),
  ("pi15_8_former_dedicated", 8, 7),
  ("pi7_4_former_legacy", 4, 3),
  ("pi10_4_generic", 4, 6),
  ("pi11_4_prose_target", 4, 7),
  ("pi12_5_generic", 5, 7),
  ("pi16_9_generic", 9, 7),
  ("pi4_3_small_unstable", 3, 1),
)

USE_MARKERS = (
  "を用いる.",
  "を用いる。",
)
CONNECTOR_ONLY = (
  "これらより,",
  "これらより、",
  "以上より,",
  "以上より、",
  "したがって,",
  "したがって、",
  "このことから,",
  "このことから、",
  "これより,",
  "これより、",
)

MATH_RE = re.compile(
  r"\$[^$]+\$|\\\[|\\\]"
)


def _presentation(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = (
    build_complete_toda_group_result_proof_replay(
      group_result
    )
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )


def _proof_body(
  markdown: str,
) -> str:
  marker = "## 証明"
  index = markdown.find(
    marker
  )

  if index < 0:
    return markdown

  return markdown[
    index
    + len(
      marker
    ):
  ]


def _nonempty_lines(
  text: str,
):
  return tuple(
    (
      line_number,
      line.strip(),
    )
    for line_number, line in enumerate(
      text.splitlines(),
      start=1,
    )
    if line.strip()
  )


def _visible_step_lines(
  presentation,
  body: str,
):
  matches = []

  for node in presentation.nodes:
    proof_step = node.proof_step
    rendered = _render_generic_narrative_step(
      proof_step
    )

    if not rendered:
      continue

    if rendered not in body:
      continue

    matches.append(
      (
        proof_step,
        rendered,
      )
    )

  return tuple(
    matches
  )


def _consumer_steps(
  presentation,
  proof_step,
):
  return tuple(
    edge.parent_step
    for edge in presentation.edges
    if edge.premise_step is proof_step
  )


def _visible_consumer_facts(
  presentation,
  proof_step,
  body: str,
):
  visible = []

  for consumer in _consumer_steps(
    presentation,
    proof_step,
  ):
    rendered = _render_generic_narrative_step(
      consumer
    )

    if (
      rendered
      and rendered in body
    ):
      visible.append(
        rendered
      )

  return tuple(
    visible
  )


def _classify_use_line(
  presentation,
  proof_step,
  rendered_line: str,
  body: str,
):
  consumers = _consumer_steps(
    presentation,
    proof_step,
  )
  visible_consumers = _visible_consumer_facts(
    presentation,
    proof_step,
    body,
  )

  if visible_consumers:
    return (
      "VISIBLE_DERIVATION",
      len(
        consumers
      ),
      visible_consumers,
    )

  if consumers:
    return (
      "RENDERER_VISIBILITY_GAP",
      len(
        consumers
      ),
      (),
    )

  return (
    "NO_CONSUMER_IN_PROOF_GRAPH",
    0,
    (),
  )


def _standalone_connector_findings(
  body: str,
):
  lines = _nonempty_lines(
    body
  )
  findings = []

  for index, (
    line_number,
    line,
  ) in enumerate(
    lines
  ):
    if line not in CONNECTOR_ONLY:
      continue

    next_line = (
      None
      if index + 1 >= len(
        lines
      )
      else lines[
        index + 1
      ][
        1
      ]
    )

    if (
      next_line is None
      or next_line.startswith(
        "#"
      )
      or next_line in CONNECTOR_ONLY
      or next_line in (
        "---",
        "□",
        r"$\square$",
      )
    ):
      findings.append(
        (
          line_number,
          line,
          next_line,
        )
      )

  return tuple(
    findings
  )


def _textual_use_findings(
  presentation,
  body: str,
):
  findings = []
  seen = set()

  for proof_step, rendered in _visible_step_lines(
    presentation,
    body,
  ):
    if not any(
      marker in rendered
      for marker in USE_MARKERS
    ):
      continue

    key = (
      id(
        proof_step
      ),
      rendered,
    )
    if key in seen:
      continue
    seen.add(
      key
    )

    (
      category,
      consumer_count,
      visible_consumers,
    ) = _classify_use_line(
      presentation,
      proof_step,
      rendered,
      body,
    )

    findings.append(
      (
        category,
        rendered,
        consumer_count,
        visible_consumers,
        type(
          proof_step.conclusion
        ).__name__,
      )
    )

  lines = _nonempty_lines(
    body
  )

  for line_number, line in lines:
    if not any(
      marker in line
      for marker in USE_MARKERS
    ):
      continue

    if any(
      line == rendered
      for _step, rendered in _visible_step_lines(
        presentation,
        body,
      )
    ):
      continue

    findings.append(
      (
        "UNMAPPED_RENDERED_USE",
        line,
        0,
        (),
        "",
      )
    )

  return tuple(
    findings
  )


def main() -> int:
  output_dir = (
    AUDIT_DIR
    / "audit_output"
  )
  rendered_dir = (
    output_dir
    / "rendered"
  )
  rendered_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  rows = []
  detail_lines = [
    "=" * 96,
    "Phase 158-R5-5 — derivation completeness audit",
    "=" * 96,
    "",
    "Production code changes: none",
    "Test code changes: none",
    "pytest: not run",
    "",
  ]
  exceptions = []
  category_counts = {}

  for label, n, k in AUDIT_TARGETS:
    try:
      presentation = _presentation(
        n,
        k,
      )
      markdown = (
        render_toda_group_proof_narrative_markdown(
          presentation
        )
      )
    except Exception as exc:
      exceptions.append(
        (
          label,
          n,
          k,
          type(
            exc
          ).__name__,
          str(
            exc
          ),
        )
      )
      continue

    body = _proof_body(
      markdown
    )
    use_findings = _textual_use_findings(
      presentation,
      body,
    )
    connector_findings = (
      _standalone_connector_findings(
        body
      )
    )

    rendered_path = (
      rendered_dir
      / f"{label}.md"
    )
    rendered_path.write_text(
      markdown,
      encoding="utf-8",
    )

    per_category = {}

    for (
      category,
      rendered,
      consumer_count,
      visible_consumers,
      statement_type,
    ) in use_findings:
      per_category[
        category
      ] = (
        per_category.get(
          category,
          0,
        )
        + 1
      )
      category_counts[
        category
      ] = (
        category_counts.get(
          category,
          0,
        )
        + 1
      )

    if connector_findings:
      per_category[
        "STANDALONE_CONNECTOR"
      ] = len(
        connector_findings
      )
      category_counts[
        "STANDALONE_CONNECTOR"
      ] = (
        category_counts.get(
          "STANDALONE_CONNECTOR",
          0,
        )
        + len(
          connector_findings
        )
      )

    rows.append(
      {
        "label": label,
        "n": n,
        "k": k,
        "group": (
          f"pi_{n + k}^{n}"
        ),
        "visible_derivation": per_category.get(
          "VISIBLE_DERIVATION",
          0,
        ),
        "renderer_visibility_gap": per_category.get(
          "RENDERER_VISIBILITY_GAP",
          0,
        ),
        "no_consumer_in_proof_graph": per_category.get(
          "NO_CONSUMER_IN_PROOF_GRAPH",
          0,
        ),
        "unmapped_rendered_use": per_category.get(
          "UNMAPPED_RENDERED_USE",
          0,
        ),
        "standalone_connector": per_category.get(
          "STANDALONE_CONNECTOR",
          0,
        ),
      }
    )

    detail_lines.extend(
      (
        "-" * 96,
        f"{label}: pi_{n + k}^{n}",
        "-" * 96,
        (
          "VISIBLE_DERIVATION: "
          f"{per_category.get('VISIBLE_DERIVATION', 0)}"
        ),
        (
          "RENDERER_VISIBILITY_GAP: "
          f"{per_category.get('RENDERER_VISIBILITY_GAP', 0)}"
        ),
        (
          "NO_CONSUMER_IN_PROOF_GRAPH: "
          f"{per_category.get('NO_CONSUMER_IN_PROOF_GRAPH', 0)}"
        ),
        (
          "UNMAPPED_RENDERED_USE: "
          f"{per_category.get('UNMAPPED_RENDERED_USE', 0)}"
        ),
        (
          "STANDALONE_CONNECTOR: "
          f"{per_category.get('STANDALONE_CONNECTOR', 0)}"
        ),
        "",
      )
    )

    for (
      category,
      rendered,
      consumer_count,
      visible_consumers,
      statement_type,
    ) in use_findings:
      detail_lines.extend(
        (
          f"[{category}]",
          f"statement_type: {statement_type}",
          f"consumer_count: {consumer_count}",
          f"rendered: {rendered}",
        )
      )

      if visible_consumers:
        detail_lines.append(
          "visible consumers:"
        )
        detail_lines.extend(
          f"  - {consumer}"
          for consumer in visible_consumers
        )

      detail_lines.append(
        ""
      )

    for (
      line_number,
      line,
      next_line,
    ) in connector_findings:
      detail_lines.extend(
        (
          "[STANDALONE_CONNECTOR]",
          f"line: {line_number}",
          f"connector: {line}",
          f"next: {next_line}",
          "",
        )
      )

  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  with (
    output_dir
    / "summary.csv"
  ).open(
    "w",
    encoding="utf-8-sig",
    newline="",
  ) as handle:
    fieldnames = (
      list(
        rows[
          0
        ].keys()
      )
      if rows
      else [
        "label",
        "n",
        "k",
        "group",
      ]
    )
    writer = csv.DictWriter(
      handle,
      fieldnames=fieldnames,
    )
    writer.writeheader()
    writer.writerows(
      rows
    )

  with (
    output_dir
    / "exceptions.csv"
  ).open(
    "w",
    encoding="utf-8-sig",
    newline="",
  ) as handle:
    writer = csv.writer(
      handle
    )
    writer.writerow(
      (
        "label",
        "n",
        "k",
        "exception_type",
        "message",
      )
    )
    writer.writerows(
      exceptions
    )

  summary_lines = [
    "=" * 96,
    "Phase 158-R5-5 — derivation completeness audit",
    "=" * 96,
    f"targets: {len(AUDIT_TARGETS)}",
    f"rendered: {len(rows)}",
    f"exceptions: {len(exceptions)}",
    "",
    "Categories:",
  ]

  for category in (
    "VISIBLE_DERIVATION",
    "RENDERER_VISIBILITY_GAP",
    "NO_CONSUMER_IN_PROOF_GRAPH",
    "UNMAPPED_RENDERED_USE",
    "STANDALONE_CONNECTOR",
  ):
    summary_lines.append(
      "  "
      + category
      + ": "
      + str(
        category_counts.get(
          category,
          0,
        )
      )
    )

  summary_lines.extend(
    (
      "",
      "Interpretation:",
      (
        "  VISIBLE_DERIVATION = a visible 'use' premise has at least one "
        "visible direct consumer fact."
      ),
      (
        "  RENDERER_VISIBILITY_GAP = proof graph has a direct consumer, "
        "but that consumer fact is not visible in the rendered proof body."
      ),
      (
        "  NO_CONSUMER_IN_PROOF_GRAPH = visible 'use' statement has no "
        "direct consumer in the current proof graph."
      ),
      (
        "  UNMAPPED_RENDERED_USE = visible 'use' prose could not be mapped "
        "back to a generic proof step."
      ),
      (
        "  STANDALONE_CONNECTOR = connector prose has no following "
        "mathematical/conclusion line."
      ),
      "",
      "Boundary:",
      "  Audit only. No repair is performed.",
      (
        "  R5-5 classifies whether the next repair belongs to renderer "
        "visibility or proof/semantic data."
      ),
      (
        "  Repository-wide contract verification remains R5-6."
      ),
      "",
      "Output:",
      "  audit_output/summary.txt",
      "  audit_output/details.txt",
      "  audit_output/summary.csv",
      "  audit_output/exceptions.csv",
      "  audit_output/rendered/*.md",
      "=" * 96,
    )
  )

  (
    output_dir
    / "summary.txt"
  ).write_text(
    "\n".join(
      summary_lines
    )
    + "\n",
    encoding="utf-8",
  )
  (
    output_dir
    / "details.txt"
  ).write_text(
    "\n".join(
      detail_lines
    )
    + "\n",
    encoding="utf-8",
  )

  print(
    "\n".join(
      summary_lines
    )
  )

  return 1 if exceptions else 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
