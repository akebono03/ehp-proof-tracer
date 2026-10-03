from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
  recognize_toda_group_proof_narrative_step_role,
)
from toda_group_proof_narrative_contribution_renderer import (
  _is_toda_group_proof_narrative_reference_statement_candidate,
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  select_toda_group_proof_narrative_reference_statement_steps,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGETS = (
  (3, 3),
  (4, 6),
  (5, 7),
  (9, 7),
)


def _group_label(
  n: int,
  k: int,
) -> str:
  return (
    "pi_"
    + str(
      n + k
    )
    + "^"
    + str(
      n
    )
  )


def _entry_title(
  entry,
) -> str:
  return (
    entry.reference.locator
    or entry.reference.label
  )


def _public_headers(
  rendered: str,
) -> tuple[
  tuple[
    int,
    int,
    str,
  ],
  ...,
]:
  result = []

  for line_index, line in enumerate(
    rendered.splitlines()
  ):
    match = re.match(
      r"^\*\*\[R([0-9]+)\]\s+(.+?)\.\*\*$",
      line.strip(),
    )

    if match is None:
      continue

    result.append(
      (
        line_index,
        int(
          match.group(
            1
          )
        ),
        match.group(
          2
        ),
      )
    )

  return tuple(
    result
  )


def _candidate_steps(
  entry,
) -> tuple:
  candidates = []
  seen_rendered = set()

  for proof_step in entry.proof_steps:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not (
      _is_toda_group_proof_narrative_reference_statement_candidate(
        proof_step,
        rendered,
      )
    ):
      continue

    if rendered in seen_rendered:
      continue

    seen_rendered.add(
      rendered
    )
    candidates.append(
      proof_step
    )

  return tuple(
    candidates
  )


def _selected_steps_by_entry_id(
  presentation,
  entries,
) -> dict[
  int,
  tuple,
]:
  result = {}

  for entry in entries:
    result[
      id(
        entry
      )
    ] = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        _candidate_steps(
          entry
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )

  return result


def _map_public_headers_to_entries(
  headers,
  entries,
):
  available_by_title = defaultdict(
    list
  )

  for entry in entries:
    available_by_title[
      _entry_title(
        entry
      )
    ].append(
      entry
    )

  used_entry_ids = set()
  mapped = []
  unmatched = []

  for line_index, public_number, title in headers:
    candidates = tuple(
      entry
      for entry in available_by_title.get(
        title,
        (),
      )
      if id(
        entry
      )
      not in used_entry_ids
    )

    if not candidates:
      unmatched.append(
        {
          "public_number": public_number,
          "title": title,
        }
      )
      continue

    entry = candidates[
      0
    ]
    used_entry_ids.add(
      id(
        entry
      )
    )
    mapped.append(
      (
        line_index,
        public_number,
        title,
        entry,
      )
    )

  return (
    tuple(
      mapped
    ),
    tuple(
      unmatched
    ),
  )


def _reference_prefix_from_public_mapping(
  rendered: str,
  mapped_headers,
  selected_lines_by_original_number,
) -> str:
  if not mapped_headers:
    return ""

  lines = rendered.splitlines()
  last_line_index = -1

  for (
    header_line_index,
    _public_number,
    _title,
    entry,
  ) in mapped_headers:
    last_line_index = max(
      last_line_index,
      header_line_index,
    )

    expected_lines = (
      selected_lines_by_original_number.get(
        entry.number,
        (),
      )
    )
    search_index = (
      header_line_index
      + 1
    )

    for expected_line in expected_lines:
      while (
        search_index
        < len(
          lines
        )
        and lines[
          search_index
        ]
        != expected_line
      ):
        if re.match(
          r"^\*\*\[R([0-9]+)\]",
          lines[
            search_index
          ].strip(),
        ):
          break

        search_index += 1

      if (
        search_index
        < len(
          lines
        )
        and lines[
          search_index
        ]
        == expected_line
      ):
        last_line_index = max(
          last_line_index,
          search_index,
        )
        search_index += 1

  if last_line_index < 0:
    return ""

  prefix_lines = lines[
    :last_line_index + 1
  ]

  return "\n".join(
    prefix_lines
  )


def _proof_body_text(
  rendered: str,
  reference_prefix: str,
) -> str:
  if "## 証明" in rendered:
    return rendered.split(
      "## 証明",
      1,
    )[1].lstrip()

  if (
    reference_prefix
    and rendered.startswith(
      reference_prefix
    )
  ):
    remainder = rendered[
      len(
        reference_prefix
      ):
    ]
    return remainder.lstrip(
      "\n"
    )

  return rendered


def _body_contexts(
  body_text: str,
  statement: str,
) -> tuple[
  dict[
    str,
    object,
  ],
  ...,
]:
  lines = body_text.splitlines()
  result = []

  for index, line in enumerate(
    lines
  ):
    if statement not in line:
      continue

    result.append(
      {
        "line_number": index + 1,
        "line": line,
        "context": "\n".join(
          lines[
            max(
              0,
              index - 3,
            ):
            min(
              len(
                lines
              ),
              index + 4,
            )
          ]
        ),
      }
    )

  return tuple(
    result
  )


def _external_consumers(
  presentation,
  entry,
  proof_step,
):
  entry_step_ids = {
    id(
      step
    )
    for step in entry.proof_steps
  }

  return tuple(
    edge.parent_step
    for edge in presentation.edges
    if (
      edge.premise_step is proof_step
      and id(
        edge.parent_step
      )
      not in entry_step_ids
    )
  )


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase156_r5_repair5_output"
    ),
  )
  args = parser.parse_args()
  args.output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  cases = []
  exceptions = []
  unmatched_public_headers = []

  for n, k in TARGETS:
    try:
      report = build_standard_toda_report(
        n=n,
        k=k,
      )
      group_result = (
        report.candidates[
          0
        ].source_candidate.group_result
      )
      replay = build_toda_group_result_proof_replay(
        group_result,
        max_depth=2,
      )
      raw = (
        build_toda_group_proof_presentation(
          replay
        )
      )
      presentation = (
        build_toda_group_proof_narrative_semantic_closure_presentation(
          raw
        )
      )
      semantic_sidecar = (
        build_toda_group_proof_narrative_semantic_sidecar(
          presentation
        )
      )
      blocks = (
        build_toda_group_proof_narrative_blocks(
          presentation,
          semantic_sidecar=semantic_sidecar,
        )
      )
      arguments = (
        build_toda_group_proof_narrative_arguments(
          presentation,
          blocks,
          semantic_sidecar=semantic_sidecar,
        )
      )
      argument_conclusion_ids = {
        id(
          conclusion_step
        )
        for argument in arguments
        for conclusion_step in (
          extract_toda_group_proof_narrative_argument_conclusion_step(
            argument
          ),
        )
        if conclusion_step is not None
      }

      rendered = (
        render_toda_group_proof_narrative_markdown(
          raw
        )
      )
      entries = (
        build_toda_group_proof_narrative_reference_entries(
          presentation
        )
      )
      selected_steps_by_entry_id = (
        _selected_steps_by_entry_id(
          presentation,
          entries,
        )
      )
      selected_lines_by_original_number = (
        _toda_group_proof_narrative_reference_statement_lines_by_number(
          presentation,
          entries,
        )
      )
      headers = _public_headers(
        rendered
      )
      (
        mapped_headers,
        unmatched,
      ) = (
        _map_public_headers_to_entries(
          headers,
          entries,
        )
      )

      if unmatched:
        unmatched_public_headers.extend(
          {
            "group": _group_label(
              n,
              k,
            ),
            **row,
          }
          for row in unmatched
        )

      reference_prefix = (
        _reference_prefix_from_public_mapping(
          rendered,
          mapped_headers,
          selected_lines_by_original_number,
        )
      )
      body_text = _proof_body_text(
        rendered,
        reference_prefix,
      )

      public_rows = []

      for (
        _header_line_index,
        public_number,
        title,
        entry,
      ) in mapped_headers:
        selected_steps = (
          selected_steps_by_entry_id.get(
            id(
              entry
            ),
            (),
          )
        )

        statement_rows = []

        for proof_step in selected_steps:
          statement = (
            _render_generic_narrative_step(
              proof_step
            )
          )
          external_consumers = (
            _external_consumers(
              presentation,
              entry,
              proof_step,
            )
          )
          different_reference_consumers = tuple(
            consumer
            for consumer in external_consumers
            if extract_toda_group_proof_step_literature_reference(
              consumer
            )
            != entry.reference
          )

          statement_rows.append(
            {
              "statement": statement,
              "mathematical_block_role": str(
                recognize_toda_group_proof_narrative_step_role(
                  presentation,
                  proof_step,
                  semantic_sidecar=semantic_sidecar,
                )
              ),
              "is_argument_conclusion": (
                id(
                  proof_step
                )
                in argument_conclusion_ids
              ),
              "entry_external_consumer_count": len(
                external_consumers
              ),
              "different_reference_consumer_count": len(
                different_reference_consumers
              ),
              "body_contexts": _body_contexts(
                body_text,
                statement,
              ),
            }
          )

        public_rows.append(
          {
            "public_number": (
              public_number
            ),
            "title": title,
            "original_entry_number": (
              entry.number
            ),
            "statement_rows": (
              statement_rows
            ),
          }
        )

      cases.append(
        {
          "n": n,
          "k": k,
          "group": _group_label(
            n,
            k,
          ),
          "public_headers": public_rows,
          "body_text": body_text,
        }
      )

    except Exception as exc:
      exceptions.append(
        {
          "n": n,
          "k": k,
          "group": _group_label(
            n,
            k,
          ),
          "type": type(
            exc
          ).__name__,
          "message": str(
            exc
          ),
        }
      )

  payload = {
    "phase": "Phase156-R5-repair5",
    "production_changes": False,
    "target_groups": len(
      TARGETS
    ),
    "exceptions": len(
      exceptions
    ),
    "unmatched_public_headers": len(
      unmatched_public_headers
    ),
    "cases": cases,
  }

  (
    args.output_dir
    / "phase156_r5_repair5_result.json"
  ).write_text(
    json.dumps(
      payload,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  (
    args.output_dir
    / "phase156_r5_repair5_unmatched_headers.json"
  ).write_text(
    json.dumps(
      unmatched_public_headers,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  (
    args.output_dir
    / "phase156_r5_repair5_exceptions.json"
  ).write_text(
    json.dumps(
      exceptions,
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
    "Phase156-R5 repair5 — final public Reference ownership diagnostic"
  )
  print(
    "=" * 78
  )
  print(
    "production changes: none"
  )
  print(
    "target groups:",
    len(
      TARGETS
    ),
  )
  print(
    "exceptions:",
    len(
      exceptions
    ),
  )
  print(
    "unmatched public headers:",
    len(
      unmatched_public_headers
    ),
  )
  print()

  for case in cases:
    print(
      case[
        "group"
      ]
    )

    for header in case[
      "public_headers"
    ]:
      print(
        "  public [R"
        + str(
          header[
            "public_number"
          ]
        )
        + "] "
        + header[
          "title"
        ]
        + " -> original entry "
        + str(
          header[
            "original_entry_number"
          ]
        )
      )

      for statement in header[
        "statement_rows"
      ]:
        print(
          "    statement: "
          + statement[
            "statement"
          ]
        )
        print(
          "    mathematical block role: "
          + statement[
            "mathematical_block_role"
          ]
        )
        print(
          "    argument conclusion: "
          + str(
            statement[
              "is_argument_conclusion"
            ]
          )
        )
        print(
          "    entry-external consumers: "
          + str(
            statement[
              "entry_external_consumer_count"
            ]
          )
        )
        print(
          "    different-reference consumers: "
          + str(
            statement[
              "different_reference_consumer_count"
            ]
          )
        )
        print(
          "    proof-body occurrences: "
          + str(
            len(
              statement[
                "body_contexts"
              ]
            )
          )
        )

        for context in statement[
          "body_contexts"
        ]:
          print(
            "      line "
            + str(
              context[
                "line_number"
              ]
            )
          )

          for line in context[
            "context"
          ].splitlines():
            print(
              "        "
              + line
            )

    print()

  if unmatched_public_headers:
    print(
      "Unmatched public headers:"
    )
    for row in unmatched_public_headers:
      print(
        "  "
        + row[
          "group"
        ]
        + ": [R"
        + str(
          row[
            "public_number"
          ]
        )
        + "] "
        + row[
          "title"
        ]
      )
    print()

  if exceptions:
    print(
      "Exceptions:"
    )
    for row in exceptions:
      print(
        "  "
        + row[
          "group"
        ]
        + ": "
        + row[
          "type"
        ]
        + ": "
        + row[
          "message"
        ]
      )
    print()

  print(
    "=" * 78
  )

  if (
    len(
      cases
    )
    == 4
    and not exceptions
    and not unmatched_public_headers
  ):
    print(
      "PASS: all final public Reference headers were mapped to "
      "graph entries and ownership data was collected."
    )
    return 0

  print(
    "FAIL: final public Reference ownership mapping is incomplete."
  )
  return 1


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
