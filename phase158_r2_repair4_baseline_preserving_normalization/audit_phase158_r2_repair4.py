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


def _presentation(
  n: int,
  k: int,
):
  from toda_calculation_facade import (
    build_standard_toda_report,
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

  return (
    build_toda_group_proof_presentation(
      replay
    )
  )


def _trim(
  lines: list[str],
) -> list[str]:
  result = lines[:]

  while (
    result
    and not result[0].strip()
  ):
    result.pop(0)

  while (
    result
    and not result[-1].strip()
  ):
    result.pop()

  return result


def _strip_qed(
  lines: list[str],
) -> list[str]:
  result = _trim(
    lines
  )

  if (
    result
    and result[-1].strip()
    in {
      "□",
      r"$\square$",
      r"\(\square\)",
      r"\square",
    }
  ):
    result.pop()

  return _trim(
    result
  )


def _baseline_payload(
  rendered: str,
) -> tuple[
  list[str],
  list[str],
]:
  lines = rendered.splitlines()

  if (
    "## 使用する結果" in lines
    and "## 証明" in lines
  ):
    reference = lines.index(
      "## 使用する結果"
    )
    proof = lines.index(
      "## 証明"
    )

    return (
      _trim(
        lines[
          reference + 1:
          proof
        ]
      ),
      _strip_qed(
        lines[
          proof + 1:
        ]
      ),
    )

  if (
    lines
    and lines[0]
    == "# Group proof narrative"
  ):
    body = lines[
      1:
    ]
  else:
    body = lines[
      :
    ]

  return (
    [],
    _strip_qed(
      body
    ),
  )


def _normalized_payload(
  rendered: str,
) -> tuple[
  list[str],
  list[str],
  bool,
]:
  lines = rendered.splitlines()

  target = lines.index(
    "## 証明対象"
  )
  reference = lines.index(
    "## 使用する結果"
  )
  separator = lines.index(
    "---"
  )
  proof = lines.index(
    "## 証明"
  )

  nonempty = [
    line.strip()
    for line in lines
    if line.strip()
  ]

  contract = (
    target
    < reference
    < separator
    < proof
    and nonempty[-1]
    == "□"
  )

  return (
    _trim(
      lines[
        reference + 1:
        separator
      ]
    ),
    _strip_qed(
      lines[
        proof + 1:
      ]
    ),
    contract,
  )


def main() -> int:
  from toda_group_proof_narrative_renderer import (
    _phase158_baseline_render_toda_group_proof_narrative_markdown,
    render_toda_group_proof_narrative_markdown,
  )

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
        presentation = (
          _presentation(
            n,
            k,
          )
        )
        baseline = (
          _phase158_baseline_render_toda_group_proof_narrative_markdown(
            presentation
          )
        )
        normalized = (
          render_toda_group_proof_narrative_markdown(
            presentation
          )
        )

        (
          baseline_reference,
          baseline_proof,
        ) = _baseline_payload(
          baseline
        )
        (
          normalized_reference,
          normalized_proof,
          contract,
        ) = _normalized_payload(
          normalized
        )

        reference_preserved = (
          baseline_reference
          == normalized_reference
        )
        proof_preserved = (
          baseline_proof
          == normalized_proof
        )

        rows.append(
          {
            "n": n,
            "k": k,
            "group": label,
            "contract": contract,
            "reference_preserved": (
              reference_preserved
            ),
            "proof_preserved": (
              proof_preserved
            ),
            "valid": (
              contract
              and reference_preserved
              and proof_preserved
            ),
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
    / "phase158_r2_repair4_112_group_preservation.csv"
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
        "contract",
        "reference_preserved",
        "proof_preserved",
        "valid",
      ),
    )
    writer.writeheader()
    writer.writerows(
      rows
    )

  contract_count = sum(
    bool(
      row[
        "contract"
      ]
    )
    for row in rows
  )
  reference_count = sum(
    bool(
      row[
        "reference_preserved"
      ]
    )
    for row in rows
  )
  proof_count = sum(
    bool(
      row[
        "proof_preserved"
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
        "Phase 158-R2 repair4 - "
        "112-group Baseline Preservation Audit"
      ),
      "=" * 78,
      "scope: n=2..15, k=0..7, depth=2",
      f"rendered: {len(rows)}",
      f"public contract valid: {contract_count}",
      (
        "Reference payload preserved: "
        + str(
          reference_count
        )
      ),
      (
        "Proof payload preserved: "
        + str(
          proof_count
        )
      ),
      f"fully valid: {valid_count}",
      f"exceptions: {len(exceptions)}",
      "=" * 78,
    )
  )

  print(
    summary
  )

  (
    output_dir
    / "phase158_r2_repair4_summary.txt"
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
      and valid_count == 112
      and not exceptions
    )
    else 1
  )


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
