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


def _headers(
  n: int,
  k: int,
  depth: int,
) -> list[str]:
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
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )
  reference_part = rendered.split(
    "まず",
    1,
  )[0]

  return re.findall(
    r"\*\*\[R\d+\] ([^\n]+?)\.\*\*",
    reference_part,
  )


def run_audit(
  output_dir: Path,
) -> dict[str, object]:
  output_dir.mkdir(
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
          _headers(
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

  pi6_depth2 = _headers(
    3,
    3,
    2,
  )
  pi6_depth3 = _headers(
    3,
    3,
    3,
  )

  passed = (
    not exceptions
    and pi6_depth2.count(
      "(5.3)"
    )
    == 1
    and pi6_depth3.count(
      "(5.3)"
    )
    == 1
    and pi6_depth2.count(
      "Lemma 5.2"
    )
    == 1
    and pi6_depth3.count(
      "Lemma 5.2"
    )
    == 1
    and "(5.3) / Lemma 5.2"
    not in pi6_depth2
    and "(5.3) / Lemma 5.2"
    not in pi6_depth3
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
    "pi6_depth2_headers": pi6_depth2,
    "pi6_depth3_headers": pi6_depth3,
    "pi6_depth2_53_count": pi6_depth2.count(
      "(5.3)"
    ),
    "pi6_depth3_53_count": pi6_depth3.count(
      "(5.3)"
    ),
    "pi6_depth2_lemma52_count": pi6_depth2.count(
      "Lemma 5.2"
    ),
    "pi6_depth3_lemma52_count": pi6_depth3.count(
      "Lemma 5.2"
    ),
    "pass": passed,
  }

  (
    output_dir
    / "phase156_r5_repair4_result.json"
  ).write_text(
    json.dumps(
      result,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  summary = "\n".join(
    (
      "=" * 78,
      "Phase156-R5 repair4 — bridge Reference inference",
      "=" * 78,
      "groups: 112",
      "depths: 2, 3",
      "exceptions: "
      + str(
        len(
          exceptions
        )
      ),
      "pi_6^3 depth2 (5.3) count: "
      + str(
        pi6_depth2.count(
          "(5.3)"
        )
      ),
      "pi_6^3 depth3 (5.3) count: "
      + str(
        pi6_depth3.count(
          "(5.3)"
        )
      ),
      "pi_6^3 depth2 Lemma 5.2 count: "
      + str(
        pi6_depth2.count(
          "Lemma 5.2"
        )
      ),
      "pi_6^3 depth3 Lemma 5.2 count: "
      + str(
        pi6_depth3.count(
          "Lemma 5.2"
        )
      ),
      "",
      (
        "PASS"
        if passed
        else "FAIL"
      ),
      "=" * 78,
      "",
    )
  )

  (
    output_dir
    / "phase156_r5_repair4_summary.txt"
  ).write_text(
    summary,
    encoding="utf-8",
  )
  print(
    summary
  )

  return result


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase156_r5_repair4_audit_output"
    ),
  )
  args = parser.parse_args()
  result = run_audit(
    args.output_dir
  )
  return (
    0
    if result[
      "pass"
    ]
    else 1
  )


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
