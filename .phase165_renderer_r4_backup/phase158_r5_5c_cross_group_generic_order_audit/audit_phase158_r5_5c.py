from __future__ import annotations

import csv
import re
import sys
import traceback
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

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
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


MAX_DEPTH = 2

# Current historical audit corpus only.
# This is not an architectural group-count contract.
AUDIT_N_RANGE = range(
  2,
  16,
)
AUDIT_K_RANGE = range(
  0,
  8,
)

OUTPUT_DIR = (
  Path(__file__).resolve().parent
  / "audit_output"
)


TAG_RE = re.compile(
  r"\\tag\{(\d+)\}"
)
CONNECTOR_RE = re.compile(
  r"^\((\d+)\)(?: と \((\d+)\))* より,$"
)


def group_label(
  n: int,
  k: int,
) -> str:
  return (
    "pi_"
    + str(
      n + k
    )
    + "^"
    + str(
      n
    )
  )


def line_text(
  line,
) -> str:
  if line.segments:
    return "".join(
      segment.value
      for segment in line.segments
    )

  return (
    line.prefix
    + (
      ""
      if line.statement_latex is None
      else line.statement_latex
    )
    + line.suffix
  )


def web_proof_lines(
  n: int,
  k: int,
) -> tuple[
  str,
  ...,
]:
  view = build_standard_web_group_proof_view(
    n,
    k,
    max_depth=MAX_DEPTH,
    mode="narrative",
  )
  result = []
  in_proof = False

  for line in view.rendered_lines:
    if (
      line.kind == "heading"
      and line.prefix == "証明"
    ):
      in_proof = True
      continue

    if not in_proof:
      continue

    text = line_text(
      line
    ).strip()

    if text:
      result.append(
        text
      )

  return tuple(
    result
  )


def searchable_step_text(
  proof_step,
) -> str:
  rendered = _render_generic_narrative_step(
    proof_step
  ).strip()

  if (
    rendered.startswith(
      "$"
    )
    and rendered.endswith(
      "$"
    )
  ):
    return rendered[
      1:-1
    ]

  return rendered


def first_line_index_containing(
  proof_lines: tuple[
    str,
    ...,
  ],
  needle: str,
) -> int | None:
  if not needle:
    return None

  for index, line in enumerate(
    proof_lines
  ):
    if needle in line:
      return index

  return None


def build_argument_data(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  if not report.candidates:
    raise RuntimeError(
      "standard report has no candidates"
    )

  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=MAX_DEPTH,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
  )

  return (
    presentation,
    blocks,
    arguments,
  )


def argument_visible_order_defects(
  proof_lines: tuple[
    str,
    ...,
  ],
  arguments,
) -> list[
  dict,
]:
  defects = []

  for argument_index, argument in enumerate(
    arguments
  ):
    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )

    if conclusion_step is None:
      continue

    conclusion_text = searchable_step_text(
      conclusion_step
    )
    conclusion_index = (
      first_line_index_containing(
        proof_lines,
        conclusion_text,
      )
    )

    if conclusion_index is None:
      continue

    candidate_premises = []
    seen_ids = set()

    for premise in conclusion_step.premises:
      if id(
        premise
      ) in seen_ids:
        continue

      seen_ids.add(
        id(
          premise
        )
      )
      candidate_premises.append(
        premise
      )

      for support in premise.premises:
        if id(
          support
        ) in seen_ids:
          continue

        seen_ids.add(
          id(
            support
          )
        )
        candidate_premises.append(
          support
        )

    for premise in candidate_premises:
      premise_text = searchable_step_text(
        premise
      )
      premise_index = (
        first_line_index_containing(
          proof_lines,
          premise_text,
        )
      )

      if premise_index is None:
        continue

      if premise_index < conclusion_index:
        continue

      defects.append(
        {
          "argument_index": argument_index,
          "argument_role": argument.role.value,
          "premise_index": premise_index,
          "conclusion_index": conclusion_index,
          "premise": premise_text,
          "conclusion": conclusion_text,
        }
      )

  return defects


def equation_chain_defects(
  proof_lines: tuple[
    str,
    ...,
  ],
) -> list[
  dict,
]:
  defects = []
  tag_line_by_number = {}

  for index, line in enumerate(
    proof_lines
  ):
    for match in TAG_RE.finditer(
      line
    ):
      number = int(
        match.group(
          1
        )
      )

      if number not in tag_line_by_number:
        tag_line_by_number[
          number
        ] = index

  for index, line in enumerate(
    proof_lines
  ):
    stripped = line.strip()

    if not (
      stripped.startswith(
        "("
      )
      and stripped.endswith(
        "より,"
      )
    ):
      continue

    numbers = tuple(
      int(
        value
      )
      for value in re.findall(
        r"\((\d+)\)",
        stripped,
      )
    )

    if not numbers:
      continue

    missing = tuple(
      number
      for number in numbers
      if number not in tag_line_by_number
    )
    late = tuple(
      number
      for number in numbers
      if (
        number in tag_line_by_number
        and tag_line_by_number[
          number
        ] >= index
      )
    )

    next_nonempty_index = (
      index + 1
      if index + 1 < len(
        proof_lines
      )
      else None
    )
    next_has_tag = (
      False
      if next_nonempty_index is None
      else bool(
        TAG_RE.search(
          proof_lines[
            next_nonempty_index
          ]
        )
      )
    )

    if (
      missing
      or late
      or not next_has_tag
    ):
      defects.append(
        {
          "connector_index": index,
          "connector": stripped,
          "missing_references": missing,
          "late_references": late,
          "next_index": next_nonempty_index,
          "next_line": (
            ""
            if next_nonempty_index is None
            else proof_lines[
              next_nonempty_index
            ]
          ),
          "next_has_tag": next_has_tag,
        }
      )

  return defects


def target_position_defect(
  proof_lines: tuple[
    str,
    ...,
  ],
  presentation,
) -> dict | None:
  target_text = searchable_step_text(
    presentation.root_step
  )
  target_index = first_line_index_containing(
    proof_lines,
    target_text,
  )

  if target_index is None:
    return {
      "kind": "target_missing",
      "target": target_text,
      "target_index": "",
      "qed_index": "",
    }

  qed_index = next(
    (
      index
      for index, line in enumerate(
        proof_lines
      )
      if line == "□"
    ),
    None,
  )

  if qed_index is None:
    return {
      "kind": "qed_missing",
      "target": target_text,
      "target_index": target_index,
      "qed_index": "",
    }

  if target_index >= qed_index:
    return {
      "kind": "target_after_qed",
      "target": target_text,
      "target_index": target_index,
      "qed_index": qed_index,
    }

  trailing_before_qed = tuple(
    line
    for line in proof_lines[
      target_index + 1:
      qed_index
    ]
    if line.strip()
  )

  if trailing_before_qed:
    return {
      "kind": "content_after_target",
      "target": target_text,
      "target_index": target_index,
      "qed_index": qed_index,
      "trailing": " || ".join(
        trailing_before_qed
      ),
    }

  return None


def write_csv(
  path: Path,
  rows: list[
    dict
  ],
  fieldnames: tuple[
    str,
    ...,
  ],
) -> None:
  with path.open(
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


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  totals = Counter()
  group_rows = []
  argument_rows = []
  equation_rows = []
  target_rows = []
  exception_rows = []

  for n in AUDIT_N_RANGE:
    for k in AUDIT_K_RANGE:
      label = group_label(
        n,
        k,
      )
      totals[
        "audited_coordinates"
      ] += 1

      try:
        (
          presentation,
          blocks,
          arguments,
        ) = build_argument_data(
          n,
          k,
        )
        proof_lines = web_proof_lines(
          n,
          k,
        )

        totals[
          "rendered"
        ] += 1

        argument_defects = (
          argument_visible_order_defects(
            proof_lines,
            arguments,
          )
        )
        equation_defects = (
          equation_chain_defects(
            proof_lines
          )
        )
        target_defect = (
          target_position_defect(
            proof_lines,
            presentation,
          )
        )

        if argument_defects:
          totals[
            "groups_with_argument_order_defect"
          ] += 1

        if equation_defects:
          totals[
            "groups_with_equation_chain_defect"
          ] += 1

        if target_defect is not None:
          totals[
            "groups_with_target_position_defect"
          ] += 1

        totals[
          "argument_order_defects"
        ] += len(
          argument_defects
        )
        totals[
          "equation_chain_defects"
        ] += len(
          equation_defects
        )

        group_rows.append(
          {
            "n": n,
            "k": k,
            "group": label,
            "proof_lines": len(
              proof_lines
            ),
            "arguments": len(
              arguments
            ),
            "argument_order_defects": len(
              argument_defects
            ),
            "equation_chain_defects": len(
              equation_defects
            ),
            "target_position_defect": (
              ""
              if target_defect is None
              else target_defect[
                "kind"
              ]
            ),
          }
        )

        for defect in argument_defects:
          argument_rows.append(
            {
              "n": n,
              "k": k,
              "group": label,
              **defect,
            }
          )

        for defect in equation_defects:
          equation_rows.append(
            {
              "n": n,
              "k": k,
              "group": label,
              **defect,
            }
          )

        if target_defect is not None:
          target_rows.append(
            {
              "n": n,
              "k": k,
              "group": label,
              **target_defect,
            }
          )

      except Exception as exc:
        totals[
          "exceptions"
        ] += 1
        exception_rows.append(
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
            "traceback": traceback.format_exc(),
          }
        )

  write_csv(
    OUTPUT_DIR
    / "groups.csv",
    group_rows,
    (
      "n",
      "k",
      "group",
      "proof_lines",
      "arguments",
      "argument_order_defects",
      "equation_chain_defects",
      "target_position_defect",
    ),
  )
  write_csv(
    OUTPUT_DIR
    / "argument_order_defects.csv",
    argument_rows,
    (
      "n",
      "k",
      "group",
      "argument_index",
      "argument_role",
      "premise_index",
      "conclusion_index",
      "premise",
      "conclusion",
    ),
  )
  write_csv(
    OUTPUT_DIR
    / "equation_chain_defects.csv",
    equation_rows,
    (
      "n",
      "k",
      "group",
      "connector_index",
      "connector",
      "missing_references",
      "late_references",
      "next_index",
      "next_line",
      "next_has_tag",
    ),
  )

  target_fieldnames = (
    "n",
    "k",
    "group",
    "kind",
    "target",
    "target_index",
    "qed_index",
    "trailing",
  )
  normalized_target_rows = []

  for row in target_rows:
    normalized_target_rows.append(
      {
        field: row.get(
          field,
          "",
        )
        for field in target_fieldnames
      }
    )

  write_csv(
    OUTPUT_DIR
    / "target_position_defects.csv",
    normalized_target_rows,
    target_fieldnames,
  )

  write_csv(
    OUTPUT_DIR
    / "exceptions.csv",
    exception_rows,
    (
      "n",
      "k",
      "group",
      "exception_type",
      "message",
      "traceback",
    ),
  )

  summary_lines = [
    "=" * 88,
    "Phase 158-R5-5c — generic public ordering cross-audit",
    "=" * 88,
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
    "Totals:",
    (
      "  audited coordinates: "
      + str(
        totals[
          "audited_coordinates"
        ]
      )
    ),
    (
      "  rendered: "
      + str(
        totals[
          "rendered"
        ]
      )
    ),
    (
      "  exceptions: "
      + str(
        totals[
          "exceptions"
        ]
      )
    ),
    (
      "  argument-order defects: "
      + str(
        totals[
          "argument_order_defects"
        ]
      )
    ),
    (
      "  groups with argument-order defect: "
      + str(
        totals[
          "groups_with_argument_order_defect"
        ]
      )
    ),
    (
      "  equation-chain defects: "
      + str(
        totals[
          "equation_chain_defects"
        ]
      )
    ),
    (
      "  groups with equation-chain defect: "
      + str(
        totals[
          "groups_with_equation_chain_defect"
        ]
      )
    ),
    (
      "  groups with target-position defect: "
      + str(
        totals[
          "groups_with_target_position_defect"
        ]
      )
    ),
    "",
    "Interpretation:",
    (
      "  argument-order defect = a visible direct/support premise "
      "appears at or after its visible conclusion."
    ),
    (
      "  equation-chain defect = a numbered connector references "
      "missing/late sources or is not followed by a tagged target."
    ),
    (
      "  target-position defect = public root target is missing, "
      "QED is missing, or visible content remains after the target."
    ),
    "",
    "Production changes: none",
    "Existing test changes: none",
    "Repository-wide pytest: not run",
    "",
  ]

  if (
    totals[
      "exceptions"
    ] == 0
    and totals[
      "argument_order_defects"
    ] == 0
    and totals[
      "equation_chain_defects"
    ] == 0
    and totals[
      "groups_with_target_position_defect"
    ] == 0
  ):
    summary_lines.extend(
      (
        "R5-5c RESULT: PASS",
        (
          "The current audit corpus satisfies the generic "
          "public ordering invariants."
        ),
      )
    )
  else:
    summary_lines.extend(
      (
        "R5-5c RESULT: FINDINGS",
        (
          "Review the CSV files before changing production code. "
          "A finding is diagnostic, not automatically a defect."
        ),
      )
    )

  summary = "\n".join(
    summary_lines
  )
  (
    OUTPUT_DIR
    / "summary.txt"
  ).write_text(
    summary
    + "\n",
    encoding="utf-8",
    newline="\n",
  )

  print(
    summary
  )

  if argument_rows:
    print(
      "\nArgument-order findings (first 20):"
    )

    for row in argument_rows[
      :20
    ]:
      print(
        (
          "  "
          + row[
            "group"
          ]
          + " "
          + row[
            "argument_role"
          ]
          + " premise@"
          + str(
            row[
              "premise_index"
            ]
          )
          + " conclusion@"
          + str(
            row[
              "conclusion_index"
            ]
          )
        )
      )

  if equation_rows:
    print(
      "\nEquation-chain findings (first 20):"
    )

    for row in equation_rows[
      :20
    ]:
      print(
        (
          "  "
          + row[
            "group"
          ]
          + " connector@"
          + str(
            row[
              "connector_index"
            ]
          )
          + " "
          + row[
            "connector"
          ]
        )
      )

  if target_rows:
    print(
      "\nTarget-position findings (first 20):"
    )

    for row in target_rows[
      :20
    ]:
      print(
        (
          "  "
          + row[
            "group"
          ]
          + " "
          + row[
            "kind"
          ]
        )
      )

  if exception_rows:
    print(
      "\nExceptions (first 20):"
    )

    for row in exception_rows[
      :20
    ]:
      print(
        (
          "  "
          + row[
            "group"
          ]
          + " "
          + row[
            "exception_type"
          ]
          + ": "
          + row[
            "message"
          ]
        )
      )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
