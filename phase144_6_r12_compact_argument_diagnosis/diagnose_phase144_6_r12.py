from toda_group_proof import build_toda_group_result_proof_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_sidecar
from toda_group_proof_narrative_blocks import build_toda_group_proof_narrative_blocks
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
  extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_argument_local_body import extract_toda_group_proof_narrative_argument_local_body_blocks
from toda_group_proof_narrative_argument_direct_premises import extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises
from toda_group_proof_narrative_argument_multi_renderer import _toda_group_proof_narrative_argument_frontier_hidden_step_ids
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step
from toda_group_proof_query import build_standard_toda_report

def data(n,k):
  report=build_standard_toda_report(n,k)
  replay=build_toda_group_result_proof_replay(report,max_depth=3)
  presentation=build_toda_group_proof_presentation(replay)
  sidecar=build_toda_group_proof_narrative_semantic_sidecar(presentation)
  blocks=build_toda_group_proof_narrative_blocks(presentation,semantic_sidecar=sidecar)
  arguments=build_toda_group_proof_narrative_arguments(presentation,blocks,semantic_sidecar=sidecar)
  return presentation,blocks,sidecar,arguments

def show(n,k):
  presentation,blocks,sidecar,arguments=data(n,k)
  print("="*78)
  print(f"pi target n={n} k={k}: blocks={len(blocks)} arguments={len(arguments)}")
  for ai,arg in enumerate(arguments):
    subject=extract_toda_group_proof_narrative_argument_purpose_subject(arg)
    conclusion=extract_toda_group_proof_narrative_argument_conclusion_step(arg)
    local=extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,blocks,sidecar,arguments,ai
    )
    hidden=_toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,blocks,local,sidecar,arg
    )
    direct=() if conclusion is None else extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(arg,arguments)
    print(f"\nARG {ai}: role={arg.role.value} children={arg.child_argument_indices} subject={subject}")
    print("  conclusion:", None if conclusion is None else _render_generic_narrative_step(conclusion))
    print("  direct premises:")
    for s in direct:
      print("   ",_render_generic_narrative_step(s))
    print("  local blocks:")
    for b in local:
      print("   BLOCK",b.role.value)
      for s in b.steps:
        flag="HIDDEN" if id(s) in hidden else "VISIBLE"
        print("    ",flag,_render_generic_narrative_step(s))

show(3,3)
show(5,3)
