from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_proof_block,
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_body_renderer import (
  _insert_toda_group_proof_narrative_connector_before_conclusion_step,
  _insert_toda_group_proof_narrative_relocated_direct_premises,
  _relocatable_toda_group_proof_narrative_direct_derivation_premises,
  _step_derivation_sources_by_target_id,
)
from toda_group_proof_narrative_argument_direct_premises import (
  extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_transition_by_conclusion_id,
)
from toda_group_proof_narrative_arguments import (
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
from toda_group_proof_narrative_statement_identity import (
  toda_group_proof_narrative_statement_semantic_key,
)
from toda_group_proof_narrative_transition_renderer import (
  render_toda_group_proof_narrative_transition_connector,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


ROOT_FRAGMENT = (
  r"\pi_{4}^{3} = "
  r"\mathbb{Z}/2\{\eta_{3}\}"
)


def rule_name(
  proof_step,
) -> str:
  inference_rule = proof_step.inference_rule

  if inference_rule is not None:
    return inference_rule.name

  rule = proof_step.rule

  return (
    rule.value
    if hasattr(
      rule,
      "value"
    )
    else str(
      rule
    )
  )


def build_data():
  report = build_standard_toda_report(
    n=3,
    k=1,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
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
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=semantic_sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=semantic_sidecar,
    )
  )

  return (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
  )


def append_step(
  lines,
  label: str,
  proof_step,
  root_key,
) -> None:
  rendered = (
    _render_generic_narrative_step(
      proof_step
    )
  )
  semantic_key = (
    toda_group_proof_narrative_statement_semantic_key(
      proof_step.conclusion
    )
  )

  lines.extend(
    (
      label,
      "  step_id: "
      + str(
        id(
          proof_step
        )
      ),
      "  rule: "
      + rule_name(
        proof_step
      ),
      "  is_root_step: "
      + str(
        proof_step is presentation.root_step
      ),
      "  semantic_equals_root: "
      + str(
        semantic_key
        == root_key
      ),
      "  rendered_contains_root_fragment: "
      + str(
        ROOT_FRAGMENT
        in rendered
      ),
      "  rendered: "
      + repr(
        rendered
      ),
      "  conclusion_type: "
      + type(
        proof_step.conclusion
      ).__name__,
      "  conclusion_repr: "
      + repr(
        proof_step.conclusion
      ),
      "",
    )
  )


def append_lines_stage(
  lines,
  label: str,
  stage_lines,
) -> None:
  text = "\n".join(
    stage_lines
  )
  lines.extend(
    (
      label,
      "root_fragment_count: "
      + str(
        text.count(
          ROOT_FRAGMENT
        )
      ),
      "",
      text,
      "",
    )
  )


def main() -> int:
  global presentation

  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
  ) = build_data()

  root_key = (
    toda_group_proof_narrative_statement_semantic_key(
      presentation.root_step.conclusion
    )
  )

  argument = next(
    argument
    for argument in arguments
    if (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
      is presentation.root_step
    )
  )
  argument_index = arguments.index(
    argument
  )
  local_body_blocks = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      argument_index,
    )
  )
  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )
  transition_by_conclusion_id = (
    _toda_group_proof_narrative_argument_transition_by_conclusion_id(
      presentation,
      blocks,
      arguments,
    )
  )
  transition = transition_by_conclusion_id.get(
    id(
      argument.conclusion_block
    )
  )
  connector = (
    None
    if transition is None
    else render_toda_group_proof_narrative_transition_connector(
      transition
    )
  )
  direct_derivation_premises = (
    extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
      argument,
      arguments,
    )
  )
  direct_derivation_support_steps = tuple(
    support_step
    for premise_step in direct_derivation_premises
    for support_step in premise_step.premises
    if all(
      support_step is not existing_step
      for existing_step in direct_derivation_premises
    )
  )
  step_sources = (
    _step_derivation_sources_by_target_id(
      presentation,
      blocks,
    )
  )
  relocated = (
    _relocatable_toda_group_proof_narrative_direct_derivation_premises(
      (
        direct_derivation_support_steps
        + direct_derivation_premises
      ),
      step_sources,
      argument.conclusion_block,
    )
  )

  block_index = next(
    index
    for index, block in enumerate(
      blocks
    )
    if block is argument.conclusion_block
  )

  lines = [
    "# Phase 159 pi4_3 target block render trace audit",
    "",
    "root_fragment: "
    + ROOT_FRAGMENT,
    "connector: "
    + repr(
      connector
    ),
    "target_block_index: "
    + str(
      block_index
    ),
    "",
    "## Target block steps",
    "",
  ]

  for index, proof_step in enumerate(
    argument.conclusion_block.steps
  ):
    append_step(
      lines,
      "### target step "
      + str(
        index
      ),
      proof_step,
      root_key,
    )

  lines.extend(
    (
      "## Direct derivation premises",
      "",
    )
  )

  for index, proof_step in enumerate(
    direct_derivation_premises
  ):
    append_step(
      lines,
      "### direct premise "
      + str(
        index
      ),
      proof_step,
      root_key,
    )

  lines.extend(
    (
      "## Direct derivation support steps",
      "",
    )
  )

  for index, proof_step in enumerate(
    direct_derivation_support_steps
  ):
    append_step(
      lines,
      "### support step "
      + str(
        index
      ),
      proof_step,
      root_key,
    )

  lines.extend(
    (
      "## Relocatable direct premises",
      "",
    )
  )

  for index, proof_step in enumerate(
    relocated
  ):
    append_step(
      lines,
      "### relocated "
      + str(
        index
      ),
      proof_step,
      root_key,
    )

  base_block_lines = tuple(
    _render_generic_narrative_proof_block(
      presentation,
      blocks,
      block_index,
      show_dependency_labels=False,
      suppress_provenance_only=True,
      preserve_provenance_step_ids=frozenset(),
    )
  )

  append_lines_stage(
    lines,
    "## Stage A: target block generic render",
    base_block_lines,
  )

  after_relocation = (
    _insert_toda_group_proof_narrative_relocated_direct_premises(
      base_block_lines,
      argument.conclusion_block,
      conclusion_step,
      direct_derivation_premises,
      relocated,
    )
  )

  append_lines_stage(
    lines,
    "## Stage B: after relocated direct premises",
    after_relocation,
  )

  if connector is None:
    after_connector = after_relocation
  else:
    after_connector = (
      _insert_toda_group_proof_narrative_connector_before_conclusion_step(
        after_relocation,
        conclusion_step,
        connector,
      )
    )

  append_lines_stage(
    lines,
    "## Stage C: after connector insertion",
    after_connector,
  )

  report = "\n".join(
    lines
  )
  output_path = (
    Path(__file__).resolve().parent
    / "phase159_pi4_3_target_block_render_trace_audit.txt"
  )
  output_path.write_text(
    report,
    encoding="utf-8",
  )

  print(
    report
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
