from __future__ import annotations

import csv
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(0, str(REPOSITORY_ROOT))

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
  build_toda_group_result_proof_replay,
)
from toda_proof_dependency import (
  extract_toda_recursive_proof_provenance,
)


N = 3
K = 1

OUTPUT_DIR = (
  Path(__file__).resolve().parent
  / "audit_output"
)


def safe_render(step) -> str:
  try:
    value = _render_generic_narrative_step(
      step
    )
  except Exception as exc:
    return (
      "<RENDER_ERROR "
      + type(exc).__name__
      + ": "
      + str(exc)
      + ">"
    )

  return "" if value is None else value


def rule_name(step) -> str:
  rule = getattr(
    step,
    "inference_rule",
    None,
  )
  if rule is None:
    return ""
  return str(
    getattr(
      rule,
      "name",
      "",
    )
  )


def statement_type(step) -> str:
  return type(
    step.conclusion
  ).__name__


def focus_kind(step, rendered: str) -> str:
  t = statement_type(step)
  rule = rule_name(step)
  compact = (
    rendered
    .replace(" ", "")
    .replace(r"\left", "")
    .replace(r"\right", "")
  )

  if (
    "two eta2 up to sign"
    in rule.lower()
    or (
      "iota5" in rule.lower()
      and "eta2" in rule.lower()
    )
  ):
    return "delta_iota5_pm_2eta2"

  if (
    t == "TodaDeltaImageUpToSignStatement"
    and (
      r"2\eta" in compact
      or "2η" in compact
    )
  ):
    return "delta_iota5_pm_2eta2"

  if (
    t == "TodaDeltaImageFreeCyclicStatement"
  ):
    return "image_delta_Z_2eta2"

  if (
    t
    == "TodaSuspensionKernelFreeCyclicStatement"
  ):
    return "kernel_E_Z_2eta2"

  if (
    t
    == "TodaSuspensionSurjectiveStatement"
  ):
    return "E_surjective"

  if t == "TodaProp42ExactnessStatement":
    if (
      r"\pi_{5}^{5}" in rendered
      and r"\pi_{3}^{2}" in rendered
      and r"\pi_{4}^{3}" in rendered
    ):
      return "exact_delta_E"

    if (
      r"\pi_{3}^{2}" in rendered
      and r"\pi_{4}^{3}" in rendered
      and r"\pi_{4}^{5}" in rendered
    ):
      return "exact_E_H"

  if (
    t == "Relation"
    and r"\pi_{5}^{5}" in rendered
    and r"\iota_{5}" in rendered
  ):
    return "pi5_5_Z_iota5"

  if (
    t == "Relation"
    and r"\pi_{3}^{2}" in rendered
    and r"\eta_{2}" in rendered
    and r"\mathbb{Z}" in rendered
  ):
    return "pi3_2_Z_eta2"

  if (
    t == "Relation"
    and r"\pi_{4}^{5}" in rendered
    and (
      "=0" in compact
      or "= 0" in rendered
    )
  ):
    return "pi4_5_zero"

  if (
    t == "Relation"
    and r"\pi_{4}^{3}" in rendered
    and r"\mathbb{Z}/2" in rendered
  ):
    return "pi4_3_Z2_eta3"

  return ""


def write_csv(
  filename: str,
  fieldnames,
  rows,
) -> None:
  with (
    OUTPUT_DIR
    / filename
  ).open(
    "w",
    encoding="utf-8",
    newline="",
  ) as handle:
    writer = csv.DictWriter(
      handle,
      fieldnames=fieldnames,
    )
    writer.writeheader()
    writer.writerows(rows)


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  report = build_standard_toda_report(
    n=N,
    k=K,
  )
  if len(report.candidates) != 1:
    raise AssertionError(
      "pi_4^3 must have exactly one candidate"
    )

  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )

  provenance = (
    extract_toda_recursive_proof_provenance(
      group_result
    )
  )

  complete = (
    build_complete_toda_group_result_proof_replay(
      group_result
    )
  )

  depth_by_step_id = {
    id(node.proof_step):
      node.shortest_depth
    for node in provenance.nodes
  }

  all_rows = []
  focus_rows = []

  for index, node in enumerate(
    provenance.nodes
  ):
    step = node.proof_step
    rendered = safe_render(step)
    focus = focus_kind(
      step,
      rendered,
    )
    row = {
      "provenance_index": index,
      "depth": node.shortest_depth,
      "focus_kind": focus,
      "statement_type": (
        statement_type(step)
      ),
      "inference_rule": (
        rule_name(step)
      ),
      "premise_count": len(
        step.premises
      ),
      "rendered": rendered,
    }
    all_rows.append(row)
    if focus:
      focus_rows.append(row)

  edge_rows = []
  for edge in provenance.edges:
    parent_rendered = safe_render(
      edge.parent_step
    )
    premise_rendered = safe_render(
      edge.premise_step
    )
    edge_rows.append(
      {
        "parent_depth": (
          depth_by_step_id[
            id(edge.parent_step)
          ]
        ),
        "parent_focus": (
          focus_kind(
            edge.parent_step,
            parent_rendered,
          )
        ),
        "parent_type": (
          statement_type(
            edge.parent_step
          )
        ),
        "parent_rule": (
          rule_name(
            edge.parent_step
          )
        ),
        "premise_depth": (
          depth_by_step_id[
            id(edge.premise_step)
          ]
        ),
        "premise_focus": (
          focus_kind(
            edge.premise_step,
            premise_rendered,
          )
        ),
        "premise_type": (
          statement_type(
            edge.premise_step
          )
        ),
        "premise_rule": (
          rule_name(
            edge.premise_step
          )
        ),
        "premise_slot": (
          edge.premise_index
        ),
      }
    )

  depth_rows = []
  for depth in range(
    complete.max_depth + 1
  ):
    replay = (
      build_toda_group_result_proof_replay(
        group_result,
        max_depth=depth,
      )
    )
    raw = (
      build_toda_group_proof_presentation(
        replay
      )
    )
    closure = (
      build_toda_group_proof_narrative_semantic_closure_presentation(
        raw
      )
    )
    sidecar = (
      build_toda_group_proof_narrative_semantic_sidecar(
        closure
      )
    )
    blocks = (
      build_toda_group_proof_narrative_blocks(
        closure,
        sidecar,
      )
    )
    arguments = (
      build_toda_group_proof_narrative_arguments(
        closure,
        blocks,
        sidecar,
      )
    )

    raw_ids = {
      id(node.proof_step)
      for node in raw.nodes
    }
    closure_ids = {
      id(node.proof_step)
      for node in closure.nodes
    }
    block_ids = {
      id(step)
      for block in blocks
      for step in block.steps
    }
    owned_ids = {
      id(step)
      for argument in arguments
      for block in (
        argument.supporting_blocks
        + (
          argument.conclusion_block,
        )
      )
      for step in block.steps
    }

    for focus_row in focus_rows:
      node = provenance.nodes[
        focus_row[
          "provenance_index"
        ]
      ]
      step_id = id(
        node.proof_step
      )
      depth_rows.append(
        {
          "requested_depth": depth,
          "focus_kind": (
            focus_row[
              "focus_kind"
            ]
          ),
          "actual_shortest_depth": (
            focus_row[
              "depth"
            ]
          ),
          "in_raw": (
            step_id in raw_ids
          ),
          "in_closure": (
            step_id in closure_ids
          ),
          "in_blocks": (
            step_id in block_ids
          ),
          "owned_by_argument": (
            step_id in owned_ids
          ),
        }
      )

  direct_delta_rows = tuple(
    row
    for row in all_rows
    if (
      "iota5"
      in row["inference_rule"].lower()
      and "eta2"
      in row["inference_rule"].lower()
    )
    or (
      row["focus_kind"]
      == "delta_iota5_pm_2eta2"
    )
  )

  expected = (
    "pi5_5_Z_iota5",
    "delta_iota5_pm_2eta2",
    "image_delta_Z_2eta2",
    "exact_delta_E",
    "kernel_E_Z_2eta2",
    "pi3_2_Z_eta2",
    "exact_E_H",
    "pi4_5_zero",
    "E_surjective",
    "pi4_3_Z2_eta3",
  )

  by_focus = {}
  for row in focus_rows:
    by_focus.setdefault(
      row["focus_kind"],
      [],
    ).append(row)

  summary = [
    "=" * 80,
    "Phase 159 - pi_4^3 provenance depth / ownership audit",
    "=" * 80,
    "Production code changes: none",
    "Existing test changes: none",
    f"complete provenance nodes: {len(provenance.nodes)}",
    f"complete provenance edges: {len(provenance.edges)}",
    f"complete max depth: {complete.max_depth}",
    "",
    "Required-chain shortest depths:",
  ]

  for kind in expected:
    matches = by_focus.get(
      kind,
      [],
    )
    if not matches:
      summary.append(
        f"  {kind}: NOT_IN_PROVENANCE"
      )
      continue

    depth_text = ", ".join(
      str(row["depth"])
      for row in matches
    )
    summary.append(
      f"  {kind}: depth={depth_text}"
    )

  summary.extend(
    (
      "",
      "Direct Delta(iota_5)=+/-2eta_2 ancestry candidates:",
    )
  )

  if not direct_delta_rows:
    summary.append(
      "  none"
    )
  else:
    for row in direct_delta_rows:
      summary.extend(
        (
          (
            "  depth="
            + str(row["depth"])
            + " focus="
            + row["focus_kind"]
          ),
          (
            "    type="
            + row["statement_type"]
          ),
          (
            "    rule="
            + row["inference_rule"]
          ),
          (
            "    rendered="
            + row["rendered"]
          ),
        )
      )

  summary.extend(
    (
      "",
      "Interpretation:",
      "  A required node at depth > 2 explains depth=2 replay truncation.",
      "  NOT_IN_PROVENANCE means the current group-result ancestry is not connected to that fact.",
      "  owned_by_argument=False after the node is present identifies a separate Narrative ownership defect.",
      "",
      "Output:",
      "  audit_output/summary.txt",
      "  audit_output/all_provenance_nodes.csv",
      "  audit_output/focus_nodes.csv",
      "  audit_output/provenance_edges.csv",
      "  audit_output/depth_matrix.csv",
      "",
      "Boundary:",
      "  Audit only. No production repair is performed.",
      "  Repository-wide pytest is not run.",
      "=" * 80,
    )
  )

  summary_text = (
    "\n".join(summary)
    + "\n"
  )

  (
    OUTPUT_DIR
    / "summary.txt"
  ).write_text(
    summary_text,
    encoding="utf-8",
    newline="\n",
  )

  write_csv(
    "all_provenance_nodes.csv",
    (
      "provenance_index",
      "depth",
      "focus_kind",
      "statement_type",
      "inference_rule",
      "premise_count",
      "rendered",
    ),
    all_rows,
  )

  write_csv(
    "focus_nodes.csv",
    (
      "provenance_index",
      "depth",
      "focus_kind",
      "statement_type",
      "inference_rule",
      "premise_count",
      "rendered",
    ),
    focus_rows,
  )

  write_csv(
    "provenance_edges.csv",
    (
      "parent_depth",
      "parent_focus",
      "parent_type",
      "parent_rule",
      "premise_depth",
      "premise_focus",
      "premise_type",
      "premise_rule",
      "premise_slot",
    ),
    edge_rows,
  )

  write_csv(
    "depth_matrix.csv",
    (
      "requested_depth",
      "focus_kind",
      "actual_shortest_depth",
      "in_raw",
      "in_closure",
      "in_blocks",
      "owned_by_argument",
    ),
    depth_rows,
  )

  print(summary_text)
  print("AUDIT_RESULT=PASS")

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
