from toda_calculation_facade import (
    build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
    TodaGroupProofNarrativeArgumentRole,
    build_toda_group_proof_narrative_arguments,
)
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
from proof import Relation


report = build_standard_toda_report(
    n=3,
    k=3,
)

group_result = (
    report.candidates[0]
    .source_candidate
    .group_result
)

replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=3,
)

presentation = build_toda_group_proof_presentation(
    replay
)

sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
        presentation
    )
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

argument = next(
    argument
    for argument in arguments
    if argument.role
    is TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER
)

print("=== conclusion block ===")

for i, step in enumerate(
    argument.conclusion_block.steps,
    start=1,
):
    statement = step.conclusion

    print(
        i,
        type(statement).__name__,
        repr(statement),
    )

    if isinstance(
        statement,
        Relation,
    ):
        print(
            "    lhs =",
            repr(statement.lhs),
        )
        print(
            "    lhs type =",
            type(statement.lhs).__name__,
        )
        print(
            "    rhs =",
            repr(statement.rhs),
        )
        print(
            "    relation_type =",
            statement.relation_type,
        )

print()
print("=== supporting blocks ===")

for block_index, block in enumerate(
    argument.supporting_blocks,
    start=1,
):
    print(
        "BLOCK",
        block_index,
        block.role.value,
    )

    for step_index, step in enumerate(
        block.steps,
        start=1,
    ):
        statement = step.conclusion

        print(
            " ",
            step_index,
            type(statement).__name__,
            repr(statement),
        )

        if isinstance(
            statement,
            Relation,
        ):
            print(
                "    lhs =",
                repr(statement.lhs),
            )
            print(
                "    rhs =",
                repr(statement.rhs),
            )
            print(
                "    rhs type =",
                type(statement.rhs).__name__,
            )

            if hasattr(
                statement.rhs,
                "generator",
            ):
                print(
                    "    generator =",
                    repr(statement.rhs.generator),
                )

print()
print(
    "child_argument_indices =",
    argument.child_argument_indices,
)
