from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_blocks import (
    build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
    build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
    build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
    build_toda_group_result_proof_replay,
)


TARGETS = (
    (3, 3, "nu-prime reference"),
    (5, 3, "nu_5 reference"),
    (5, 7, "sigma triple-prime target"),
    (9, 7, "sigma_9 reference"),
)

INTERESTING_TYPE_NAMES = {
    "TodaLemma513Statement",
}


def _rule_name(proof_step):
    inference_rule = proof_step.inference_rule
    if inference_rule is None:
        return None
    return inference_rule.name


def _semantic_step_roles(sidecar, proof_step):
    return tuple(
        semantic.role.value
        for semantic in sidecar.step_semantics
        if semantic.proof_step is proof_step
    )


def _incoming_edges(presentation, proof_step):
    return tuple(
        edge
        for edge in presentation.edges
        if edge.premise_step is proof_step
    )


def _outgoing_edges(presentation, proof_step):
    return tuple(
        edge
        for edge in presentation.edges
        if edge.parent_step is proof_step
    )


def _print_step_path(
    presentation,
    sidecar,
    proof_step,
    node_index,
):
    print(f"node={node_index}")
    print(
        f"  statement_type="
        f"{type(proof_step.conclusion).__name__}"
    )
    print(
        f"  own_rule={_rule_name(proof_step)!r}"
    )
    print(
        f"  semantic_step_roles="
        f"{_semantic_step_roles(sidecar, proof_step)}"
    )

    incoming = _incoming_edges(
        presentation,
        proof_step,
    )
    outgoing = _outgoing_edges(
        presentation,
        proof_step,
    )

    print(f"  consumers={len(incoming)}")
    for edge in incoming:
        print(
            "    "
            f"consumer_rule={_rule_name(edge.parent_step)!r}, "
            f"premise_index={edge.premise_index}, "
            f"consumer_statement_type="
            f"{type(edge.parent_step.conclusion).__name__}"
        )

    print(f"  premises={len(outgoing)}")
    for edge in outgoing:
        print(
            "    "
            f"premise_index={edge.premise_index}, "
            f"premise_rule={_rule_name(edge.premise_step)!r}, "
            f"premise_statement_type="
            f"{type(edge.premise_step.conclusion).__name__}"
        )


def audit_target(n, k, label):
    report = build_standard_toda_report(
        n=n,
        k=k,
    )
    group_result = (
        report.candidates[
            0
        ].source_candidate.group_result
    )
    replay = (
        build_toda_group_result_proof_replay(
            group_result,
            max_depth=3,
        )
    )
    presentation = (
        build_toda_group_proof_presentation(
            replay
        )
    )
    sidecar = (
        build_toda_group_proof_narrative_semantic_sidecar(
            presentation
        )
    )
    blocks = (
        build_toda_group_proof_narrative_blocks(
            presentation,
            semantic_sidecar=sidecar,
        )
    )

    print("=" * 100)
    print(
        f"n={n}, k={k}, "
        f"target=pi_{n + k}^{n}, "
        f"label={label}"
    )
    print(
        f"nodes={len(presentation.nodes)}, "
        f"edges={len(presentation.edges)}, "
        f"blocks={len(blocks)}"
    )

    semantic_definition_steps = tuple(
        semantic.proof_step
        for semantic in sidecar.step_semantics
        if (
            semantic.role.value
            == "definition_introduction"
        )
    )

    print(
        "semantic_definition_steps="
        f"{len(semantic_definition_steps)}"
    )

    for proof_step in semantic_definition_steps:
        node_index = next(
            index
            for index, node in enumerate(
                presentation.nodes
            )
            if node.proof_step is proof_step
        )
        print("-" * 100)
        print("CURRENT DEFINITION SEMANTIC")
        _print_step_path(
            presentation,
            sidecar,
            proof_step,
            node_index,
        )

    interesting_steps = tuple(
        (
            index,
            node.proof_step,
        )
        for index, node in enumerate(
            presentation.nodes
        )
        if (
            type(
                node.proof_step.conclusion
            ).__name__
            in INTERESTING_TYPE_NAMES
        )
    )

    print(
        "TodaLemma513Statement_steps="
        f"{len(interesting_steps)}"
    )

    for node_index, proof_step in interesting_steps:
        print("-" * 100)
        print("SIGMA TRIPLE-PRIME CANDIDATE")
        _print_step_path(
            presentation,
            sidecar,
            proof_step,
            node_index,
        )

    print()


def main():
    for n, k, label in TARGETS:
        audit_target(
            n,
            k,
            label,
        )


if __name__ == "__main__":
    main()
