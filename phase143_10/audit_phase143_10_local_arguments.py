from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay


for n, k in ((3, 3), (5, 3), (8, 7), (9, 7)):
  report = build_standard_toda_report(n=n, k=k)
  result = report.candidates[0].source_candidate.group_result
  replay = build_toda_group_result_proof_replay(result, max_depth=3)
  presentation = build_toda_group_proof_presentation(replay)
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(presentation)
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
  )
  block_number = {id(block): i + 1 for i, block in enumerate(blocks)}
  print("=" * 78)
  print(f"n={n}, k={k}, blocks={len(blocks)}, arguments={len(arguments)}")
  for i, argument in enumerate(arguments):
    supports = [
      f"B{block_number[id(block)]:02d}:{block.role.value}"
      for block in argument.supporting_blocks
    ]
    children = [
      f"A{child + 1:02d}"
      for child in argument.child_argument_indices
    ]
    conclusion = block_number[id(argument.conclusion_block)]
    print(
      f"A{i + 1:02d} {argument.role.value} "
      f"-> B{conclusion:02d}:{argument.conclusion_block.role.value}"
    )
    print(f"  supports={supports}")
    print(f"  children={children}")
