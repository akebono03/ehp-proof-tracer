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
      "phase156_r5_repair5_audit_output"
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

  rendered = _render(
    3,
    3,
    2,
  )
  reference_part, body_tail = rendered.split(
    "まず",
    1,
  )
  body = "まず" + body_tail

  bracket = (
    "$\\nu' \\in "
    "\\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}$"
  )
  precondition = "$2\\eta_{3} = 0$"
  application = (
    "この前提条件のもとで, "
    "Lemma 5.2 の $\\beta$ を $\\nu'$ として適用する."
  )

  source_ok = (
    "(5.3)" in reference_part
    and "Lemma 5.2.**"
    not in reference_part
  )
  order_ok = (
    bracket in body
    and precondition in body
    and application in body
    and body.index(
      bracket
    ) < body.index(
      precondition
    ) < body.index(
      application
    )
  )

  passed = (
    not exceptions
    and source_ok
    and order_ok
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
    "pi6_3_reference_53_present": "(5.3)" in reference_part,
    "pi6_3_reference_lemma52_header_present": (
      "Lemma 5.2.**"
      in reference_part
    ),
    "pi6_3_body_order_correct": order_ok,
    "pass": passed,
  }

  (
    args.output_dir
    / "phase156_r5_repair5_result.json"
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
    "Phase156-R5 repair5 — (5.3) source / Lemma 5.2 proof dependency"
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
  print(
    "pi_6^3 Reference has (5.3):",
    result[
      "pi6_3_reference_53_present"
    ],
  )
  print(
    "pi_6^3 Reference has Lemma 5.2 header:",
    result[
      "pi6_3_reference_lemma52_header_present"
    ],
  )
  print(
    "pi_6^3 body order bracket -> precondition -> Lemma 5.2:",
    order_ok,
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
