from __future__ import annotations

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_argument_renderer import (
    render_toda_group_proof_narrative_argument_purpose_sentence,
)
from toda_group_proof_narrative_arguments import (
    TodaGroupProofNarrativeArgumentRole,
    build_toda_group_proof_narrative_arguments,
    extract_toda_group_proof_narrative_argument_conclusion_step,
    extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_blocks import (
    build_toda_group_proof_narrative_blocks,
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


def _data(n: int, k: int):
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
    return presentation, blocks, sidecar, arguments


def _reachable_argument_indices(arguments, root_index: int) -> set[int]:
    reached = set()
    pending = [root_index]

    while pending:
        index = pending.pop()
        if index in reached:
            continue
        reached.add(index)
        pending.extend(arguments[index].child_argument_indices)

    return reached


def main() -> int:
    print("=" * 78)
    print("Phase 146-3 Semantic Capability Diagnosis")
    print("Production changes: none")
    print("Existing test changes: none")
    print("=" * 78)

    for n, k in TARGETS:
        _, _, _, arguments = _data(n, k)

        subject_ok = tuple(
            extract_toda_group_proof_narrative_argument_purpose_subject(
                argument
            ) is not None
            for argument in arguments
        )
        conclusion_ok = tuple(
            extract_toda_group_proof_narrative_argument_conclusion_step(
                argument
            ) is not None
            for argument in arguments
        )
        purpose_ok = tuple(
            render_toda_group_proof_narrative_argument_purpose_sentence(
                argument
            ) is not None
            for argument in arguments
        )

        root_indices = tuple(
            index
            for index, argument in enumerate(arguments)
            if (
                argument.role
                is TodaGroupProofNarrativeArgumentRole
                .ESTABLISH_GROUP_STRUCTURE
            )
        )

        if len(root_indices) == 1:
            reachable = _reachable_argument_indices(
                arguments,
                root_indices[0],
            )
        else:
            reachable = set()

        print()
        print(f"pi_{n + k}^{n}")
        print(f"  arguments: {len(arguments)}")
        print(
            "  all purpose subjects resolved: "
            f"{all(subject_ok)} ({sum(subject_ok)}/{len(subject_ok)})"
        )
        print(
            "  all conclusion steps resolved: "
            f"{all(conclusion_ok)} ({sum(conclusion_ok)}/{len(conclusion_ok)})"
        )
        print(
            "  all purpose sentences renderable: "
            f"{all(purpose_ok)} ({sum(purpose_ok)}/{len(purpose_ok)})"
        )
        print(
            "  unique group-structure root argument: "
            f"{len(root_indices) == 1}"
        )
        print(
            "  arguments reachable from root by child links: "
            f"{len(reachable)}/{len(arguments)}"
        )

    print()
    print("=" * 78)
    print("Diagnosis complete.")
    print(
        "Do not use target coordinates, theorem names, or raw argument counts "
        "as the capability predicate."
    )
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
