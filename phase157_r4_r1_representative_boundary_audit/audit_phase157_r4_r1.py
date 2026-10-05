from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path.cwd()
if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

from dataclasses import asdict
import json
from pathlib import Path

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_literature_statement_boundary import (
  classify_toda_literature_statement_step,
)


CASES = (
  ("pi_8^5", 5, 3),
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)


def _build_presentation(
  n: int,
  k: int,
  depth: int,
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
    max_depth=depth,
  )
  return build_toda_group_proof_presentation(
    replay
  )


def _reference_prefix(
  rendered: str,
) -> str:
  markers = (
    "\n\nまず,",
    "\n\n次に,",
    "\n\n最後に,",
    "\n\n$\\pi_",
    "\n\nこの群構造",
  )

  positions = tuple(
    position
    for marker in markers
    for position in (
      rendered.find(
        marker
      ),
    )
    if position >= 0
  )

  if not positions:
    return rendered

  return rendered[
    :min(
      positions
    )
  ]


def _step_record(
  proof_step,
):
  inference_rule = proof_step.inference_rule
  reference = (
    None
    if inference_rule is None
    else inference_rule.literature_reference
  )
  boundary = classify_toda_literature_statement_step(
    proof_step
  )

  return {
    "statement_type": type(
      proof_step.conclusion
    ).__name__,
    "rule_name": (
      None
      if inference_rule is None
      else inference_rule.name
    ),
    "reference_label": (
      None
      if reference is None
      else reference.label
    ),
    "reference_locator": (
      None
      if reference is None
      else reference.locator
    ),
    "boundary_classification": (
      "UNTRACKED"
      if boundary is None
      else boundary.classification.value
    ),
    "boundary_locator": (
      None
      if boundary is None
      else boundary.reference_locator
    ),
    "boundary_component_key": (
      None
      if boundary is None
      else boundary.component_key
    ),
  }


def _audit_case(
  label: str,
  n: int,
  k: int,
  depth: int,
):
  presentation = _build_presentation(
    n,
    k,
    depth,
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
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  return {
    "group": label,
    "n": n,
    "k": k,
    "depth": depth,
    "reference_prefix": _reference_prefix(
      rendered
    ),
    "reference_entries": [
      {
        "number": entry.number,
        "reference_label": entry.reference.label,
        "reference_locator": entry.reference.locator,
        "selected_statement_lines": list(
          statement_lines.get(
            entry.number,
            (),
          )
        ),
        "steps": [
          _step_record(
            step
          )
          for step in entry.proof_steps
        ],
      }
      for entry in entries
    ],
  }


def _summary(
  cases,
):
  locator_summary = {}

  for case in cases:
    for entry in case[
      "reference_entries"
    ]:
      locator = (
        entry[
          "reference_locator"
        ]
        or entry[
          "reference_label"
        ]
      )
      bucket = locator_summary.setdefault(
        locator,
        {
          "groups": set(),
          "fixed_statement_steps": 0,
          "proof_internal_steps": 0,
          "untracked_steps": 0,
          "component_keys": set(),
          "rule_names": set(),
        },
      )
      bucket[
        "groups"
      ].add(
        case[
          "group"
        ]
      )

      for step in entry[
        "steps"
      ]:
        classification = step[
          "boundary_classification"
        ]

        if classification == "fixed_statement":
          bucket[
            "fixed_statement_steps"
          ] += 1
        elif classification == "proof_internal":
          bucket[
            "proof_internal_steps"
          ] += 1
        else:
          bucket[
            "untracked_steps"
          ] += 1

        component_key = step[
          "boundary_component_key"
        ]
        if component_key is not None:
          bucket[
            "component_keys"
          ].add(
            component_key
          )

        rule_name = step[
          "rule_name"
        ]
        if rule_name is not None:
          bucket[
            "rule_names"
          ].add(
            rule_name
          )

  return {
    locator: {
      "groups": sorted(
        bucket[
          "groups"
        ]
      ),
      "fixed_statement_steps": bucket[
        "fixed_statement_steps"
      ],
      "proof_internal_steps": bucket[
        "proof_internal_steps"
      ],
      "untracked_steps": bucket[
        "untracked_steps"
      ],
      "component_keys": sorted(
        bucket[
          "component_keys"
        ]
      ),
      "rule_names": sorted(
        bucket[
          "rule_names"
        ]
      ),
    }
    for locator, bucket in sorted(
      locator_summary.items()
    )
  }


def _markdown_report(
  cases,
  summary,
) -> str:
  lines = [
    "# Phase157-R4-R1 representative boundary audit",
    "",
    "Production code changes: none.",
    "",
    "## Reference locator summary",
    "",
    "| Reference | Groups | FIXED | PROOF_INTERNAL | UNTRACKED |",
    "| --- | --- | ---: | ---: | ---: |",
  ]

  for locator, item in summary.items():
    lines.append(
      "| "
      + locator.replace(
        "|",
        "\\|",
      )
      + " | "
      + ", ".join(
        item[
          "groups"
        ]
      )
      + " | "
      + str(
        item[
          "fixed_statement_steps"
        ]
      )
      + " | "
      + str(
        item[
          "proof_internal_steps"
        ]
      )
      + " | "
      + str(
        item[
          "untracked_steps"
        ]
      )
      + " |"
    )

  for case in cases:
    lines.extend(
      (
        "",
        "## "
        + case[
          "group"
        ]
        + " depth="
        + str(
          case[
            "depth"
          ]
        ),
        "",
        "### Current public Reference prefix",
        "",
        "```text",
        case[
          "reference_prefix"
        ].rstrip(),
        "```",
        "",
        "### Reference entries",
        "",
      )
    )

    for entry in case[
      "reference_entries"
    ]:
      lines.append(
        "#### "
        + str(
          entry[
            "number"
          ]
        )
        + ". "
        + (
          entry[
            "reference_locator"
          ]
          or entry[
            "reference_label"
          ]
        )
      )
      lines.append("")

      if entry[
        "selected_statement_lines"
      ]:
        lines.append(
          "Selected statement lines:"
        )
        for statement_line in entry[
          "selected_statement_lines"
        ]:
          lines.append(
            "- `"
            + statement_line.replace(
              "`",
              "\\`",
            )
            + "`"
          )
      else:
        lines.append(
          "Selected statement lines: none"
        )

      lines.append("")
      lines.append(
        "| classification | statement type | component | rule |"
      )
      lines.append(
        "| --- | --- | --- | --- |"
      )

      for step in entry[
        "steps"
      ]:
        lines.append(
          "| "
          + step[
            "boundary_classification"
          ]
          + " | "
          + step[
            "statement_type"
          ]
          + " | "
          + (
            step[
              "boundary_component_key"
            ]
            or ""
          )
          + " | "
          + (
            step[
              "rule_name"
            ]
            or ""
          ).replace(
            "|",
            "\\|",
          )
          + " |"
        )

  lines.extend(
    (
      "",
      "## R4-R2 gate",
      "",
      "R4-R2 では、この監査で UNTRACKED となった文献について、",
      "fixed statement の境界を確認できたものだけ catalog に追加する。",
      "rule name や literature_reference が同じという理由だけで",
      "Reference へ採用しない。",
      "",
    )
  )

  return "\n".join(
    lines
  )


def main():
  output_dir = Path(
    "phase157_r4_r1_audit_output"
  )
  output_dir.mkdir(
    exist_ok=True
  )

  cases = [
    _audit_case(
      label,
      n,
      k,
      depth,
    )
    for label, n, k in CASES
    for depth in (
      2,
      3,
    )
  ]
  summary = _summary(
    cases
  )

  payload = {
    "cases": cases,
    "summary": summary,
  }

  (
    output_dir
    / "phase157_r4_r1_representative_boundary_audit.json"
  ).write_text(
    json.dumps(
      payload,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  (
    output_dir
    / "phase157_r4_r1_representative_boundary_audit.md"
  ).write_text(
    _markdown_report(
      cases,
      summary,
    ),
    encoding="utf-8",
  )

  print(
    "Phase157-R4-R1 representative boundary audit complete."
  )
  print(
    "cases:",
    len(
      cases
    ),
  )
  print("")
  print("Reference locator summary:")

  for locator, item in summary.items():
    print(
      "  "
      + locator
      + ": "
      + "groups="
      + str(
        len(
          item[
            "groups"
          ]
        )
      )
      + ", fixed="
      + str(
        item[
          "fixed_statement_steps"
        ]
      )
      + ", internal="
      + str(
        item[
          "proof_internal_steps"
        ]
      )
      + ", untracked="
      + str(
        item[
          "untracked_steps"
        ]
      )
    )

  print("")
  print(
    "output:",
    (
      output_dir
      / "phase157_r4_r1_representative_boundary_audit.md"
    ).resolve(),
  )
  print(
    "output:",
    (
      output_dir
      / "phase157_r4_r1_representative_boundary_audit.json"
    ).resolve(),
  )


if __name__ == "__main__":
  main()
