from toda_calculation_facade import build_standard_toda_report
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_sidecar
from toda_group_proof_narrative_blocks import build_toda_group_proof_narrative_blocks
from toda_group_proof_narrative_arguments import build_toda_group_proof_narrative_arguments

report = build_standard_toda_report(n=3, k=3)
group_result = report.candidates[0].source_candidate.group_result
replay = build_toda_group_result_proof_replay(group_result, max_depth=2)
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

roles = tuple(argument.role.value for argument in arguments)
print("depth=2 argument roles:", roles)
print("depth=2 nodes:", len(presentation.nodes))
print("depth=2 blocks:", len(blocks))
print("depth=2 arguments:", len(arguments))

if "establish_definition" in roles:
    raise SystemExit(20)

raise SystemExit(21)
