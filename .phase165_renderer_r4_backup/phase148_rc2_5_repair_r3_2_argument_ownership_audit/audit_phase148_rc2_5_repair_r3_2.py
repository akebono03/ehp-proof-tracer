from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_blocks import build_toda_group_proof_narrative_blocks
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_sidecar
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step


def main():
    group_result = build_standard_toda_report(
        n=3,
        k=3,
    ).candidates[0].source_candidate.group_result
    presentation = build_toda_group_proof_presentation(
        build_toda_group_result_proof_replay(
            group_result,
            max_depth=2,
        )
    )
    sidecar = build_toda_group_proof_narrative_semantic_sidecar(
        presentation
    )
    blocks = build_toda_group_proof_narrative_blocks(
        presentation,
        sidecar,
    )
    arguments = build_toda_group_proof_narrative_arguments(
        presentation,
        blocks,
        sidecar,
    )

    print("=" * 80)
    print("Phase 148 RC2-5 R3.2 Argument Ownership Audit")
    print(f"nodes={len(presentation.nodes)} blocks={len(blocks)} arguments={len(arguments)}")
    for index, argument in enumerate(arguments):
        conclusion = extract_toda_group_proof_narrative_argument_conclusion_step(
            argument
        )
        local = extract_toda_group_proof_narrative_argument_local_body_blocks(
            presentation,
            blocks,
            sidecar,
            arguments,
            index,
        )
        print("-" * 80)
        print(f"ARG[{index}] role={argument.role.value}")
        print(
            "conclusion="
            + (
                "<none>"
                if conclusion is None
                else _render_generic_narrative_step(conclusion)
            )
        )
        print("local blocks:")
        for block in local:
            print(f"  block_role={block.role.value}")
            for step in block.steps:
                print("    " + _render_generic_narrative_step(step))
        if conclusion is not None:
            print("direct premises:")
            for premise_index, premise in enumerate(conclusion.premises):
                print(
                    f"  index={premise_index} "
                    + _render_generic_narrative_step(premise)
                )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
