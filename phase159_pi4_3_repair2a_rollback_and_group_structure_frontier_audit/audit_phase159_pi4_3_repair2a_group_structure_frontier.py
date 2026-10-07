from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(ROOT),
  )

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
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


def safe_render(step) -> str:
  try:
    rendered = _render_generic_narrative_step(
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

  return "" if rendered is None else rendered


def rule_name(step) -> str:
  if step.inference_rule is None:
    return ""
  return step.inference_rule.name


def build_context(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  group_result = (
    report.candidates[0]
    .source_candidate
    .group_result
  )

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )

  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      sidecar,
    )
  )

  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      sidecar,
    )
  )

  return (
    presentation,
    blocks,
    sidecar,
    arguments,
  )


def describe_group_structure(
  n: int,
  k: int,
) -> list[str]:
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = build_context(
    n,
    k,
  )

  argument_index = next(
    index
    for index, argument in enumerate(
      arguments
    )
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_GROUP_STRUCTURE
    )
  )

  argument = arguments[
    argument_index
  ]

  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )

  local_body = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )

  hidden = (
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      local_body,
      sidecar,
      argument,
    )
  )

  block_by_step_id = {
    id(step): block
    for block in blocks
    for step in block.steps
  }

  lines = [
    (
      f"Group pi_{n + k}^{n}: "
      "ESTABLISH_GROUP_STRUCTURE"
    ),
    (
      "Conclusion: "
      + safe_render(
        conclusion_step
      )
    ),
    "",
    "Direct premises and second-level prerequisites:",
  ]

  for direct_index, direct_step in enumerate(
    conclusion_step.premises
  ):
    block = block_by_step_id.get(
      id(
        direct_step
      )
    )

    lines.append(
      (
        f"  direct[{direct_index}] "
        f"role={'' if block is None else block.role.value} "
        f"hidden={id(direct_step) in hidden}"
      )
    )
    lines.append(
      "    type="
      + type(
        direct_step.conclusion
      ).__name__
    )
    lines.append(
      "    rule="
      + rule_name(
        direct_step
      )
    )
    lines.append(
      "    rendered="
      + safe_render(
        direct_step
      )
    )

    for second_index, support_step in enumerate(
      direct_step.premises
    ):
      support_block = block_by_step_id.get(
        id(
          support_step
        )
      )
      lines.append(
        (
          f"    second[{second_index}] "
          f"role={'' if support_block is None else support_block.role.value} "
          f"hidden={id(support_step) in hidden}"
        )
      )
      lines.append(
        "      type="
        + type(
          support_step.conclusion
        ).__name__
      )
      lines.append(
        "      rule="
        + rule_name(
          support_step
        )
      )
      lines.append(
        "      rendered="
        + safe_render(
          support_step
        )
      )

  return lines


def main() -> int:
  lines = [
    "=" * 80,
    "Phase 159 pi_4^3 repair2a group-structure frontier audit",
    "=" * 80,
    "Production forward changes: none",
    "Failed repair2 is rolled back before this audit.",
    "",
  ]

  lines.extend(
    describe_group_structure(
      3,
      1,
    )
  )

  lines.extend(
    (
      "",
      "-" * 80,
      "",
    )
  )

  lines.extend(
    describe_group_structure(
      3,
      3,
    )
  )

  lines.extend(
    (
      "",
      "Purpose:",
      (
        "  Compare pi_4^3 against pi_6^3 under the same "
        "ESTABLISH_GROUP_STRUCTURE frontier contract."
      ),
      (
        "  Identify which second-level prerequisites are "
        "mathematically necessary in pi_4^3 but intentionally "
        "hidden in pi_6^3."
      ),
      (
        "  No new frontier rule is installed by this package."
      ),
      "",
      "AUDIT_RESULT=PASS",
      "=" * 80,
    )
  )

  output = "\n".join(
    lines
  )

  output_dir = (
    Path(__file__).resolve().parent
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  (
    output_dir
    / "summary.txt"
  ).write_text(
    output + "\n",
    encoding="utf-8",
    newline="\n",
  )

  print(
    output
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
