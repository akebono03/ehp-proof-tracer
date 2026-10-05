from __future__ import annotations

from pathlib import Path
import csv
import sys
import traceback


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(REPO_ROOT),
  )


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
  violations = []

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
        rendered = _render_group(
          n,
          k,
        )
        lines = (
          rendered.splitlines()
        )
        nonempty = [
          line.strip()
          for line in lines
          if line.strip()
        ]

        markers = {
          "target": (
            lines.index(
              "## 証明対象"
            )
            if "## 証明対象" in lines
            else None
          ),
          "reference": (
            lines.index(
              "## 使用する結果"
            )
            if "## 使用する結果" in lines
            else None
          ),
          "separator": (
            lines.index(
              "---"
            )
            if "---" in lines
            else None
          ),
          "proof": (
            lines.index(
              "## 証明"
            )
            if "## 証明" in lines
            else None
          ),
        }

        ordered = (
          all(
            value is not None
            for value in markers.values()
          )
          and markers["target"]
          < markers["reference"]
          < markers["separator"]
          < markers["proof"]
        )
        qed = bool(
          nonempty
          and nonempty[-1]
          == "□"
        )
        valid = (
          ordered
          and qed
        )

        row = {
          "n": n,
          "k": k,
          "group": group,
          "ordered": ordered,
          "qed": qed,
          "valid": valid,
        }
        rows.append(
          row
        )

        if not valid:
          violations.append(
            row
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
            "traceback": (
              traceback.format_exc()
            ),
          }
        )

  output = (
    PACKAGE_DIR
    / "output"
  )
  output.mkdir(
    parents=True,
    exist_ok=True,
  )

  with (
    output
    / "phase158_r2_contract_audit.csv"
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
        "ordered",
        "qed",
        "valid",
      ),
    )
    writer.writeheader()
    writer.writerows(
      rows
    )

  summary = "\n".join(
    (
      "=" * 78,
      (
        "Phase 158-R2 - "
        "112-group Public Contract Audit"
      ),
      "=" * 78,
      "scope: n=2..15, k=0..7, depth=2",
      (
        "rendered: "
        + str(
          len(
            rows
          )
        )
      ),
      (
        "valid contract: "
        + str(
          sum(
            bool(
              row[
                "valid"
              ]
            )
            for row in rows
          )
        )
      ),
      (
        "violations: "
        + str(
          len(
            violations
          )
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
    output
    / "phase158_r2_summary.txt"
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
      and not violations
      and not exceptions
    )
    else 1
  )


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
