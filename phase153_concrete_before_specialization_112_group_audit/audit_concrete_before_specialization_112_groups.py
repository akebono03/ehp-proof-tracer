from __future__ import annotations

import csv
from collections import Counter
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


def _is_stable_specialization_key(
  key: str,
) -> bool:
  return (
    isinstance(
      key,
      str,
    )
    and key.startswith(
      "standard.toda.stable::"
    )
    and key.endswith(
      "_specialization"
    )
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


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  totals = Counter()
  inventory_rows = []
  defect_rows = []
  candidate_rows = []
  exception_rows = []

  repository = (
    build_standard_production_proof_repository()
  )
  scope = (
    build_repository_proof_scope(
      repository
    )
  )

  for n in range(
    2,
    16,
  ):
    for k in range(
      0,
      8,
    ):
      totals[
        "groups"
      ] += 1

      label = _group_label(
        n,
        k,
      )

      try:
        report = (
          build_standard_toda_report(
            n=n,
            k=k,
          )
        )

        if not report.candidates:
          inventory_rows.append(
            {
              "n": n,
              "k": k,
              "group": label,
              "has_candidate": False,
              "selected_source_key": "",
              "selected_is_stable_specialization": False,
              "pre_specialization_concrete_match_count": 0,
              "shortest_concrete_depth": "",
              "shortest_concrete_root_key": "",
              "shortest_concrete_rule": "",
              "concrete_before_specialization_defect": False,
            }
          )
          continue

        totals[
          "groups_with_candidate"
        ] += 1

        group_result = (
          report.candidates[
            0
          ].source_candidate.group_result
        )
        source_entry = (
          group_result.source_entry
        )
        source_key = (
          source_entry.key
        )
        selected_is_stable = (
          _is_stable_specialization_key(
            source_key
          )
        )

        if selected_is_stable:
          totals[
            "stable_specialization_selected"
          ] += 1

        query = TodaGroupQuery(
          n=n,
          k=k,
        )

        concrete_matches = tuple(
          node
          for node in scope.nodes
          if is_toda_group_result_for_target(
            node.proof_step.conclusion,
            query.target,
          )
        )

        if concrete_matches:
          totals[
            "groups_with_preexisting_concrete_match"
          ] += 1

        concrete_defect = (
          selected_is_stable
          and bool(
            concrete_matches
          )
        )

        shortest_node = (
          min(
            concrete_matches,
            key=lambda node: (
              node.shortest_depth,
              node.root_entry.key,
              _rule_name(
                node.proof_step
              ),
            ),
          )
          if concrete_matches
          else None
        )

        if concrete_defect:
          totals[
            "concrete_before_specialization_defects"
          ] += 1

          defect_rows.append(
            {
              "n": n,
              "k": k,
              "group": label,
              "selected_source_key": source_key,
              "selected_source_phase": (
                source_entry.phase
              ),
              "selected_source_theorem": (
                source_entry.theorem
              ),
              "selected_rule": (
                _rule_name(
                  group_result.proof_step
                )
              ),
              "pre_specialization_concrete_match_count": len(
                concrete_matches
              ),
              "shortest_concrete_depth": (
                shortest_node.shortest_depth
              ),
              "shortest_concrete_root_key": (
                shortest_node.root_entry.key
              ),
              "shortest_concrete_root_phase": (
                shortest_node.root_entry.phase
              ),
              "shortest_concrete_root_theorem": (
                shortest_node.root_entry.theorem
              ),
              "shortest_concrete_rule": (
                _rule_name(
                  shortest_node.proof_step
                )
              ),
              "selected_conclusion_equals_shortest_concrete": (
                group_result.proof_step.conclusion
                == shortest_node.proof_step.conclusion
              ),
            }
          )

          for candidate_index, node in enumerate(
            sorted(
              concrete_matches,
              key=lambda item: (
                item.shortest_depth,
                item.root_entry.key,
                _rule_name(
                  item.proof_step
                ),
              ),
            ),
            start=1,
          ):
            candidate_rows.append(
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
                    node.proof_step
                  )
                ),
                "premise_count": len(
                  node.proof_step.premises
                ),
                "same_conclusion_as_selected": (
                  node.proof_step.conclusion
                  == group_result.proof_step.conclusion
                ),
              }
            )

        inventory_rows.append(
          {
            "n": n,
            "k": k,
            "group": label,
            "has_candidate": True,
            "selected_source_key": source_key,
            "selected_is_stable_specialization": (
              selected_is_stable
            ),
            "pre_specialization_concrete_match_count": len(
              concrete_matches
            ),
            "shortest_concrete_depth": (
              shortest_node.shortest_depth
              if shortest_node is not None
              else ""
            ),
            "shortest_concrete_root_key": (
              shortest_node.root_entry.key
              if shortest_node is not None
              else ""
            ),
            "shortest_concrete_rule": (
              _rule_name(
                shortest_node.proof_step
              )
              if shortest_node is not None
              else ""
            ),
            "concrete_before_specialization_defect": (
              concrete_defect
            ),
          }
        )

      except Exception as exc:
        totals[
          "exceptions"
        ] += 1
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

  stable_without_concrete = (
    totals[
      "stable_specialization_selected"
    ]
    - totals[
      "concrete_before_specialization_defects"
    ]
  )

  summary_lines = [
    "=" * 78,
    "112-Group Concrete-Before-Specialization Audit",
    "=" * 78,
    "scope: n=2..15, k=0..7",
    "production changes: none",
    "tests changes: none",
    "",
    f"groups: {totals['groups']}",
    f"exceptions: {totals['exceptions']}",
    (
      "groups with selected candidate: "
      + str(
        totals[
          "groups_with_candidate"
        ]
      )
    ),
    (
      "stable specialization selected: "
      + str(
        totals[
          "stable_specialization_selected"
        ]
      )
    ),
    (
      "groups with pre-specialization concrete target match: "
      + str(
        totals[
          "groups_with_preexisting_concrete_match"
        ]
      )
    ),
    (
      "stable specialization selected AND concrete proof already exists: "
      + str(
        totals[
          "concrete_before_specialization_defects"
        ]
      )
    ),
    (
      "stable specialization selected with NO prior concrete match: "
      + str(
        stable_without_concrete
      )
    ),
    "",
    "Confirmed concrete-before-specialization cases:",
  ]

  if defect_rows:
    for row in defect_rows:
      summary_lines.append(
        (
          "  "
          + row[
            "group"
          ]
          + "  selected="
          + row[
            "selected_source_key"
          ]
          + "  concrete_matches="
          + str(
            row[
              "pre_specialization_concrete_match_count"
            ]
          )
          + "  shortest="
          + row[
            "shortest_concrete_root_key"
          ]
          + "@depth"
          + str(
            row[
              "shortest_concrete_depth"
            ]
          )
          + "  rule="
          + row[
            "shortest_concrete_rule"
          ]
        )
      )
  else:
    summary_lines.append(
      "  (none)"
    )

  summary_lines.extend(
    (
      "",
      "Interpretation:",
      (
        "  A confirmed case means the current group query selects a "
        "standard.toda.stable specialization even though the unspecialized "
        "repository proof scope already contains a concrete proof whose "
        "conclusion matches the query target."
      ),
      (
        "  This audit does not yet decide the general selection rule; it "
        "only measures the affected population and inventories the existing "
        "concrete candidates."
      ),
      "",
      "Output files:",
      "  concrete_before_specialization_summary.txt",
      "  defect_groups.csv",
      "  concrete_candidate_inventory.csv",
      "  all_112_group_inventory.csv",
      "  exception_inventory.csv",
      "=" * 78,
    )
  )

  summary = "\n".join(
    summary_lines
  )

  print(
    summary
  )

  (
    OUTPUT_DIR
    / "concrete_before_specialization_summary.txt"
  ).write_text(
    summary + "\n",
    encoding="utf-8",
  )

  _write_csv(
    OUTPUT_DIR / "defect_groups.csv",
    defect_rows,
    (
      "n",
      "k",
      "group",
      "selected_source_key",
      "selected_source_phase",
      "selected_source_theorem",
      "selected_rule",
      "pre_specialization_concrete_match_count",
      "shortest_concrete_depth",
      "shortest_concrete_root_key",
      "shortest_concrete_root_phase",
      "shortest_concrete_root_theorem",
      "shortest_concrete_rule",
      "selected_conclusion_equals_shortest_concrete",
    ),
  )

  _write_csv(
    OUTPUT_DIR / "concrete_candidate_inventory.csv",
    candidate_rows,
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
      "premise_count",
      "same_conclusion_as_selected",
    ),
  )

  _write_csv(
    OUTPUT_DIR / "all_112_group_inventory.csv",
    inventory_rows,
    (
      "n",
      "k",
      "group",
      "has_candidate",
      "selected_source_key",
      "selected_is_stable_specialization",
      "pre_specialization_concrete_match_count",
      "shortest_concrete_depth",
      "shortest_concrete_root_key",
      "shortest_concrete_rule",
      "concrete_before_specialization_defect",
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
