from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--repo-root",
    type=Path,
    default=Path.cwd(),
  )
  parser.add_argument(
    "--plan",
    type=Path,
    required=True,
  )
  args = parser.parse_args()

  repo_root = args.repo_root.resolve()
  plan_path = args.plan.resolve()

  if not plan_path.exists():
    raise SystemExit(
      "Existing Closure-R3 shard plan not found: "
      + str(
        plan_path
      )
    )

  plan = json.loads(
    plan_path.read_text(
      encoding="utf-8"
    )
  )

  expected = {
    "shard_count": 8,
    "routine_test_count": 10392,
    "routine_file_count": 837,
    "audit_only_count": 5,
  }

  for key, value in expected.items():
    actual = plan.get(
      key
    )

    if actual != value:
      raise SystemExit(
        "Existing shard plan does not match "
        + key
        + ": expected "
        + repr(
          value
        )
        + ", found "
        + repr(
          actual
        )
      )

  manifest_path = (
    repo_root
    / "tests"
    / "phase155_audit_only_nodeids.txt"
  )

  audit_only = {
    line.strip()
    for line in manifest_path.read_text(
      encoding="utf-8"
    ).splitlines()
    if line.strip()
  }

  if len(
    audit_only
  ) != 5:
    raise SystemExit(
      "Expected exactly 5 audit-only nodeids; "
      + str(
        len(
          audit_only
        )
      )
      + " found."
    )

  assigned_shards = set(
    int(
      value
    )
    for value in plan[
      "file_to_shard"
    ].values()
  )

  if assigned_shards != set(
    range(
      1,
      9,
    )
  ):
    raise SystemExit(
      "Existing shard plan does not use all 8 shards."
    )

  print(
    "Existing Closure-R3 plan validated."
  )
  print(
    "Routine tests:",
    plan[
      "routine_test_count"
    ],
  )
  print(
    "Routine files:",
    plan[
      "routine_file_count"
    ],
  )
  print(
    "Audit-only excluded:",
    plan[
      "audit_only_count"
    ],
  )
  print(
    "Shards:",
    plan[
      "shard_count"
    ],
  )
  print(
    "Collection rerun required: no"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
