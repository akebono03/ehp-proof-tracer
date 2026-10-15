from __future__ import annotations

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_generic_narrative_renderer import (
    _render_generic_narrative_step,
)
from toda_group_proof_narrative_blocks import (
    TodaGroupProofNarrativeMathematicalBlockRole,
    build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
    build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay


def build_presentation(depth: int):
    report = build_standard_toda_report(n=3, k=3)
    group_result = report.candidates[0].source_candidate.group_result
    replay = build_toda_group_result_proof_replay(
        group_result,
        max_depth=depth,
    )
    return build_toda_group_proof_presentation(replay)


def rule_name(step) -> str:
    rule = step.inference_rule
    return "<none>" if rule is None else rule.name


def short(value, limit: int = 500) -> str:
    text = repr(value).replace("\n", " ")
    return text if len(text) <= limit else text[:limit] + "..."


def main() -> int:
    presentation = build_presentation(3)
    sidecar = build_toda_group_proof_narrative_semantic_sidecar(
        presentation
    )
    blocks = build_toda_group_proof_narrative_blocks(
        presentation,
        semantic_sidecar=sidecar,
    )

    reference_steps = []
    for block_index, block in enumerate(blocks):
        if (
            block.role
            is not TodaGroupProofNarrativeMathematicalBlockRole.REFERENCE
        ):
            continue
        for step_index, step in enumerate(block.steps):
            reference_steps.append(
                (block_index, step_index, step)
            )

    print("=" * 78)
    print("Phase 144-6-R3: generic reference mapping audit")
    print("=" * 78)
    print("AUDIT ONLY: no production source changes")
    print(f"reference_blocks={sum(1 for b in blocks if b.role is TodaGroupProofNarrativeMathematicalBlockRole.REFERENCE)}")
    print(f"reference_steps={len(reference_steps)}")
    print()

    ref_number_by_id = {
        id(step): index
        for index, (_, _, step) in enumerate(reference_steps, start=1)
    }

    for number, (block_index, step_index, step) in enumerate(
        reference_steps,
        start=1,
    ):
        print("-" * 78)
        print(f"[R{number}] candidate")
        print(f"block=B{block_index:02d}, step={step_index}")
        print(f"statement_type={type(step.conclusion).__name__}")
        print(f"inference_rule={rule_name(step)}")
        print(f"generic_render={_render_generic_narrative_step(step)}")
        print(f"statement={short(step.conclusion)}")

        consumers = []
        premises = []
        for edge in presentation.edges:
            if edge.premise_step is step:
                consumers.append(
                    (
                        edge.premise_index,
                        type(edge.parent_step.conclusion).__name__,
                        rule_name(edge.parent_step),
                        short(edge.parent_step.conclusion, 220),
                    )
                )
            if edge.parent_step is step:
                premises.append(
                    (
                        edge.premise_index,
                        type(edge.premise_step.conclusion).__name__,
                        rule_name(edge.premise_step),
                        short(edge.premise_step.conclusion, 220),
                    )
                )

        print("consumers:")
        if not consumers:
            print("  <none>")
        for item in consumers:
            print(" ", item)

        print("premises:")
        if not premises:
            print("  <none>")
        for item in premises:
            print(" ", item)
        print()

    print("=" * 78)
    print("Cross-reference edges between selected proof steps")
    print("=" * 78)
    for edge in presentation.edges:
        ref_number = ref_number_by_id.get(id(edge.premise_step))
        if ref_number is None:
            continue
        print(
            f"[R{ref_number}] -> "
            f"{type(edge.parent_step.conclusion).__name__} "
            f"| consumer_rule={rule_name(edge.parent_step)} "
            f"| premise_index={edge.premise_index}"
        )

    print()
    print("=" * 78)
    print("R3 implementation decision data")
    print("=" * 78)
    print("Use this output to decide:")
    print("1. whether the five generic REFERENCE steps match legacy R1-R5;")
    print("2. which stable semantic/provenance field can provide human titles;")
    print("3. where body references can be derived from actual dependency edges;")
    print("4. whether any legacy reference exists only as hand-authored prose.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
