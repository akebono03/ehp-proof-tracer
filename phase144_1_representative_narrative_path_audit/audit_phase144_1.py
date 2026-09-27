from collections import Counter

from toda_calculation_facade import build_standard_toda_report
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
    extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_blocks import (
    build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
    build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay


TARGETS = (
    (3, 3),
    (5, 3),
    (4, 6),
    (5, 7),
    (8, 7),
    (9, 7),
)


def _rule_name(proof_step):
    inference_rule = proof_step.inference_rule
    if inference_rule is None:
        return None
    return inference_rule.name


def _root_reachable_argument_indices(arguments):
    root_indices = tuple(
        index
        for index, argument in enumerate(arguments)
        if (
            argument.role.value == "establish_group_structure"
            and argument.conclusion_block.role.value == "target"
        )
    )

    reachable = set()

    def visit(argument_index):
        if argument_index in reachable:
            return
        reachable.add(argument_index)
        for child_index in arguments[argument_index].child_argument_indices:
            visit(child_index)

    for root_index in root_indices:
        visit(root_index)

    return tuple(sorted(root_indices)), frozenset(reachable)


def audit_target(n, k):
    report = build_standard_toda_report(n=n, k=k)

    print("=" * 100)
    print(f"n={n}, k={k}, target=pi_{n + k}^{n}")
    print(f"candidate_count={len(report.candidates)}")

    if not report.candidates:
        print("NO CANDIDATE")
        return

    group_result = report.candidates[0].source_candidate.group_result
    replay = build_toda_group_result_proof_replay(
        group_result,
        max_depth=3,
    )
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
    ordered_arguments = order_toda_group_proof_narrative_arguments(arguments)
    discourse_roles = classify_toda_group_proof_narrative_argument_discourse_roles(
        arguments
    )

    source_index_by_identity = {
        id(argument): index
        for index, argument in enumerate(arguments)
    }
    root_indices, root_reachable = _root_reachable_argument_indices(arguments)

    block_role_counts = Counter(block.role.value for block in blocks)
    argument_role_counts = Counter(argument.role.value for argument in arguments)

    print(f"root_rule={_rule_name(group_result.proof_step)!r}")
    print(f"nodes={len(presentation.nodes)}")
    print(f"edges={len(presentation.edges)}")
    print(f"blocks={len(blocks)}")
    print(f"arguments={len(arguments)}")
    print(f"root_argument_indices={root_indices}")
    print(f"root_reachable_argument_indices={tuple(sorted(root_reachable))}")
    print(
        "block_role_counts="
        + repr(dict(sorted(block_role_counts.items())))
    )
    print(
        "argument_role_counts="
        + repr(dict(sorted(argument_role_counts.items())))
    )

    print("argument_summary:")
    detached_count = 0

    for ordered_position, (argument, discourse_role) in enumerate(
        zip(ordered_arguments, discourse_roles)
    ):
        source_index = source_index_by_identity[id(argument)]
        subject = extract_toda_group_proof_narrative_argument_purpose_subject(
            argument
        )
        reachable = source_index in root_reachable
        if discourse_role is TodaGroupProofNarrativeArgumentDiscourseRole.DETACHED:
            detached_count += 1

        print(
            "  "
            f"ordered={ordered_position}, "
            f"source={source_index}, "
            f"role={argument.role.value}, "
            f"conclusion_block={argument.conclusion_block.role.value}, "
            f"discourse={discourse_role.value}, "
            f"root_reachable={reachable}, "
            f"subject={subject!r}, "
            f"supporting_blocks={len(argument.supporting_blocks)}, "
            f"children={argument.child_argument_indices}"
        )

    print(f"detached_arguments={detached_count}")

    print("-" * 100)
    print("NARRATIVE")
    print("-" * 100)

    narrative = render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        sidecar,
        arguments,
    )
    print(narrative)
    print()


def main():
    for n, k in TARGETS:
        audit_target(n, k)


if __name__ == "__main__":
    main()
