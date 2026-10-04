from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

from proof import (
  Relation,
  RelationType,
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
  build_toda_group_result_proof_replay,
)


OUTPUT_DIR = (
  Path(__file__).resolve().parent
  / "audit_output"
)

FRAGMENT_PARAGRAPHS = {
  "である.",
  "を得る.",
  "を用いる.",
  "となる.",
}


def render_group(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
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
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      raw
    )
  )

  return (
    raw,
    presentation,
    rendered,
  )


def public_body(
  rendered: str,
) -> str:
  if "\n## 証明\n" in rendered:
    return rendered.split(
      "\n## 証明\n",
      1,
    )[1]

  if rendered.startswith(
    "# Group proof narrative"
  ):
    return rendered.split(
      "\n",
      1,
    )[
      1
    ]

  return rendered


def normalized_statement_text(
  rendered_step: str,
) -> str:
  return (
    rendered_step
    .strip()
    .rstrip(
      ".,"
    )
  )


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  rows = []
  summary = Counter()
  exceptions = []

  for n in range(
    2,
    16,
  ):
    for k in range(
      0,
      8,
    ):
      label = (
        f"pi_{n + k}^{n}"
      )

      try:
        (
          raw,
          presentation,
          rendered,
        ) = render_group(
          n,
          k,
        )
      except Exception as exc:
        exceptions.append(
          {
            "n": n,
            "k": k,
            "group": label,
            "exception_type": type(
              exc
            ).__name__,
            "message": str(
              exc
            ),
          }
        )
        continue

      body = public_body(
        rendered
      )
      paragraphs = tuple(
        paragraph.strip()
        for paragraph in body.split(
          "\n\n"
        )
        if paragraph.strip()
      )

      for index, paragraph in enumerate(
        paragraphs
      ):
        if paragraph in FRAGMENT_PARAGRAPHS:
          rows.append(
            {
              "n": n,
              "k": k,
              "group": label,
              "kind": "isolated_sentence_fragment",
              "detail": (
                f"paragraph={index}: "
                f"{paragraph}"
              ),
            }
          )
          summary[
            "isolated_sentence_fragment"
          ] += 1

      for node in presentation.nodes:
        step = node.proof_step
        conclusion = step.conclusion

        if (
          not isinstance(
            conclusion,
            Relation,
          )
          or conclusion.relation_type
          is not RelationType.EQUALITY
          or conclusion.lhs
          != conclusion.rhs
        ):
          continue

        rendered_step = (
          _render_generic_narrative_step(
            step
          )
        )

        if (
          rendered_step
          and normalized_statement_text(
            rendered_step
          )
          in normalized_statement_text(
            body
          )
        ):
          rows.append(
            {
              "n": n,
              "k": k,
              "group": label,
              "kind": "visible_reflexive_equality",
              "detail": rendered_step,
            }
          )
          summary[
            "visible_reflexive_equality"
          ] += 1

      root_rendered = (
        _render_generic_narrative_step(
          presentation.root_step
        )
      )

      if root_rendered:
        root_key = normalized_statement_text(
          root_rendered
        )

        occurrences = (
          normalized_statement_text(
            body
          )
          .count(
            root_key
          )
        )

        if occurrences > 1:
          rows.append(
            {
              "n": n,
              "k": k,
              "group": label,
              "kind": "root_statement_repeated",
              "detail": (
                f"count={occurrences}: "
                f"{root_rendered}"
              ),
            }
          )
          summary[
            "root_statement_repeated"
          ] += 1

  with (
    OUTPUT_DIR
    / "findings.csv"
  ).open(
    "w",
    encoding="utf-8",
    newline="",
  ) as handle:
    writer = csv.DictWriter(
      handle,
      fieldnames=(
        "n",
        "k",
        "group",
        "kind",
        "detail",
      ),
    )
    writer.writeheader()
    writer.writerows(
      rows
    )

  with (
    OUTPUT_DIR
    / "exceptions.csv"
  ).open(
    "w",
    encoding="utf-8",
    newline="",
  ) as handle:
    writer = csv.DictWriter(
      handle,
      fieldnames=(
        "n",
        "k",
        "group",
        "exception_type",
        "message",
      ),
    )
    writer.writeheader()
    writer.writerows(
      exceptions
    )

  report_lines = [
    "=" * 96,
    "Phase157-R20 repair51 - residual display defect audit",
    "=" * 96,
    "Production code changes: none",
    "pytest: not run",
    "Scope: 112 groups, depth 2",
    "",
    f"exceptions: {len(exceptions)}",
    f"findings: {len(rows)}",
    "",
    "Finding counts:",
  ]

  if summary:
    for kind, count in sorted(
      summary.items()
    ):
      report_lines.append(
        f"  {kind}: {count}"
      )
  else:
    report_lines.append(
      "  none"
    )

  report_lines.append(
    ""
  )
  report_lines.append(
    "Findings:"
  )

  for row in rows:
    report_lines.append(
      f"  {row['group']} | "
      f"{row['kind']} | "
      f"{row['detail']}"
    )

  report = "\n".join(
    report_lines
  )

  (
    OUTPUT_DIR
    / "report.txt"
  ).write_text(
    report
    + "\n",
    encoding="utf-8",
    newline="\n",
  )

  print(
    report
  )
  print("")
  print(
    "Output:"
  )
  print(
    "  audit_output/findings.csv"
  )
  print(
    "  audit_output/exceptions.csv"
  )
  print(
    "  audit_output/report.txt"
  )
  print("")
  print(
    "AUDIT COMPLETE"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
