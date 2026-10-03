from __future__ import annotations

import argparse
import json
from pathlib import Path

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _render(
  n: int,
  k: int,
  depth: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=depth,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase156_r6_3_audit_output"
    ),
  )
  args = parser.parse_args()
  args.output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  exceptions = []

  for n in range(
    2,
    16,
  ):
    for k in range(
      0,
      8,
    ):
      for depth in (
        2,
        3,
      ):
        try:
          _render(
            n,
            k,
            depth,
          )
        except Exception as exc:
          exceptions.append(
            (
              n,
              k,
              depth,
              type(
                exc
              ).__name__,
              str(
                exc
              ),
            )
          )

  pi6_depth2 = _render(
    3,
    3,
    2,
  )
  pi6_depth3 = _render(
    3,
    3,
    3,
  )

  canonical_reason = (
    r"$\operatorname{ord}(\eta_{3}^{3})=2$ "
    r"かつ $2\nu'=\eta_{3}^{3}$ より, "
  )
  expanded_reason_order = (
    r"\operatorname{ord}(\eta_{3}\eta_{4}\eta_{5})"
  )
  expanded_reason_equality = (
    r"2\nu'=\eta_{3}\eta_{4}\eta_{5}"
  )

  checks = {}

  for label, rendered in (
    (
      "depth2",
      pi6_depth2,
    ),
    (
      "depth3",
      pi6_depth3,
    ),
  ):
    checks[
      label
    ] = {
      "canonical_reason_present": (
        canonical_reason
        in rendered
      ),
      "expanded_reason_order_absent": (
        expanded_reason_order
        not in rendered
      ),
      "equation3_present": (
        r"$2\nu' = \eta_{3}^{3}\tag{3}$"
        in rendered
      ),
      "reference_53_canonical_present": (
        r"$2\nu' = \eta_{3}\eta_{4}\eta_{5}$"
        in rendered
      ),
    }

  passed = (
    not exceptions
    and all(
      check[
        "canonical_reason_present"
      ]
      and check[
        "expanded_reason_order_absent"
      ]
      and check[
        "equation3_present"
      ]
      and check[
        "reference_53_canonical_present"
      ]
      for check in checks.values()
    )
  )

  result = {
    "groups": 112,
    "depths": [
      2,
      3,
    ],
    "exceptions": len(
      exceptions
    ),
    "pi6": checks,
    "pass": passed,
  }

  (
    args.output_dir
    / "phase156_r6_3_result.json"
  ).write_text(
    json.dumps(
      result,
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
    "Phase156-R6-3 — reason prose canonicalization"
  )
  print(
    "=" * 78
  )
  print(
    "groups: 112"
  )
  print(
    "depths: 2, 3"
  )
  print(
    "exceptions:",
    len(
      exceptions
    ),
  )

  for label, check in checks.items():
    print(
      label
      + " canonical reason present:",
      check[
        "canonical_reason_present"
      ],
    )
    print(
      label
      + " expanded reason order absent:",
      check[
        "expanded_reason_order_absent"
      ],
    )
    print(
      label
      + " equation (3) present:",
      check[
        "equation3_present"
      ],
    )
    print(
      label
      + " (5.3) canonical present:",
      check[
        "reference_53_canonical_present"
      ],
    )

  print()
  print(
    "PASS"
    if passed
    else "FAIL"
  )
  print(
    "=" * 78
  )

  return (
    0
    if passed
    else 1
  )


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
