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


def _pi6_checks(
  depth: int,
) -> dict[
  str,
  bool,
]:
  rendered = _render(
    3,
    3,
    depth,
  )
  reference_part, body_tail = rendered.split(
    "まず",
    1,
  )
  body = "まず" + body_tail

  return {
    "reference_53": "(5.3)" in reference_part,
    "reference_lemma52": "Lemma 5.2.**" in reference_part,
    "body_lemma52": "Lemma 5.2" in body,
    "body_bracket": (
      "\\nu' \\in "
      "\\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}"
      in body
    ),
    "body_eta3_zero": "$2\\eta_{3} = 0$" in body,
    "body_nu_definition": "$\\nu'$ を定める." in body,
  }


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase156_r5_repair7_audit_output"
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

  depth2 = _pi6_checks(
    2
  )
  depth3 = _pi6_checks(
    3
  )

  def good(
    checks: dict[
      str,
      bool,
    ],
  ) -> bool:
    return (
      checks[
        "reference_53"
      ]
      and not checks[
        "reference_lemma52"
      ]
      and not checks[
        "body_lemma52"
      ]
      and not checks[
        "body_bracket"
      ]
      and not checks[
        "body_eta3_zero"
      ]
      and not checks[
        "body_nu_definition"
      ]
    )

  passed = (
    not exceptions
    and good(
      depth2
    )
    and good(
      depth3
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
    "depth2": depth2,
    "depth3": depth3,
    "pass": passed,
  }

  (
    args.output_dir
    / "phase156_r5_repair7_result.json"
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
    "Phase156-R5 repair7 — Reference boundary filter order"
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

  for label, checks in (
    (
      "depth2",
      depth2,
    ),
    (
      "depth3",
      depth3,
    ),
  ):
    print(
      label
      + " Reference (5.3):",
      checks[
        "reference_53"
      ],
    )
    print(
      label
      + " Reference Lemma 5.2:",
      checks[
        "reference_lemma52"
      ],
    )
    print(
      label
      + " body Lemma 5.2:",
      checks[
        "body_lemma52"
      ],
    )
    print(
      label
      + " body bracket definition:",
      checks[
        "body_bracket"
      ],
    )
    print(
      label
      + " body 2 eta_3 = 0:",
      checks[
        "body_eta3_zero"
      ],
    )
    print(
      label
      + " body nu-prime definition:",
      checks[
        "body_nu_definition"
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
