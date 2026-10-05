from __future__ import annotations

from pathlib import Path
import csv
import re
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = PACKAGE_DIR.parent

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
)


CONNECTOR_ONLY = (
  "まず,",
  "次に,",
  "したがって,",
  "以上より,",
  "これより,",
  "このことから,",
  "これらより,",
  "一方,",
  "また,",
  "よって,",
)

TAG_RE = re.compile(
  r"\\tag\{\d+\}"
)
WHITESPACE_RE = re.compile(
  r"\s+"
)


def _canonical_visible_text(
  text: str,
) -> str:
  if not isinstance(
    text,
    str,
  ):
    raise TypeError(
      "text must be a str"
    )

  normalized = text.strip()
  normalized = normalized.replace(
    "**",
    "",
  )
  normalized = normalized.replace(
    "$",
    "",
  )
  normalized = TAG_RE.sub(
    "",
    normalized,
  )
  normalized = WHITESPACE_RE.sub(
    " ",
    normalized,
  )

  return normalized.strip()


def _web_text(
  n: int,
  k: int,
) -> str:
  view = build_standard_web_group_proof_view(
    n,
    k,
    max_depth=2,
    mode="narrative",
  )
  lines = []

  for line in view.rendered_lines:
    if line.segments:
      lines.append(
        "".join(
          segment.value
          for segment in line.segments
        )
      )
      continue

    lines.append(
      line.prefix
      + (
        ""
        if line.statement_latex is None
        else line.statement_latex
      )
      + line.suffix
    )

  return "\n".join(
    lines
  )


def _proof_body(
  text: str,
) -> str:
  lines = text.splitlines()

  try:
    proof_index = lines.index(
      "証明"
    )
  except ValueError:
    return text

  return "\n".join(
    lines[
      proof_index + 1:
    ]
  )


def _nonempty_lines(
  text: str,
) -> tuple[
  tuple[
    int,
    str,
  ],
  ...,
]:
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


def _line_positions(
  text: str,
  needle: str,
) -> tuple[
  int,
  ...,
]:
  canonical_needle = (
    _canonical_visible_text(
      needle
    )
  )

  if not canonical_needle:
    return ()

  positions = []

  for line_number, line in _nonempty_lines(
    text
  ):
    canonical_line = (
      _canonical_visible_text(
        line
      )
    )

    if canonical_needle in canonical_line:
      positions.append(
        line_number
      )

  return tuple(
    positions
  )


def _paragraphs(
  text: str,
) -> tuple[
  str,
  ...,
]:
  return tuple(
    paragraph.strip()
    for paragraph in re.split(
      r"\n\s*\n",
      text,
    )
    if paragraph.strip()
  )


def _transition_findings_from_paragraphs(
  paragraphs: tuple[
    str,
    ...,
  ],
) -> tuple[
  tuple[
    int,
    str,
    str | None,
  ],
  ...,
]:
  findings = []

  for index, paragraph in enumerate(
    paragraphs
  ):
    canonical_paragraph = (
      _canonical_visible_text(
        paragraph
      )
    )

    if canonical_paragraph not in CONNECTOR_ONLY:
      continue

    next_paragraph = (
      None
      if index + 1 >= len(
        paragraphs
      )
      else paragraphs[
        index + 1
      ]
    )
    canonical_next = (
      None
      if next_paragraph is None
      else _canonical_visible_text(
        next_paragraph
      )
    )

    if (
      canonical_next is None
      or canonical_next
      in CONNECTOR_ONLY
      or canonical_next == "□"
      or canonical_next.startswith(
        "## "
      )
    ):
      findings.append(
        (
          index,
          paragraph,
          next_paragraph,
        )
      )

  return tuple(
    findings
  )


def _interval_crosses(
  first: tuple[
    int,
    int,
  ],
  second: tuple[
    int,
    int,
  ],
) -> bool:
  first_start, first_end = first
  second_start, second_end = second

  return (
    first_start
    < second_start
    <= first_end
    < second_end
    or second_start
    < first_start
    <= second_end
    < first_end
  )


def _argument_is_ancestor(
  arguments,
  ancestor_index: int,
  descendant_index: int,
) -> bool:
  pending = list(
    arguments[
      ancestor_index
    ].child_argument_indices
  )
  visited = set()

  while pending:
    current = pending.pop()

    if current in visited:
      continue

    visited.add(
      current
    )

    if current == descendant_index:
      return True

    pending.extend(
      arguments[
        current
      ].child_argument_indices
    )

  return False


def _duplicate_visible_conclusions(
  body: str,
  conclusion_texts: tuple[
    tuple[
      int,
      str,
    ],
    ...,
  ],
) -> tuple[
  tuple[
    int,
    str,
    tuple[
      int,
      ...,
    ],
  ],
  ...,
]:
  findings = []

  for argument_index, conclusion_text in conclusion_texts:
    positions = _line_positions(
      body,
      conclusion_text,
    )

    if len(
      positions
    ) <= 1:
      continue

    findings.append(
      (
        argument_index,
        conclusion_text,
        positions,
      )
    )

  return tuple(
    findings
  )


def _presentation_data(
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
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=semantic_sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=semantic_sidecar,
  )

  return (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
  )


def _visible_argument_intervals(
  presentation,
  semantic_sidecar,
  blocks,
  arguments,
  body: str,
):
  block_index_by_id = {
    id(
      block
    ): index
    for index, block in enumerate(
      blocks
    )
  }
  records = []

  for argument_index, argument in enumerate(
    arguments
  ):
    local_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )
    visible_positions = []
    visible_steps = []

    for block in local_blocks:
      for step in block.steps:
        rendered = _render_generic_narrative_step(
          step
        )

        if not rendered:
          continue

        positions = _line_positions(
          body,
          rendered,
        )

        if not positions:
          continue

        visible_positions.extend(
          positions
        )
        visible_steps.append(
          (
            block_index_by_id[
              id(
                block
              )
            ],
            rendered,
            positions,
          )
        )

    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )
    conclusion_rendered = (
      None
      if conclusion_step is None
      else _render_generic_narrative_step(
        conclusion_step
      )
    )
    conclusion_positions = (
      ()
      if not conclusion_rendered
      else _line_positions(
        body,
        conclusion_rendered,
      )
    )

    if conclusion_positions:
      visible_positions.extend(
        conclusion_positions
      )

    interval = (
      None
      if not visible_positions
      else (
        min(
          visible_positions
        ),
        max(
          visible_positions
        ),
      )
    )

    records.append(
      {
        "argument_index": argument_index,
        "role": argument.role.name,
        "interval": interval,
        "visible_steps": tuple(
          visible_steps
        ),
        "conclusion_rendered": (
          conclusion_rendered
        ),
        "conclusion_positions": (
          conclusion_positions
        ),
        "child_argument_indices": (
          argument.child_argument_indices
        ),
      }
    )

  return tuple(
    records
  )


def _argument_interval_findings(
  arguments,
  records,
):
  findings = []

  for first_index in range(
    len(
      records
    )
  ):
    first = records[
      first_index
    ]

    if first[
      "interval"
    ] is None:
      continue

    for second_index in range(
      first_index + 1,
      len(
        records
      ),
    ):
      second = records[
        second_index
      ]

      if second[
        "interval"
      ] is None:
        continue

      if _argument_is_ancestor(
        arguments,
        first_index,
        second_index,
      ):
        continue

      if _argument_is_ancestor(
        arguments,
        second_index,
        first_index,
      ):
        continue

      if not _interval_crosses(
        first[
          "interval"
        ],
        second[
          "interval"
        ],
      ):
        continue

      findings.append(
        (
          first_index,
          first[
            "interval"
          ],
          second_index,
          second[
            "interval"
          ],
        )
      )

  return tuple(
    findings
  )


def _target_qed_finding(
  body: str,
  root_text: str | None,
):
  lines = _nonempty_lines(
    body
  )

  if not lines:
    return (
      "EMPTY_PROOF_BODY",
      None,
      None,
    )

  qed_positions = tuple(
    line_number
    for line_number, line in lines
    if _canonical_visible_text(
      line
    ) == "□"
  )

  if len(
    qed_positions
  ) != 1:
    return (
      "QED_COUNT",
      qed_positions,
      None,
    )

  qed_line = qed_positions[
    0
  ]

  if (
    _canonical_visible_text(
      lines[
        -1
      ][
        1
      ]
    )
    != "□"
  ):
    return (
      "QED_NOT_TERMINAL",
      qed_line,
      lines[
        -1
      ],
    )

  if root_text:
    root_positions = _line_positions(
      body,
      root_text,
    )

    if not root_positions:
      return (
        "ROOT_TARGET_NOT_VISIBLE",
        root_text,
        qed_line,
      )

    if root_positions[
      -1
    ] >= qed_line:
      return (
        "ROOT_TARGET_NOT_BEFORE_QED",
        root_positions,
        qed_line,
      )

  return None


def main() -> int:
  output_dir = (
    PACKAGE_DIR
    / "audit_output"
  )
  context_dir = (
    output_dir
    / "contexts"
  )
  context_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  group_rows = []
  argument_rows = []
  transition_rows = []
  duplicate_rows = []
  target_rows = []
  exceptions = []

  total_arguments = 0
  total_visible_argument_intervals = 0

  for n in range(
    2,
    16,
  ):
    for k in range(
      0,
      8,
    ):
      group = (
        f"pi_{n + k}^{n}"
      )

      try:
        (
          presentation,
          semantic_sidecar,
          blocks,
          arguments,
        ) = _presentation_data(
          n,
          k,
        )
        text = _web_text(
          n,
          k,
        )
        body = _proof_body(
          text
        )

        records = _visible_argument_intervals(
          presentation,
          semantic_sidecar,
          blocks,
          arguments,
          body,
        )
        interval_findings = (
          _argument_interval_findings(
            arguments,
            records,
          )
        )
        transition_findings = (
          _transition_findings_from_paragraphs(
            _paragraphs(
              body
            )
          )
        )

        conclusion_texts = tuple(
          (
            record[
              "argument_index"
            ],
            record[
              "conclusion_rendered"
            ],
          )
          for record in records
          if record[
            "conclusion_rendered"
          ]
        )
        duplicate_findings = (
          _duplicate_visible_conclusions(
            body,
            conclusion_texts,
          )
        )

        root_rendered = _render_generic_narrative_step(
          presentation.root_step
        )
        target_finding = (
          _target_qed_finding(
            body,
            root_rendered,
          )
        )

        total_arguments += len(
          arguments
        )
        visible_interval_count = sum(
          record[
            "interval"
          ] is not None
          for record in records
        )
        total_visible_argument_intervals += (
          visible_interval_count
        )

        for (
          first_index,
          first_interval,
          second_index,
          second_interval,
        ) in interval_findings:
          argument_rows.append(
            {
              "n": n,
              "k": k,
              "group": group,
              "first_argument": (
                first_index
              ),
              "first_interval": (
                repr(
                  first_interval
                )
              ),
              "second_argument": (
                second_index
              ),
              "second_interval": (
                repr(
                  second_interval
                )
              ),
              "classification": (
                "CROSSING_VISIBLE_ARGUMENT_INTERVALS"
              ),
            }
          )

        for (
          paragraph_index,
          connector,
          next_paragraph,
        ) in transition_findings:
          transition_rows.append(
            {
              "n": n,
              "k": k,
              "group": group,
              "paragraph_index": (
                paragraph_index
              ),
              "connector": connector,
              "next_paragraph": (
                ""
                if next_paragraph is None
                else next_paragraph
              ),
              "classification": (
                "DANGLING_TRANSITION"
              ),
            }
          )

        for (
          argument_index,
          conclusion_text,
          positions,
        ) in duplicate_findings:
          duplicate_rows.append(
            {
              "n": n,
              "k": k,
              "group": group,
              "argument_index": (
                argument_index
              ),
              "positions": repr(
                positions
              ),
              "conclusion": (
                conclusion_text
              ),
              "classification": (
                "REPEATED_VISIBLE_ARGUMENT_CONCLUSION"
              ),
            }
          )

        if target_finding is not None:
          target_rows.append(
            {
              "n": n,
              "k": k,
              "group": group,
              "classification": (
                target_finding[
                  0
                ]
              ),
              "detail_1": repr(
                target_finding[
                  1
                ]
              ),
              "detail_2": repr(
                target_finding[
                  2
                ]
              ),
            }
          )

        group_rows.append(
          {
            "n": n,
            "k": k,
            "group": group,
            "arguments": len(
              arguments
            ),
            "visible_argument_intervals": (
              visible_interval_count
            ),
            "argument_interval_findings": (
              len(
                interval_findings
              )
            ),
            "transition_findings": (
              len(
                transition_findings
              )
            ),
            "duplicate_conclusion_findings": (
              len(
                duplicate_findings
              )
            ),
            "target_qed_findings": (
              0
              if target_finding is None
              else 1
            ),
          }
        )

        (
          context_dir
          / f"{group}.txt"
        ).write_text(
          "\n".join(
            (
              f"group: {group}",
              f"n={n} k={k}",
              f"arguments={len(arguments)}",
              (
                "visible_argument_intervals="
                + str(
                  visible_interval_count
                )
              ),
              (
                "argument_interval_findings="
                + str(
                  len(
                    interval_findings
                  )
                )
              ),
              (
                "transition_findings="
                + str(
                  len(
                    transition_findings
                  )
                )
              ),
              (
                "duplicate_conclusion_findings="
                + str(
                  len(
                    duplicate_findings
                  )
                )
              ),
              (
                "target_qed_finding="
                + repr(
                  target_finding
                )
              ),
              "",
              "ARGUMENT RECORDS",
              *(
                (
                  "A"
                  + str(
                    record[
                      "argument_index"
                    ]
                  )
                  + " role="
                  + record[
                    "role"
                  ]
                  + " interval="
                  + repr(
                    record[
                      "interval"
                    ]
                  )
                  + " conclusion_positions="
                  + repr(
                    record[
                      "conclusion_positions"
                    ]
                  )
                  + " conclusion="
                  + repr(
                    record[
                      "conclusion_rendered"
                    ]
                  )
                )
                for record in records
              ),
              "",
              "PUBLIC PROOF BODY",
              body,
            )
          )
          + "\n",
          encoding="utf-8",
        )

      except Exception as exc:
        exceptions.append(
          {
            "n": n,
            "k": k,
            "group": group,
            "exception_type": (
              type(
                exc
              ).__name__
            ),
            "message": str(
              exc
            ),
          }
        )

  def write_csv(
    name: str,
    rows,
    fieldnames,
  ) -> None:
    with (
      output_dir
      / name
    ).open(
      "w",
      encoding="utf-8-sig",
      newline="",
    ) as handle:
      writer = csv.DictWriter(
        handle,
        fieldnames=fieldnames,
      )
      writer.writeheader()
      writer.writerows(
        rows
      )

  write_csv(
    "groups.csv",
    group_rows,
    (
      "n",
      "k",
      "group",
      "arguments",
      "visible_argument_intervals",
      "argument_interval_findings",
      "transition_findings",
      "duplicate_conclusion_findings",
      "target_qed_findings",
    ),
  )
  write_csv(
    "argument_interval_findings.csv",
    argument_rows,
    (
      "n",
      "k",
      "group",
      "first_argument",
      "first_interval",
      "second_argument",
      "second_interval",
      "classification",
    ),
  )
  write_csv(
    "transition_findings.csv",
    transition_rows,
    (
      "n",
      "k",
      "group",
      "paragraph_index",
      "connector",
      "next_paragraph",
      "classification",
    ),
  )
  write_csv(
    "duplicate_conclusion_findings.csv",
    duplicate_rows,
    (
      "n",
      "k",
      "group",
      "argument_index",
      "positions",
      "conclusion",
      "classification",
    ),
  )
  write_csv(
    "target_qed_findings.csv",
    target_rows,
    (
      "n",
      "k",
      "group",
      "classification",
      "detail_1",
      "detail_2",
    ),
  )
  write_csv(
    "exceptions.csv",
    exceptions,
    (
      "n",
      "k",
      "group",
      "exception_type",
      "message",
    ),
  )

  groups_with_findings = sum(
    (
      row[
        "argument_interval_findings"
      ]
      + row[
        "transition_findings"
      ]
      + row[
        "duplicate_conclusion_findings"
      ]
      + row[
        "target_qed_findings"
      ]
    )
    > 0
    for row in group_rows
  )

  summary_lines = [
    (
      "Phase 158-R5-5d repair1 — "
      "Web/Markdown representation normalization"
    ),
    "",
    "Scope:",
    (
      "  current historical audit corpus: "
      "n=2..15, k=0..7, Web Narrative depth=2"
    ),
    (
      "  NOTE: this coordinate window is an audit corpus only; "
      "it is NOT an architectural group-count contract."
    ),
    "",
    "Normalization applied only inside the audit harness:",
    (
      "  - remove Markdown $ delimiters"
    ),
    (
      "  - remove Markdown ** strong delimiters"
    ),
    (
      "  - ignore display-only equation tags \\\\tag{N}"
    ),
    (
      "  - collapse whitespace"
    ),
    (
      "  - preserve mathematical LaTeX and prose content"
    ),
    "",
    "Totals:",
    (
      "  audited coordinates: "
      + str(
        14
        * 8
      )
    ),
    (
      "  rendered: "
      + str(
        len(
          group_rows
        )
      )
    ),
    (
      "  exceptions: "
      + str(
        len(
          exceptions
        )
      )
    ),
    (
      "  arguments: "
      + str(
        total_arguments
      )
    ),
    (
      "  visible argument intervals: "
      + str(
        total_visible_argument_intervals
      )
    ),
    (
      "  crossing argument-interval findings: "
      + str(
        len(
          argument_rows
        )
      )
    ),
    (
      "  dangling-transition findings: "
      + str(
        len(
          transition_rows
        )
      )
    ),
    (
      "  repeated-conclusion findings: "
      + str(
        len(
          duplicate_rows
        )
      )
    ),
    (
      "  target/QED findings: "
      + str(
        len(
          target_rows
        )
      )
    ),
    (
      "  groups with any finding: "
      + str(
        groups_with_findings
      )
    ),
    "",
    "Interpretation:",
    (
      "  This repair changes only audit matching semantics."
    ),
    (
      "  A remaining finding is diagnostic, not automatically a production bug."
    ),
    "",
    "Production changes: none",
    "Existing test changes: none",
    "Repository-wide pytest: not run",
  ]

  if exceptions:
    result = "EXCEPTIONS"
  elif (
    argument_rows
    or transition_rows
    or duplicate_rows
    or target_rows
  ):
    result = "FINDINGS"
  else:
    result = "PASS"

  summary_lines.extend(
    (
      "",
      "R5-5d repair1 RESULT: "
      + result,
      (
        "Review remaining finding CSV files before any production change."
        if result == "FINDINGS"
        else (
          "The normalized cross-audit found no generic public-sequence defect."
          if result == "PASS"
          else "Review exceptions before interpreting the audit."
        )
      ),
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

  print(
    "\n".join(
      summary_lines
    )
  )

  return (
    1
    if exceptions
    else 0
  )


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
