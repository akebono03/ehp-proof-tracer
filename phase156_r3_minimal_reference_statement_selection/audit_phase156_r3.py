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
from toda_group_proof_narrative_contribution_renderer import (
  _is_toda_group_proof_narrative_reference_statement_candidate,
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  select_toda_group_proof_narrative_reference_statement_steps,
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


EXPECTED_GROUPS = 112


def _presentations():
  for n in range(
    2,
    16,
  ):
    for k in range(
      0,
      8,
    ):
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
      raw_presentation = (
        build_toda_group_proof_presentation(
          replay
        )
      )
      presentation = (
        build_toda_group_proof_narrative_semantic_closure_presentation(
          raw_presentation
        )
      )
      yield (
        n,
        k,
        presentation,
      )


def _candidate_steps(
  entry,
):
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


def _boundary_candidates(
  presentation,
  entry,
  candidates,
):
  boundary_ids = {
    id(
      edge.premise_step
    )
    for edge in presentation.edges
    if (
      edge.premise_step
      is not presentation.root_step
      and extract_toda_group_proof_step_literature_reference(
        edge.premise_step
      )
      == entry.reference
      and extract_toda_group_proof_step_literature_reference(
        edge.parent_step
      )
      != entry.reference
    )
  }

  return tuple(
    step
    for step in candidates
    if id(
      step
    ) in boundary_ids
    and step is not presentation.root_step
  )


def run_audit(
  output_dir: Path,
) -> dict[str, object]:
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  groups = 0
  exceptions = []
  violations = []
  reference_entries = 0
  selected_statement_count = 0
  multi_statement_references = 0
  max_statement_count = 0

  for (
    n,
    k,
    presentation,
  ) in _presentations():
    groups += 1

    try:
      entries = (
        build_toda_group_proof_narrative_reference_entries(
          presentation
        )
      )
      statement_lines = (
        _toda_group_proof_narrative_reference_statement_lines_by_number(
          presentation,
          entries,
        )
      )
      reference_entries += len(
        entries
      )
      selected_statement_count += sum(
        len(
          lines
        )
        for lines in statement_lines.values()
      )

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
        boundary = _boundary_candidates(
          presentation,
          entry,
          candidates,
        )

        if boundary:
          if selected != boundary:
            violations.append(
              {
                "n": n,
                "k": k,
                "reference": (
                  entry.reference.locator
                  or entry.reference.label
                ),
                "kind": "boundary_selection_mismatch",
                "selected": len(
                  selected
                ),
                "boundary": len(
                  boundary
                ),
              }
            )
        elif len(
          selected
        ) > 1:
          violations.append(
            {
              "n": n,
              "k": k,
              "reference": (
                entry.reference.locator
                or entry.reference.label
              ),
              "kind": "internal_only_public_expansion",
              "selected": len(
                selected
              ),
              "boundary": 0,
            }
          )

        line_count = len(
          statement_lines.get(
            entry.number,
            (),
          )
        )
        max_statement_count = max(
          max_statement_count,
          line_count,
        )

        if line_count > 1:
          multi_statement_references += 1

    except Exception as exc:
      exceptions.append(
        {
          "n": n,
          "k": k,
          "type": type(
            exc
          ).__name__,
          "message": str(
            exc
          ),
        }
      )

  payload = {
    "phase": "Phase156-R3",
    "groups": groups,
    "exceptions": len(
      exceptions
    ),
    "violations": len(
      violations
    ),
    "reference_entries": reference_entries,
    "selected_statement_count": (
      selected_statement_count
    ),
    "multi_statement_references": (
      multi_statement_references
    ),
    "max_statement_count": (
      max_statement_count
    ),
    "production_changes": True,
    "full_pytest_run": False,
  }

  (
    output_dir
    / "phase156_r3_result.json"
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
    output_dir
    / "phase156_r3_violations.json"
  ).write_text(
    json.dumps(
      violations,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )
  (
    output_dir
    / "phase156_r3_exceptions.json"
  ).write_text(
    json.dumps(
      exceptions,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  summary = "\n".join(
    [
      "=" * 78,
      "Phase156-R3 — minimal Reference statement selection audit",
      "=" * 78,
      "groups: "
      + str(
        groups
      ),
      "exceptions: "
      + str(
        len(
          exceptions
        )
      ),
      "selection violations: "
      + str(
        len(
          violations
        )
      ),
      "reference entries: "
      + str(
        reference_entries
      ),
      "selected statements: "
      + str(
        selected_statement_count
      ),
      "multi-statement References: "
      + str(
        multi_statement_references
      ),
      "max statements in one Reference: "
      + str(
        max_statement_count
      ),
      "",
      "Rule:",
      (
        "  boundary-used statements remain selected; when a Reference "
        "has no boundary-used statement, same-Reference internal "
        "consumers do not expand the public selection beyond one fallback."
      ),
      "=" * 78,
    ]
  ) + "\n"

  (
    output_dir
    / "phase156_r3_summary.txt"
  ).write_text(
    summary,
    encoding="utf-8",
  )
  print(
    summary
  )

  return payload


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase156_r3_audit_output"
    ),
  )
  args = parser.parse_args()

  result = run_audit(
    args.output_dir
  )

  passed = (
    result[
      "groups"
    ]
    == EXPECTED_GROUPS
    and result[
      "exceptions"
    ]
    == 0
    and result[
      "violations"
    ]
    == 0
  )

  if passed:
    print(
      "PASS: Phase156-R3 minimal Reference statement selection "
      "invariants hold across all 112 groups."
    )
    return 0

  print(
    "FAIL: Phase156-R3 selection invariants did not hold."
  )
  return 1


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
