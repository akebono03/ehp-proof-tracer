from collections import defaultdict
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import build_toda_group_proof_narrative_arguments, extract_toda_group_proof_narrative_argument_conclusion_step
from toda_group_proof_narrative_blocks import build_toda_group_proof_narrative_blocks
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_sidecar
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step

report=build_standard_toda_report(n=3,k=3)
group_result=report.candidates[0].source_candidate.group_result
replay=build_toda_group_result_proof_replay(group_result,max_depth=3)
presentation=build_toda_group_proof_presentation(replay)
sidecar=build_toda_group_proof_narrative_semantic_sidecar(presentation)
blocks=build_toda_group_proof_narrative_blocks(presentation,semantic_sidecar=sidecar)
arguments=build_toda_group_proof_narrative_arguments(presentation,blocks,semantic_sidecar=sidecar)

consumers=defaultdict(list)
for edge in presentation.edges:
  consumers[id(edge.premise_step)].append(edge.parent_step)
for semantic in sidecar.dependency_semantics:
  consumers[id(semantic.prerequisite_step)].append(semantic.dependent_step)

for ai, argument in enumerate(arguments):
  conclusion=extract_toda_group_proof_narrative_argument_conclusion_step(argument)
  print("="*100)
  print(f"ARGUMENT {ai}: {argument.role.name}")
  print("="*100)
  for block in blocks:
    for step in block.steps:
      step_consumers=consumers.get(id(step),[])
      if not step_consumers:
        continue
      print(_render_generic_narrative_step(step))
      for consumer in step_consumers:
        marker="CONCLUSION" if consumer is conclusion else "intermediate"
        print(f"  -> {marker}: {_render_generic_narrative_step(consumer)}")
