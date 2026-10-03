from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _presentation(
  n: int,
  k: int,
  depth: int,
):
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
  return build_toda_group_proof_presentation(
    replay
  )


def _render(
  n: int,
  k: int,
  depth: int,
) -> str:
  return render_toda_group_proof_narrative_markdown(
    _presentation(
      n,
      k,
      depth,
    )
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
      "phase156_r5_repair11_audit_output"
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
    raw = _presentation(
      3,
      3,
      depth,
    )
    closure = (
      build_toda_group_proof_narrative_semantic_closure_presentation(
        raw
      )
    )
    raw_entries = build_toda_group_proof_narrative_reference_entries(
      closure
    )
    raw_locators = {
      entry.reference.locator
      for entry in raw_entries
    }

    rendered = render_toda_group_proof_narrative_markdown(
      raw
    )
    headers = _headers(
      rendered
    )

    checks[
      "depth"
      + str(
        depth
      )
    ] = {
      "raw_has_proposition_51": (
        "Proposition 5.1"
        in raw_locators
      ),
      "public_has_proposition_51": (
        "Proposition 5.1"
        in headers
      ),
      "public_has_53": (
        "(5.3)"
        in headers
      ),
      "public_has_52": (
        "(5.2)"
        in headers
      ),
      "compact_numbers": (
        [
          int(
            number
          )
          for number in re.findall(
            r"\*\*\[R(\d+)\] ",
            rendered,
          )
        ]
        == list(
          range(
            1,
            len(
              headers
            )
            + 1,
          )
        )
      ),
    }

  passed = (
    not exceptions
    and all(
      value[
        "raw_has_proposition_51"
      ]
      and not value[
        "public_has_proposition_51"
      ]
      and value[
        "public_has_53"
      ]
      and value[
        "public_has_52"
      ]
      and value[
        "compact_numbers"
      ]
      for value in checks.values()
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
    / "phase156_r5_repair11_result.json"
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
    "Phase156-R5 repair11 — Reference dependency pruning"
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

  for label, value in checks.items():
    print(
      label
      + " raw Proposition 5.1:",
      value[
        "raw_has_proposition_51"
      ],
    )
    print(
      label
      + " public Proposition 5.1:",
      value[
        "public_has_proposition_51"
      ],
    )
    print(
      label
      + " public (5.3):",
      value[
        "public_has_53"
      ],
    )
    print(
      label
      + " public (5.2):",
      value[
        "public_has_52"
      ],
    )
    print(
      label
      + " compact numbering:",
      value[
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
