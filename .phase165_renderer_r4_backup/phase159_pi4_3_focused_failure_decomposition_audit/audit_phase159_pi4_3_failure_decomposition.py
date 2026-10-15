from __future__ import annotations

import csv
import re
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
  build_toda_group_result_proof_replay,
)
from web_group_proof import (
  WebGroupProofRenderedLineView,
  build_standard_web_group_proof_view,
)


N = 3
K = 1
MAX_DEPTH = 2

OUTPUT_DIR = (
  Path(__file__).resolve().parent
  / "audit_output"
)

REFERENCE_PREFIX_RE = re.compile(
  r"^\[R\d+\](?:(?:より)|(?:を用いて)|(?:を用いる))?"
  r"[\s,、.。]*"
)

TRAILING_PUNCTUATION = (
  ".",
  "。",
  ",",
  "、",
)


def render_web_line(
  line: WebGroupProofRenderedLineView,
) -> str:
  if line.kind == "heading":
    return "## " + line.prefix

  if line.kind == "separator":
    return "---"

  parts = []

  for segment in line.segments:
    if segment.kind == "text":
      parts.append(segment.value)
    elif segment.kind == "strong":
      parts.append(
        "**"
        + segment.value
        + "**"
      )
    elif segment.kind == "inline_math":
      parts.append(
        "$"
        + segment.value
        + "$"
      )
    elif segment.kind == "display_math":
      parts.append(
        "$"
        + segment.value
        + "$"
      )
    else:
      raise ValueError(
        "unsupported inline segment kind: "
        + segment.kind
      )

  if parts:
    return "".join(parts)

  if line.statement_latex is not None:
    return (
      line.prefix
      + "$"
      + line.statement_latex
      + "$"
      + line.suffix
    )

  return (
    line.prefix
    + line.suffix
  )


def proof_body_lines(
  rendered_lines: tuple[
    WebGroupProofRenderedLineView,
    ...,
  ],
) -> tuple[str, ...]:
  in_proof = False
  body = []

  for line in rendered_lines:
    if (
      line.kind == "heading"
      and line.prefix == "証明"
    ):
      in_proof = True
      continue

    if not in_proof:
      continue

    rendered = render_web_line(line)
    if rendered.strip():
      body.append(rendered)

  return tuple(body)


def normalize_visible_text(
  text: str,
) -> str:
  normalized = " ".join(
    text.strip().split()
  )

  normalized = REFERENCE_PREFIX_RE.sub(
    "",
    normalized,
    count=1,
  )

  while (
    normalized
    and normalized[-1]
    in TRAILING_PUNCTUATION
  ):
    normalized = (
      normalized[:-1].rstrip()
    )

  return normalized


def safe_render_step(
  proof_step,
) -> str:
  try:
    rendered = (
      _render_generic_narrative_step(
        proof_step
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

  if rendered is None:
    return ""

  return rendered


def inference_name(
  proof_step,
) -> str:
  rule = getattr(
    proof_step,
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


def statement_type(
  proof_step,
) -> str:
  return type(
    proof_step.conclusion
  ).__name__


def focus_kind(
  proof_step,
  rendered: str,
) -> str:
  type_name = statement_type(
    proof_step
  )
  compact = (
    rendered
    .replace(" ", "")
    .replace(r"\left", "")
    .replace(r"\right", "")
  )

  if (
    type_name
    == "TodaDeltaImageUpToSignStatement"
  ):
    return "delta_iota5_pm_2eta2"

  if (
    type_name
    == "TodaDeltaImageFreeCyclicStatement"
  ):
    return "image_delta_Z_2eta2"

  if (
    type_name
    == "TodaSuspensionKernelFreeCyclicStatement"
  ):
    return "kernel_E_Z_2eta2"

  if (
    type_name
    == "TodaSuspensionSurjectiveStatement"
  ):
    return "E_surjective"

  if (
    type_name
    == "TodaProp42ExactnessStatement"
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
    type_name == "Relation"
    and r"\pi_{3}^{2}" in rendered
    and r"\mathbb{Z}" in rendered
    and r"\eta_{2}" in rendered
  ):
    return "pi3_2_Z_eta2"

  if (
    type_name == "Relation"
    and r"\pi_{4}^{5}" in rendered
    and (
      "=0" in compact
      or "= 0" in rendered
    )
  ):
    return "pi4_5_zero"

  if (
    type_name == "Relation"
    and r"\pi_{5}^{5}" in rendered
    and r"\mathbb{Z}" in rendered
    and r"\iota_{5}" in rendered
  ):
    return "pi5_5_Z_iota5"

  if (
    type_name == "Relation"
    and r"\pi_{4}^{3}" in rendered
    and r"\mathbb{Z}/2" in rendered
  ):
    return "pi4_3_Z2_eta3"

  if (
    type_name == "Relation"
    and r"\eta_{3}" in rendered
    and r"\eta_{2}" in rendered
    and (
      "E" in rendered
      or r"\Sigma" in rendered
    )
  ):
    return "E_eta2_eta3"

  return ""


def build_step_locations(
  raw_presentation,
  closure,
  blocks,
  arguments,
  body_lines: tuple[str, ...],
):
  raw_step_ids = {
    id(node.proof_step)
    for node in raw_presentation.nodes
  }

  block_locations = {}
  for block_index, block in enumerate(
    blocks
  ):
    for proof_step in block.steps:
      block_locations[
        id(proof_step)
      ] = (
        block_index,
        block.role.value,
      )

  argument_locations = {}
  for argument_index, argument in enumerate(
    arguments
  ):
    for proof_step in (
      argument.conclusion_block.steps
    ):
      argument_locations.setdefault(
        id(proof_step),
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
      for proof_step in block.steps:
        argument_locations.setdefault(
          id(proof_step),
          [],
        ).append(
          (
            argument_index,
            argument.role.value,
            "support",
          )
        )

  normalized_body = tuple(
    normalize_visible_text(
      line
    )
    for line in body_lines
  )

  rows = []

  for closure_index, node in enumerate(
    closure.nodes
  ):
    proof_step = node.proof_step
    rendered = safe_render_step(
      proof_step
    )
    normalized_rendered = (
      normalize_visible_text(
        rendered
      )
      if rendered
      else ""
    )

    body_positions = tuple(
      index
      for index, line in enumerate(
        normalized_body
      )
      if (
        normalized_rendered
        and line == normalized_rendered
      )
    )

    block_info = (
      block_locations.get(
        id(proof_step)
      )
    )

    argument_info = (
      argument_locations.get(
        id(proof_step),
        [],
      )
    )

    rows.append(
      {
        "closure_index": (
          closure_index
        ),
        "shortest_depth": (
          getattr(
            node,
            "shortest_depth",
            "",
          )
        ),
        "focus_kind": (
          focus_kind(
            proof_step,
            rendered,
          )
        ),
        "statement_type": (
          statement_type(
            proof_step
          )
        ),
        "inference_rule": (
          inference_name(
            proof_step
          )
        ),
        "in_raw_depth2": (
          id(proof_step)
          in raw_step_ids
        ),
        "in_closure": True,
        "block_index": (
          ""
          if block_info is None
          else block_info[0]
        ),
        "block_role": (
          ""
          if block_info is None
          else block_info[1]
        ),
        "argument_locations": repr(
          argument_info
        ),
        "public_body_positions": repr(
          body_positions
        ),
        "public_visible_exact": (
          len(body_positions) > 0
        ),
        "generic_rendered": rendered,
      }
    )

  return rows


def classify_focus_stage(
  row,
) -> str:
  if not row["in_raw_depth2"]:
    return "NOT_IN_RAW_DEPTH2"

  if not row["in_closure"]:
    return "LOST_BEFORE_CLOSURE"

  if row["block_index"] == "":
    return "LOST_BEFORE_BLOCKS"

  if row["argument_locations"] == "[]":
    return "NOT_OWNED_BY_ARGUMENT"

  if not row["public_visible_exact"]:
    return "LOST_BEFORE_PUBLIC_BODY"

  return "PUBLIC_VISIBLE"


def write_csv(
  path: Path,
  fieldnames,
  rows,
) -> None:
  with path.open(
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

  if len(
    report.candidates
  ) != 1:
    raise AssertionError(
      "pi_4^3 must have exactly one "
      "proof-backed group-result candidate"
    )

  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=MAX_DEPTH,
    )
  )

  raw_presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw_presentation
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

  body_lines = proof_body_lines(
    public_view.rendered_lines
  )

  rows = build_step_locations(
    raw_presentation,
    closure,
    blocks,
    arguments,
    body_lines,
  )

  for row in rows:
    row["failure_stage"] = (
      classify_focus_stage(
        row
      )
    )

  focus_rows = tuple(
    row
    for row in rows
    if row["focus_kind"]
  )

  expected_focus = {
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
  }

  found_focus = {
    row["focus_kind"]
    for row in focus_rows
  }

  missing_focus = sorted(
    expected_focus
    - found_focus
  )

  duplicate_focus = sorted(
    kind
    for kind in expected_focus
    if sum(
      1
      for row in focus_rows
      if row["focus_kind"] == kind
    ) > 1
  )

  edge_rows = []
  closure_index_by_step_id = {
    id(node.proof_step): index
    for index, node in enumerate(
      closure.nodes
    )
  }

  focus_kind_by_step_id = {
    id(
      closure.nodes[
        row["closure_index"]
      ].proof_step
    ): row["focus_kind"]
    for row in focus_rows
  }

  for edge in closure.edges:
    parent_id = id(
      edge.parent_step
    )
    premise_id = id(
      edge.premise_step
    )
    parent_focus = (
      focus_kind_by_step_id.get(
        parent_id,
        "",
      )
    )
    premise_focus = (
      focus_kind_by_step_id.get(
        premise_id,
        "",
      )
    )

    if not (
      parent_focus
      or premise_focus
    ):
      continue

    edge_rows.append(
      {
        "parent_index": (
          closure_index_by_step_id[
            parent_id
          ]
        ),
        "parent_focus": (
          parent_focus
        ),
        "parent_type": (
          statement_type(
            edge.parent_step
          )
        ),
        "premise_index": (
          closure_index_by_step_id[
            premise_id
          ]
        ),
        "premise_focus": (
          premise_focus
        ),
        "premise_type": (
          statement_type(
            edge.premise_step
          )
        ),
        "premise_slot": (
          edge.premise_index
        ),
      }
    )

  fields = (
    "closure_index",
    "shortest_depth",
    "focus_kind",
    "failure_stage",
    "statement_type",
    "inference_rule",
    "in_raw_depth2",
    "in_closure",
    "block_index",
    "block_role",
    "argument_locations",
    "public_body_positions",
    "public_visible_exact",
    "generic_rendered",
  )

  write_csv(
    OUTPUT_DIR
    / "all_steps.csv",
    fields,
    rows,
  )

  write_csv(
    OUTPUT_DIR
    / "focus_chain.csv",
    fields,
    focus_rows,
  )

  write_csv(
    OUTPUT_DIR
    / "focus_edges.csv",
    (
      "parent_index",
      "parent_focus",
      "parent_type",
      "premise_index",
      "premise_focus",
      "premise_type",
      "premise_slot",
    ),
    edge_rows,
  )

  (
    OUTPUT_DIR
    / "public_body.txt"
  ).write_text(
    "\n".join(
      f"{index:03d}: {line}"
      for index, line in enumerate(
        body_lines
      )
    )
    + "\n",
    encoding="utf-8",
    newline="\n",
  )

  (
    OUTPUT_DIR
    / "focus_chain.txt"
  ).write_text(
    "\n".join(
      (
        f"[{row['focus_kind']}] "
        f"stage={row['failure_stage']} "
        f"raw={row['in_raw_depth2']} "
        f"block={row['block_index']}:{row['block_role']} "
        f"args={row['argument_locations']} "
        f"public={row['public_body_positions']}\n"
        f"  type={row['statement_type']}\n"
        f"  rule={row['inference_rule']}\n"
        f"  rendered={row['generic_rendered']}"
      )
      for row in focus_rows
    )
    + "\n",
    encoding="utf-8",
    newline="\n",
  )

  summary = [
    "=" * 78,
    "Phase 159 - pi_4^3 focused failure decomposition audit",
    "=" * 78,
    "Production code changes: none",
    "Existing test changes: none",
    "Target: pi_4^3 (n=3, k=1), public depth=2 Narrative",
    "",
    f"raw nodes: {len(raw_presentation.nodes)}",
    f"closure nodes: {len(closure.nodes)}",
    f"blocks: {len(blocks)}",
    f"arguments: {len(arguments)}",
    f"public proof-body lines: {len(body_lines)}",
    "",
    "Expected proof chain:",
    "  pi_5^5 = Z{iota_5}",
    "  -> Delta(iota_5) = +/- 2 eta_2",
    "  -> Im Delta = Z{2 eta_2}",
    "  -> exactness",
    "  -> ker E = Z{2 eta_2}",
    "  -> pi_3^2 = Z{eta_2}",
    "  -> exactness with pi_4^5 = 0",
    "  -> E surjective",
    "  -> pi_4^3 = Z/2{eta_3}",
    "",
    "Focus classification:",
  ]

  for row in focus_rows:
    summary.append(
      "  "
      + row["focus_kind"]
      + ": "
      + row["failure_stage"]
    )

  summary.extend(
    (
      "",
      "Missing expected focus nodes:",
      (
        "  none"
        if not missing_focus
        else "  "
        + ", ".join(
          missing_focus
        )
      ),
      "",
      "Duplicate focus nodes:",
      (
        "  none"
        if not duplicate_focus
        else "  "
        + ", ".join(
          duplicate_focus
        )
      ),
      "",
      "Interpretation:",
      "  NOT_IN_RAW_DEPTH2      = depth=2 replay does not expose the required step.",
      "  LOST_BEFORE_BLOCKS     = semantic closure has it, but block construction loses it.",
      "  NOT_OWNED_BY_ARGUMENT  = block exists, but no Narrative Argument owns it.",
      "  LOST_BEFORE_PUBLIC_BODY= structural pipeline retains it, public body suppresses it.",
      "  PUBLIC_VISIBLE         = the generic-rendered step is visibly present in public proof body.",
      "",
      "Output:",
      "  audit_output/summary.txt",
      "  audit_output/public_body.txt",
      "  audit_output/focus_chain.txt",
      "  audit_output/focus_chain.csv",
      "  audit_output/focus_edges.csv",
      "  audit_output/all_steps.csv",
      "",
      "Boundary:",
      "  Audit only. No production repair is performed.",
      "  Repository-wide pytest is not run.",
      "=" * 78,
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

  if missing_focus:
    print(
      "AUDIT_RESULT=NEEDS_CLASSIFICATION"
    )
  else:
    print(
      "AUDIT_RESULT=PASS_DECOMPOSITION"
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
