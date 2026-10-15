from __future__ import annotations

import argparse
import json
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
)
from toda_group_proof_narrative_classifier import (
  classify_toda_group_proof_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
  _is_toda_group_proof_narrative_reference_statement_candidate,
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


def _candidate_steps(
  entry,
) -> tuple:
  result = []
  seen = set()

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

    if rendered in seen:
      continue

    seen.add(
      rendered
    )
    result.append(
      proof_step
    )

  return tuple(
    result
  )


def _proof_body_start_index(
  rendered: str,
) -> int:
  lines = rendered.splitlines()

  if "## 証明" in lines:
    return (
      lines.index(
        "## 証明"
      )
      + 1
    )

  if "# Group proof narrative" in lines:
    return (
      lines.index(
        "# Group proof narrative"
      )
      + 1
    )

  return 0


def _body_contexts(
  rendered: str,
  statement: str,
) -> tuple[
  dict[
    str,
    object,
  ],
  ...,
]:
  lines = rendered.splitlines()
  body_start = (
    _proof_body_start_index(
      rendered
    )
  )
  result = []

  for index, line in enumerate(
    lines
  ):
    if index < body_start:
      continue

    if statement not in line:
      continue

    result.append(
      {
        "line_number": index + 1,
        "line": line,
        "context": "\n".join(
          lines[
            max(
              body_start,
              index - 4,
            ):
            min(
              len(
                lines
              ),
              index + 3,
            )
          ]
        ),
      }
    )

  return tuple(
    result
  )


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase156_r5_repair4_output"
    ),
  )
  args = parser.parse_args()
  args.output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  cases = []
  exceptions = []

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
      raw = build_toda_group_proof_presentation(
        replay
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
      block_step_ids = {
        id(
          proof_step
        )
        for block in blocks
        for proof_step in block.steps
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

      entry_rows = []

      for entry in entries:
        candidates = _candidate_steps(
          entry
        )
        selected = (
          select_toda_group_proof_narrative_reference_statement_steps(
            entry,
            candidates,
            presentation.edges,
            root_step=presentation.root_step,
          )
        )
        entry_step_ids = {
          id(
            proof_step
          )
          for proof_step in entry.proof_steps
        }

        selected_rows = []

        for proof_step in selected:
          classification = (
            classify_toda_group_proof_narrative_step(
              presentation,
              proof_step,
            )
          )
          external_consumers = tuple(
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
          different_reference_consumers = tuple(
            consumer
            for consumer in external_consumers
            if extract_toda_group_proof_step_literature_reference(
              consumer
            )
            != entry.reference
          )
          same_entry_consumers = tuple(
            edge.parent_step
            for edge in presentation.edges
            if (
              edge.premise_step is proof_step
              and id(
                edge.parent_step
              )
              in entry_step_ids
            )
          )
          statement = (
            _render_generic_narrative_step(
              proof_step
            )
          )

          selected_rows.append(
            {
              "statement": statement,
              "statement_type": type(
                proof_step.conclusion
              ).__name__,
              "fact_role": str(
                classification.fact_role
              ),
              "block_role": str(
                classification.block_role
              ),
              "is_argument_conclusion": (
                id(
                  proof_step
                )
                in argument_conclusion_ids
              ),
              "is_in_narrative_blocks": (
                id(
                  proof_step
                )
                in block_step_ids
              ),
              "same_entry_consumer_count": len(
                same_entry_consumers
              ),
              "entry_external_consumer_count": len(
                external_consumers
              ),
              "different_reference_consumer_count": len(
                different_reference_consumers
              ),
              "body_contexts": _body_contexts(
                rendered,
                statement,
              ),
            }
          )

        if selected_rows:
          entry_rows.append(
            {
              "number": entry.number,
              "reference_label": (
                entry.reference.label
              ),
              "reference_locator": (
                entry.reference.locator
              ),
              "selected": selected_rows,
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
          "entries": entry_rows,
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
    "phase": "Phase156-R5-repair4",
    "production_changes": False,
    "target_groups": len(
      TARGETS
    ),
    "exceptions": len(
      exceptions
    ),
    "cases": cases,
  }

  (
    args.output_dir
    / "phase156_r5_repair4_result.json"
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
    / "phase156_r5_repair4_exceptions.json"
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
    "Phase156-R5 repair4 — Reference/body ownership diagnostic"
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
  print()

  for case in cases:
    print(
      case[
        "group"
      ]
    )

    for entry in case[
      "entries"
    ]:
      print(
        "  [R"
        + str(
          entry[
            "number"
          ]
        )
        + "] "
        + str(
          entry[
            "reference_locator"
          ]
          or entry[
            "reference_label"
          ]
        )
      )

      for selected in entry[
        "selected"
      ]:
        print(
          "    statement: "
          + selected[
            "statement"
          ]
        )
        print(
          "    fact_role: "
          + selected[
            "fact_role"
          ]
        )
        print(
          "    block_role: "
          + selected[
            "block_role"
          ]
        )
        print(
          "    argument conclusion: "
          + str(
            selected[
              "is_argument_conclusion"
            ]
          )
        )
        print(
          "    in narrative blocks: "
          + str(
            selected[
              "is_in_narrative_blocks"
            ]
          )
        )
        print(
          "    same-entry consumers: "
          + str(
            selected[
              "same_entry_consumer_count"
            ]
          )
        )
        print(
          "    entry-external consumers: "
          + str(
            selected[
              "entry_external_consumer_count"
            ]
          )
        )
        print(
          "    different-reference consumers: "
          + str(
            selected[
              "different_reference_consumer_count"
            ]
          )
        )
        print(
          "    body occurrences: "
          + str(
            len(
              selected[
                "body_contexts"
              ]
            )
          )
        )

        for context in selected[
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

  if exceptions:
    print(
      "Exceptions:"
    )

    for exception in exceptions:
      print(
        "  "
        + exception[
          "group"
        ]
        + ": "
        + exception[
          "type"
        ]
        + ": "
        + exception[
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
  ):
    print(
      "PASS: ownership data for all four R5 cases collected."
    )
    return 0

  print(
    "FAIL: ownership diagnostic incomplete."
  )
  return 1


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
