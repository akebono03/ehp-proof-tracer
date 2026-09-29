from __future__ import annotations

from collections import Counter

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
    build_toda_group_proof_narrative_arguments,
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


def _group_result(n: int, k: int):
    report = build_standard_toda_report(
        n=n,
        k=k,
    )

    if not report.candidates:
        raise AssertionError(
            f"expected at least one candidate for n={n}, k={k}"
        )

    return report.candidates[0].source_candidate.group_result


def _diagnose(n: int, k: int) -> dict[str, object]:
    result = _group_result(n, k)
    replay = build_complete_toda_group_result_proof_replay(
        result
    )
    presentation = build_toda_group_proof_presentation(
        replay
    )
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

    block_roles = tuple(
        block.role.value
        for block in blocks
    )
    argument_roles = tuple(
        argument.role.value
        for argument in arguments
    )

    return {
        "n": n,
        "k": k,
        "nodes": len(presentation.nodes),
        "blocks": len(blocks),
        "arguments": len(arguments),
        "block_role_counts": Counter(block_roles),
        "argument_role_counts": Counter(argument_roles),
    }


def main() -> int:
    print("=" * 78)
    print("Phase 146-2 R1 Structural Capability Diagnosis")
    print("Production changes: none")
    print("Existing test changes: none")
    print("=" * 78)

    rows = tuple(
        _diagnose(n, k)
        for n, k in TARGETS
    )

    for row in rows:
        print()
        print(
            f"pi_{row['n'] + row['k']}^{row['n']}: "
            f"nodes={row['nodes']} "
            f"blocks={row['blocks']} "
            f"arguments={row['arguments']}"
        )
        print("  block roles:")
        for role, count in sorted(
            row["block_role_counts"].items()
        ):
            print(f"    {role}: {count}")

        print("  argument roles:")
        if row["argument_role_counts"]:
            for role, count in sorted(
                row["argument_role_counts"].items()
            ):
                print(f"    {role}: {count}")
        else:
            print("    (none)")

    print()
    print("=" * 78)
    print("Phase 146-2 R1 diagnosis complete.")
    print(
        "Use this matrix to choose a target-independent capability "
        "predicate before changing the public Narrative route."
    )
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
