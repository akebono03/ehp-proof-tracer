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

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_references import (
  extract_toda_group_proof_step_literature_reference,
)
from test_phase68_pi_n_plus_4_n_zero import (
  build_phase68_10_data,
)
from test_phase70_pi_n_plus_5_n_zero import (
  build_phase70_9_data,
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


def _render(
  proof_step,
) -> str:
  return (
    _render_generic_narrative_step(
      proof_step
    )
  )


def _walk_ancestry(
  root_step,
  *,
  max_depth: int,
):
  rows = []
  visited = set()
  queue = [
    (
      root_step,
      0,
      "",
    ),
  ]

  while queue:
    (
      step,
      depth,
      path,
    ) = queue.pop(
      0
    )
    step_id = id(
      step
    )

    if (
      step_id in visited
      and depth > 0
    ):
      continue

    visited.add(
      step_id
    )

    rows.append(
      (
        depth,
        path,
        step,
      )
    )

    if depth >= max_depth:
      continue

    for premise_index, premise in enumerate(
      step.premises,
      start=1,
    ):
      child_path = (
        str(
          premise_index
        )
        if not path
        else (
          path
          + "."
          + str(
            premise_index
          )
        )
      )
      queue.append(
        (
          premise,
          depth + 1,
          child_path,
        )
      )

  return tuple(
    rows
  )


def _contains_step_identity(
  root_step,
  target_step,
) -> bool:
  visited = set()
  stack = [
    root_step,
  ]

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

    if step is target_step:
      return True

    stack.extend(
      step.premises
    )

  return False


def _contains_rule_fragment(
  root_step,
  fragment: str,
) -> bool:
  visited = set()
  stack = [
    root_step,
  ]

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

    if fragment in _rule_name(
      step
    ):
      return True

    stack.extend(
      step.premises
    )

  return False


def _build_target_data():
  phase68 = (
    build_phase68_10_data()
  )
  phase70 = (
    build_phase70_9_data()
  )

  return (
    {
      "n": 6,
      "k": 4,
      "label": "pi_10^6",
      "base_step": (
        phase68[
          "pi10_6_zero_step"
        ]
      ),
      "general_step": (
        phase68[
          "final_step"
        ]
      ),
      "range_step": (
        phase68[
          "n_ge_6_step"
        ]
      ),
      "stable_step": (
        phase68[
          "stable_isomorphism_step"
        ]
      ),
    },
    {
      "n": 7,
      "k": 5,
      "label": "pi_12^7",
      "base_step": (
        phase70[
          "pi12_7_zero_step"
        ]
      ),
      "general_step": (
        phase70[
          "higher_zero_step"
        ]
      ),
      "range_step": (
        phase70[
          "n_ge_7_step"
        ]
      ),
      "stable_step": (
        phase70[
          "stable_isomorphism_step"
        ]
      ),
    },
  )


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  comparison_rows = []
  ancestry_rows = []
  exception_rows = []

  report_lines = [
    "=" * 78,
    "Base-Case / Repository Root Direction Audit",
    "=" * 78,
    "targets: pi_10^6, pi_12^7",
    "production changes: none",
    "tests changes: none",
    "",
  ]

  try:
    targets = (
      _build_target_data()
    )
  except Exception as exc:
    exception_rows.append(
      {
        "target": "canonical builders",
        "exception_type": type(
          exc
        ).__name__,
        "message": str(
          exc
        ),
        "traceback": traceback.format_exc(),
      }
    )
    targets = ()

  for target in targets:
    n = target[
      "n"
    ]
    k = target[
      "k"
    ]
    label = target[
      "label"
    ]

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
      repository_root = (
        group_result.proof_step
      )
      base_step = target[
        "base_step"
      ]
      general_step = target[
        "general_step"
      ]
      stable_step = target[
        "stable_step"
      ]
      range_step = target[
        "range_step"
      ]

      same_conclusion_as_base = (
        repository_root.conclusion
        == base_step.conclusion
      )
      root_is_base_identity = (
        repository_root
        is base_step
      )
      root_contains_base_identity = (
        _contains_step_identity(
          repository_root,
          base_step,
        )
      )
      root_contains_general_identity = (
        _contains_step_identity(
          repository_root,
          general_step,
        )
      )
      general_contains_base_identity = (
        _contains_step_identity(
          general_step,
          base_step,
        )
      )
      base_contains_stable_identity = (
        _contains_step_identity(
          base_step,
          stable_step,
        )
      )
      base_contains_range_identity = (
        _contains_step_identity(
          base_step,
          range_step,
        )
      )
      general_contains_stable_identity = (
        _contains_step_identity(
          general_step,
          stable_step,
        )
      )
      general_contains_range_identity = (
        _contains_step_identity(
          general_step,
          range_step,
        )
      )

      comparison_rows.append(
        {
          "target": label,
          "source_theorem": (
            group_result.source_entry.theorem
            if hasattr(
              group_result,
              "source_entry"
            )
            else ""
          ),
          "repository_root_statement": (
            _render(
              repository_root
            )
          ),
          "repository_root_rule": (
            _rule_name(
              repository_root
            )
          ),
          "canonical_base_statement": (
            _render(
              base_step
            )
          ),
          "canonical_base_rule": (
            _rule_name(
              base_step
            )
          ),
          "canonical_general_statement": (
            _render(
              general_step
            )
          ),
          "canonical_general_rule": (
            _rule_name(
              general_step
            )
          ),
          "same_conclusion_as_base": (
            same_conclusion_as_base
          ),
          "repository_root_is_base_identity": (
            root_is_base_identity
          ),
          "repository_root_contains_base_identity": (
            root_contains_base_identity
          ),
          "repository_root_contains_general_identity": (
            root_contains_general_identity
          ),
          "general_contains_base_identity": (
            general_contains_base_identity
          ),
          "base_contains_stable_45": (
            base_contains_stable_identity
          ),
          "base_contains_range_condition": (
            base_contains_range_identity
          ),
          "general_contains_stable_45": (
            general_contains_stable_identity
          ),
          "general_contains_range_condition": (
            general_contains_range_identity
          ),
          "repository_root_contains_higher_transport_rule": (
            _contains_rule_fragment(
              repository_root,
              "higher",
            )
            and _contains_rule_fragment(
              repository_root,
              "zero transport",
            )
          ),
        }
      )

      report_lines.append(
        label
      )
      report_lines.append(
        "  Repository root:"
      )
      report_lines.append(
        "    "
        + _render(
          repository_root
        )
      )
      report_lines.append(
        "    rule="
        + _rule_name(
          repository_root
        )
      )
      report_lines.append(
        "    reference="
        + (
          _reference_name(
            repository_root
          )
          or "(none)"
        )
      )
      report_lines.append(
        "  Canonical base-case step:"
      )
      report_lines.append(
        "    "
        + _render(
          base_step
        )
      )
      report_lines.append(
        "    rule="
        + _rule_name(
          base_step
        )
      )
      report_lines.append(
        "    premises="
        + str(
          len(
            base_step.premises
          )
        )
      )

      for premise_index, premise in enumerate(
        base_step.premises,
        start=1,
      ):
        report_lines.append(
          (
            "      B"
            + str(
              premise_index
            )
            + ": "
            + _render(
              premise
            )
          )
        )
        report_lines.append(
          (
            "         rule="
            + _rule_name(
              premise
            )
            + "  reference="
            + (
              _reference_name(
                premise
              )
              or "(none)"
            )
          )
        )

      report_lines.append(
        "  Canonical general transport step:"
      )
      report_lines.append(
        "    "
        + _render(
          general_step
        )
      )
      report_lines.append(
        "    rule="
        + _rule_name(
          general_step
        )
      )
      report_lines.append(
        "    premises="
        + str(
          len(
            general_step.premises
          )
        )
      )

      for premise_index, premise in enumerate(
        general_step.premises,
        start=1,
      ):
        report_lines.append(
          (
            "      G"
            + str(
              premise_index
            )
            + ": "
            + _render(
              premise
            )
          )
        )
        report_lines.append(
          (
            "         rule="
            + _rule_name(
              premise
            )
            + "  reference="
            + (
              _reference_name(
                premise
              )
              or "(none)"
            )
          )
        )

      report_lines.append(
        "  Direction checks:"
      )
      report_lines.append(
        (
          "    repository conclusion == base conclusion: "
          + str(
            same_conclusion_as_base
          )
        )
      )
      report_lines.append(
        (
          "    repository root is canonical base identity: "
          + str(
            root_is_base_identity
          )
        )
      )
      report_lines.append(
        (
          "    general transport contains canonical base: "
          + str(
            general_contains_base_identity
          )
        )
      )
      report_lines.append(
        (
          "    canonical base contains Toda (4.5): "
          + str(
            base_contains_stable_identity
          )
        )
      )
      report_lines.append(
        (
          "    canonical base contains range condition: "
          + str(
            base_contains_range_identity
          )
        )
      )
      report_lines.append(
        (
          "    general transport contains Toda (4.5): "
          + str(
            general_contains_stable_identity
          )
        )
      )
      report_lines.append(
        (
          "    general transport contains range condition: "
          + str(
            general_contains_range_identity
          )
        )
      )
      report_lines.append(
        ""
      )

      for ancestry_kind, ancestry_root in (
        (
          "repository_root",
          repository_root,
        ),
        (
          "canonical_base",
          base_step,
        ),
        (
          "canonical_general",
          general_step,
        ),
      ):
        for (
          depth,
          path,
          step,
        ) in _walk_ancestry(
          ancestry_root,
          max_depth=3,
        ):
          ancestry_rows.append(
            {
              "target": label,
              "ancestry_kind": (
                ancestry_kind
              ),
              "depth": depth,
              "path": path,
              "statement_type": type(
                step.conclusion
              ).__name__,
              "statement": (
                _render(
                  step
                )
              ),
              "rule": (
                _rule_name(
                  step
                )
              ),
              "reference": (
                _reference_name(
                  step
                )
              ),
              "premise_count": len(
                step.premises
              ),
              "is_canonical_base_identity": (
                step is base_step
              ),
              "is_canonical_general_identity": (
                step is general_step
              ),
              "is_stable_45_identity": (
                step is stable_step
              ),
              "is_range_identity": (
                step is range_step
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
      "Interpretation rule",
      "=" * 78,
      (
        "A correct base-case direction has "
        "base_contains_stable_45=False and "
        "base_contains_range_condition=False."
      ),
      (
        "The general transport should instead contain "
        "the base-case step, Toda (4.5), and the range condition."
      ),
      (
        "If the repository root has the base conclusion but is not "
        "the canonical base step and reaches the general transport first, "
        "the repository proof root is directionally miswired."
      ),
      "",
      "Output files:",
      "  base_case_direction_report.txt",
      "  comparison.csv",
      "  ancestry_inventory.csv",
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
    / "base_case_direction_report.txt"
  ).write_text(
    report_text + "\n",
    encoding="utf-8",
  )

  _write_csv(
    OUTPUT_DIR / "comparison.csv",
    comparison_rows,
    (
      "target",
      "source_theorem",
      "repository_root_statement",
      "repository_root_rule",
      "canonical_base_statement",
      "canonical_base_rule",
      "canonical_general_statement",
      "canonical_general_rule",
      "same_conclusion_as_base",
      "repository_root_is_base_identity",
      "repository_root_contains_base_identity",
      "repository_root_contains_general_identity",
      "general_contains_base_identity",
      "base_contains_stable_45",
      "base_contains_range_condition",
      "general_contains_stable_45",
      "general_contains_range_condition",
      "repository_root_contains_higher_transport_rule",
    ),
  )

  _write_csv(
    OUTPUT_DIR / "ancestry_inventory.csv",
    ancestry_rows,
    (
      "target",
      "ancestry_kind",
      "depth",
      "path",
      "statement_type",
      "statement",
      "rule",
      "reference",
      "premise_count",
      "is_canonical_base_identity",
      "is_canonical_general_identity",
      "is_stable_45_identity",
      "is_range_identity",
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
