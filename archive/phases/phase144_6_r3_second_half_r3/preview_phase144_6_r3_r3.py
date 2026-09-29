from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import build_toda_group_proof_narrative_arguments
from toda_group_proof_narrative_argument_multi_renderer import render_toda_group_proof_narrative_multi_argument_markdown
from toda_group_proof_narrative_blocks import build_toda_group_proof_narrative_blocks
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_sidecar
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay

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
rendered = render_toda_group_proof_narrative_multi_argument_markdown(
  presentation,
  blocks,
  sidecar,
  arguments,
)
print(rendered)
print()
print("=" * 78)
print("R3 coexistence checks")
print("=" * 78)
for needle in (
  "**[R1]",
  "**[R2]",
  "(1) と (2) より、",
  "(4) と (5) より、",
):
  print(f"{needle}: {needle in rendered}")
