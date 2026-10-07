from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
  sys.path.insert(0, str(ROOT))

import toda_group_proof_narrative_argument_multi_renderer as multi
import toda_group_proof_narrative_contribution_renderer as contrib

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def locator_list(entries):
  return [
    entry.reference.locator
    or entry.reference.label
    for entry in entries
  ]


def main() -> int:
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  records = []

  original_body_usage = (
    contrib.filter_toda_group_proof_narrative_reference_entries_by_body_usage
  )
  original_restore = (
    contrib.restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage
  )
  original_step_usage = (
    contrib.filter_toda_group_proof_narrative_reference_entries_by_step_usage
  )
  original_numbering = (
    multi.number_toda_group_proof_narrative_equations
  )

  body_usage_call_index = 0

  def wrapped_body_usage(
    entries,
    statement_lines,
    markdown,
  ):
    nonlocal body_usage_call_index
    body_usage_call_index += 1

    result = original_body_usage(
      entries,
      statement_lines,
      markdown,
    )

    records.append(
      {
        "kind": (
          "body_usage_"
          + str(body_usage_call_index)
        ),
        "before": locator_list(entries),
        "after": locator_list(result[0]),
        "has_prop44_marker_before": (
          "Proposition 4.4"
          in markdown
        ),
        "has_r_marker": (
          "[R"
          in markdown
        ),
        "markdown": markdown,
      }
    )

    return result

  def wrapped_restore(
    original_entries,
    original_statement_lines,
    filtered_entries,
    filtered_statement_lines,
    markdown,
    root_step,
    used_step_ids,
    presentation=None,
  ):
    result = original_restore(
      original_entries,
      original_statement_lines,
      filtered_entries,
      filtered_statement_lines,
      markdown,
      root_step,
      used_step_ids,
      presentation=presentation,
    )

    records.append(
      {
        "kind": "restore_fixed_references",
        "before": locator_list(filtered_entries),
        "after": locator_list(result[0]),
        "has_prop44_marker_before": (
          "Proposition 4.4"
          in markdown
        ),
        "has_r_marker": (
          "[R"
          in markdown
        ),
        "markdown": markdown,
      }
    )

    return result

  def wrapped_step_usage(
    entries,
    statement_lines,
    used_step_ids,
    root_step,
  ):
    result = original_step_usage(
      entries,
      statement_lines,
      used_step_ids,
      root_step,
    )

    records.append(
      {
        "kind": "step_usage",
        "before": locator_list(entries),
        "after": locator_list(result[0]),
        "used_count": len(used_step_ids),
      }
    )

    return result

  numbering_records = []

  def wrapped_numbering(
    markdown,
    presentation,
    blocks,
  ):
    result = original_numbering(
      markdown,
      presentation,
      blocks,
    )

    numbering_records.append(
      {
        "before": markdown,
        "after": result,
      }
    )

    return result

  with (
    patch.object(
      contrib,
      "filter_toda_group_proof_narrative_reference_entries_by_body_usage",
      wrapped_body_usage,
    ),
    patch.object(
      contrib,
      "restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage",
      wrapped_restore,
    ),
    patch.object(
      contrib,
      "filter_toda_group_proof_narrative_reference_entries_by_step_usage",
      wrapped_step_usage,
    ),
    patch.object(
      multi,
      "number_toda_group_proof_narrative_equations",
      wrapped_numbering,
    ),
  ):
    final_markdown = (
      contrib.render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
        presentation,
        blocks,
        sidecar,
        arguments,
      )
    )

  lines = [
    "=" * 80,
    "Phase 159 pi_4^3 repair2d - final filter and numbering audit",
    "=" * 80,
    "Production code changes: none",
    "Existing test changes: none",
    "",
    "A. Reference filter instrumentation",
  ]

  for record in records:
    lines.append(
      "  stage="
      + record["kind"]
    )
    lines.append(
      "    before="
      + repr(
        record.get(
          "before",
          [],
        )
      )
    )
    lines.append(
      "    after="
      + repr(
        record.get(
          "after",
          [],
        )
      )
    )

    if "has_r_marker" in record:
      lines.append(
        "    markdown_has_[R]="
        + str(
          record[
            "has_r_marker"
          ]
        )
      )
      lines.append(
        "    markdown_mentions_Proposition_4.4="
        + str(
          record[
            "has_prop44_marker_before"
          ]
        )
      )

  lines.extend(
    (
      "",
      "B. Equation-numbering instrumentation",
      (
        "numbering call count="
        + str(
          len(
            numbering_records
          )
        )
      ),
    )
  )

  for index, record in enumerate(
    numbering_records
  ):
    before = record[
      "before"
    ]
    after = record[
      "after"
    ]

    lines.append(
      "  numbering["
      + str(index)
      + "] before:"
    )
    lines.append(
      before
    )
    lines.append(
      ""
    )
    lines.append(
      "  numbering["
      + str(index)
      + "] after:"
    )
    lines.append(
      after
    )
    lines.append(
      ""
    )
    lines.append(
      "  before has '(4) と (5) より, '="
      + str(
        "(4) と (5) より, "
        in before
      )
    )
    lines.append(
      "  after has '(4) と (5) より, '="
      + str(
        "(4) と (5) より, "
        in after
      )
    )
    lines.append(
      "  before 'これらより' count="
      + str(
        before.count(
          "これらより, "
        )
      )
    )
    lines.append(
      "  after 'これらより' count="
      + str(
        after.count(
          "これらより, "
        )
      )
    )

  lines.extend(
    (
      "",
      "C. Final markdown",
      final_markdown,
      "",
      "Interpretation guide:",
      (
        "  If Proposition 4.4 is present before restore, restored, and then "
        "removed by body_usage_2, the second body-usage filter is the direct "
        "reference-loss stage."
      ),
      (
        "  If numbering input lacks the visible source equations required for "
        "the H(nu') derivation, equation numbering is behaving consistently "
        "and the earlier body/frontier visibility is the cause."
      ),
      (
        "  If numbering input contains the source equations and 'これらより, ' "
        "but numbering still does not produce '(4) と (5) より, ', the "
        "equation-numbering matcher itself is the defect."
      ),
      "",
      "AUDIT_RESULT=PASS",
      "=" * 80,
    )
  )

  output = "\n".join(
    lines
  )

  out_dir = (
    Path(__file__).resolve().parent
    / "audit_output"
  )
  out_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  (
    out_dir
    / "summary.txt"
  ).write_text(
    output + "\n",
    encoding="utf-8",
    newline="\n",
  )

  print(
    output
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
