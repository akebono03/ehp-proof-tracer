from __future__ import annotations

from toda_group_proof_generic_narrative_renderer import (
    _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
    render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_argument_ordering import (
    order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_arguments import (
    extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
    TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_contribution_ordering import (
    build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_exactness_components import (
    build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_display_contributions import (
    extract_toda_group_proof_narrative_exactness_display_contributions,
)
from toda_group_proof_narrative_exactness_exposure import (
    classify_toda_group_proof_narrative_exactness_component_exposure,
)
from toda_group_proof_narrative_method_evidence import (
    extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_proof_chains import (
    build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_relevant_groups import (
    extract_toda_group_proof_narrative_argument_relevant_groups,
)
from tests.test_phase143_19_method_evidence import (
    _method_evidence_data,
)


def _position(markdown: str, fragment: str) -> int:
    return markdown.find(fragment)


def _block_index(blocks, target) -> int:
    return next(
        index
        for index, block in enumerate(blocks)
        if block is target
    )


def main() -> int:
    presentation, blocks, sidecar, arguments = _method_evidence_data(3, 3)

    base_markdown = render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        sidecar,
        arguments,
    )
    proof_chains = build_toda_group_proof_narrative_proof_chains(
        presentation,
        sidecar,
        arguments,
    )
    ordered_contributions = build_toda_group_proof_narrative_ordered_contributions(
        presentation,
        blocks,
        sidecar,
        arguments,
        proof_chains,
        current_markdown=base_markdown,
    )
    final_markdown = (
        render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
            presentation,
            blocks,
            sidecar,
            arguments,
        )
    )

    ordered_arguments = order_toda_group_proof_narrative_arguments(arguments)
    source_index_by_identity = {
        id(argument): index
        for index, argument in enumerate(arguments)
    }

    print("=" * 78)
    print("Phase 149 / RC3-1 Narrative ordering audit")
    print("Target: pi_6^3")
    print("Production changes: none")
    print("=" * 78)

    print("\n[A] Argument order")
    for ordered_position, argument in enumerate(ordered_arguments):
        source_index = source_index_by_identity[id(argument)]
        conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
            argument
        )
        conclusion_text = (
            "<none>"
            if conclusion_step is None
            else _render_generic_narrative_step(conclusion_step)
        )
        print(
            f"{ordered_position}: source_index={source_index} "
            f"role={argument.role.value}"
        )
        print(f"   conclusion={conclusion_text}")

    print("\n[B] Block order")
    for index, block in enumerate(blocks):
        print(
            f"{index}: role={block.role.value} steps={len(block.steps)}"
        )
        for step in block.steps:
            print(f"   - {_render_generic_narrative_step(step)}")

    print("\n[C] Exactness ownership / exposure / display contributions")
    exactness_records = []
    for argument_index, argument in enumerate(arguments):
        evidence = extract_toda_group_proof_narrative_argument_method_evidence(
            presentation,
            blocks,
            sidecar,
            arguments,
            argument_index,
        )
        components = build_toda_group_proof_narrative_exactness_method_components(
            evidence
        )
        relevant_groups = extract_toda_group_proof_narrative_argument_relevant_groups(
            presentation,
            blocks,
            argument,
        )
        for component_index, component in enumerate(components):
            exposure = classify_toda_group_proof_narrative_exactness_component_exposure(
                relevant_groups,
                components,
                component,
            )
            print(
                f"argument={argument_index}:{argument.role.value} "
                f"component={component_index} exposure={exposure.value}"
            )
            for evidence_block in component.evidence_blocks:
                block_index = _block_index(blocks, evidence_block)
                print(f"   evidence_block={block_index}")
                for contribution in (
                    extract_toda_group_proof_narrative_exactness_display_contributions(
                        presentation,
                        evidence_block,
                    )
                ):
                    exactness_records.append(
                        (
                            argument_index,
                            argument.role.value,
                            block_index,
                            exposure.value,
                            contribution.kind.value,
                            contribution.latex,
                        )
                    )
                    print(
                        "   contribution="
                        f"{contribution.kind.value} "
                        f"latex={contribution.latex}"
                    )

    print("\n[D] Existing hidden-contribution ordering")
    for argument_index, contributions in enumerate(ordered_contributions):
        print(f"argument={argument_index}")
        if not contributions:
            print("   <none>")
            continue
        for contribution in contributions:
            print(
                "   "
                f"placement={contribution.placement.value} "
                f"role={contribution.contribution_role.value} "
                f"provider_anchor={contribution.provider_anchor} "
                f"distance={contribution.distance_to_conclusion}"
            )
            print(
                "   step="
                + _render_generic_narrative_step(contribution.proof_step)
            )

    print("\n[E] Rendered positions")
    for (
        argument_index,
        argument_role,
        block_index,
        exposure,
        kind,
        latex,
    ) in exactness_records:
        print(
            f"exactness argument={argument_index}:{argument_role} "
            f"block={block_index} exposure={exposure} kind={kind}"
        )
        print(f"   base_position={_position(base_markdown, latex)}")
        print(f"   final_position={_position(final_markdown, latex)}")

    print("\n[F] Argument conclusion positions")
    for argument_index, argument in enumerate(arguments):
        conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
            argument
        )
        if conclusion_step is None:
            continue
        conclusion_text = _render_generic_narrative_step(conclusion_step)
        print(
            f"argument={argument_index}:{argument.role.value} "
            f"base={_position(base_markdown, conclusion_text)} "
            f"final={_position(final_markdown, conclusion_text)}"
        )
        print(f"   conclusion={conclusion_text}")

    short_exact = (
        r"0\longrightarrow \pi_{5}^{2}"
        r"\xrightarrow{E} \pi_{6}^{3}"
        r"\xrightarrow{H} \pi_{6}^{5}"
        r"\longrightarrow 0"
    )
    group_result = r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"

    print("\n[G] RC3 symptom")
    short_pos = _position(final_markdown, short_exact)
    group_pos = _position(final_markdown, group_result)
    print(f"short_exact_sequence_position={short_pos}")
    print(f"group_structure_conclusion_position={group_pos}")
    print(
        "short_exact_before_group_conclusion="
        + str(
            short_pos >= 0
            and group_pos >= 0
            and short_pos < group_pos
        )
    )

    print("\n[H] Classification boundary")
    exactness_block_indices = tuple(
        index
        for index, block in enumerate(blocks)
        if (
            block.role
            is TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
        )
    )
    print(f"exactness_block_indices={exactness_block_indices}")
    print(
        "Observation target: RC2 decides visibility; "
        "RC3 must decide placement without changing exposure."
    )

    print("\n[I] Base markdown")
    print("-" * 78)
    print(base_markdown)
    print("-" * 78)

    print("\n[J] Final markdown with hidden contributions")
    print("-" * 78)
    print(final_markdown)
    print("-" * 78)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
