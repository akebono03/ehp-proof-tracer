from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import re
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _phase154_r5_reference_source_steps_by_number,
  _phase154_r5_unique_visible_non_root_consumer_line,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
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


REPRESENTATIVES = (
  (
    "pi6_3",
    3,
    3,
  ),
  (
    "pi10_4",
    4,
    6,
  ),
  (
    "pi11_4",
    4,
    7,
  ),
  (
    "pi12_5",
    5,
    7,
  ),
  (
    "pi16_9",
    9,
    7,
  ),
)


def build_presentation(
  n: int,
  k: int,
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
    max_depth=2,
  )
  raw_presentation = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw_presentation
    )
  )

  return (
    raw_presentation,
    presentation,
  )


def split_public_narrative(
  rendered: str,
) -> tuple[
  str,
  str,
]:
  reference_header = "## 使用する結果"
  proof_header = "## 証明"

  reference_index = rendered.find(
    reference_header
  )
  proof_index = rendered.find(
    proof_header
  )

  if (
    reference_index < 0
    or proof_index < 0
    or reference_index >= proof_index
  ):
    return (
      "",
      rendered,
    )

  reference_section = rendered[
    reference_index
    + len(
      reference_header
    ):
    proof_index
  ].strip()
  proof_body = rendered[
    proof_index
    + len(
      proof_header
    ):
  ].strip()

  return (
    reference_section,
    proof_body,
  )


def public_reference_titles(
  reference_section: str,
) -> dict[
  int,
  str,
]:
  result = {}

  for match in re.finditer(
    r"\*\*\[R([0-9]+)\] ([^*]+)\.\*\*",
    reference_section,
  ):
    result[
      int(
        match.group(
          1
        )
      )
    ] = match.group(
      2
    ).strip()

  return result


def literature_reference_title(
  entry,
) -> str:
  return (
    entry.reference.locator
    or entry.reference.label
  )


def public_entries(
  presentation,
  reference_titles: dict[
    int,
    str,
  ],
):
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  empty_statement_lines = {
    entry.number: ()
    for entry in entries
  }
  entries, _ = (
    exclude_toda_group_proof_narrative_root_reference(
      entries,
      empty_statement_lines,
      presentation.root_step,
    )
  )

  matched = []

  for public_number, title in sorted(
    reference_titles.items()
  ):
    candidates = tuple(
      entry
      for entry in entries
      if literature_reference_title(
        entry
      ) == title
    )

    if len(
      candidates
    ) != 1:
      continue

    matched.append(
      replace(
        candidates[0],
        number=public_number,
      )
    )

  return tuple(
    matched
  )


def neutral_markers(
  proof_body: str,
) -> tuple[
  int,
  ...,
]:
  return tuple(
    int(
      match.group(
        1
      )
    )
    for match in re.finditer(
      r"\[R([0-9]+)\]を用いる。",
      proof_body,
    )
  )


def linked_markers(
  proof_body: str,
) -> tuple[
  int,
  ...,
]:
  return tuple(
    int(
      match.group(
        1
      )
    )
    for match in re.finditer(
      r"\[R([0-9]+)\]より、",
      proof_body,
    )
  )


def incomplete_reference_marker_lines(
  proof_body: str,
) -> tuple[
  str,
  ...,
]:
  result = []

  for line in proof_body.splitlines():
    if "[R" not in line:
      continue

    if re.search(
      r"\[R[0-9]+\](?:を用いる。|より、)",
      line,
    ):
      continue

    result.append(
      line
    )

  return tuple(
    result
  )


def audit_group(
  name: str,
  n: int,
  k: int,
):
  (
    raw_presentation,
    presentation,
  ) = build_presentation(
    n,
    k,
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw_presentation
  )
  reference_section, proof_body = (
    split_public_narrative(
      rendered
    )
  )
  titles = public_reference_titles(
    reference_section
  )
  entries = public_entries(
    presentation,
    titles,
  )
  sources_by_number = (
    _phase154_r5_reference_source_steps_by_number(
      presentation,
      entries,
    )
  )

  neutral = neutral_markers(
    proof_body
  )
  linked = linked_markers(
    proof_body
  )
  incomplete = (
    incomplete_reference_marker_lines(
      proof_body
    )
  )

  residual_candidates = []
  accepted_neutral = []

  for number in neutral:
    source_steps = sources_by_number.get(
      number,
      (),
    )
    consumer = (
      _phase154_r5_unique_visible_non_root_consumer_line(
        presentation,
        source_steps,
        proof_body,
      )
      if source_steps
      else None
    )

    if consumer is None:
      accepted_neutral.append(
        number
      )
    else:
      residual_candidates.append(
        (
          number,
          consumer,
        )
      )

  return {
    "name": name,
    "n": n,
    "k": k,
    "rendered": rendered,
    "reference_count": len(
      titles
    ),
    "neutral_markers": neutral,
    "linked_markers": linked,
    "accepted_neutral": tuple(
      accepted_neutral
    ),
    "residual_candidates": tuple(
      residual_candidates
    ),
    "incomplete_lines": incomplete,
  }


def main() -> int:
  output_dir = (
    Path(__file__).resolve().parent
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  results = tuple(
    audit_group(
      name,
      n,
      k,
    )
    for name, n, k in REPRESENTATIVES
  )

  total_residual = sum(
    len(
      result[
        "residual_candidates"
      ]
    )
    for result in results
  )
  total_incomplete = sum(
    len(
      result[
        "incomplete_lines"
      ]
    )
    for result in results
  )

  lines = [
    "# Phase 154-R5 Representative Re-audit",
    "",
    "Production changes: none.",
    "",
    "Conditions:",
    "- Narrative",
    "- depth 2",
    "- representatives: pi6_3, pi10_4, pi11_4, pi12_5, pi16_9",
    "",
    "## Summary",
    "",
    f"residual_linkage_candidates: {total_residual}",
    f"incomplete_reference_marker_lines: {total_incomplete}",
    "",
  ]

  for result in results:
    lines.extend(
      (
        "## "
        + result[
          "name"
        ],
        "",
        (
          "reference_count: "
          + str(
            result[
              "reference_count"
            ]
          )
        ),
        (
          "linked_reference_markers: "
          + str(
            len(
              result[
                "linked_markers"
              ]
            )
          )
        ),
        (
          "neutral_reference_markers: "
          + str(
            len(
              result[
                "neutral_markers"
              ]
            )
          )
        ),
        (
          "accepted_root_or_ambiguous_neutral_markers: "
          + str(
            len(
              result[
                "accepted_neutral"
              ]
            )
          )
        ),
        (
          "residual_linkage_candidates: "
          + str(
            len(
              result[
                "residual_candidates"
              ]
            )
          )
        ),
        (
          "incomplete_reference_marker_lines: "
          + str(
            len(
              result[
                "incomplete_lines"
              ]
            )
          )
        ),
        "",
      )
    )

    if result[
      "linked_markers"
    ]:
      lines.append(
        "Linked markers: "
        + ", ".join(
          "[R"
          + str(
            number
          )
          + "]"
          for number in result[
            "linked_markers"
          ]
        )
      )
      lines.append("")

    if result[
      "accepted_neutral"
    ]:
      lines.append(
        "Accepted neutral markers: "
        + ", ".join(
          "[R"
          + str(
            number
          )
          + "]"
          for number in result[
            "accepted_neutral"
          ]
        )
      )
      lines.append("")

    if result[
      "residual_candidates"
    ]:
      lines.append(
        "Residual candidates:"
      )
      lines.append("")

      for number, consumer in result[
        "residual_candidates"
      ]:
        lines.append(
          "- [R"
          + str(
            number
          )
          + "] -> `"
          + consumer.replace(
            "`",
            r"\`",
          )
          + "`"
        )

      lines.append("")

    if result[
      "incomplete_lines"
    ]:
      lines.append(
        "Incomplete marker lines:"
      )
      lines.append("")

      for line in result[
        "incomplete_lines"
      ]:
        lines.append(
          "- `"
          + line.replace(
            "`",
            r"\`",
          )
          + "`"
        )

      lines.append("")

    narrative_path = (
      output_dir
      / (
        result[
          "name"
        ]
        + "_narrative.txt"
      )
    )
    narrative_path.write_text(
      result[
        "rendered"
      ],
      encoding="utf-8",
    )

  lines.extend(
    (
      "## Completion rule",
      "",
      (
        "- R5 is complete if "
        "`residual_linkage_candidates = 0` and "
        "`incomplete_reference_marker_lines = 0`."
      ),
      (
        "- Neutral `[R#]を用いる。` is acceptable when no unique "
        "visible non-root consumer exists."
      ),
      (
        "- Any residual candidate must be inspected before R5 closes."
      ),
      "",
      "## Next boundary",
      "",
      (
        "- If R5 closes, proceed to Phase 154-R6 punctuation normalization."
      ),
      (
        "- Full test suite remains reserved for the end of Phase 154."
      ),
      "",
    )
  )

  report = "\n".join(
    lines
  )
  report_path = (
    output_dir
    / "phase154_r5_representative_reaudit.md"
  )
  report_path.write_text(
    report,
    encoding="utf-8",
  )

  print(
    report
  )
  print(
    "Report:",
    report_path,
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
