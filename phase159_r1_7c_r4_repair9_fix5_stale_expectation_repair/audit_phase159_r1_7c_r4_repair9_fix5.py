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
    return tuple(
      rendered.split(
        "---",
        1,
      )
    )

  marker = "\n## 証明\n"

  if marker in rendered:
    return tuple(
      rendered.split(
        marker,
        1,
      )
    )

  return (
    "",
    rendered,
  )


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

  simple_double = (
    r"$2\nu' = \eta_{3}^{3}"
    in pi6_body
  )
  expanded_double = (
    (
      r"$2\nu' = \eta_{3}\eta_{4}\eta_{5}"
      r" = \eta_{3}^{3}$"
    )
    in pi6_body
  )

  print(
    "=== pi_6^3 ==="
  )
  print(
    "eta5_reflexive=",
    int(
      r"$\eta_{5}=\eta_{5}$"
      in compact_pi6
    ),
    sep="",
  )
  print(
    "double_nu_prime_semantic=",
    int(
      simple_double
      or expanded_double
    ),
    sep="",
  )
  print(
    "double_nu_prime_expanded=",
    int(
      expanded_double
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

  reference_numbers = {
    int(number)
    for number in re.findall(
      r"\*\*\[R([0-9]+)\]",
      pi15_reference,
    )
  }
  body_numbers = {
    int(number)
    for number in re.findall(
      r"\[R([0-9]+)\]",
      pi15_body,
    )
  }

  print(
    "=== pi_15^8 ==="
  )
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
      body_numbers
    ),
    sep="",
  )
  print(
    "missing_markers=",
    len(
      reference_numbers
      - body_numbers
    ),
    sep="",
  )
  print(
    "transported_relation=",
    int(
      (
        r"$\pi_{15}^{8} \cong "
        r"\mathbb{Z}/8\{E\sigma'\} "
        r"\oplus \mathbb{Z}\{\sigma_{8}\}$"
      )
      in pi15_body
    ),
    sep="",
  )

  return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
