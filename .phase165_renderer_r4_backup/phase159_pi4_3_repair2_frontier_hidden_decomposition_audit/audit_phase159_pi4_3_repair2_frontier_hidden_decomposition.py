from __future__ import annotations

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
from toda_group_proof_narrative_argument_body_renderer import (
  render_toda_group_proof_narrative_argument_body_markdown,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
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
from toda_group_proof_narrative_exactness_exposure import (
  classify_toda_group_proof_narrative_exactness_component_exposure,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_argument_primary_exactness_component,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
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

  if rendered is None:
    return ""

  return rendered


def rule_name(step) -> str:
  if step.inference_rule is None:
    return ""
  return step.inference_rule.name


def main() -> int:
  report = build_standard_toda_report(
    n=N,
    k=K,
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
      "expected exactly one Narrative Argument"
    )

  argument = arguments[0]

  local_body_blocks = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      closure,
      blocks,
      sidecar,
      arguments,
      0,
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

  evidence = (
    extract_toda_group_proof_narrative_argument_method_evidence(
      closure,
      blocks,
      sidecar,
      arguments,
      0,
    )
  )

  components = (
    build_toda_group_proof_narrative_exactness_method_components(
      evidence
    )
  )

  relevant_groups = (
    extract_toda_group_proof_narrative_argument_relevant_groups(
      closure,
      blocks,
      argument,
    )
  )

  primary_component = (
    select_toda_group_proof_narrative_argument_primary_exactness_component(
      closure,
      blocks,
      sidecar,
      arguments,
      0,
    )
  )

  exposure_by_block_id = {}

  for component in components:
    exposure = (
      classify_toda_group_proof_narrative_exactness_component_exposure(
        relevant_groups,
        components,
        component,
      )
    )
    for evidence_block in component.evidence_blocks:
      exposure_by_block_id[
        id(evidence_block)
      ] = exposure

  hidden_records = []

  for block_index, block in enumerate(
    blocks
  ):
    for step_index, step in enumerate(
      block.steps
    ):
      if id(step) not in hidden_step_ids:
        continue

      hidden_records.append(
        (
          block_index,
          step_index,
          block.role.value,
          type(
            step.conclusion
          ).__name__,
          rule_name(step),
          safe_render(step),
        )
      )

  body_with_frontier_hiding = (
    render_toda_group_proof_narrative_argument_body_markdown(
      closure,
      blocks,
      local_body_blocks,
      primary_component,
      exactness_exposure_by_block_id=(
        exposure_by_block_id
      ),
      excluded_non_exact_block_ids=frozenset(),
      excluded_non_exact_step_ids=frozenset(),
      excluded_exactness_contribution_keys=frozenset(),
      context_hidden_step_ids=(
        hidden_step_ids
      ),
      preserve_provenance_block_ids=frozenset(),
    )
  )

  body_without_frontier_hiding = (
    render_toda_group_proof_narrative_argument_body_markdown(
      closure,
      blocks,
      local_body_blocks,
      primary_component,
      exactness_exposure_by_block_id=(
        exposure_by_block_id
      ),
      excluded_non_exact_block_ids=frozenset(),
      excluded_non_exact_step_ids=frozenset(),
      excluded_exactness_contribution_keys=frozenset(),
      context_hidden_step_ids=frozenset(),
      preserve_provenance_block_ids=frozenset(),
    )
  )

  full_multi = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      closure,
      blocks,
      sidecar,
      arguments,
    )
  )

  lines = [
    "=" * 80,
    "Phase 159 - pi_4^3 repair2 frontier-hidden decomposition audit",
    "=" * 80,
    "Production code changes: none",
    "Existing test changes: none",
    "",
    f"hidden step count: {len(hidden_records)}",
    "",
    "Frontier-hidden steps:",
  ]

  for (
    block_index,
    step_index,
    role,
    statement_type,
    rule,
    rendered,
  ) in hidden_records:
    lines.append(
      "  "
      + f"block={block_index} "
      + f"step={step_index} "
      + f"role={role} "
      + f"type={statement_type}"
    )
    lines.append(
      "    rule="
      + rule
    )
    lines.append(
      "    rendered="
      + rendered
    )

  lines.extend(
    (
      "",
      "Body WITH frontier hiding:",
      body_with_frontier_hiding,
      "",
      "Body WITHOUT frontier hiding:",
      body_without_frontier_hiding,
      "",
      "Current multi-argument markdown:",
      full_multi,
      "",
      "Interpretation:",
      (
        "  If the missing mathematical support appears in "
        "Body WITHOUT frontier hiding, the current frontier "
        "policy is suppressing relevant proof content."
      ),
      (
        "  If it remains absent even without frontier hiding, "
        "the loss is inside body rendering or exactness "
        "contribution filtering."
      ),
      (
        "  Proposition 5.1 direct Delta / Im(Delta) / Delta-E "
        "exactness remain outside depth=2 closure and are not "
        "repaired by this audit."
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
