from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_argument_discourse import (
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
    (3, 4),
    (4, 5),
    (6, 5),
    (4, 6),
    (5, 6),
    (7, 7),
)


def _rule_name(proof_step):
    inference_rule = proof_step.inference_rule
    if inference_rule is None:
        return None
    return inference_rule.name


def audit_target(n, k):
    report = build_standard_toda_report(n=n, k=k)
    print("=" * 78)
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

    print(f"root_rule={_rule_name(group_result.proof_step)!r}")
    print(f"nodes={len(presentation.nodes)}")
    print(f"edges={len(presentation.edges)}")
    print(f"blocks={len(blocks)}")
    print(f"arguments={len(arguments)}")
    print("argument_summary:")

    for index, (argument, discourse_role) in enumerate(
        zip(ordered_arguments, discourse_roles)
    ):
        subject = extract_toda_group_proof_narrative_argument_purpose_subject(
            argument
        )
        print(
            "  "
            f"{index}: "
            f"role={argument.role.value}, "
            f"discourse={discourse_role.value}, "
            f"subject={subject!r}, "
            f"supporting_blocks={len(argument.supporting_blocks)}, "
            f"children={argument.child_argument_indices}"
        )

    print("-" * 78)
    print("NARRATIVE")
    print("-" * 78)
    narrative = render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        sidecar,
        arguments,
    )
    print(narrative)


def main():
    for n, k in TARGETS:
        audit_target(n, k)


if __name__ == "__main__":
    main()
