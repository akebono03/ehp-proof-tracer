from __future__ import annotations

from pathlib import Path
import csv
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(
  REPO_ROOT
) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


INTRO = "使用する結果を先にまとめる."


def _render_group(
  n: int,
  k: int,
) -> str:
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
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def main() -> int:
  rows = []
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
        rendered = (
          _render_group(
            n,
            k,
          )
        )
        lines = (
          rendered.splitlines()
        )

        intro_absent = (
          INTRO not in rendered
        )

        reference_index = (
          lines.index(
            "## 使用する結果"
          )
        )
        separator_index = (
          lines.index(
            "---"
          )
        )

        reference_body = [
          line.strip()
          for line in lines[
            reference_index + 1:
            separator_index
          ]
          if line.strip()
        ]

        if reference_body:
          first_reference_is_r1 = (
            reference_body[
              0
            ].startswith(
              "**[R1] "
            )
          )
        else:
          first_reference_is_r1 = True

        valid = (
          intro_absent
          and first_reference_is_r1
        )

        rows.append(
          {
            "n": n,
            "k": k,
            "group": label,
            "intro_absent": (
              intro_absent
            ),
            "reference_body_nonempty": (
              bool(
                reference_body
              )
            ),
            "first_reference_is_r1": (
              first_reference_is_r1
            ),
            "valid": valid,
          }
        )

      except Exception as exc:
        exceptions.append(
          {
            "n": n,
            "k": k,
            "group": label,
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

  output_dir = (
    PACKAGE_DIR
    / "output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  with (
    output_dir
    / "phase158_r3_112_group_intro_audit.csv"
  ).open(
    "w",
    encoding="utf-8-sig",
    newline="",
  ) as handle:
    writer = csv.DictWriter(
      handle,
      fieldnames=(
        "n",
        "k",
        "group",
        "intro_absent",
        "reference_body_nonempty",
        "first_reference_is_r1",
        "valid",
      ),
    )
    writer.writeheader()
    writer.writerows(
      rows
    )

  intro_absent_count = sum(
    bool(
      row[
        "intro_absent"
      ]
    )
    for row in rows
  )
  valid_count = sum(
    bool(
      row[
        "valid"
      ]
    )
    for row in rows
  )

  summary = "\n".join(
    (
      "=" * 78,
      (
        "Phase 158-R3 - "
        "112-group Reference Intro Normalization Audit"
      ),
      "=" * 78,
      "scope: n=2..15, k=0..7, depth=2",
      f"rendered: {len(rows)}",
      (
        "intro sentence absent: "
        + str(
          intro_absent_count
        )
      ),
      (
        "valid normalized Reference section: "
        + str(
          valid_count
        )
      ),
      (
        "exceptions: "
        + str(
          len(
            exceptions
          )
        )
      ),
      "=" * 78,
    )
  )

  print(
    summary
  )

  (
    output_dir
    / "phase158_r3_summary.txt"
  ).write_text(
    summary + "\n",
    encoding="utf-8-sig",
  )

  return (
    0
    if (
      len(
        rows
      )
      == 112
      and intro_absent_count == 112
      and valid_count == 112
      and not exceptions
    )
    else 1
  )


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
