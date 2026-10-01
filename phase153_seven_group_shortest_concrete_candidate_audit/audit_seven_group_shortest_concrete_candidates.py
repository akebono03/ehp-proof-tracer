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
from toda_calculation_facade import (
  build_standard_toda_report,
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


def _reference_name(
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


def _has_same_conclusion_in_ancestry(
  root_step,
) -> bool:
  target = root_step.conclusion
  visited = set()
  stack = list(
    root_step.premises
  )

  while stack:
    step = stack.pop()
    step_id = id(
      step
    )

    if step_id in visited:
      continue

    visited.add(
      step_id
    )

    if step.conclusion == target:
      return True

    stack.extend(
      step.premises
    )

  return False


def _has_stable_specialization_shape(
  step,
) -> bool:
  return (
    len(
      step.premises
    )
    == 1
    and step.inference_rule is None
    and (
      "specialization"
      in (
        step.note
        or ""
      ).lower()
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

  summary_rows = []
  premise_rows = []
  all_candidate_rows = []
  exception_rows = []

  report_lines = [
    "=" * 78,
    "7-Group Shortest Concrete Candidate Audit",
    "=" * 78,
    "targets: pi_6^5, pi_10^6, pi_10^7, pi_12^7, pi_12^9, pi_13^11, pi_14^13",
    "production changes: none",
    "tests changes: none",
    "",
  ]

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
      report = (
        build_standard_toda_report(
          n=n,
          k=k,
        )
      )

      if not report.candidates:
        raise RuntimeError(
          "standard report has no candidates"
        )

      selected_result = (
        report.candidates[
          0
        ].source_candidate.group_result
      )
      selected_step = (
        selected_result.proof_step
      )

      concrete_matches = tuple(
        node
        for node in scope.nodes
        if is_toda_group_result_for_target(
          node.proof_step.conclusion,
          query.target,
        )
      )

      if not concrete_matches:
        raise RuntimeError(
          "no pre-specialization concrete proof-scope match"
        )

      ordered_matches = tuple(
        sorted(
          concrete_matches,
          key=lambda node: (
            node.shortest_depth,
            node.root_entry.key,
            _rule_name(
              node.proof_step
            ),
          ),
        )
      )
      shortest = ordered_matches[
        0
      ]
      shortest_step = (
        shortest.proof_step
      )

      shortest_has_self_conclusion = (
        _has_same_conclusion_in_ancestry(
          shortest_step
        )
      )
      selected_has_self_conclusion = (
        _has_same_conclusion_in_ancestry(
          selected_step
        )
      )

      shortest_reference = (
        _reference_name(
          shortest_step
        )
      )
      selected_reference = (
        _reference_name(
          selected_step
        )
      )

      summary_rows.append(
        {
          "n": n,
          "k": k,
          "group": label,
          "selected_source_key": (
            selected_result.source_entry.key
          ),
          "selected_rule": (
            _rule_name(
              selected_step
            )
          ),
          "selected_reference": (
            selected_reference
          ),
          "selected_premise_count": len(
            selected_step.premises
          ),
          "selected_has_same_conclusion_in_ancestry": (
            selected_has_self_conclusion
          ),
          "selected_has_specialization_shape": (
            _has_stable_specialization_shape(
              selected_step
            )
          ),
          "concrete_candidate_count": len(
            ordered_matches
          ),
          "shortest_root_key": (
            shortest.root_entry.key
          ),
          "shortest_root_phase": (
            shortest.root_entry.phase
          ),
          "shortest_root_theorem": (
            shortest.root_entry.theorem
          ),
          "shortest_depth": (
            shortest.shortest_depth
          ),
          "shortest_rule": (
            _rule_name(
              shortest_step
            )
          ),
          "shortest_reference": (
            shortest_reference
          ),
          "shortest_premise_count": len(
            shortest_step.premises
          ),
          "shortest_has_same_conclusion_in_ancestry": (
            shortest_has_self_conclusion
          ),
          "shortest_has_specialization_shape": (
            _has_stable_specialization_shape(
              shortest_step
            )
          ),
          "same_conclusion": (
            selected_step.conclusion
            == shortest_step.conclusion
          ),
        }
      )

      report_lines.append(
        label
      )
      report_lines.append(
        "  current selected:"
      )
      report_lines.append(
        "    source="
        + selected_result.source_entry.key
      )
      report_lines.append(
        "    rule="
        + _rule_name(
          selected_step
        )
      )
      report_lines.append(
        "    reference="
        + (
          selected_reference
          or "(none)"
        )
      )
      report_lines.append(
        "    premises="
        + str(
          len(
            selected_step.premises
          )
        )
        + " same-conclusion-in-ancestry="
        + str(
          selected_has_self_conclusion
        )
      )

      for premise_index, premise in enumerate(
        selected_step.premises,
        start=1,
      ):
        report_lines.append(
          (
            "      S"
            + str(
              premise_index
            )
            + ": "
            + type(
              premise.conclusion
            ).__name__
            + " | "
            + _rule_name(
              premise
            )
            + " | ref="
            + (
              _reference_name(
                premise
              )
              or "(none)"
            )
          )
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
        "    rule="
        + _rule_name(
          shortest_step
        )
      )
      report_lines.append(
        "    reference="
        + (
          shortest_reference
          or "(none)"
        )
      )
      report_lines.append(
        "    premises="
        + str(
          len(
            shortest_step.premises
          )
        )
        + " same-conclusion-in-ancestry="
        + str(
          shortest_has_self_conclusion
        )
      )

      for premise_index, premise in enumerate(
        shortest_step.premises,
        start=1,
      ):
        premise_reference = (
          _reference_name(
            premise
          )
        )
        premise_rows.append(
          {
            "n": n,
            "k": k,
            "group": label,
            "premise_index": (
              premise_index
            ),
            "premise_statement_type": type(
              premise.conclusion
            ).__name__,
            "premise_rule": (
              _rule_name(
                premise
              )
            ),
            "premise_reference": (
              premise_reference
            ),
            "premise_count": len(
              premise.premises
            ),
            "premise_has_same_conclusion_as_target": (
              premise.conclusion
              == shortest_step.conclusion
            ),
          }
        )

        report_lines.append(
          (
            "      C"
            + str(
              premise_index
            )
            + ": "
            + type(
              premise.conclusion
            ).__name__
            + " | "
            + _rule_name(
              premise
            )
            + " | ref="
            + (
              premise_reference
              or "(none)"
            )
          )
        )

      report_lines.append(
        "  all concrete candidates:"
      )

      for candidate_index, node in enumerate(
        ordered_matches,
        start=1,
      ):
        step = node.proof_step
        all_candidate_rows.append(
          {
            "n": n,
            "k": k,
            "group": label,
            "candidate_index": (
              candidate_index
            ),
            "root_entry_key": (
              node.root_entry.key
            ),
            "root_entry_phase": (
              node.root_entry.phase
            ),
            "root_entry_theorem": (
              node.root_entry.theorem
            ),
            "shortest_depth": (
              node.shortest_depth
            ),
            "step_rule": (
              _rule_name(
                step
              )
            ),
            "step_reference": (
              _reference_name(
                step
              )
            ),
            "premise_count": len(
              step.premises
            ),
            "has_same_conclusion_in_ancestry": (
              _has_same_conclusion_in_ancestry(
                step
              )
            ),
            "has_specialization_shape": (
              _has_stable_specialization_shape(
                step
              )
            ),
          }
        )

        report_lines.append(
          (
            "    #"
            + str(
              candidate_index
            )
            + " "
            + node.root_entry.key
            + "@depth"
            + str(
              node.shortest_depth
            )
            + " | "
            + _rule_name(
              step
            )
            + " | premises="
            + str(
              len(
                step.premises
              )
            )
            + " | self-ancestry="
            + str(
              _has_same_conclusion_in_ancestry(
                step
              )
            )
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

  report_lines.extend(
    (
      "=" * 78,
      "Interpretation",
      "=" * 78,
      (
        "A shortest concrete candidate is structurally safer than the "
        "selected stable specialization when it has real premises, carries "
        "the theorem/lemma-specific inference rule, and does not contain "
        "its own conclusion in its ancestry."
      ),
      (
        "This audit does not yet change selection priority. It identifies "
        "whether shortest-depth is a safe generic representative rule for "
        "all seven affected groups."
      ),
      "",
      "Output files:",
      "  seven_group_shortest_candidate_report.txt",
      "  seven_group_summary.csv",
      "  shortest_candidate_premises.csv",
      "  all_concrete_candidates.csv",
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
    / "seven_group_shortest_candidate_report.txt"
  ).write_text(
    report_text + "\n",
    encoding="utf-8",
  )

  _write_csv(
    OUTPUT_DIR / "seven_group_summary.csv",
    summary_rows,
    (
      "n",
      "k",
      "group",
      "selected_source_key",
      "selected_rule",
      "selected_reference",
      "selected_premise_count",
      "selected_has_same_conclusion_in_ancestry",
      "selected_has_specialization_shape",
      "concrete_candidate_count",
      "shortest_root_key",
      "shortest_root_phase",
      "shortest_root_theorem",
      "shortest_depth",
      "shortest_rule",
      "shortest_reference",
      "shortest_premise_count",
      "shortest_has_same_conclusion_in_ancestry",
      "shortest_has_specialization_shape",
      "same_conclusion",
    ),
  )

  _write_csv(
    OUTPUT_DIR / "shortest_candidate_premises.csv",
    premise_rows,
    (
      "n",
      "k",
      "group",
      "premise_index",
      "premise_statement_type",
      "premise_rule",
      "premise_reference",
      "premise_count",
      "premise_has_same_conclusion_as_target",
    ),
  )

  _write_csv(
    OUTPUT_DIR / "all_concrete_candidates.csv",
    all_candidate_rows,
    (
      "n",
      "k",
      "group",
      "candidate_index",
      "root_entry_key",
      "root_entry_phase",
      "root_entry_theorem",
      "shortest_depth",
      "step_rule",
      "step_reference",
      "premise_count",
      "has_same_conclusion_in_ancestry",
      "has_specialization_shape",
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
