from __future__ import annotations

import csv
from pathlib import Path
import traceback

from repository_proof_scope import (
  build_repository_proof_scope,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)
from toda_group_lookup import (
  is_toda_group_result_for_target,
)
from toda_group_query import (
  TodaGroupQuery,
)
from toda_group_proof_narrative_references import (
  extract_toda_group_proof_step_literature_reference,
)


OUTPUT_DIR = Path(__file__).resolve().parent / "output"

TARGETS = (
  (5, 1),
  (6, 4),
  (7, 3),
  (7, 5),
  (9, 3),
  (11, 2),
  (13, 1),
)

REFERENCE_METADATA = {
  "Lemma 5.4": (
    "60",
    "Toda Lemma 5.4",
  ),
  "Proposition 5.8": (
    "68",
    "Toda Proposition 5.8",
  ),
  "Proposition 5.9": (
    "70",
    "Toda Proposition 5.9",
  ),
  "Proposition 5.11": (
    "73",
    "Toda Proposition 5.11",
  ),
}


def _write_csv(
  path: Path,
  rows: list[dict],
  fieldnames: tuple[str, ...],
) -> None:
  with path.open(
    "w",
    encoding="utf-8-sig",
    newline="",
  ) as handle:
    writer = csv.DictWriter(
      handle,
      fieldnames=fieldnames,
    )
    writer.writeheader()

    for row in rows:
      writer.writerow(
        {
          field: row.get(
            field,
            "",
          )
          for field in fieldnames
        }
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


def _rule_name(
  step,
) -> str:
  if step.inference_rule is None:
    return str(
      step.rule
    )

  return step.inference_rule.name


def _reference_locator(
  step,
) -> str:
  reference = (
    extract_toda_group_proof_step_literature_reference(
      step
    )
  )

  if reference is None:
    return ""

  return (
    reference.locator
    or reference.label
  )


def _reference_label(
  step,
) -> str:
  reference = (
    extract_toda_group_proof_step_literature_reference(
      step
    )
  )

  if reference is None:
    return ""

  return reference.label


def _metadata_from_reference(
  locator: str,
):
  return (
    REFERENCE_METADATA.get(
      locator
    )
  )


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  repository = (
    build_standard_production_proof_repository()
  )
  scope = (
    build_repository_proof_scope(
      repository
    )
  )

  rows = []
  exception_rows = []

  report_lines = [
    "=" * 78,
    "7-Group Concrete Source-Metadata Audit",
    "=" * 78,
    "production changes: none",
    "tests changes: none",
    "",
    "Reference -> canonical metadata table:",
  ]

  for locator, (
    phase,
    theorem,
  ) in REFERENCE_METADATA.items():
    report_lines.append(
      "  "
      + locator
      + " -> phase="
      + phase
      + " theorem="
      + theorem
    )

  report_lines.append(
    ""
  )

  for n, k in TARGETS:
    label = _group_label(
      n,
      k,
    )

    try:
      query = TodaGroupQuery(
        n=n,
        k=k,
      )

      matches = tuple(
        node
        for node in scope.nodes
        if is_toda_group_result_for_target(
          node.proof_step.conclusion,
          query.target,
        )
      )

      if not matches:
        raise RuntimeError(
          "no concrete proof-scope matches"
        )

      shortest = min(
        matches,
        key=lambda node: (
          node.shortest_depth,
          node.root_entry.key,
          _rule_name(
            node.proof_step
          ),
        ),
      )

      step = shortest.proof_step
      locator = _reference_locator(
        step
      )
      reference_label = (
        _reference_label(
          step
        )
      )

      inferred = (
        _metadata_from_reference(
          locator
        )
      )

      if inferred is None:
        inferred_phase = ""
        inferred_theorem = ""
        metadata_resolved = False
      else:
        (
          inferred_phase,
          inferred_theorem,
        ) = inferred
        metadata_resolved = True

      root_phase = (
        shortest.root_entry.phase
        or ""
      )
      root_theorem = (
        shortest.root_entry.theorem
        or ""
      )

      root_metadata_matches_reference = (
        metadata_resolved
        and root_phase
        == inferred_phase
        and root_theorem
        == inferred_theorem
      )

      should_recover_from_step_reference = (
        metadata_resolved
        and not root_metadata_matches_reference
      )

      suggested_key = (
        "standard.toda.concrete::"
        + label
      )

      rows.append(
        {
          "n": n,
          "k": k,
          "group": label,
          "shortest_root_key": (
            shortest.root_entry.key
          ),
          "shortest_depth": (
            shortest.shortest_depth
          ),
          "root_phase": root_phase,
          "root_theorem": root_theorem,
          "step_rule": (
            _rule_name(
              step
            )
          ),
          "step_reference_locator": (
            locator
          ),
          "step_reference_label": (
            reference_label
          ),
          "metadata_resolved_from_reference": (
            metadata_resolved
          ),
          "resolved_phase": (
            inferred_phase
          ),
          "resolved_theorem": (
            inferred_theorem
          ),
          "root_metadata_matches_reference": (
            root_metadata_matches_reference
          ),
          "should_recover_from_step_reference": (
            should_recover_from_step_reference
          ),
          "suggested_generic_key": (
            suggested_key
          ),
        }
      )

      report_lines.append(
        label
      )
      report_lines.append(
        "  shortest concrete:"
      )
      report_lines.append(
        "    root="
        + shortest.root_entry.key
        + " depth="
        + str(
          shortest.shortest_depth
        )
      )
      report_lines.append(
        "    root phase="
        + root_phase
      )
      report_lines.append(
        "    root theorem="
        + root_theorem
      )
      report_lines.append(
        "    step rule="
        + _rule_name(
          step
        )
      )
      report_lines.append(
        "    step reference="
        + (
          locator
          or "(none)"
        )
      )
      report_lines.append(
        "  resolved metadata:"
      )
      report_lines.append(
        "    phase="
        + (
          inferred_phase
          or "(unresolved)"
        )
      )
      report_lines.append(
        "    theorem="
        + (
          inferred_theorem
          or "(unresolved)"
        )
      )
      report_lines.append(
        "  root metadata matches step reference: "
        + str(
          root_metadata_matches_reference
        )
      )
      report_lines.append(
        "  recover metadata from step reference: "
        + str(
          should_recover_from_step_reference
        )
      )
      report_lines.append(
        ""
      )

    except Exception as exc:
      exception_rows.append(
        {
          "n": n,
          "k": k,
          "group": label,
          "exception_type": type(
            exc
          ).__name__,
          "message": str(
            exc
          ),
          "traceback": traceback.format_exc(),
        }
      )

  resolved_count = sum(
    1
    for row in rows
    if row[
      "metadata_resolved_from_reference"
    ]
  )
  mismatch_count = sum(
    1
    for row in rows
    if row[
      "should_recover_from_step_reference"
    ]
  )
  matching_count = sum(
    1
    for row in rows
    if row[
      "root_metadata_matches_reference"
    ]
  )

  report_lines.extend(
    (
      "=" * 78,
      "Summary",
      "=" * 78,
      "groups audited: "
      + str(
        len(
          rows
        )
      ),
      "exceptions: "
      + str(
        len(
          exception_rows
        )
      ),
      "metadata resolved from step reference: "
      + str(
        resolved_count
      ),
      "root metadata already correct: "
      + str(
        matching_count
      ),
      "root metadata differs and must be recovered: "
      + str(
        mismatch_count
      ),
      "",
      "Interpretation:",
      (
        "  The root_entry identifies the repository tree that contains "
        "the proof step; it does not necessarily identify the theorem "
        "that originally proves that step."
      ),
      (
        "  For generic concrete recovery, theorem/phase metadata should "
        "come from the selected proof step's literature reference when "
        "that reference has canonical project metadata."
      ),
      (
        "  The generic key should identify the recovered concrete query "
        "result and should not reuse an unrelated root-entry key."
      ),
      "",
      "Output files:",
      "  source_metadata_report.txt",
      "  source_metadata_audit.csv",
      "  exception_inventory.csv",
      "=" * 78,
    )
  )

  report_text = "\n".join(
    report_lines
  )

  print(
    report_text
  )

  (
    OUTPUT_DIR
    / "source_metadata_report.txt"
  ).write_text(
    report_text + "\n",
    encoding="utf-8",
  )

  _write_csv(
    OUTPUT_DIR / "source_metadata_audit.csv",
    rows,
    (
      "n",
      "k",
      "group",
      "shortest_root_key",
      "shortest_depth",
      "root_phase",
      "root_theorem",
      "step_rule",
      "step_reference_locator",
      "step_reference_label",
      "metadata_resolved_from_reference",
      "resolved_phase",
      "resolved_theorem",
      "root_metadata_matches_reference",
      "should_recover_from_step_reference",
      "suggested_generic_key",
    ),
  )

  _write_csv(
    OUTPUT_DIR / "exception_inventory.csv",
    exception_rows,
    (
      "n",
      "k",
      "group",
      "exception_type",
      "message",
      "traceback",
    ),
  )

  print()
  print(
    "AUDIT COMPLETE."
  )
  print(
    "Production files were NOT changed."
  )
  print(
    "Tests were NOT changed."
  )
  print(
    "Full pytest was NOT run."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
