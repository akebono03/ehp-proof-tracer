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
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
)


TAG_RE = re.compile(
  r"\\tag\{(\d+)\}"
)
NUMBERED_CONNECTOR_RE = re.compile(
  r"^\((\d+)\)(?:\s*と\s*\((\d+)\))?\s*より,"
)
WHITESPACE_RE = re.compile(
  r"\s+"
)


def _canonical_visible_text(
  text: str,
) -> str:
  normalized = text.strip()
  normalized = normalized.replace(
    "**",
    "",
  )
  normalized = normalized.replace(
    "$",
    "",
  )
  normalized = WHITESPACE_RE.sub(
    " ",
    normalized,
  )
  return normalized.strip()


def _web_view(
  n: int,
  k: int,
):
  return build_standard_web_group_proof_view(
    n,
    k,
    max_depth=2,
    mode="narrative",
  )


def _web_lines(
  view,
) -> tuple[
  str,
  ...,
]:
  lines = []

  for line in view.rendered_lines:
    if line.kind == "heading":
      lines.append(
        line.prefix
      )
      continue

    if line.kind == "separator":
      lines.append(
        "---"
      )
      continue

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

  return tuple(
    lines
  )


def _proof_lines(
  view,
) -> tuple[
  str,
  ...,
]:
  lines = _web_lines(
    view
  )

  try:
    proof_index = lines.index(
      "証明"
    )
  except ValueError:
    return ()

  return tuple(
    line.strip()
    for line in lines[
      proof_index + 1:
    ]
    if line.strip()
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
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  return build_toda_group_proof_presentation(
    replay
  )


def _connector_findings(
  proof_lines: tuple[
    str,
    ...,
  ],
):
  visible_tag_lines = {}
  findings = []
  connector_count = 0
  tagged_targets = 0
  untagged_targets = 0

  for index, line in enumerate(
    proof_lines
  ):
    for match in TAG_RE.finditer(
      line
    ):
      visible_tag_lines[
        int(
          match.group(
            1
          )
        )
      ] = index

    connector_match = (
      NUMBERED_CONNECTOR_RE.match(
        line
      )
    )

    if connector_match is None:
      continue

    connector_count += 1
    source_numbers = tuple(
      int(
        value
      )
      for value in (
        connector_match.group(
          1
        ),
        connector_match.group(
          2
        ),
      )
      if value is not None
    )

    missing_or_late = tuple(
      number
      for number in source_numbers
      if (
        number
        not in visible_tag_lines
        or visible_tag_lines[
          number
        ] >= index
      )
    )

    if missing_or_late:
      findings.append(
        (
          index,
          "MISSING_OR_LATE_SOURCE",
          line,
          repr(
            missing_or_late
          ),
        )
      )
      continue

    if index + 1 >= len(
      proof_lines
    ):
      findings.append(
        (
          index,
          "MISSING_TARGET",
          line,
          "",
        )
      )
      continue

    target = proof_lines[
      index + 1
    ]

    if (
      target == "□"
      or target == "---"
      or NUMBERED_CONNECTOR_RE.match(
        target
      )
      is not None
    ):
      findings.append(
        (
          index,
          "MISSING_VISIBLE_TARGET",
          line,
          target,
        )
      )
      continue

    if TAG_RE.search(
      target
    ):
      tagged_targets += 1
    else:
      untagged_targets += 1

  return (
    tuple(
      findings
    ),
    connector_count,
    tagged_targets,
    untagged_targets,
  )


def _root_qed_finding(
  n: int,
  k: int,
  proof_lines: tuple[
    str,
    ...,
  ],
):
  if not proof_lines:
    return (
      "EMPTY_PROOF",
      "",
    )

  if proof_lines[
    -1
  ] != "□":
    return (
      "QED_NOT_TERMINAL",
      proof_lines[
        -1
      ],
    )

  if proof_lines.count(
    "□"
  ) != 1:
    return (
      "QED_COUNT",
      str(
        proof_lines.count(
          "□"
        )
      ),
    )

  presentation = _presentation(
    n,
    k,
  )
  root_text = _render_generic_narrative_step(
    presentation.root_step
  )
  canonical_root = (
    _canonical_visible_text(
      root_text
    )
  )
  root_positions = tuple(
    index
    for index, line in enumerate(
      proof_lines
    )
    if canonical_root
    in _canonical_visible_text(
      TAG_RE.sub(
        "",
        line,
      )
    )
  )

  if not root_positions:
    return (
      "ROOT_TARGET_NOT_VISIBLE",
      root_text,
    )

  if root_positions[
    -1
  ] != (
    len(
      proof_lines
    )
    - 2
  ):
    return (
      "VISIBLE_CONTENT_AFTER_ROOT_TARGET",
      repr(
        proof_lines[
          root_positions[
            -1
          ] + 1:
          -1
        ]
      ),
    )

  return None


def main() -> int:
  output_dir = (
    PACKAGE_DIR
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  group_rows = []
  connector_rows = []
  target_rows = []
  exceptions = []

  total_connectors = 0
  total_tagged_targets = 0
  total_untagged_targets = 0

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
        view = _web_view(
          n,
          k,
        )
        proof_lines = (
          _proof_lines(
            view
          )
        )
        (
          connector_findings,
          connector_count,
          tagged_targets,
          untagged_targets,
        ) = _connector_findings(
          proof_lines
        )
        root_finding = (
          _root_qed_finding(
            n,
            k,
            proof_lines,
          )
        )

        total_connectors += (
          connector_count
        )
        total_tagged_targets += (
          tagged_targets
        )
        total_untagged_targets += (
          untagged_targets
        )

        for (
          line_index,
          classification,
          connector,
          detail,
        ) in connector_findings:
          connector_rows.append(
            {
              "n": n,
              "k": k,
              "group": group,
              "line_index": line_index,
              "classification": (
                classification
              ),
              "connector": (
                connector
              ),
              "detail": detail,
            }
          )

        if root_finding is not None:
          target_rows.append(
            {
              "n": n,
              "k": k,
              "group": group,
              "classification": (
                root_finding[
                  0
                ]
              ),
              "detail": (
                root_finding[
                  1
                ]
              ),
            }
          )

        group_rows.append(
          {
            "n": n,
            "k": k,
            "group": group,
            "web_mode": view.mode,
            "web_depth": view.max_depth,
            "proof_lines": len(
              proof_lines
            ),
            "numbered_connectors": (
              connector_count
            ),
            "connector_findings": (
              len(
                connector_findings
              )
            ),
            "root_qed_findings": (
              0
              if root_finding is None
              else 1
            ),
          }
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
    name,
    rows,
    fieldnames,
  ):
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
      "web_mode",
      "web_depth",
      "proof_lines",
      "numbered_connectors",
      "connector_findings",
      "root_qed_findings",
    ),
  )
  write_csv(
    "connector_findings.csv",
    connector_rows,
    (
      "n",
      "k",
      "group",
      "line_index",
      "classification",
      "connector",
      "detail",
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
      "detail",
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

  bad_mode_depth = sum(
    (
      row[
        "web_mode"
      ] != "narrative"
      or row[
        "web_depth"
      ] != 2
    )
    for row in group_rows
  )

  summary_lines = [
    (
      "Phase 158-R5-5 closure — focused verification"
    ),
    "",
    "Scope:",
    (
      "  current historical audit corpus: "
      "n=2..15, k=0..7"
    ),
    (
      "  architecture contract is generic; "
      "the coordinate window is only the current audit corpus."
    ),
    "",
    "Verified closure contracts:",
    (
      "  - Web public Narrative is generated at depth=2"
    ),
    (
      "  - numbered connector sources are already visible"
    ),
    (
      "  - numbered connector has an immediate visible target"
    ),
    (
      "  - target tags are optional unless later referenced"
    ),
    (
      "  - root target is immediately before one terminal □"
    ),
    "",
    "Totals:",
    (
      "  audited coordinates: 112"
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
      "  wrong Web mode/depth: "
      + str(
        bad_mode_depth
      )
    ),
    (
      "  numbered connectors: "
      + str(
        total_connectors
      )
    ),
    (
      "  connector targets with tag: "
      + str(
        total_tagged_targets
      )
    ),
    (
      "  connector targets without tag: "
      + str(
        total_untagged_targets
      )
    ),
    (
      "  connector findings: "
      + str(
        len(
          connector_rows
        )
      )
    ),
    (
      "  root/QED findings: "
      + str(
        len(
          target_rows
        )
      )
    ),
    "",
    "Production code changes: none",
    "Existing test changes: none",
    "Repository-wide pytest: not run",
  ]

  passed = (
    len(
      group_rows
    )
    == 112
    and not exceptions
    and bad_mode_depth == 0
    and not connector_rows
    and not target_rows
  )

  summary_lines.extend(
    (
      "",
      (
        "R5-5 CLOSURE RESULT: PASS"
        if passed
        else "R5-5 CLOSURE RESULT: FINDINGS"
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
    0
    if passed
    else 1
  )


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
