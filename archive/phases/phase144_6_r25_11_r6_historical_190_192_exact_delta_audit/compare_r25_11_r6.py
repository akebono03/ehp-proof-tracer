from collections import Counter
import json
from pathlib import Path
import sys


EXPECTED_HISTORICAL_TOTAL = 190
EXPECTED_CURRENT_TOTAL = 192


def load(path):
  return json.loads(
    Path(
      path
    ).read_text(
      encoding="utf-8"
    )
  )


def identity_signature(row):
  return (
    row["n"],
    row["k"],
    row["argument_role"],
    row["discourse_role"],
    row["statement_type"],
    row["rendered"],
    row["provider_anchor"],
    row["placement"],
    row["provider_key_count"],
  )


def insertion_signature(row):
  return (
    row["n"],
    row["k"],
    row["argument_role"],
    row["discourse_role"],
    row["statement_type"],
    row["rendered"],
    row["provider_anchor"],
    row["placement"],
    row["provider_key_count"],
    row["insertable"],
  )


def group_name(signature):
  n = signature[
    0
  ]
  k = signature[
    1
  ]
  return f"pi_{n + k}^{n}"


def print_signature(
  prefix,
  signature,
  multiplicity,
):
  print(
    f"{prefix} multiplicity={multiplicity}"
  )
  print(
    f"  group={group_name(signature)} "
    f"argument_role={signature[2]} "
    f"discourse={signature[3]}"
  )
  print(
    f"  type={signature[4]}"
  )
  print(
    f"  provider_anchor={signature[6]} "
    f"placement={signature[7]} "
    f"provider_key_count={signature[8]}"
  )
  print(
    f"  rendered={signature[5]}"
  )


def expanded(counter):
  result = []
  for signature, count in counter.items():
    result.extend(
      [
        signature
      ]
      * count
    )
  return tuple(
    result
  )


def main():
  if len(
    sys.argv
  ) != 3:
    raise SystemExit(
      "usage: compare_r25_11_r6.py HISTORICAL_JSON CURRENT_JSON"
    )

  historical = load(
    sys.argv[
      1
    ]
  )
  current = load(
    sys.argv[
      2
    ]
  )

  print("=" * 78)
  print("A. Historical baseline validation")
  print("=" * 78)
  print(
    f"historical_selected={historical['selected_total']}"
  )
  print(
    f"expected_historical={EXPECTED_HISTORICAL_TOTAL}"
  )
  print(
    "historical_group_counts="
    + json.dumps(
      historical[
        "group_counts"
      ],
      ensure_ascii=False,
      sort_keys=True,
    )
  )
  print(
    f"historical_participating={historical['participating']}"
  )
  print(
    f"historical_detached={historical['detached']}"
  )
  print(
    "historical_detached_insertable="
    + str(
      historical[
        "detached_insertable"
      ]
    )
  )

  if (
    historical[
      "selected_total"
    ]
    != EXPECTED_HISTORICAL_TOTAL
  ):
    print()
    print(
      "STOP: the selected historical commit does not reproduce "
      "the retained 190 baseline."
    )
    print(
      "No 190->192 exact-delta claim is made."
    )
    raise SystemExit(
      2
    )

  if (
    current[
      "selected_total"
    ]
    != EXPECTED_CURRENT_TOTAL
  ):
    print()
    print(
      "STOP: the current checkout does not reproduce 192."
    )
    print(
      "No 190->192 exact-delta claim is made."
    )
    raise SystemExit(
      3
    )

  historical_identity = Counter(
    identity_signature(
      row
    )
    for row in historical[
      "rows"
    ]
  )
  current_identity = Counter(
    identity_signature(
      row
    )
    for row in current[
      "rows"
    ]
  )

  added = (
    current_identity
    - historical_identity
  )
  removed = (
    historical_identity
    - current_identity
  )

  print()
  print("=" * 78)
  print("B. Exact semantic selected-set delta")
  print("=" * 78)
  print(
    f"added_count={sum(added.values())}"
  )
  print(
    f"removed_count={sum(removed.values())}"
  )
  print(
    "net_delta="
    + f"{sum(added.values()) - sum(removed.values()):+d}"
  )

  for index, (
    signature,
    count,
  ) in enumerate(
    sorted(
      added.items(),
      key=lambda item: repr(
        item[
          0
        ]
      ),
    )
  ):
    print_signature(
      f"ADDED[{index}]",
      signature,
      count,
    )

  for index, (
    signature,
    count,
  ) in enumerate(
    sorted(
      removed.items(),
      key=lambda item: repr(
        item[
          0
        ]
      ),
    )
  ):
    print_signature(
      f"REMOVED[{index}]",
      signature,
      count,
    )

  historical_by_identity = {}
  current_by_identity = {}
  for row in historical[
    "rows"
  ]:
    historical_by_identity.setdefault(
      identity_signature(
        row
      ),
      [],
    ).append(
      row[
        "insertable"
      ]
    )
  for row in current[
    "rows"
  ]:
    current_by_identity.setdefault(
      identity_signature(
        row
      ),
      [],
    ).append(
      row[
        "insertable"
      ]
    )

  insertion_changes = []
  for signature in (
    set(
      historical_by_identity
    )
    & set(
      current_by_identity
    )
  ):
    old = sorted(
      historical_by_identity[
        signature
      ]
    )
    new = sorted(
      current_by_identity[
        signature
      ]
    )
    if old != new:
      insertion_changes.append(
        (
          signature,
          old,
          new,
        )
      )

  print()
  print("=" * 78)
  print("C. Insertion-state changes for semantically retained rows")
  print("=" * 78)
  print(
    f"insertion_change_signatures={len(insertion_changes)}"
  )
  for index, (
    signature,
    old,
    new,
  ) in enumerate(
    sorted(
      insertion_changes,
      key=lambda item: repr(
        item[
          0
        ]
      ),
    )
  ):
    print_signature(
      f"INSERTION_CHANGE[{index}]",
      signature,
      1,
    )
    print(
      f"  historical_insertable={old}"
    )
    print(
      f"  current_insertable={new}"
    )

  print()
  print("=" * 78)
  print("D. Exact-delta completion guard")
  print("=" * 78)
  print(
    f"historical_total={historical['selected_total']}"
  )
  print(
    f"current_total={current['selected_total']}"
  )
  print(
    f"added={sum(added.values())}"
  )
  print(
    f"removed={sum(removed.values())}"
  )
  print(
    "exact_net_delta="
    + f"{sum(added.values()) - sum(removed.values()):+d}"
  )

  if (
    sum(
      added.values()
    )
    - sum(
      removed.values()
    )
    != 2
  ):
    raise SystemExit(
      "semantic Counter delta does not explain the +2 population"
    )

  print(
    "R25-11-R6 exact historical delta: PASS"
  )


if __name__ == "__main__":
  main()
