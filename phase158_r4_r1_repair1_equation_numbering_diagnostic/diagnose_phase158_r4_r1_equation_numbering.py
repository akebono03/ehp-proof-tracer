from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(REPO_ROOT),
  )


from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_step_transitions import (
  extract_toda_group_proof_narrative_step_transitions,
)


TAG_RE = re.compile(
  r"\\tag\{(\d+)\}"
)


def _render_pi6_3():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  rendered = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  return (
    presentation,
    blocks,
    rendered,
  )


def _numbered_lines(
  rendered: str,
) -> tuple[
  tuple[
    int,
    str,
  ],
  ...,
]:
  result = []

  for line_number, line in enumerate(
    rendered.splitlines(),
    start=1,
  ):
    if r"\tag{" not in line:
      continue

    result.append(
      (
        line_number,
        line,
      )
    )

  return tuple(
    result
  )


def _duplicate_tag_numbers(
  rendered: str,
) -> tuple[
  int,
  ...,
]:
  counts = Counter(
    int(
      value
    )
    for value in TAG_RE.findall(
      rendered
    )
  )

  return tuple(
    number
    for number, count in sorted(
      counts.items()
    )
    if count > 1
  )


def _transition_rows(
  presentation,
  blocks,
):
  transitions = (
    extract_toda_group_proof_narrative_step_transitions(
      presentation,
      blocks,
    )
  )

  result = []

  for index, transition in enumerate(
    transitions,
    start=1,
  ):
    result.append(
      {
        "index": index,
        "source_id": id(
          transition.source_step
        ),
        "target_id": id(
          transition.target_step
        ),
        "source": (
          _render_generic_narrative_step(
            transition.source_step
          )
        ),
        "target": (
          _render_generic_narrative_step(
            transition.target_step
          )
        ),
      }
    )

  return result


def _render_text_collisions(
  rows,
):
  step_ids_by_text = defaultdict(
    set
  )
  appearances_by_text = defaultdict(
    list
  )

  for row in rows:
    for role in (
      "source",
      "target",
    ):
      text = row[
        role
      ]
      step_id = row[
        role + "_id"
      ]

      step_ids_by_text[
        text
      ].add(
        step_id
      )
      appearances_by_text[
        text
      ].append(
        (
          row["index"],
          role,
          step_id,
        )
      )

  result = []

  for text, step_ids in step_ids_by_text.items():
    if len(
      step_ids
    ) <= 1:
      continue

    result.append(
      {
        "text": text,
        "step_ids": tuple(
          sorted(
            step_ids
          )
        ),
        "appearances": tuple(
          appearances_by_text[
            text
          ]
        ),
      }
    )

  return tuple(
    result
  )


def main() -> int:
  (
    presentation,
    blocks,
    rendered,
  ) = _render_pi6_3()

  rows = _transition_rows(
    presentation,
    blocks,
  )
  collisions = (
    _render_text_collisions(
      rows
    )
  )
  numbered_lines = (
    _numbered_lines(
      rendered
    )
  )
  duplicate_tags = (
    _duplicate_tag_numbers(
      rendered
    )
  )

  output_dir = (
    PACKAGE_DIR
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  (
    output_dir
    / "pi6_3_multi_argument.txt"
  ).write_text(
    rendered + "\n",
    encoding="utf-8",
  )

  lines = [
    "=" * 78,
    "Phase 158-R4-R1 repair1 - equation numbering diagnostic",
    "=" * 78,
    "Production code changes: none",
    "Existing test changes: none",
    "Full pytest: not run",
    "",
    "pi_6^3 current multi-argument Narrative",
    "-" * 78,
    rendered,
    "",
    "Numbered lines",
    "-" * 78,
  ]

  for line_number, line in numbered_lines:
    lines.append(
      f"{line_number:03d}: {line}"
    )

  lines.extend(
    [
      "",
      "Duplicate visible tag numbers",
      "-" * 78,
      repr(
        duplicate_tags
      ),
      "",
      "Transition render-text collisions",
      "-" * 78,
    ]
  )

  if not collisions:
    lines.append(
      "none"
    )
  else:
    for collision in collisions:
      lines.extend(
        [
          "",
          "text: "
          + collision["text"],
          "distinct step ids: "
          + repr(
            collision[
              "step_ids"
            ]
          ),
          "transition appearances: "
          + repr(
            collision[
              "appearances"
            ]
          ),
        ]
      )

  lines.extend(
    [
      "",
      "All step transitions",
      "-" * 78,
    ]
  )

  for row in rows:
    lines.extend(
      [
        (
          f"[{row['index']}] "
          f"source_id={row['source_id']} "
          f"target_id={row['target_id']}"
        ),
        "  source: "
        + row["source"],
        "  target: "
        + row["target"],
      ]
    )

  summary = "\n".join(
    lines
  ) + "\n"

  (
    output_dir
    / "summary.txt"
  ).write_text(
    summary,
    encoding="utf-8",
  )

  print(
    summary,
    end="",
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
