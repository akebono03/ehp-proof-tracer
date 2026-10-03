from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
  _is_toda_group_proof_narrative_reference_statement_candidate,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
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


N_RANGE = range(2, 16)
K_RANGE = range(0, 8)
MAX_DEPTH = 2
EXPECTED_GROUPS = 112
BAD_COMPOSITE = "(5.3) / Lemma 5.2"


def _title(
  reference,
) -> str:
  return (
    reference.locator
    or reference.label
  )


def _components(
  title: str,
) -> tuple[
  str,
  ...,
]:
  return tuple(
    part.strip()
    for part in title.split(
      "/"
    )
    if part.strip()
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


def run_audit(
  output_dir: Path,
) -> dict[
  str,
  object,
]:
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  groups = 0
  exceptions = []
  suspicious = []
  all_rows = []
  classification_counts = Counter()
  classification_groups = defaultdict(
    set
  )
  pi6_53_found = False
  bad_composite_found = False

  for n in N_RANGE:
    for k in K_RANGE:
      groups += 1
      group = (
        "pi_"
        + str(
          n + k
        )
        + "^"
        + str(
          n
        )
      )

      try:
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
        replay = (
          build_toda_group_result_proof_replay(
            group_result,
            max_depth=MAX_DEPTH,
          )
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
        entries = (
          build_toda_group_proof_narrative_reference_entries(
            presentation
          )
        )

        for entry in entries:
          selected = (
            select_toda_group_proof_narrative_reference_statement_steps(
              entry,
              _candidate_steps(
                entry
              ),
              presentation.edges,
              root_step=presentation.root_step,
            )
          )
          reference_title = _title(
            entry.reference
          )
          components = _components(
            reference_title
          )

          for proof_step in selected:
            rendered = (
              _render_generic_narrative_step(
                proof_step
              )
            )
            classification = (
              "single_source"
              if len(
                components
              )
              <= 1
              else "composite_reference"
            )
            classification_counts[
              classification
            ] += 1
            classification_groups[
              classification
            ].add(
              group
            )

            row = {
              "n": n,
              "k": k,
              "group": group,
              "reference_number": entry.number,
              "reference_title": reference_title,
              "classification": classification,
              "statement": rendered,
            }
            all_rows.append(
              row
            )

            if classification == "composite_reference":
              suspicious.append(
                row
              )

            if (
              group == "pi_6^3"
              and reference_title == "(5.3)"
            ):
              pi6_53_found = True

            if reference_title == BAD_COMPOSITE:
              bad_composite_found = True

      except Exception as exc:
        exceptions.append(
          {
            "n": n,
            "k": k,
            "group": group,
            "exception_type": type(
              exc
            ).__name__,
            "exception_message": str(
              exc
            ),
          }
        )

  def write_csv(
    name: str,
    rows,
    fields,
  ) -> None:
    with (
      output_dir
      / name
    ).open(
      "w",
      encoding="utf-8-sig",
      newline="",
    ) as handle:
      writer = csv.DictWriter(
        handle,
        fieldnames=fields,
      )
      writer.writeheader()
      writer.writerows(
        rows
      )

  fields = (
    "n",
    "k",
    "group",
    "reference_number",
    "reference_title",
    "classification",
    "statement",
  )
  write_csv(
    "phase156_r5_repair_all_selected_statements.csv",
    all_rows,
    fields,
  )
  write_csv(
    "phase156_r5_repair_suspicious.csv",
    suspicious,
    fields,
  )
  write_csv(
    "phase156_r5_repair_exceptions.csv",
    exceptions,
    (
      "n",
      "k",
      "group",
      "exception_type",
      "exception_message",
    ),
  )

  passed = (
    groups
    == EXPECTED_GROUPS
    and not exceptions
    and not suspicious
    and pi6_53_found
    and not bad_composite_found
  )

  payload = {
    "phase": "Phase156-R5 repair attribution separation",
    "production_changes": True,
    "groups": groups,
    "exceptions": len(
      exceptions
    ),
    "selected_reference_statements": len(
      all_rows
    ),
    "suspicious_composite_reference_statements": len(
      suspicious
    ),
    "pi6_53_reference_found": pi6_53_found,
    "bad_composite_found": bad_composite_found,
    "classification_counts": dict(
      classification_counts
    ),
    "classification_affected_groups": {
      key: len(
        groups_set
      )
      for key, groups_set
      in classification_groups.items()
    },
    "pass": passed,
  }

  (
    output_dir
    / "phase156_r5_repair_result.json"
  ).write_text(
    json.dumps(
      payload,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  summary = "\n".join(
    (
      "=" * 78,
      "Phase156-R5 repair — Reference attribution separation reaudit",
      "=" * 78,
      "scope: n=2..15, k=0..7, depth=2",
      "",
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
      "selected Reference statements: "
      + str(
        len(
          all_rows
        )
      ),
      "suspicious composite Reference statements: "
      + str(
        len(
          suspicious
        )
      ),
      "pi_6^3 (5.3) Reference found: "
      + str(
        pi6_53_found
      ),
      "bad (5.3) / Lemma 5.2 composite found: "
      + str(
        bad_composite_found
      ),
      "",
      (
        "PASS"
        if passed
        else "FAIL"
      ),
      "=" * 78,
      "",
    )
  )
  (
    output_dir
    / "phase156_r5_repair_summary.txt"
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
      "phase156_r5_repair_audit_output"
    ),
  )
  args = parser.parse_args()
  result = run_audit(
    args.output_dir
  )
  return (
    0
    if result[
      "pass"
    ]
    else 1
  )


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
