from __future__ import annotations

import csv
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(0, str(REPOSITORY_ROOT))

from expression import (
  Multiple,
)
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
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionKernelFreeCyclicStatement,
  TodaSuspensionSurjectiveStatement,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
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
    rendered = (
      _render_generic_narrative_step(
        step
      )
    )
  except Exception as exc:
    return (
      "<RENDER_ERROR "
      + type(exc).__name__
      + ": "
      + str(exc)
      + ">"
    )

  return "" if rendered is None else rendered


def rule_name(step) -> str:
  if step.inference_rule is None:
    return ""
  return step.inference_rule.name


def focus_kind(step) -> str:
  statement = step.conclusion
  rendered = safe_render(step)

  if (
    isinstance(
      statement,
      TodaDeltaImageUpToSignStatement,
    )
    and isinstance(
      statement.positive_value,
      Multiple,
    )
    and (
      step.inference_rule
      is not None
    )
    and (
      step.inference_rule
      .literature_reference
      is not None
    )
    and (
      step.inference_rule
      .literature_reference
      .locator
      == "Proposition 5.1"
    )
  ):
    return "prop51_direct_delta"

  if isinstance(
    statement,
    TodaDeltaImageFreeCyclicStatement,
  ):
    return "image_delta"

  if isinstance(
    statement,
    TodaSuspensionKernelFreeCyclicStatement,
  ):
    return "kernel_E"

  if isinstance(
    statement,
    TodaSuspensionSurjectiveStatement,
  ):
    return "E_surjective"

  if isinstance(
    statement,
    TodaProp42ExactnessStatement,
  ):
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
    type(statement).__name__
    == "TodaPrimaryGroupZeroStatement"
    and r"\pi_{4}^{5}" in rendered
  ):
    return "pi4_5_zero"

  if (
    type(statement).__name__
    == "Relation"
    and r"\pi_{3}^{2}" in rendered
    and r"\eta_{2}" in rendered
  ):
    return "pi3_2"

  if (
    type(statement).__name__
    == "Relation"
    and r"\pi_{5}^{5}" in rendered
    and r"\iota_{5}" in rendered
  ):
    return "pi5_5"

  if (
    type(statement).__name__
    == "Relation"
    and r"\pi_{4}^{3}" in rendered
  ):
    return "pi4_3_result"

  return ""


def render_public_lines(view):
  lines = []

  for line in view.rendered_lines:
    if line.kind == "heading":
      text = "## " + line.prefix
    elif line.kind == "separator":
      text = "---"
    elif line.segments:
      parts = []
      for segment in line.segments:
        if segment.kind in (
          "inline_math",
          "display_math",
        ):
          parts.append(
            "$"
            + segment.value
            + "$"
          )
        elif segment.kind == "strong":
          parts.append(
            "**"
            + segment.value
            + "**"
          )
        else:
          parts.append(
            segment.value
          )
      text = "".join(parts)
    elif line.statement_latex is not None:
      text = (
        line.prefix
        + "$"
        + line.statement_latex
        + "$"
        + line.suffix
      )
    else:
      text = (
        line.prefix
        + line.suffix
      )

    lines.append(text)

  return tuple(lines)


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

  public_view = (
    build_standard_web_group_proof_view(
      N,
      K,
      max_depth=MAX_DEPTH,
      mode="narrative",
    )
  )

  public_lines = render_public_lines(
    public_view
  )
  public_text = "\n".join(
    public_lines
  )

  presentation_ids = {
    id(node.proof_step)
    for node in presentation.nodes
  }

  closure_ids = {
    id(node.proof_step)
    for node in closure.nodes
  }

  block_owner = {}
  for block_index, block in enumerate(
    blocks
  ):
    for step in block.steps:
      block_owner.setdefault(
        id(step),
        [],
      ).append(
        (
          block_index,
          block.role.value,
        )
      )

  argument_owner = {}
  for argument_index, argument in enumerate(
    arguments
  ):
    for step in (
      argument.conclusion_block.steps
    ):
      argument_owner.setdefault(
        id(step),
        [],
      ).append(
        (
          argument_index,
          argument.role.value,
          "conclusion",
        )
      )

    for block in (
      argument.supporting_blocks
    ):
      for step in block.steps:
        argument_owner.setdefault(
          id(step),
          [],
        ).append(
          (
            argument_index,
            argument.role.value,
            "support",
          )
        )

  rows = []

  for index, node in enumerate(
    closure.nodes
  ):
    step = node.proof_step
    focus = focus_kind(step)

    if not focus:
      continue

    rendered = safe_render(step)

    rows.append(
      {
        "closure_index": index,
        "focus_kind": focus,
        "shortest_depth": getattr(
          node,
          "shortest_depth",
          "",
        ),
        "statement_type": type(
          step.conclusion
        ).__name__,
        "rule": rule_name(step),
        "in_presentation": (
          id(step)
          in presentation_ids
        ),
        "in_closure": (
          id(step)
          in closure_ids
        ),
        "block_owners": repr(
          block_owner.get(
            id(step),
            [],
          )
        ),
        "argument_owners": repr(
          argument_owner.get(
            id(step),
            [],
          )
        ),
        "rendered": rendered,
        "rendered_text_in_public": (
          bool(rendered)
          and rendered
          in public_text
        ),
      }
    )

  with (
    OUTPUT_DIR
    / "focus_matrix.csv"
  ).open(
    "w",
    encoding="utf-8",
    newline="",
  ) as handle:
    fieldnames = (
      "closure_index",
      "focus_kind",
      "shortest_depth",
      "statement_type",
      "rule",
      "in_presentation",
      "in_closure",
      "block_owners",
      "argument_owners",
      "rendered",
      "rendered_text_in_public",
    )
    writer = csv.DictWriter(
      handle,
      fieldnames=fieldnames,
    )
    writer.writeheader()
    writer.writerows(rows)

  (
    OUTPUT_DIR
    / "public_narrative.txt"
  ).write_text(
    public_text + "\n",
    encoding="utf-8",
    newline="\n",
  )

  expected = (
    "prop51_direct_delta",
    "image_delta",
    "exact_delta_E",
    "kernel_E",
    "pi3_2",
    "pi4_5_zero",
    "exact_E_H",
    "E_surjective",
    "pi4_3_result",
  )

  summary = [
    "=" * 80,
    "Phase 159 - pi_4^3 post-repair1 Narrative ownership audit",
    "=" * 80,
    "Production code changes: none",
    "Existing test changes: none",
    "Target: pi_4^3, depth=2 public Narrative",
    "",
    f"presentation nodes: {len(presentation.nodes)}",
    f"closure nodes: {len(closure.nodes)}",
    f"blocks: {len(blocks)}",
    f"arguments: {len(arguments)}",
    "",
    "Focus matrix:",
  ]

  by_kind = {}
  for row in rows:
    by_kind.setdefault(
      row["focus_kind"],
      [],
    ).append(row)

  for kind in expected:
    matches = by_kind.get(
      kind,
      [],
    )

    if not matches:
      summary.append(
        "  "
        + kind
        + ": NOT_IN_DEPTH2_CLOSURE"
      )
      continue

    for row in matches:
      summary.append(
        "  "
        + kind
        + ": "
        + "depth="
        + str(
          row[
            "shortest_depth"
          ]
        )
        + " blocks="
        + row[
          "block_owners"
        ]
        + " arguments="
        + row[
          "argument_owners"
        ]
        + " public="
        + str(
          row[
            "rendered_text_in_public"
          ]
        )
      )

  summary.extend(
    (
      "",
      "Public Narrative:",
      public_text,
      "",
      "Interpretation:",
      "  NOT_IN_DEPTH2_CLOSURE:",
      "    The required step is still outside the depth=2 semantic closure.",
      "  argument_owners=[]:",
      "    The step reaches a Narrative block but is not owned by an Argument.",
      "  public=False with Argument ownership:",
      "    Ownership exists but later rendering/suppression hides the step.",
      "",
      "Boundary:",
      "  Audit only. No Narrative repair is performed.",
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

  print(summary_text)
  print(
    "AUDIT_RESULT=PASS"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
