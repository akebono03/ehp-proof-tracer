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
from toda_group_proof_narrative_argument_body import (
  extract_toda_group_proof_narrative_argument_body_blocks,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_argument_primary_exactness_component,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


N = 3
K = 1
MAX_DEPTH = 2

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
  if step.inference_rule is None:
    return ""
  return step.inference_rule.name


def block_index_map(blocks):
  return {
    id(block): index
    for index, block in enumerate(
      blocks
    )
  }


def block_summary(
  blocks,
  selected,
):
  index_by_id = block_index_map(
    blocks
  )
  rows = []

  for block in selected:
    rows.append(
      {
        "block_index": index_by_id[
          id(block)
        ],
        "role": block.role.value,
        "step_count": len(
          block.steps
        ),
        "steps": " | ".join(
          safe_render(step)
          or (
            type(
              step.conclusion
            ).__name__
            + " :: "
            + rule_name(step)
          )
          for step in block.steps
        ),
      }
    )

  return rows


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
      "pi_4^3 must have one candidate"
    )

  group_result = (
    report.candidates[0]
    .source_candidate
    .group_result
  )

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=MAX_DEPTH,
    )
  )

  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
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

  if len(arguments) != 1:
    raise AssertionError(
      "expected exactly one pi_4^3 Narrative Argument, "
      f"found {len(arguments)}"
    )

  argument_index = 0
  argument = arguments[
    argument_index
  ]

  evidence = (
    extract_toda_group_proof_narrative_argument_method_evidence(
      closure,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )

  components = (
    build_toda_group_proof_narrative_exactness_method_components(
      evidence
    )
  )

  primary_component = (
    select_toda_group_proof_narrative_argument_primary_exactness_component(
      closure,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )

  body_blocks = (
    extract_toda_group_proof_narrative_argument_body_blocks(
      closure,
      blocks,
      sidecar,
      arguments,
      argument_index,
      primary_component,
    )
  )

  local_body_blocks = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      closure,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )

  hidden_step_ids = (
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      closure,
      blocks,
      local_body_blocks,
      sidecar,
      argument,
    )
  )

  multi_markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      closure,
      blocks,
      sidecar,
      arguments,
    )
  )

  all_rows = block_summary(
    blocks,
    blocks,
  )
  body_rows = block_summary(
    blocks,
    body_blocks,
  )
  local_rows = block_summary(
    blocks,
    local_body_blocks,
  )
  evidence_rows = block_summary(
    blocks,
    evidence,
  )

  index_by_id = block_index_map(
    blocks
  )

  primary_indices = (
    []
    if primary_component is None
    else [
      index_by_id[
        id(block)
      ]
      for block in (
        primary_component
        .evidence_blocks
      )
    ]
  )

  hidden_rows = []
  for block_index, block in enumerate(
    blocks
  ):
    for step_index, step in enumerate(
      block.steps
    ):
      hidden_rows.append(
        {
          "block_index": block_index,
          "step_index": step_index,
          "role": block.role.value,
          "hidden_by_frontier": (
            id(step)
            in hidden_step_ids
          ),
          "statement_type": type(
            step.conclusion
          ).__name__,
          "rule": rule_name(step),
          "rendered": safe_render(
            step
          ),
        }
      )

  def write_csv(
    filename,
    rows,
    fieldnames,
  ):
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
      writer.writerows(
        rows
      )

  block_fields = (
    "block_index",
    "role",
    "step_count",
    "steps",
  )

  write_csv(
    "all_blocks.csv",
    all_rows,
    block_fields,
  )
  write_csv(
    "argument_body_blocks.csv",
    body_rows,
    block_fields,
  )
  write_csv(
    "local_body_blocks.csv",
    local_rows,
    block_fields,
  )
  write_csv(
    "method_evidence_blocks.csv",
    evidence_rows,
    block_fields,
  )
  write_csv(
    "frontier_hidden_steps.csv",
    hidden_rows,
    (
      "block_index",
      "step_index",
      "role",
      "hidden_by_frontier",
      "statement_type",
      "rule",
      "rendered",
    ),
  )

  (
    OUTPUT_DIR
    / "multi_argument_markdown.txt"
  ).write_text(
    multi_markdown + "\n",
    encoding="utf-8",
    newline="\n",
  )

  summary = [
    "=" * 80,
    "Phase 159 - pi_4^3 repair2 Argument body exposure audit",
    "=" * 80,
    "Production code changes: none",
    "Existing test changes: none",
    "",
    f"depth: {MAX_DEPTH}",
    f"presentation nodes: {len(presentation.nodes)}",
    f"closure nodes: {len(closure.nodes)}",
    f"blocks: {len(blocks)}",
    f"arguments: {len(arguments)}",
    "",
    "Argument:",
    (
      "  role: "
      + argument.role.value
    ),
    (
      "  direct supporting blocks: "
      + repr(
        [
          index_by_id[
            id(block)
          ]
          for block in (
            argument.supporting_blocks
          )
        ]
      )
    ),
    (
      "  child arguments: "
      + repr(
        list(
          argument.child_argument_indices
        )
      )
    ),
    (
      "  conclusion block: "
      + str(
        index_by_id[
          id(
            argument.conclusion_block
          )
        ]
      )
    ),
    "",
    (
      "Method evidence blocks: "
      + repr(
        [
          row[
            "block_index"
          ]
          for row in evidence_rows
        ]
      )
    ),
    (
      "Exactness components: "
      + str(
        len(
          components
        )
      )
    ),
    (
      "Primary exactness component blocks: "
      + repr(
        primary_indices
      )
    ),
    (
      "Recursive argument body blocks: "
      + repr(
        [
          row[
            "block_index"
          ]
          for row in body_rows
        ]
      )
    ),
    (
      "Local body blocks used by renderer: "
      + repr(
        [
          row[
            "block_index"
          ]
          for row in local_rows
        ]
      )
    ),
    (
      "Frontier-hidden step count: "
      + str(
        len(
          hidden_step_ids
        )
      )
    ),
    "",
    "All blocks:",
  ]

  for row in all_rows:
    summary.append(
      "  ["
      + str(
        row[
          "block_index"
        ]
      )
      + "] "
      + row[
        "role"
      ]
      + " :: "
      + row[
        "steps"
      ]
    )

  summary.extend(
    (
      "",
      "Renderer local body:",
    )
  )

  for row in local_rows:
    summary.append(
      "  ["
      + str(
        row[
          "block_index"
        ]
      )
      + "] "
      + row[
        "role"
      ]
      + " :: "
      + row[
        "steps"
      ]
    )

  summary.extend(
    (
      "",
      "Multi-argument markdown:",
      multi_markdown,
      "",
      "Interpretation guide:",
      (
        "  If recursive body contains ker(E), zero, exactness, "
        "and E-surjective but local body does not, the loss is "
        "in local-body selection."
      ),
      (
        "  If local body contains them but multi markdown omits them, "
        "the loss is in frontier hiding or body rendering/suppression."
      ),
      (
        "  If recursive body itself lacks them, the dependency graph "
        "or argument-body traversal is the defect."
      ),
      (
        "  Steps outside the semantic closure remain a separate "
        "depth/closure issue."
      ),
      "",
      "Boundary:",
      "  Audit only. No production repair is performed.",
      "  Repository-wide pytest is not run.",
      "=" * 80,
    )
  )

  summary_text = (
    "\n".join(
      summary
    )
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

  print(
    summary_text
  )
  print(
    "AUDIT_RESULT=PASS"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
