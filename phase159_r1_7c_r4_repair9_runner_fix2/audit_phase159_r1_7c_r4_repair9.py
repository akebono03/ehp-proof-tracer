from __future__ import annotations

import re

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


def _render_group(
  n: int,
  k: int,
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
    max_depth=2,
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def _sections(
  rendered: str,
) -> tuple[str, str]:
  if "---" in rendered:
    reference, body = rendered.split(
      "---",
      1,
    )
    return reference, body

  marker = "\n## 証明\n"
  if marker in rendered:
    reference, body = rendered.split(
      marker,
      1,
    )
    return reference, body

  return "", rendered


def main() -> int:
  pi6 = _render_group(
    3,
    3,
  )
  _, pi6_body = _sections(
    pi6
  )
  compact_pi6 = re.sub(
    r"\s+",
    "",
    pi6_body,
  )

  print("=== pi_6^3 ===")
  print(
    "eta5_reflexive=",
    int(
      (
        r"$\eta_{5}=\eta_{5}$"
        in compact_pi6
      )
      or (
        r"$\eta_5=\eta_5$"
        in compact_pi6
      )
    ),
    sep="",
  )

  pi15 = _render_group(
    8,
    7,
  )
  pi15_reference, pi15_body = (
    _sections(
      pi15
    )
  )

  reference_numbers = tuple(
    int(number)
    for number in re.findall(
      r"\*\*\[R([0-9]+)\]",
      pi15_reference,
    )
  )
  body_numbers = tuple(
    int(number)
    for number in re.findall(
      r"\[R([0-9]+)\]",
      pi15_body,
    )
  )
  missing = tuple(
    number
    for number in reference_numbers
    if number not in set(
      body_numbers
    )
  )

  print("=== pi_15^8 ===")
  print(
    "references=",
    len(
      reference_numbers
    ),
    sep="",
  )
  print(
    "body_markers=",
    len(
      set(
        body_numbers
      )
    ),
    sep="",
  )
  print(
    "missing_markers=",
    len(
      missing
    ),
    sep="",
  )
  print(
    "reference_numbers=",
    reference_numbers,
    sep="",
  )
  print(
    "body_reference_numbers=",
    tuple(
      sorted(
        set(
          body_numbers
        )
      )
    ),
    sep="",
  )
  return 0


if __name__ == "__main__":
    raise SystemExit(main())
