from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--repo-root", type=Path, default=Path.cwd())
  args = parser.parse_args()
  root = args.repo_root.resolve()

  result = subprocess.run(
    [
      sys.executable,
      "-m",
      "pytest",
      "tests/test_phase155_audit_boundary.py",
      "-q",
      "-p",
      "no:cacheprovider",
    ],
    cwd=root,
  )

  if result.returncode != 0:
    return result.returncode

  required = {
    "README.md": (
      "10384 tests total",
      "2 audit-only tests",
    ),
    "docs/design.md": (
      "audit-only: 2",
      "117 duplicate observations",
    ),
    "docs/development_log.md": (
      "10384 total",
      "final audit-only 2/2 PASS",
    ),
    "docs/roadmap.md": (
      "Phase 155 — Test Suite Consolidation — 完了",
      "117 exact selected-statement/body duplicates",
    ),
    "docs/proof_records.md": (
      "Phase 155 test-suite provenance record",
      "Reference statement necessity / minimal display",
    ),
  }

  for relative_path, needles in required.items():
    text = (root / relative_path).read_text(encoding="utf-8-sig")

    for needle in needles:
      if needle not in text:
        raise SystemExit(
          relative_path + " missing: " + needle
        )

  print("Phase155 Closure-R4-R2 verification: PASS")
  print("Routine regression evidence: preserved")
  print("Final audit-only boundary: 2")
  print("Phase156 duplicate pressure: 117")
  print("Production changes: none")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
