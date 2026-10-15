from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_provenance_catalog import (
  is_toda_group_proof_narrative_provenance_only_statement,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_narrative_step_transitions import (
  extract_toda_group_proof_narrative_step_transitions,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)


report = build_standard_toda_report(n=3, k=3)
group_result = report.candidates[0].source_candidate.group_result
replay = build_toda_group_result_proof_replay(
  group_result,
  max_depth=3,
)
presentation = build_toda_group_proof_presentation(replay)
sidecar = build_toda_group_proof_narrative_semantic_sidecar(
  presentation
)
blocks = build_toda_group_proof_narrative_blocks(
  presentation,
  semantic_sidecar=sidecar,
)
arguments = build_toda_group_proof_narrative_arguments(
  presentation,
  blocks,
  semantic_sidecar=sidecar,
)
transitions = extract_toda_group_proof_narrative_step_transitions(
  presentation,
  blocks,
)

source_ids = {
  id(transition.source_step)
  for transition in transitions
}
target_ids = {
  id(transition.target_step)
  for transition in transitions
}

print("=" * 110)
print("Phase 144-6-R4 supporting-fact structural audit")
print("=" * 110)

for argument_index, argument in enumerate(arguments):
  local_blocks = extract_toda_group_proof_narrative_argument_local_body_blocks(
    presentation,
    blocks,
    sidecar,
    arguments,
    argument_index,
  )
  conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
    argument
  )
  direct_ids = (
    set()
    if conclusion_step is None
    else {
      id(step)
      for step in conclusion_step.premises
    }
  )

  print()
  print("-" * 110)
  print(
    f"ARGUMENT {argument_index}: "
    f"role={argument.role.name}; "
    f"local_blocks={len(local_blocks)}"
  )
  print("-" * 110)

  for block in local_blocks:
    for step in block.steps:
      rendered = _render_generic_narrative_step(step)
      print(
        " | ".join(
          (
            f"block={block.role.name}",
            f"type={type(step.conclusion).__name__}",
            f"direct={id(step) in direct_ids}",
            f"transition_source={id(step) in source_ids}",
            f"transition_target={id(step) in target_ids}",
            "provenance_only="
            + str(
              is_toda_group_proof_narrative_provenance_only_statement(
                step.conclusion
              )
            ),
          )
        )
      )
      print(f"  {rendered}")
