from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED = {
  "README.md": (
    "Phase 155 closure — Test Suite Consolidation",
    "Phase 155 replaced the former monolithic-regression-first",
  ),
  "docs/design.md": (
    "Phase 155 Test Suite Consolidation 設計",
    "audit-only 5件",
  ),
  "docs/development_log.md": (
    "Phase 155 Test Suite Consolidation 完了",
    "5/5 PASS",
  ),
  "docs/roadmap.md": (
    "Phase 155 — Test Suite Consolidation — 完了",
    "Phase 156 — Reference statement relevance / minimal display",
  ),
  "docs/proof_records.md": (
    "Phase 155 test-suite provenance record",
    "Reference statement necessity / minimal display",
  ),
}


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--repo-root",
    type=Path,
    default=Path.cwd(),
  )
  args = parser.parse_args()

  root = args.repo_root.resolve()

  for relative_path, needles in (
    REQUIRED.items()
  ):
    path = root / relative_path
    text = path.read_text(
      encoding="utf-8-sig"
    )

    for needle in needles:
      if needle not in text:
        raise SystemExit(
          relative_path
          + " missing required closure text: "
          + needle
        )

  roadmap = (
    root
    / "docs"
    / "roadmap.md"
  ).read_text(
    encoding="utf-8-sig"
  )

  if (
    "### Phase 155 — Reference statement relevance / minimal display"
    in roadmap
  ):
    raise SystemExit(
      "Roadmap still assigns Reference relevance to Phase155."
    )

  print(
    "Phase155 closure documentation verification: PASS"
  )
  print(
    "Phase156 boundary: Reference statement relevance / minimal display"
  )
  print(
    "Production changes: none"
  )
  print(
    "Monolithic repository-wide pytest: NOT run"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
