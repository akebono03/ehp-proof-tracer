from toda_group_proof_narrative_argument_discourse import (
    classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_argument_ordering import (
    order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_single_renderer import (
    render_toda_group_proof_narrative_single_argument_markdown,
)
from toda_group_proof_narrative_exactness_components import (
    build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_selection import (
    select_toda_group_proof_narrative_primary_exactness_component,
)
from toda_group_proof_narrative_method_evidence import (
    extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_relevant_groups import (
    extract_toda_group_proof_narrative_argument_relevant_groups,
)
from tests.test_phase143_19_method_evidence import (
    _method_evidence_data,
)


def audit_case(
    n: int,
    k: int,
) -> None:
    (
        presentation,
        blocks,
        sidecar,
        arguments,
    ) = _method_evidence_data(
        n,
        k,
    )

    ordered_arguments = (
        order_toda_group_proof_narrative_arguments(
            arguments
        )
    )

    discourse_roles = (
        classify_toda_group_proof_narrative_argument_discourse_roles(
            arguments
        )
    )

    source_index_by_identity = {
        id(argument): index
        for index, argument in enumerate(
            arguments
        )
    }

    print("=" * 78)
    print(
        f"n={n}, k={k}, "
        f"arguments={len(arguments)}, "
        f"ordered={len(ordered_arguments)}"
    )
    print("=" * 78)

    rendered_arguments = []

    for ordered_position, argument in enumerate(
        ordered_arguments
    ):
        source_index = source_index_by_identity[
            id(argument)
        ]

        discourse_role = discourse_roles[
            ordered_position
        ]

        relevant_groups = (
            extract_toda_group_proof_narrative_argument_relevant_groups(
                presentation,
                blocks,
                argument,
            )
        )

        evidence = (
            extract_toda_group_proof_narrative_argument_method_evidence(
                presentation,
                blocks,
                sidecar,
                arguments,
                source_index,
            )
        )

        components = (
            build_toda_group_proof_narrative_exactness_method_components(
                evidence
            )
        )

        primary_component = (
            select_toda_group_proof_narrative_primary_exactness_component(
                relevant_groups,
                components,
            )
        )

        rendered = (
            render_toda_group_proof_narrative_single_argument_markdown(
                presentation,
                blocks,
                sidecar,
                arguments,
                source_index,
                discourse_role,
                primary_component,
            )
        )

        rendered_arguments.append(
            rendered
        )

        print(
            f"[Argument {ordered_position + 1}] "
            f"source_index={source_index}, "
            f"role={argument.role.value}, "
            f"discourse={discourse_role.value}, "
            f"primary={primary_component is not None}"
        )
        print()
        print(
            rendered
        )
        print()

    print("-" * 78)
    print("NAIVE MULTI-ARGUMENT ASSEMBLY")
    print("-" * 78)
    print()
    print(
        "\n\n".join(
            rendered_arguments
        )
    )
    print()


def main() -> None:
    cases = (
        (3, 3),
        (5, 3),
        (8, 7),
        (9, 7),
    )

    for n, k in cases:
        audit_case(
            n,
            k,
        )


if __name__ == "__main__":
    main()
