from __future__ import annotations

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_generic_narrative_renderer import (
    _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_discourse import (
    TodaGroupProofNarrativeArgumentDiscourseRole,
    classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_argument_multi_renderer import (
    render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_argument_ordering import (
    order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_arguments import (
    build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
    build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_ordering import (
    build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
    _contribution_insertion_indices,
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_proof_chains import (
    build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_semantics import (
    build_toda_group_proof_narrative_semantic_closure_presentation,
    build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import (
    build_complete_toda_group_result_proof_replay,
)


TARGETS = (
    (3, 3),
    (5, 3),
    (4, 6),
    (5, 7),
    (8, 7),
    (9, 7),
)


def _context(n: int, k: int):
    report = build_standard_toda_report(n=n, k=k)
    group_result = report.candidates[0].source_candidate.group_result
    replay = build_complete_toda_group_result_proof_replay(group_result)
    presentation = build_toda_group_proof_presentation(replay)
    presentation = (
        build_toda_group_proof_narrative_semantic_closure_presentation(
            presentation
        )
    )
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
    proof_chains = build_toda_group_proof_narrative_proof_chains(
        presentation,
        sidecar,
        arguments,
    )
    return presentation, sidecar, blocks, arguments, proof_chains


def _is_rendering_fallback(step, rendered: str) -> bool:
    rule = step.inference_rule
    if rule is not None and rendered == rule.name:
        return True
    return rendered == "`" + type(step.conclusion).__name__ + "`"


def main() -> int:
    print("=" * 78)
    print("Phase 146-4 Renderer Quality Contract Audit")
    print("Production changes: none")
    print("Existing test changes: none")
    print("=" * 78)

    for n, k in TARGETS:
        (
            presentation,
            sidecar,
            blocks,
            arguments,
            proof_chains,
        ) = _context(n, k)

        base = render_toda_group_proof_narrative_multi_argument_markdown(
            presentation,
            blocks,
            sidecar,
            arguments,
        )
        ordered = build_toda_group_proof_narrative_ordered_contributions(
            presentation,
            blocks,
            sidecar,
            arguments,
            proof_chains,
            current_markdown=base,
        )
        indices = _contribution_insertion_indices(
            base,
            blocks,
            arguments,
            ordered,
        )
        connected = (
            render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
                presentation,
                blocks,
                sidecar,
                arguments,
            )
        )

        ordered_arguments = order_toda_group_proof_narrative_arguments(
            arguments
        )
        discourse_roles = (
            classify_toda_group_proof_narrative_argument_discourse_roles(
                arguments
            )
        )
        discourse_by_id = {
            id(argument): discourse_roles[position]
            for position, argument in enumerate(ordered_arguments)
        }

        selected = 0
        insertable = 0
        non_detached_selected = 0
        non_detached_insertable = 0
        detached_selected = 0
        detached_insertable = 0
        fallback_selected = 0

        for argument_index, contributions in enumerate(ordered):
            role = discourse_by_id[id(arguments[argument_index])]
            for contribution_index, contribution in enumerate(contributions):
                selected += 1
                insertion_index = indices[argument_index][contribution_index]
                if insertion_index is not None:
                    insertable += 1

                rendered = _render_generic_narrative_step(
                    contribution.proof_step
                )
                if _is_rendering_fallback(
                    contribution.proof_step,
                    rendered,
                ):
                    fallback_selected += 1

                if role is TodaGroupProofNarrativeArgumentDiscourseRole.DETACHED:
                    detached_selected += 1
                    if insertion_index is not None:
                        detached_insertable += 1
                else:
                    non_detached_selected += 1
                    if insertion_index is not None:
                        non_detached_insertable += 1

        print()
        print(f"pi_{n + k}^{n}")
        print(f"  base chars: {len(base)}")
        print(f"  connected chars: {len(connected)}")
        print(f"  selected contributions: {selected}")
        print(f"  insertable contributions: {insertable}/{selected}")
        print(
            "  non-detached insertable: "
            f"{non_detached_insertable}/{non_detached_selected}"
        )
        print(
            "  detached insertable: "
            f"{detached_insertable}/{detached_selected}"
        )
        print(
            "  selected contribution renderer fallbacks: "
            f"{fallback_selected}/{selected}"
        )
        print(f"  connected output differs from base: {connected != base}")

    print()
    print("=" * 78)
    print("Audit complete.")
    print(
        "Interpretation: non-detached contribution insertability is already "
        "an established generic invariant. Differences confined to detached "
        "arguments must not be used as a hidden target identifier."
    )
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
