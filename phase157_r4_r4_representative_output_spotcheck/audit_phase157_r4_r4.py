import json
from pathlib import Path
import sys

REPOSITORY_ROOT = Path.cwd()
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
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


CASES = (
  ("pi_8^5", 5, 3),
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)

FORBIDDEN_REFERENCE_FRAGMENTS = (
  "は単射である.",
  "は全射である.",
  " is exact",
  "transported decomposition",
  "suspension isomorphism",
  "suspension injective",
  "suspension surjective",
)

OUTPUT_DIR = Path(
  "phase157_r4_r4_spotcheck_output"
)


def _split_public_narrative(
  rendered: str,
) -> tuple[
  str,
  str,
]:
  if "## 使用する結果" in rendered:
    reference_header = "## 使用する結果"
    proof_header = "## 証明"
    reference_start = rendered.find(
      reference_header
    )
    proof_start = rendered.find(
      proof_header,
      reference_start,
    )

    if proof_start < 0:
      return (
        rendered,
        "",
      )

    reference = rendered[
      reference_start:
      proof_start
    ].strip()
    body = rendered[
      proof_start:
    ].strip()
    return (
      reference,
      body,
    )

  marker = "使用する結果を先にまとめる."
  start = rendered.find(
    marker
  )

  if start < 0:
    return (
      "",
      rendered.strip(),
    )

  candidate_body_markers = (
    "\n\nまず,",
    "\n\n次に,",
    "\n\n最後に,",
    "\n\nこの群構造",
    "\n\n以上",
  )

  positions = tuple(
    position
    for candidate in candidate_body_markers
    for position in (
      rendered.find(
        candidate,
        start + len(
          marker
        ),
      ),
    )
    if position >= 0
  )

  if not positions:
    return (
      rendered[
        start:
      ].strip(),
      "",
    )

  body_start = min(
    positions
  )

  return (
    rendered[
      start:
      body_start
    ].strip(),
    rendered[
      body_start:
    ].strip(),
  )


def _render_case(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  group_result = (
    report
    .candidates[
      0
    ]
    .source_candidate
    .group_result
  )

  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=3,
  )

  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def main():
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  cases = []
  all_reference_forbidden_hits = []

  print(
    "Phase157-R4-R4 representative output spot-check"
  )
  print(
    "Each representative is rendered exactly once at depth 3."
  )
  print()

  for label, n, k in CASES:
    print(
      f"rendering {label} ..."
    )

    rendered = _render_case(
      n,
      k,
    )
    reference, body = _split_public_narrative(
      rendered
    )

    forbidden_hits = tuple(
      fragment
      for fragment in FORBIDDEN_REFERENCE_FRAGMENTS
      if fragment in reference
    )

    all_reference_forbidden_hits.extend(
      (
        label,
        fragment,
      )
      for fragment in forbidden_hits
    )

    output_file = OUTPUT_DIR / (
      label
      .replace(
        "^",
        "_",
      )
      + ".md"
    )

    output_file.write_text(
      rendered,
      encoding="utf-8",
      newline="\n",
    )

    case = {
      "label": label,
      "n": n,
      "k": k,
      "depth": 3,
      "reference_present": bool(
        reference
      ),
      "reference_marker_count": reference.count(
        "[R"
      ),
      "reference_chars": len(
        reference
      ),
      "body_chars": len(
        body
      ),
      "forbidden_reference_hits": list(
        forbidden_hits
      ),
      "reference_section": reference,
      "body_prefix": body[
        :1200
      ],
      "output_file": str(
        output_file
      ),
    }
    cases.append(
      case
    )

    print(
      "  "
      + "references="
      + str(
        case[
          "reference_marker_count"
        ]
      )
      + ", forbidden="
      + str(
        len(
          forbidden_hits
        )
      )
    )

  summary = {
    "phase": "157-R4-R4",
    "production_code_changes": False,
    "existing_test_changes": False,
    "depth": 3,
    "render_count": len(
      CASES
    ),
    "cases": cases,
    "forbidden_reference_hits": [
      {
        "case": label,
        "fragment": fragment,
      }
      for label, fragment in all_reference_forbidden_hits
    ],
  }

  json_path = OUTPUT_DIR / (
    "phase157_r4_r4_spotcheck.json"
  )
  json_path.write_text(
    json.dumps(
      summary,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
    newline="\n",
  )

  lines = [
    "# Phase157-R4-R4 representative output spot-check",
    "",
    "- production code changes: none",
    "- existing test changes: none",
    "- depth: 3",
    "- each representative rendered exactly once",
    "",
  ]

  for case in cases:
    lines.extend(
      (
        "## "
        + case[
          "label"
        ],
        "",
        "- Reference markers: "
        + str(
          case[
            "reference_marker_count"
          ]
        ),
        "- Reference chars: "
        + str(
          case[
            "reference_chars"
          ]
        ),
        "- Body chars: "
        + str(
          case[
            "body_chars"
          ]
        ),
        "- Forbidden Reference hits: "
        + (
          ", ".join(
            case[
              "forbidden_reference_hits"
            ]
          )
          if case[
            "forbidden_reference_hits"
          ]
          else "none"
        ),
        "",
        "### Reference section",
        "",
        case[
          "reference_section"
        ],
        "",
        "### Body prefix",
        "",
        case[
          "body_prefix"
        ],
        "",
      )
    )

  md_path = OUTPUT_DIR / (
    "phase157_r4_r4_spotcheck.md"
  )
  md_path.write_text(
    "\n".join(
      lines
    ),
    encoding="utf-8",
    newline="\n",
  )

  print()
  print(
    "Spot-check complete."
  )
  print(
    "cases: "
    + str(
      len(
        cases
      )
    )
  )
  print(
    "forbidden Reference hits: "
    + str(
      len(
        all_reference_forbidden_hits
      )
    )
  )
  print(
    "output: "
    + str(
      md_path.resolve()
    )
  )
  print(
    "output: "
    + str(
      json_path.resolve()
    )
  )

  if all_reference_forbidden_hits:
    print()
    print(
      "ATTENTION: forbidden Reference fragments were detected."
    )
    for label, fragment in all_reference_forbidden_hits:
      print(
        "  "
        + label
        + ": "
        + fragment
      )


if __name__ == "__main__":
  main()
