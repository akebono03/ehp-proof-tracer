from __future__ import annotations

import csv
from pathlib import Path
import sys
import traceback

REPO_ROOT = Path.cwd()
TESTS_DIR = REPO_ROOT / "tests"

if str(TESTS_DIR) not in sys.path:
  sys.path.insert(
    0,
    str(
      TESTS_DIR
    ),
  )

from repository_proof_scope import (
  build_repository_proof_scope,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)
from test_phase68_pi_n_plus_4_n_zero import (
  build_phase68_10_data,
)
from test_phase70_pi_n_plus_5_n_zero import (
  build_phase70_9_data,
)
from toda_group_lookup import (
  is_toda_group_result_for_target,
)
from toda_group_query import (
  TodaGroupQuery,
)


OUTPUT_DIR = Path(__file__).resolve().parent / "output"


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


def _rule_name(
  step,
) -> str:
  if step.inference_rule is None:
    return str(
      step.rule
    )

  return step.inference_rule.name


def _premise_signature(
  step,
):
  return tuple(
    (
      type(
        premise.conclusion
      ).__name__,
      premise.conclusion,
      _rule_name(
        premise
      ),
    )
    for premise in step.premises
  )


def _premise_conclusion_signature(
  step,
):
  return tuple(
    premise.conclusion
    for premise in step.premises
  )


def _canonical_targets():
  phase68 = build_phase68_10_data()
  phase70 = build_phase70_9_data()

  return (
    (
      "pi_10^6",
      6,
      4,
      phase68[
        "pi10_6_zero_step"
      ],
    ),
    (
      "pi_12^7",
      7,
      5,
      phase70[
        "pi12_7_zero_step"
      ],
    ),
  )


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  rows = []
  summary_rows = []
  exception_rows = []

  report_lines = [
    "=" * 78,
    "Concrete Proof-Scope Candidate Structure Audit",
    "=" * 78,
    "targets: pi_10^6, pi_12^7",
    "production changes: none",
    "tests changes: none",
    "",
  ]

  try:
    repository = (
      build_standard_production_proof_repository()
    )
    scope = (
      build_repository_proof_scope(
        repository
      )
    )
    targets = (
      _canonical_targets()
    )
  except Exception as exc:
    exception_rows.append(
      {
        "target": "setup",
        "exception_type": type(
          exc
        ).__name__,
        "message": str(
          exc
        ),
        "traceback": traceback.format_exc(),
      }
    )
    repository = None
    scope = None
    targets = ()

  for (
    label,
    n,
    k,
    canonical_base,
  ) in targets:
    try:
      if scope is None:
        raise RuntimeError(
          "scope setup failed"
        )

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

      canonical_premise_conclusions = (
        _premise_conclusion_signature(
          canonical_base
        )
      )
      canonical_premise_signature = (
        _premise_signature(
          canonical_base
        )
      )
      canonical_rule = (
        _rule_name(
          canonical_base
        )
      )

      structural_matches = []

      report_lines.append(
        label
      )
      report_lines.append(
        "  target-matching nodes: "
        + str(
          len(
            matches
          )
        )
      )
      report_lines.append(
        "  canonical base rule: "
        + canonical_rule
      )
      report_lines.append(
        "  canonical premise count: "
        + str(
          len(
            canonical_base.premises
          )
        )
      )

      for index, node in enumerate(
        matches,
        start=1,
      ):
        step = node.proof_step
        same_rule = (
          _rule_name(
            step
          )
          == canonical_rule
        )
        same_premise_conclusions = (
          _premise_conclusion_signature(
            step
          )
          == canonical_premise_conclusions
        )
        same_full_premise_signature = (
          _premise_signature(
            step
          )
          == canonical_premise_signature
        )
        structural_match = (
          same_rule
          and same_premise_conclusions
        )

        if structural_match:
          structural_matches.append(
            node
          )

        row = {
          "target": label,
          "candidate_index": index,
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
          "premise_count": len(
            step.premises
          ),
          "same_rule_as_canonical": (
            same_rule
          ),
          "same_premise_conclusions_as_canonical": (
            same_premise_conclusions
          ),
          "same_full_premise_signature_as_canonical": (
            same_full_premise_signature
          ),
          "structural_base_match": (
            structural_match
          ),
        }
        rows.append(
          row
        )

        report_lines.append(
          (
            "    C"
            + str(
              index
            )
            + ": depth="
            + str(
              node.shortest_depth
            )
            + " root="
            + node.root_entry.key
          )
        )
        report_lines.append(
          (
            "       rule="
            + _rule_name(
              step
            )
          )
        )
        report_lines.append(
          (
            "       premises="
            + str(
              len(
                step.premises
              )
            )
            + " same_rule="
            + str(
              same_rule
            )
            + " same_premise_conclusions="
            + str(
              same_premise_conclusions
            )
            + " structural_base_match="
            + str(
              structural_match
            )
          )
        )

        for premise_index, premise in enumerate(
          step.premises,
          start=1,
        ):
          report_lines.append(
            (
              "         P"
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
            )
          )

      summary_rows.append(
        {
          "target": label,
          "target_matching_nodes": len(
            matches
          ),
          "structural_base_matches": len(
            structural_matches
          ),
          "unique_structural_base_match": (
            len(
              structural_matches
            )
            == 1
          ),
          "structural_match_root_entry_key": (
            structural_matches[
              0
            ].root_entry.key
            if len(
              structural_matches
            )
            == 1
            else ""
          ),
          "structural_match_depth": (
            structural_matches[
              0
            ].shortest_depth
            if len(
              structural_matches
            )
            == 1
            else ""
          ),
        }
      )

      report_lines.append(
        "  structural base matches: "
        + str(
          len(
            structural_matches
          )
        )
      )
      report_lines.append(
        ""
      )

    except Exception as exc:
      exception_rows.append(
        {
          "target": label,
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
        "structural_base_match requires the same inference-rule name "
        "and the same ordered premise conclusions as the canonical "
        "Phase68/Phase70 base-case proof."
      ),
      (
        "If each target has exactly one structural_base_match, "
        "the existing production proof scope already contains a unique "
        "canonical concrete proof candidate."
      ),
      "",
      "Output files:",
      "  candidate_structure_summary.txt",
      "  candidate_structure_summary.csv",
      "  candidate_inventory.csv",
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
    / "candidate_structure_summary.txt"
  ).write_text(
    report_text + "\n",
    encoding="utf-8",
  )

  _write_csv(
    OUTPUT_DIR / "candidate_structure_summary.csv",
    summary_rows,
    (
      "target",
      "target_matching_nodes",
      "structural_base_matches",
      "unique_structural_base_match",
      "structural_match_root_entry_key",
      "structural_match_depth",
    ),
  )

  _write_csv(
    OUTPUT_DIR / "candidate_inventory.csv",
    rows,
    (
      "target",
      "candidate_index",
      "root_entry_key",
      "root_entry_phase",
      "root_entry_theorem",
      "shortest_depth",
      "step_rule",
      "premise_count",
      "same_rule_as_canonical",
      "same_premise_conclusions_as_canonical",
      "same_full_premise_signature_as_canonical",
      "structural_base_match",
    ),
  )

  _write_csv(
    OUTPUT_DIR / "exception_inventory.csv",
    exception_rows,
    (
      "target",
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
