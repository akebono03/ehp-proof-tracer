from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path


DURATION_RE = re.compile(
  r"^(?P<seconds>\d+(?:\.\d+)?)s\s+"
  r"(?:call|setup|teardown)\s+"
  r"(?P<nodeid>tests/[^\s]+::[^\s]+)\s*$"
)

REPLACED_EXTREME_NODEIDS = {
  (
    "tests/test_phase97_single_found_calculation_to_report_api.py::"
    "test_phase97_3_aggregate_found_preserves_goal_source_provenance"
  ),
  (
    "tests/test_phase95_top_level_calculation_orchestration.py::"
    "test_phase95_18_preserves_multiple_aggregate_candidates_in_registration_order"
  ),
  (
    "tests/test_phase97_not_found_multiple_results_top_level_handling.py::"
    "test_phase97_4_multiple_aggregate_results_preserve_goal_source_order"
  ),
}


def _file_nodeid(
  nodeid: str,
) -> str:
  return nodeid.split(
    "::",
    1,
  )[0].replace(
    "\\",
    "/",
  )


def _historical_durations(
  path: Path,
  current_nodeids: set[str],
) -> dict[str, float]:
  if not path.exists():
    return {}

  result = {}

  for line in path.read_text(
    encoding="utf-8",
    errors="replace",
  ).splitlines():
    match = DURATION_RE.match(
      line.strip()
    )

    if match is None:
      continue

    nodeid = match.group(
      "nodeid"
    )

    if (
      nodeid not in current_nodeids
      or nodeid in REPLACED_EXTREME_NODEIDS
    ):
      continue

    seconds = float(
      match.group(
        "seconds"
      )
    )

    result[
      nodeid
    ] = max(
      result.get(
        nodeid,
        0.0,
      ),
      seconds,
    )

  return result


def _file_weights(
  nodeids: list[str],
  historical: dict[str, float],
) -> tuple[
  dict[str, float],
  Counter,
]:
  counts = Counter(
    _file_nodeid(
      nodeid
    )
    for nodeid in nodeids
  )

  historical_by_file = Counter()

  for nodeid, seconds in (
    historical.items()
  ):
    historical_by_file[
      _file_nodeid(
        nodeid
      )
    ] += seconds

  weights = {}

  for file_nodeid, count in counts.items():
    baseline = max(
      1.0,
      count * 0.11,
    )
    known = historical_by_file.get(
      file_nodeid,
      0.0,
    )

    weights[
      file_nodeid
    ] = baseline + known

  return (
    weights,
    counts,
  )


def _ordered_files(
  counts: Counter,
) -> list[str]:
  return sorted(
    counts
  )


def _contiguous_partition(
  files: list[str],
  weights: dict[str, float],
  shard_count: int,
) -> list[list[str]]:
  if shard_count <= 0:
    raise ValueError(
      "shard_count must be positive"
    )

  if not files:
    return [
      []
      for _ in range(
        shard_count
      )
    ]

  shard_count = min(
    shard_count,
    len(
      files
    ),
  )

  total_weight = sum(
    weights[
      file_nodeid
    ]
    for file_nodeid in files
  )

  shards = []
  cursor = 0
  remaining_weight = total_weight

  for shard_index in range(
    shard_count
  ):
    shards_left = (
      shard_count
      - shard_index
    )
    files_left = (
      len(
        files
      )
      - cursor
    )

    if shards_left == 1:
      shards.append(
        files[
          cursor:
        ]
      )
      break

    target = (
      remaining_weight
      / shards_left
    )

    current = []
    current_weight = 0.0
    must_leave = (
      shards_left
      - 1
    )

    while (
      cursor
      < len(
        files
      ) - must_leave
    ):
      file_nodeid = files[
        cursor
      ]
      weight = weights[
        file_nodeid
      ]

      if (
        current
        and current_weight + weight
        > target
      ):
        before_gap = abs(
          target
          - current_weight
        )
        after_gap = abs(
          target
          - (
            current_weight
            + weight
          )
        )

        if before_gap <= after_gap:
          break

      current.append(
        file_nodeid
      )
      current_weight += weight
      cursor += 1

      if current_weight >= target:
        break

    if not current:
      file_nodeid = files[
        cursor
      ]
      current.append(
        file_nodeid
      )
      current_weight += weights[
        file_nodeid
      ]
      cursor += 1

    shards.append(
      current
    )
    remaining_weight -= current_weight

  return shards


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--collection",
    type=Path,
    required=True,
  )
  parser.add_argument(
    "--historical-log",
    type=Path,
    required=True,
  )
  parser.add_argument(
    "--audit-manifest",
    type=Path,
    required=True,
  )
  parser.add_argument(
    "--shard-count",
    type=int,
    default=8,
  )
  parser.add_argument(
    "--output",
    type=Path,
    required=True,
  )
  args = parser.parse_args()

  collection = json.loads(
    args.collection.read_text(
      encoding="utf-8"
    )
  )
  nodeids = list(
    collection[
      "nodeids"
    ]
  )

  audit_only = {
    line.strip()
    for line in args.audit_manifest.read_text(
      encoding="utf-8"
    ).splitlines()
    if line.strip()
  }

  if len(
    audit_only
  ) != 5:
    raise SystemExit(
      "Expected exactly 5 Phase155 audit-only nodeids; "
      f"found {len(audit_only)}"
    )

  overlap = (
    set(
      nodeids
    )
    & audit_only
  )

  if overlap:
    raise SystemExit(
      "Audit-only nodeids leaked into routine collection: "
      + repr(
        sorted(
          overlap
        )
      )
    )

  historical = _historical_durations(
    args.historical_log,
    set(
      nodeids
    ),
  )

  weights, counts = _file_weights(
    nodeids,
    historical,
  )
  files = _ordered_files(
    counts
  )

  shards = _contiguous_partition(
    files,
    weights,
    args.shard_count,
  )

  file_to_shard = {}

  shard_rows = []

  for index, shard_files in enumerate(
    shards,
    start=1,
  ):
    for file_nodeid in shard_files:
      file_to_shard[
        file_nodeid
      ] = index

    shard_rows.append(
      {
        "index": index,
        "file_count": len(
          shard_files
        ),
        "test_count": sum(
          counts[
            file_nodeid
          ]
          for file_nodeid in shard_files
        ),
        "estimated_weight_seconds": round(
          sum(
            weights[
              file_nodeid
            ]
            for file_nodeid in shard_files
          ),
          2,
        ),
        "first_file": (
          shard_files[
            0
          ]
          if shard_files
          else None
        ),
        "last_file": (
          shard_files[
            -1
          ]
          if shard_files
          else None
        ),
      }
    )

  planned_files = set(
    file_to_shard
  )

  if planned_files != set(
    files
  ):
    raise SystemExit(
      "Shard plan does not cover exactly "
      "the collected routine test files."
    )

  payload = {
    "version": 1,
    "shard_count": len(
      shards
    ),
    "routine_test_count": len(
      nodeids
    ),
    "routine_file_count": len(
      files
    ),
    "audit_only_count": len(
      audit_only
    ),
    "historical_duration_nodeids_used": len(
      historical
    ),
    "partition": (
      "contiguous_weighted_by_test_count_and_current_historical_slow_rows"
    ),
    "file_to_shard": file_to_shard,
    "shards": shard_rows,
  }

  args.output.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  args.output.write_text(
    json.dumps(
      payload,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  print(
    "Phase155 Closure-R3 shard plan"
  )
  print(
    "Routine tests:",
    len(
      nodeids
    ),
  )
  print(
    "Routine files:",
    len(
      files
    ),
  )
  print(
    "Audit-only excluded:",
    len(
      audit_only
    ),
  )
  print(
    "Shards:",
    len(
      shards
    ),
  )
  print(
    "Historical slow nodeids used:",
    len(
      historical
    ),
  )
  print("")

  for row in shard_rows:
    print(
      "Shard "
      + str(
        row[
          "index"
        ]
      )
      + ": "
      + str(
        row[
          "test_count"
        ]
      )
      + " tests, "
      + str(
        row[
          "file_count"
        ]
      )
      + " files, estimated weight "
      + str(
        row[
          "estimated_weight_seconds"
        ]
      )
      + "s"
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
