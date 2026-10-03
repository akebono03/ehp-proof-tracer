from __future__ import annotations

import argparse
import json
from pathlib import Path


SHARD_COUNT = 4
EXPECTED_GROUPS_PER_SHARD = 28
EXPECTED_TOTAL_GROUPS = 112


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output-dir",
    type=Path,
    required=True,
  )
  args = parser.parse_args()

  shard_results = []
  missing = []

  for shard_index in range(
    SHARD_COUNT
  ):
    path = (
      args.output_dir
      / (
        "phase156_r6_shard_"
        + str(
          shard_index
        )
        + "_result.json"
      )
    )

    if not path.exists():
      missing.append(
        str(
          path
        )
      )
      continue

    shard_results.append(
      json.loads(
        path.read_text(
          encoding="utf-8",
        )
      )
    )

  all_group_keys = []
  total_exceptions = 0
  total_violations = 0
  shard_failures = []

  for result in shard_results:
    shard_index = result[
      "shard_index"
    ]

    if result[
      "groups"
    ] != EXPECTED_GROUPS_PER_SHARD:
      shard_failures.append(
        (
          shard_index,
          "group_count",
          result[
            "groups"
          ],
        )
      )

    if not result[
      "pass"
    ]:
      shard_failures.append(
        (
          shard_index,
          "shard_pass",
          False,
        )
      )

    total_exceptions += result[
      "exceptions"
    ]
    total_violations += result[
      "violations"
    ]

    all_group_keys.extend(
      (
        row[
          "n"
        ],
        row[
          "k"
        ],
      )
      for row in result[
        "group_keys"
      ]
    )

  unique_group_keys = set(
    all_group_keys
  )
  duplicate_count = (
    len(
      all_group_keys
    )
    - len(
      unique_group_keys
    )
  )

  expected_group_keys = {
    (
      n,
      k,
    )
    for n in range(
      2,
      16,
    )
    for k in range(
      0,
      8,
    )
  }
  missing_group_keys = tuple(
    sorted(
      expected_group_keys
      - unique_group_keys
    )
  )
  unexpected_group_keys = tuple(
    sorted(
      unique_group_keys
      - expected_group_keys
    )
  )

  passed = (
    not missing
    and len(
      shard_results
    )
    == SHARD_COUNT
    and not shard_failures
    and len(
      all_group_keys
    )
    == EXPECTED_TOTAL_GROUPS
    and len(
      unique_group_keys
    )
    == EXPECTED_TOTAL_GROUPS
    and duplicate_count
    == 0
    and not missing_group_keys
    and not unexpected_group_keys
    and total_exceptions
    == 0
    and total_violations
    == 0
  )

  payload = {
    "phase": "Phase156-R6",
    "shards": len(
      shard_results
    ),
    "expected_shards": SHARD_COUNT,
    "groups": len(
      all_group_keys
    ),
    "unique_groups": len(
      unique_group_keys
    ),
    "duplicate_groups": (
      duplicate_count
    ),
    "missing_groups": [
      {
        "n": n,
        "k": k,
      }
      for n, k in missing_group_keys
    ],
    "unexpected_groups": [
      {
        "n": n,
        "k": k,
      }
      for n, k in unexpected_group_keys
    ],
    "exceptions": total_exceptions,
    "violations": total_violations,
    "missing_shard_files": missing,
    "shard_failures": (
      shard_failures
    ),
    "pass": passed,
  }

  (
    args.output_dir
    / "phase156_r6_aggregate_result.json"
  ).write_text(
    json.dumps(
      payload,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  print(
    "=" * 78
  )
  print(
    "Phase156-R6 — shard aggregate"
  )
  print(
    "=" * 78
  )
  print(
    "shards:",
    len(
      shard_results
    ),
    "/",
    SHARD_COUNT,
  )
  print(
    "groups:",
    len(
      all_group_keys
    ),
  )
  print(
    "unique groups:",
    len(
      unique_group_keys
    ),
  )
  print(
    "duplicate groups:",
    duplicate_count,
  )
  print(
    "missing groups:",
    len(
      missing_group_keys
    ),
  )
  print(
    "unexpected groups:",
    len(
      unexpected_group_keys
    ),
  )
  print(
    "exceptions:",
    total_exceptions,
  )
  print(
    "violations:",
    total_violations,
  )
  print(
    "=" * 78
  )

  if passed:
    print(
      "PASS: four shards cover exactly the 112-group population "
      "with zero regression violations."
    )
    return 0

  print(
    "FAIL: sharded regression aggregate did not close."
  )
  return 1


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
