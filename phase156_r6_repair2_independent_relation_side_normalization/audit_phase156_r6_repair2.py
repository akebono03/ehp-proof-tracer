from __future__ import annotations

import argparse
import json
from pathlib import Path

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_equation_tag_number,
  _toda_group_proof_narrative_two_equation_reference_numbers,
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


def _local_ordering_violations(
  markdown: str,
) -> int:
  paragraphs = markdown.split(
    "\n\n"
  )
  tag_index_by_number = {
    tag_number: index
    for index, paragraph in enumerate(
      paragraphs
    )
    for tag_number in (
      _toda_group_proof_narrative_equation_tag_number(
        paragraph
      ),
    )
    if tag_number is not None
  }
  violations = 0

  for index, paragraph in enumerate(
    paragraphs[
      :-1
    ]
  ):
    reference_numbers = (
      _toda_group_proof_narrative_two_equation_reference_numbers(
        paragraph
      )
    )

    if reference_numbers is None:
      continue

    if any(
      number not in tag_index_by_number
      for number in reference_numbers
    ):
      continue

    if (
      _toda_group_proof_narrative_equation_tag_number(
        paragraphs[
          index + 1
        ]
      )
      is None
    ):
      continue

    expected = (
      max(
        tag_index_by_number[
          number
        ]
        for number in reference_numbers
      )
      + 1
    )

    if index != expected:
      violations += 1

  return violations


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase156_r6_repair2_audit_output"
    ),
  )
  args = parser.parse_args()
  args.output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  exceptions = []
  duplicate_connector_occurrences = 0
  local_ordering_violations = 0

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
          rendered = _render(
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
          continue

        duplicate_connector_occurrences += rendered.count(
          "以上より,\n\n"
          "以上で得た群構造, 生成元, および写像に関する結果を合わせると,"
        )
        local_ordering_violations += (
          _local_ordering_violations(
            rendered
          )
        )

  pi6 = _render(
    3,
    3,
    2,
  )
  eq1 = (
    r"$2\nu' = "
    r"\eta_{3}\eta_{4}\eta_{5}\tag{1}$"
  )
  eq2 = (
    r"$\eta_{3}\eta_{4}\eta_{5} = "
    r"\eta_{3}^{3}\tag{2}$"
  )
  eq3 = (
    r"$2\nu' = \eta_{3}^{3}\tag{3}$"
  )
  order_statement = (
    r"$\operatorname{ord}\left("
    r"\eta_{3}^{3}"
    r"\right) = 2$"
  )
  expanded_order = (
    r"$\operatorname{ord}\left("
    r"\eta_{3}\eta_{4}\eta_{5}"
    r"\right) = 2$"
  )

  pi6_chain = (
    eq1 in pi6
    and eq2 in pi6
    and eq3 in pi6
    and order_statement in pi6
    and (
      pi6.index(
        eq1
      )
      < pi6.index(
        eq2
      )
      < pi6.index(
        "(1) と (2) より,"
      )
      < pi6.index(
        eq3
      )
      < pi6.index(
        order_statement
      )
    )
  )
  expanded_order_absent = (
    expanded_order not in pi6
  )
  collapsed_identity_absent = (
    r"$\eta_{3}^{3} = \eta_{3}^{3}\tag{2}$"
    not in pi6
  )

  passed = (
    not exceptions
    and duplicate_connector_occurrences == 0
    and local_ordering_violations == 0
    and pi6_chain
    and expanded_order_absent
    and collapsed_identity_absent
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
    "duplicate_connector_occurrences": (
      duplicate_connector_occurrences
    ),
    "local_ordering_violations": (
      local_ordering_violations
    ),
    "pi6_canonical_chain": pi6_chain,
    "pi6_expanded_order_absent": (
      expanded_order_absent
    ),
    "pi6_collapsed_identity_absent": (
      collapsed_identity_absent
    ),
    "pass": passed,
  }

  (
    args.output_dir
    / "phase156_r6_repair2_result.json"
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
    "Phase156-R6 repair2 — independent relation-side normalization"
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
    "duplicate connector occurrences:",
    duplicate_connector_occurrences,
  )
  print(
    "local ordering violations:",
    local_ordering_violations,
  )
  print(
    "pi6 canonical chain:",
    pi6_chain,
  )
  print(
    "pi6 expanded order absent:",
    expanded_order_absent,
  )
  print(
    "pi6 collapsed identity absent:",
    collapsed_identity_absent,
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
