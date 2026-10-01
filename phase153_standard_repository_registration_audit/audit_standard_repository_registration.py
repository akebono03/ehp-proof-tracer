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

from proof_repository import ProofRepositoryEntry
from repository_proof_scope import (
  build_repository_proof_scope,
)
from repository_symbolic_stable_group_specialization import (
  specialize_repository_proof_scope_for_toda_group_query,
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
from toda_calculation import (
  _find_specialized_stable_toda_group_results,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_lookup import (
  find_normalized_toda_group_results,
  is_toda_group_result_for_target,
)
from toda_group_query import (
  TodaGroupQuery,
)


OUTPUT_DIR = Path(__file__).resolve().parent / "output"

TARGETS = (
  {
    "n": 6,
    "k": 4,
    "label": "pi_10^6",
  },
  {
    "n": 7,
    "k": 5,
    "label": "pi_12^7",
  },
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


def _rule_name(
  step,
) -> str:
  if step.inference_rule is None:
    return str(
      step.rule
    )

  return step.inference_rule.name


def _canonical_steps():
  phase68 = build_phase68_10_data()
  phase70 = build_phase70_9_data()

  return {
    "pi_10^6": {
      "base": phase68[
        "pi10_6_zero_step"
      ],
      "general": phase68[
        "final_step"
      ],
    },
    "pi_12^7": {
      "base": phase70[
        "pi12_7_zero_step"
      ],
      "general": phase70[
        "higher_zero_step"
      ],
    },
  }


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  summary_rows = []
  scope_rows = []
  specialization_rows = []
  exception_rows = []

  report_lines = [
    "=" * 78,
    "Standard Repository Registration Audit",
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
    canonical = (
      _canonical_steps()
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
    canonical = {}

  if repository is not None and scope is not None:
    report_lines.append(
      "Registered repository entries:"
    )

    for entry in repository.entries():
      report_lines.append(
        "  "
        + entry.key
        + " | "
        + entry.phase
        + " | "
        + entry.theorem
      )

    report_lines.append(
      ""
    )

  for target in TARGETS:
    label = target[
      "label"
    ]
    n = target[
      "n"
    ]
    k = target[
      "k"
    ]

    try:
      if repository is None or scope is None:
        raise RuntimeError(
          "repository setup failed"
        )

      query = TodaGroupQuery(
        n=n,
        k=k,
      )
      base_step = canonical[
        label
      ][
        "base"
      ]
      general_step = canonical[
        label
      ][
        "general"
      ]

      normalized_results = (
        find_normalized_toda_group_results(
          repository,
          query,
        )
      )

      matching_scope_nodes = tuple(
        node
        for node in scope.nodes
        if is_toda_group_result_for_target(
          node.proof_step.conclusion,
          query.target,
        )
      )

      base_identity_nodes = tuple(
        node
        for node in scope.nodes
        if node.proof_step is base_step
      )

      base_equal_nodes = tuple(
        node
        for node in scope.nodes
        if (
          node.proof_step.conclusion
          == base_step.conclusion
        )
      )

      general_identity_nodes = tuple(
        node
        for node in scope.nodes
        if node.proof_step is general_step
      )

      specialized_scope = (
        specialize_repository_proof_scope_for_toda_group_query(
          scope,
          query,
        )
      )

      added_nodes = (
        specialized_scope.nodes[
          len(
            scope.nodes
          ):
        ]
      )

      specialized_matching_nodes = tuple(
        node
        for node in added_nodes
        if is_toda_group_result_for_target(
          node.proof_step.conclusion,
          query.target,
        )
      )

      specialized_results = (
        _find_specialized_stable_toda_group_results(
          repository,
          query,
        )
      )

      standard_report = (
        build_standard_toda_report(
          n=n,
          k=k,
        )
      )

      selected_group_result = (
        standard_report.candidates[
          0
        ].source_candidate.group_result
      )
      selected_step = (
        selected_group_result.proof_step
      )

      selected_source_entry = (
        selected_group_result.source_entry
      )

      summary_rows.append(
        {
          "target": label,
          "n": n,
          "k": k,
          "normalized_repository_result_count": len(
            normalized_results
          ),
          "matching_scope_node_count": len(
            matching_scope_nodes
          ),
          "canonical_base_identity_in_scope": bool(
            base_identity_nodes
          ),
          "canonical_base_equal_conclusion_node_count": len(
            base_equal_nodes
          ),
          "canonical_general_identity_in_scope": bool(
            general_identity_nodes
          ),
          "specialized_added_matching_node_count": len(
            specialized_matching_nodes
          ),
          "specialized_result_count": len(
            specialized_results
          ),
          "selected_source_key": (
            selected_source_entry.key
          ),
          "selected_source_phase": (
            selected_source_entry.phase
          ),
          "selected_source_theorem": (
            selected_source_entry.theorem
          ),
          "selected_step_rule": (
            _rule_name(
              selected_step
            )
          ),
          "selected_step_is_canonical_base": (
            selected_step is base_step
          ),
          "selected_step_conclusion_equals_base": (
            selected_step.conclusion
            == base_step.conclusion
          ),
          "selected_step_has_single_general_premise": (
            len(
              selected_step.premises
            )
            == 1
            and (
              selected_step.premises[
                0
              ].conclusion
              == general_step.conclusion
            )
          ),
        }
      )

      report_lines.append(
        label
      )
      report_lines.append(
        "  direct repository normalized results: "
        + str(
          len(
            normalized_results
          )
        )
      )
      report_lines.append(
        "  proof-scope target matches: "
        + str(
          len(
            matching_scope_nodes
          )
        )
      )
      report_lines.append(
        "  canonical base identity in scope: "
        + str(
          bool(
            base_identity_nodes
          )
        )
      )
      report_lines.append(
        "  equal-conclusion nodes in scope: "
        + str(
          len(
            base_equal_nodes
          )
        )
      )
      report_lines.append(
        "  canonical general identity in scope: "
        + str(
          bool(
            general_identity_nodes
          )
        )
      )
      report_lines.append(
        "  added specialization matches: "
        + str(
          len(
            specialized_matching_nodes
          )
        )
      )
      report_lines.append(
        "  selected source key: "
        + selected_source_entry.key
      )
      report_lines.append(
        "  selected step rule: "
        + _rule_name(
          selected_step
        )
      )
      report_lines.append(
        "  selected is canonical base identity: "
        + str(
          selected_step
          is base_step
        )
      )
      report_lines.append(
        "  selected conclusion == canonical base conclusion: "
        + str(
          selected_step.conclusion
          == base_step.conclusion
        )
      )
      report_lines.append(
        ""
      )

      for node in matching_scope_nodes:
        scope_rows.append(
          {
            "target": label,
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
            "is_canonical_base_identity": (
              node.proof_step
              is base_step
            ),
            "conclusion_equals_canonical_base": (
              node.proof_step.conclusion
              == base_step.conclusion
            ),
            "premise_count": len(
              node.proof_step.premises
            ),
          }
        )

      for node in specialized_matching_nodes:
        specialization_rows.append(
          {
            "target": label,
            "source_root_entry_key": (
              node.root_entry.key
            ),
            "source_root_entry_phase": (
              node.root_entry.phase
            ),
            "source_root_entry_theorem": (
              node.root_entry.theorem
            ),
            "specialized_shortest_depth": (
              node.shortest_depth
            ),
            "specialized_step_rule": (
              _rule_name(
                node.proof_step
              )
            ),
            "specialized_premise_count": len(
              node.proof_step.premises
            ),
            "specialized_premise_rule": (
              _rule_name(
                node.proof_step.premises[
                  0
                ]
              )
              if node.proof_step.premises
              else ""
            ),
            "premise_is_canonical_general_identity": (
              bool(
                node.proof_step.premises
              )
              and (
                node.proof_step.premises[
                  0
                ]
                is general_step
              )
            ),
            "premise_conclusion_equals_canonical_general": (
              bool(
                node.proof_step.premises
              )
              and (
                node.proof_step.premises[
                  0
                ].conclusion
                == general_step.conclusion
              )
            ),
          }
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
        "If canonical_base_identity_in_scope=True but "
        "direct repository normalized results=0, the base proof exists "
        "inside repository proof scope but is not registered as a direct "
        "group-result source."
      ),
      (
        "If the selected source key begins with standard.toda.stable:: "
        "and its proof step has the symbolic general zero as its sole "
        "premise, selection is coming from stable specialization rather "
        "than the existing concrete base-case proof."
      ),
      "",
      "Output files:",
      "  registration_summary.txt",
      "  registration_comparison.csv",
      "  matching_scope_nodes.csv",
      "  specialization_nodes.csv",
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
    / "registration_summary.txt"
  ).write_text(
    report_text + "\n",
    encoding="utf-8",
  )

  _write_csv(
    OUTPUT_DIR / "registration_comparison.csv",
    summary_rows,
    (
      "target",
      "n",
      "k",
      "normalized_repository_result_count",
      "matching_scope_node_count",
      "canonical_base_identity_in_scope",
      "canonical_base_equal_conclusion_node_count",
      "canonical_general_identity_in_scope",
      "specialized_added_matching_node_count",
      "specialized_result_count",
      "selected_source_key",
      "selected_source_phase",
      "selected_source_theorem",
      "selected_step_rule",
      "selected_step_is_canonical_base",
      "selected_step_conclusion_equals_base",
      "selected_step_has_single_general_premise",
    ),
  )

  _write_csv(
    OUTPUT_DIR / "matching_scope_nodes.csv",
    scope_rows,
    (
      "target",
      "root_entry_key",
      "root_entry_phase",
      "root_entry_theorem",
      "shortest_depth",
      "step_rule",
      "is_canonical_base_identity",
      "conclusion_equals_canonical_base",
      "premise_count",
    ),
  )

  _write_csv(
    OUTPUT_DIR / "specialization_nodes.csv",
    specialization_rows,
    (
      "target",
      "source_root_entry_key",
      "source_root_entry_phase",
      "source_root_entry_theorem",
      "specialized_shortest_depth",
      "specialized_step_rule",
      "specialized_premise_count",
      "specialized_premise_rule",
      "premise_is_canonical_general_identity",
      "premise_conclusion_equals_canonical_general",
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
