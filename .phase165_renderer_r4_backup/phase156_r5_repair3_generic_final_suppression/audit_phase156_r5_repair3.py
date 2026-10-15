from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
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


DERIVATION_TOKENS = (
  "これらから",
  "このことから",
  "したがって",
  "従って",
  "よって",
  "ゆえに",
  "以上より",
  "ここから",
  "計算",
  "導く",
  "導か",
  "得る",
  "従う",
  "分かる",
  "わかる",
  "示す",
  "確認",
)


def _normalize(
  text: str,
) -> str:
  text = text.replace(
    "\\[",
    "$",
  ).replace(
    "\\]",
    "$",
  ).replace(
    "$$",
    "$",
  ).replace(
    "**",
    "",
  ).replace(
    "`",
    "",
  )
  return re.sub(
    r"\s+",
    "",
    text,
  )


def _headers(
  rendered: str,
):
  result = []

  for line_index, line in enumerate(
    rendered.splitlines()
  ):
    match = re.match(
      r"^\*\*\[R([0-9]+)\]",
      line.strip(),
    )

    if match is not None:
      result.append(
        (
          line_index,
          int(
            match.group(
              1
            )
          ),
        )
      )

  return tuple(
    result
  )


def _body_markers(
  rendered: str,
):
  header_indices = {
    line_index
    for line_index, _number in _headers(
      rendered
    )
  }

  return tuple(
    int(
      number
    )
    for line_index, line in enumerate(
      rendered.splitlines()
    )
    if line_index not in header_indices
    for number in re.findall(
      r"\[R([0-9]+)\]",
      line,
    )
  )


def _proof_body(
  rendered: str,
) -> str:
  if "## 証明" in rendered:
    return rendered.split(
      "## 証明",
      1,
    )[1]

  return rendered


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
  ids = {
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
    proof_step
    for proof_step in candidates
    if (
      proof_step is not presentation.root_step
      and id(
        proof_step
      )
      in ids
    )
  )


def _entry_external_candidates(
  presentation,
  entry,
  candidates,
):
  entry_ids = {
    id(
      proof_step
    )
    for proof_step in entry.proof_steps
  }
  used_ids = {
    id(
      edge.premise_step
    )
    for edge in presentation.edges
    if id(
      edge.parent_step
    )
    not in entry_ids
  }

  return tuple(
    proof_step
    for proof_step in candidates
    if (
      proof_step is not presentation.root_step
      and id(
        proof_step
      )
      in used_ids
    )
  )


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase156_r5_repair3_audit_output"
    ),
  )
  args = parser.parse_args()
  args.output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  groups = 0
  exceptions = []
  violations = []
  informational_header_without_marker_groups = set()
  total_headers = 0
  total_markers = 0
  selected_statements = 0
  multi_statement_entries = 0
  max_selected = 0

  for n in range(
    2,
    16,
  ):
    for k in range(
      0,
      8,
    ):
      groups += 1

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
        rendered = (
          render_toda_group_proof_narrative_markdown(
            raw
          )
        )

        headers = _headers(
          rendered
        )
        header_numbers = tuple(
          number
          for _line_index, number in headers
        )
        markers = _body_markers(
          rendered
        )
        total_headers += len(
          headers
        )
        total_markers += len(
          markers
        )

        expected_headers = tuple(
          range(
            1,
            len(
              header_numbers
            )
            + 1,
          )
        )

        if header_numbers != expected_headers:
          violations.append(
            (
              n,
              k,
              "non_contiguous_reference_headers",
              header_numbers,
            )
          )

        missing = (
          set(
            markers
          )
          - set(
            header_numbers
          )
        )

        if missing:
          violations.append(
            (
              n,
              k,
              "body_marker_without_header",
              tuple(
                sorted(
                  missing
                )
              ),
            )
          )

        if (
          set(
            header_numbers
          )
          - set(
            markers
          )
        ):
          informational_header_without_marker_groups.add(
            (
              n,
              k,
            )
          )

        entries = (
          build_toda_group_proof_narrative_reference_entries(
            presentation
          )
        )
        selected_by_number = (
          _toda_group_proof_narrative_reference_statement_lines_by_number(
            presentation,
            entries,
          )
        )
        selected_statements += sum(
          len(
            lines
          )
          for lines in selected_by_number.values()
        )

        body = _proof_body(
          rendered
        )

        for reference_number, statements in (
          selected_by_number.items()
        ):
          if reference_number not in set(
            header_numbers
          ):
            continue

          for statement in statements:
            if statement not in body:
              continue

            matching_lines = tuple(
              line
              for line in body.splitlines()
              if statement in line
            )

            suppressible = tuple(
              line
              for line in matching_lines
              if not any(
                token in line
                for token in DERIVATION_TOKENS
              )
            )

            if suppressible:
              violations.append(
                (
                  n,
                  k,
                  "suppressible_exact_body_restatement",
                  statement,
                )
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
          external = _entry_external_candidates(
            presentation,
            entry,
            candidates,
          )

          max_selected = max(
            max_selected,
            len(
              selected
            ),
          )

          if len(
            selected
          ) > 1:
            multi_statement_entries += 1

          if boundary:
            if selected != boundary:
              violations.append(
                (
                  n,
                  k,
                  "boundary_selection_mismatch",
                  entry.number,
                )
              )
          elif external:
            if selected != external:
              violations.append(
                (
                  n,
                  k,
                  "entry_external_selection_mismatch",
                  entry.number,
                )
              )
          elif len(
            selected
          ) > 1:
            violations.append(
              (
                n,
                k,
                "same_entry_internal_public_expansion",
                entry.number,
              )
            )

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

  counts = Counter(
    row[
      2
    ]
    for row in violations
  )

  result = {
    "phase": "Phase156-R5-repair3",
    "production_changes": True,
    "groups": groups,
    "exceptions": len(
      exceptions
    ),
    "reference_headers": total_headers,
    "body_reference_markers": total_markers,
    "header_without_marker_groups_informational": len(
      informational_header_without_marker_groups
    ),
    "canonical_selected_statements": selected_statements,
    "multi_statement_entries": multi_statement_entries,
    "max_selected_statements_in_one_entry": max_selected,
    "violations": len(
      violations
    ),
    "violation_counts": dict(
      counts
    ),
  }

  (
    args.output_dir
    / "phase156_r5_repair3_result.json"
  ).write_text(
    json.dumps(
      result,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  (
    args.output_dir
    / "phase156_r5_repair3_violations.json"
  ).write_text(
    json.dumps(
      violations,
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
    "Phase156-R5 repair3 — cross-group minimal-display audit"
  )
  print(
    "=" * 78
  )
  print(
    "groups:",
    groups,
  )
  print(
    "exceptions:",
    len(
      exceptions
    ),
  )
  print(
    "Reference headers:",
    total_headers,
  )
  print(
    "body Reference markers:",
    total_markers,
  )
  print(
    "header-without-marker groups (informational):",
    len(
      informational_header_without_marker_groups
    ),
  )
  print(
    "canonical selected statements:",
    selected_statements,
  )
  print(
    "multi-statement entries:",
    multi_statement_entries,
  )
  print(
    "max selected statements in one entry:",
    max_selected,
  )
  print(
    "violations:",
    len(
      violations
    ),
  )

  for kind in (
    "non_contiguous_reference_headers",
    "body_marker_without_header",
    "boundary_selection_mismatch",
    "entry_external_selection_mismatch",
    "same_entry_internal_public_expansion",
    "suppressible_exact_body_restatement",
  ):
    print(
      "  "
      + kind
      + ": "
      + str(
        counts.get(
          kind,
          0,
        )
      )
    )

  print(
    "=" * 78
  )

  if (
    groups == 112
    and not exceptions
    and not violations
  ):
    print(
      "PASS: all Phase156-R5 minimal-display invariants hold."
    )
    return 0

  print(
    "FAIL: Phase156-R5 minimal-display violations remain."
  )
  return 1


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
