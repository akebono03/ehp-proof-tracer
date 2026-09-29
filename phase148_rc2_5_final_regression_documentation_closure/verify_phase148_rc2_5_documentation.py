from pathlib import Path
import sys


CHECKS = {
  "README.md": (
    "## Phase 148 closure",
    "Phase 149 is intentionally separate",
  ),
  "docs/design.md": (
    "# 32. Phase 148 RC2 完了境界",
    "OWNED_PRIMARY",
    "UNOWNED_RECURSIVE",
    "AMBIGUOUS_RELEVANT",
  ),
  "docs/development_log.md": (
    "# Phase 148 — RC2 Recursive exactness evidence exposure",
    "RC2-5 — final regression / documentation closure",
    "Phase 148 完了。次は Phase 149 / RC3。",
  ),
  "docs/roadmap.md": (
    "## Phase 148 — 完了: RC2 Recursive exactness evidence exposure",
    "## 現在地: Phase 149 — RC3 Contribution ownership / insertion ordering",
    "## Phase 149 — RC3: Contribution ownership / insertion ordering",
  ),
  "docs/proof_records.md": (
    "# Phase 148 recursive exactness exposure provenance record",
    "visible raw exactness ProofStep = 0",
    "Phase 149 / RC3",
  ),
}


def main():
  if len(sys.argv) != 2:
    raise SystemExit(
      "usage: verify_phase148_rc2_5_documentation.py "
      "<regression-summary-file>"
    )

  summary = Path(sys.argv[1]).read_text(
    encoding="utf-8"
  ).strip()

  for path_string, markers in CHECKS.items():
    path = Path(path_string)
    text = path.read_text(
      encoding="utf-8",
      errors="strict",
    )
    for marker in markers:
      if marker not in text:
        raise AssertionError(
          f"{path}: missing marker: {marker}"
        )
    if summary not in text:
      raise AssertionError(
        f"{path}: final regression summary missing"
      )

  print("Phase 148 RC2-5 documentation verification: PASS")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
