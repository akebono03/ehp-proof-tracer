from __future__ import annotations

import argparse
import json
import re
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


def _headers(
  rendered: str,
) -> list[
  str
]:
  return re.findall(
    r"\*\*\[R\d+\] ([^\n]+?)\.\*\*",
    rendered,
  )


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase156_r5_repair12_audit_output"
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

  checks = {}

  for depth in (
    2,
    3,
  ):
    rendered = _render(
      3,
      3,
      depth,
    )
    headers = _headers(
      rendered
    )
    numbers = [
      int(
        number
      )
      for number in re.findall(
        r"\*\*\[R(\d+)\] ",
        rendered,
      )
    ]

    checks[
      "depth"
      + str(
        depth
      )
    ] = {
      "proposition_51_absent": (
        "Proposition 5.1"
        not in headers
      ),
      "reference_53_present": (
        "(5.3)"
        in headers
      ),
      "proposition_53_present": (
        "Proposition 5.3"
        in headers
      ),
      "lemma_54_present": (
        "Lemma 5.4"
        in headers
      ),
      "reference_52_present": (
        "(5.2)"
        in headers
      ),
      "compact_numbers": (
        numbers
        == list(
          range(
            1,
            len(
              numbers
            )
            + 1,
          )
        )
      ),
    }

  passed = (
    not exceptions
    and all(
      check[
        "proposition_51_absent"
      ]
      and check[
        "reference_53_present"
      ]
      and check[
        "proposition_53_present"
      ]
      and check[
        "lemma_54_present"
      ]
      and check[
        "reference_52_present"
      ]
      and check[
        "compact_numbers"
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
    "pi6_3": checks,
    "pass": passed,
  }

  (
    args.output_dir
    / "phase156_r5_repair12_result.json"
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
    "Phase156-R5 repair12 — Reference frontier"
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
      + " Proposition 5.1 absent:",
      check[
        "proposition_51_absent"
      ],
    )
    print(
      label
      + " (5.3) present:",
      check[
        "reference_53_present"
      ],
    )
    print(
      label
      + " Proposition 5.3 present:",
      check[
        "proposition_53_present"
      ],
    )
    print(
      label
      + " Lemma 5.4 present:",
      check[
        "lemma_54_present"
      ],
    )
    print(
      label
      + " (5.2) present:",
      check[
        "reference_52_present"
      ],
    )
    print(
      label
      + " compact numbering:",
      check[
        "compact_numbers"
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
