from __future__ import annotations

import csv
from pathlib import Path
import traceback

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_references import (
  extract_toda_group_proof_step_literature_reference,
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


OUTPUT_DIR = Path(__file__).resolve().parent / "output"

TARGETS = (
  (2, 2),
  (2, 3),
  (2, 4),
  (2, 5),
  (2, 6),
  (2, 7),
  (6, 4),
  (7, 5),
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


def _reference_name(
  proof_step,
) -> str:
  reference = (
    extract_toda_group_proof_step_literature_reference(
      proof_step
    )
  )

  if reference is None:
    return ""

  return (
    reference.locator
    or reference.label
  )


def _rule_name(
  proof_step,
) -> str:
  if proof_step.inference_rule is None:
    return str(
      proof_step.rule
    )

  return proof_step.inference_rule.name


def _depth_by_step_id(
  presentation,
) -> dict[int, int]:
  return {
    id(
      node.proof_step
    ): node.depth
    for node in presentation.nodes
  }


def _edges_for_parent(
  presentation,
  parent_step,
):
  return tuple(
    sorted(
      (
        edge
        for edge in presentation.edges
        if edge.parent_step is parent_step
      ),
      key=lambda edge: edge.premise_index,
    )
  )


def _step_summary(
  proof_step,
) -> str:
  return (
    _render_generic_narrative_step(
      proof_step
    )
  )


def _classify_premise(
  proof_step,
  root_step,
) -> str:
  if proof_step is root_step:
    return "self_reference"

  try:
    if (
      proof_step.conclusion
      == root_step.conclusion
    ):
      return "self_reference_equal_conclusion"
  except Exception:
    pass

  reference = (
    extract_toda_group_proof_step_literature_reference(
      proof_step
    )
  )

  if reference is not None:
    return "literature_backed"

  if proof_step.inference_rule is not None:
    return "derived_without_literature_reference"

  return "given_or_unreferenced"


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  root_rows = []
  direct_rows = []
  second_level_rows = []
  exception_rows = []
  report_lines = [
    "=" * 78,
    "Eight-Group Direct Root Premise Audit",
    "=" * 78,
    "targets: pi_4^2, pi_5^2, pi_6^2, pi_7^2, pi_8^2, pi_9^2, pi_10^6, pi_12^7",
    "depth: 2",
    "production changes: none",
    "tests changes: none",
    "",
  ]

  for n, k in TARGETS:
    try:
      report = build_standard_toda_report(
        n=n,
        k=k,
      )

      if not report.candidates:
        raise RuntimeError(
          "standard report has no candidates"
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
      root_step = presentation.root_step
      depth_by_id = (
        _depth_by_step_id(
          presentation
        )
      )
      direct_edges = (
        _edges_for_parent(
          presentation,
          root_step,
        )
      )

      root_rows.append(
        {
          "n": n,
          "k": k,
          "group": (
            "pi_"
            + str(
              n + k
            )
            + "^"
            + str(
              n
            )
          ),
          "source_theorem": (
            presentation.source_entry.theorem
            or ""
          ),
          "root_statement_type": type(
            root_step.conclusion
          ).__name__,
          "root_statement": (
            _step_summary(
              root_step
            )
          ),
          "root_rule": (
            _rule_name(
              root_step
            )
          ),
          "root_reference": (
            _reference_name(
              root_step
            )
          ),
          "direct_premise_count": len(
            direct_edges
          ),
        }
      )

      report_lines.append(
        (
          "pi_"
          + str(
            n + k
          )
          + "^"
          + str(
            n
          )
          + "  "
          + (
            presentation.source_entry.theorem
            or ""
          )
        )
      )
      report_lines.append(
        "  root: "
        + _step_summary(
          root_step
        )
      )
      report_lines.append(
        "  root rule: "
        + _rule_name(
          root_step
        )
      )
      report_lines.append(
        "  direct premises: "
        + str(
          len(
            direct_edges
          )
        )
      )

      for edge in direct_edges:
        premise = edge.premise_step
        premise_class = (
          _classify_premise(
            premise,
            root_step,
          )
        )
        premise_reference = (
          _reference_name(
            premise
          )
        )
        premise_children = (
          _edges_for_parent(
            presentation,
            premise,
          )
        )

        direct_rows.append(
          {
            "n": n,
            "k": k,
            "group": (
              "pi_"
              + str(
                n + k
              )
              + "^"
              + str(
                n
              )
            ),
            "source_theorem": (
              presentation.source_entry.theorem
              or ""
            ),
            "premise_index": (
              edge.premise_index
            ),
            "premise_depth": (
              depth_by_id.get(
                id(
                  premise
                ),
                "",
              )
            ),
            "premise_class": (
              premise_class
            ),
            "premise_statement_type": type(
              premise.conclusion
            ).__name__,
            "premise_statement": (
              _step_summary(
                premise
              )
            ),
            "premise_rule": (
              _rule_name(
                premise
              )
            ),
            "premise_reference": (
              premise_reference
            ),
            "premise_has_literature_reference": (
              bool(
                premise_reference
              )
            ),
            "premise_child_count": len(
              premise_children
            ),
          }
        )

        report_lines.append(
          (
            "    P"
            + str(
              edge.premise_index + 1
            )
            + ": "
            + _step_summary(
              premise
            )
          )
        )
        report_lines.append(
          (
            "       class="
            + premise_class
            + "  depth="
            + str(
              depth_by_id.get(
                id(
                  premise
                ),
                ""
              )
            )
          )
        )
        report_lines.append(
          (
            "       rule="
            + _rule_name(
              premise
            )
          )
        )
        report_lines.append(
          (
            "       reference="
            + (
              premise_reference
              or "(none)"
            )
          )
        )

        for child_edge in premise_children:
          child = child_edge.premise_step
          child_reference = (
            _reference_name(
              child
            )
          )
          second_level_rows.append(
            {
              "n": n,
              "k": k,
              "group": (
                "pi_"
                + str(
                  n + k
                )
                + "^"
                + str(
                  n
                )
              ),
              "root_premise_index": (
                edge.premise_index
              ),
              "child_premise_index": (
                child_edge.premise_index
              ),
              "child_depth": (
                depth_by_id.get(
                  id(
                    child
                  ),
                  "",
                )
              ),
              "child_class": (
                _classify_premise(
                  child,
                  root_step,
                )
              ),
              "child_statement_type": type(
                child.conclusion
              ).__name__,
              "child_statement": (
                _step_summary(
                  child
                )
              ),
              "child_rule": (
                _rule_name(
                  child
                )
              ),
              "child_reference": (
                child_reference
              ),
              "child_has_literature_reference": (
                bool(
                  child_reference
                )
              ),
            }
          )

          report_lines.append(
            (
              "         -> P"
              + str(
                edge.premise_index + 1
              )
              + "."
              + str(
                child_edge.premise_index + 1
              )
              + ": "
              + _step_summary(
                child
              )
            )
          )
          report_lines.append(
            (
              "            rule="
              + _rule_name(
                child
              )
              + "  reference="
              + (
                child_reference
                or "(none)"
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
          "exception_type": type(
            exc
          ).__name__,
          "message": str(
            exc
          ),
          "traceback": traceback.format_exc(),
        }
      )

  literature_direct = sum(
    1
    for row in direct_rows
    if row[
      "premise_has_literature_reference"
    ]
  )
  unreferenced_direct = (
    len(
      direct_rows
    )
    - literature_direct
  )

  report_lines.extend(
    (
      "=" * 78,
      "Summary",
      "=" * 78,
      "target groups: "
      + str(
        len(
          TARGETS
        )
      ),
      "exceptions: "
      + str(
        len(
          exception_rows
        )
      ),
      "direct root premises: "
      + str(
        len(
          direct_rows
        )
      ),
      "direct premises with literature reference: "
      + str(
        literature_direct
      ),
      "direct premises without literature reference: "
      + str(
        unreferenced_direct
      ),
      "second-level premises: "
      + str(
        len(
          second_level_rows
        )
      ),
      "",
      "Output files:",
      "  direct_root_premise_report.txt",
      "  roots.csv",
      "  direct_root_premises_detailed.csv",
      "  second_level_premises.csv",
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
    / "direct_root_premise_report.txt"
  ).write_text(
    report_text + "\n",
    encoding="utf-8",
  )

  _write_csv(
    OUTPUT_DIR / "roots.csv",
    root_rows,
    (
      "n",
      "k",
      "group",
      "source_theorem",
      "root_statement_type",
      "root_statement",
      "root_rule",
      "root_reference",
      "direct_premise_count",
    ),
  )

  _write_csv(
    OUTPUT_DIR / "direct_root_premises_detailed.csv",
    direct_rows,
    (
      "n",
      "k",
      "group",
      "source_theorem",
      "premise_index",
      "premise_depth",
      "premise_class",
      "premise_statement_type",
      "premise_statement",
      "premise_rule",
      "premise_reference",
      "premise_has_literature_reference",
      "premise_child_count",
    ),
  )

  _write_csv(
    OUTPUT_DIR / "second_level_premises.csv",
    second_level_rows,
    (
      "n",
      "k",
      "group",
      "root_premise_index",
      "child_premise_index",
      "child_depth",
      "child_class",
      "child_statement_type",
      "child_statement",
      "child_rule",
      "child_reference",
      "child_has_literature_reference",
    ),
  )

  _write_csv(
    OUTPUT_DIR / "exception_inventory.csv",
    exception_rows,
    (
      "n",
      "k",
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
