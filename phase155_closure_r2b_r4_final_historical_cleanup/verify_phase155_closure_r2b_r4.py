from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


FOCUSED = (
  "tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py::test_phase144_6_r5_42_nonunique_phase41_arguments_are_deterministic",
  "tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py::test_phase144_6_r5_43_10_pi6_transport_connector_is_rendered_between_c2_and_c3",
  "tests/test_phase155_audit_boundary.py",
)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--repo-root", type=Path, default=Path.cwd())
  args = parser.parse_args()

  repo_root = args.repo_root.resolve()
  manifest_path = repo_root / "tests" / "phase155_audit_only_nodeids.txt"

  nodeids = tuple(
    line.strip()
    for line in manifest_path.read_text(encoding="utf-8").splitlines()
    if line.strip()
  )

  if len(nodeids) != 2:
    raise SystemExit(
      "Expected exactly 2 audit-only nodeids after R2B-R4; "
      f"found {len(nodeids)}"
    )

  print("Final audit-only boundary: 2")
  for nodeid in nodeids:
    print(" -", nodeid)
  print("")
  print("Run only two lightweight replacements + boundary tests.")

  result = subprocess.run(
    [
      sys.executable,
      "-m",
      "pytest",
      *FOCUSED,
      "-q",
      "--tb=line",
      "--durations=10",
      "-p",
      "no:cacheprovider",
    ],
    cwd=repo_root,
  )

  if result.returncode != 0:
    return result.returncode

  print("")
  print("Closure-R2B-R4 focused verification: PASS")
  print("Heavy audit-only tests executed: 0")
  print("Repository-wide pytest: NOT run")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
