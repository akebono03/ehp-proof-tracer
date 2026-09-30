from __future__ import annotations

from collections import Counter

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
    build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
    TodaGroupProofNarrativeMathematicalBlockRole,
    build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_renderer import (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_renderer import (
    render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
    build_toda_group_proof_narrative_semantic_closure_presentation,
    build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
    build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
    build_toda_group_result_proof_replay,
)


N_RANGE = range(2, 16)
K_RANGE = range(0, 8)
MAX_DEPTH = 2
EXPECTED_GROUP_COUNT = 112


def _target_label(n: int, k: int) -> str:
    return f"pi_{n + k}^{n}"


def _group_result(n: int, k: int):
    report = build_standard_toda_report(n=n, k=k)

    if not report.candidates:
        raise AssertionError(
            f"no report candidate for n={n}, k={k}"
        )

    return report.candidates[0].source_candidate.group_result


def _generic_context(n: int, k: int):
    group_result = _group_result(n, k)
    replay = build_toda_group_result_proof_replay(
        group_result,
        max_depth=MAX_DEPTH,
    )
    presentation = build_toda_group_proof_presentation(
        replay
    )
    presentation = (
        build_toda_group_proof_narrative_semantic_closure_presentation(
            presentation
        )
    )
    semantic_sidecar = (
        build_toda_group_proof_narrative_semantic_sidecar(
            presentation
        )
    )
    blocks = build_toda_group_proof_narrative_blocks(
        presentation,
        semantic_sidecar=semantic_sidecar,
    )
    arguments = build_toda_group_proof_narrative_arguments(
        presentation,
        blocks,
        semantic_sidecar=semantic_sidecar,
    )

    return (
        presentation,
        semantic_sidecar,
        blocks,
        arguments,
    )


def main() -> int:
    scanned_groups = 0
    generic_successes = 0
    generic_failures = []
    public_failures = []
    empty_generic_outputs = []
    block_role_counts = Counter()
    total_blocks = 0
    total_arguments = 0
    total_presentation_nodes = 0

    print("=" * 78)
    print("Phase 151-1 — All-Group Generic Baseline Feasibility Audit")
    print("Production changes: none")
    print("Existing test changes: none")
    print(f"Range: n=2..15, k=0..7 ({EXPECTED_GROUP_COUNT} groups)")
    print(f"Replay depth: {MAX_DEPTH}")
    print(
        "Generic route: bounded replay -> presentation -> semantic closure -> "
        "sidecar -> blocks -> arguments -> contribution renderer"
    )
    print("=" * 78)

    for n in N_RANGE:
        for k in K_RANGE:
            scanned_groups += 1
            label = _target_label(n, k)

            try:
                (
                    presentation,
                    semantic_sidecar,
                    blocks,
                    arguments,
                ) = _generic_context(n, k)

                generic = (
                    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
                        presentation,
                        blocks,
                        semantic_sidecar,
                        arguments,
                    )
                )

                if not generic.strip():
                    empty_generic_outputs.append(label)
                else:
                    generic_successes += 1

                total_presentation_nodes += len(
                    presentation.nodes
                )
                total_blocks += len(blocks)
                total_arguments += len(arguments)
                block_role_counts.update(
                    block.role.value
                    for block in blocks
                )
            except Exception as exc:
                generic_failures.append(
                    (
                        label,
                        type(exc).__name__,
                        str(exc),
                    )
                )
                continue

            try:
                render_toda_group_proof_narrative_markdown(
                    presentation
                )
            except Exception as exc:
                public_failures.append(
                    (
                        label,
                        type(exc).__name__,
                        str(exc),
                    )
                )

    print()
    print("Summary")
    print("-" * 78)
    print("scanned groups:", scanned_groups)
    print("generic non-empty successes:", generic_successes)
    print("generic failures:", len(generic_failures))
    print("generic empty outputs:", len(empty_generic_outputs))
    print("public renderer failures:", len(public_failures))
    print("presentation nodes after semantic closure:", total_presentation_nodes)
    print("blocks:", total_blocks)
    print("arguments:", total_arguments)
    print(
        "OTHER blocks:",
        block_role_counts[
            TodaGroupProofNarrativeMathematicalBlockRole.OTHER.value
        ],
    )

    print()
    print("Block-role inventory")
    print("-" * 78)
    for role, count in sorted(block_role_counts.items()):
        print(f"{role}: {count}")

    if generic_failures:
        print()
        print("Generic failures")
        print("-" * 78)
        for label, exc_type, message in generic_failures:
            print(f"{label}: {exc_type}: {message}")

    if empty_generic_outputs:
        print()
        print("Generic empty outputs")
        print("-" * 78)
        for label in empty_generic_outputs:
            print(label)

    if public_failures:
        print()
        print("Public renderer failures")
        print("-" * 78)
        for label, exc_type, message in public_failures:
            print(f"{label}: {exc_type}: {message}")

    print()
    print("=" * 78)

    feasible = (
        scanned_groups == EXPECTED_GROUP_COUNT
        and generic_successes == EXPECTED_GROUP_COUNT
        and not generic_failures
        and not empty_generic_outputs
    )

    if feasible:
        print(
            "PASS: all 112 groups can be evaluated through the same generic "
            "renderer path without changing the public renderer."
        )
        print(
            "Phase 151-2 can build the all-group generic baseline on this "
            "audit-only route."
        )
        return 0

    print(
        "NOT YET FEASIBLE: at least one group cannot currently produce a "
        "non-empty generic Narrative at depth 2."
    )
    print(
        "Do not change the public route. Classify the failures before "
        "starting Phase 151-2."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
