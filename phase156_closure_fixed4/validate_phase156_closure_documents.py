from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

EXPECTED = {
  ROOT / "README.md": (
    "## Phase 156 closure",
    "Phase 156-R6 then partitioned the same 112-group population",
  ),
  ROOT / "docs" / "design.md": (
    "# Phase 156 Reference minimal-display 設計境界",
    "body [R#]",
  ),
  ROOT / "docs" / "development_log.md": (
    "# Phase 156 — Reference statement relevance / minimal display",
    "Total required violations: 0",
  ),
  ROOT / "docs" / "roadmap.md": (
    "# Phase 156 完了境界と Phase 157 以降",
    "Phase 157 境界",
  ),
  ROOT / "docs" / "proof_records.md": (
    "# Phase 156 Reference minimal-display provenance record",
    "unique groups: 112",
  ),
}


def main() -> int:
  failures = []

  for path, markers in EXPECTED.items():
    if not path.exists():
      failures.append(
        (
          str(
            path
          ),
          "missing",
        )
      )
      continue

    text = path.read_text(
      encoding="utf-8",
    )

    for marker in markers:
      if marker not in text:
        failures.append(
          (
            str(
              path
            ),
            marker,
          )
        )

  if failures:
    print(
      "FAIL: Phase156 closure document validation"
    )

    for failure in failures:
      print(
        "  "
        + repr(
          failure
        )
      )

    return 1

  print(
    "PASS: all five Phase156 closure documents contain "
    "the expected full-file closure sections."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
