from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_argument_body_renderer import render_toda_group_proof_narrative_argument_body_markdown
from toda_group_proof_narrative_argument_direct_premises import extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises
from toda_group_proof_narrative_argument_discourse import classify_toda_group_proof_narrative_argument_discourse_roles
from toda_group_proof_narrative_argument_local_body import extract_toda_group_proof_narrative_argument_local_body_blocks
from toda_group_proof_narrative_argument_multi_renderer import (
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
    _toda_group_proof_narrative_argument_transition_by_conclusion_id,
    render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_argument_ordering import order_toda_group_proof_narrative_arguments
from toda_group_proof_narrative_arguments import (
    TodaGroupProofNarrativeArgumentRole,
    extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_exactness_components import build_toda_group_proof_narrative_exactness_method_components
from toda_group_proof_narrative_exactness_selection import select_toda_group_proof_narrative_primary_exactness_component
from toda_group_proof_narrative_method_evidence import extract_toda_group_proof_narrative_argument_method_evidence
from toda_group_proof_narrative_relevant_groups import extract_toda_group_proof_narrative_argument_relevant_groups
from toda_group_proof_narrative_transition_renderer import render_toda_group_proof_narrative_transition_connector
from toda_group_proof_narrative_transitions import TodaGroupProofNarrativeTransitionRole
from toda_rules import TodaEtaFamilyDefinitionStatement


def inspect(n, k):
    presentation, blocks, sidecar, arguments = _method_evidence_data(n, k)
    ordered = order_toda_group_proof_narrative_arguments(arguments)
    discourse = classify_toda_group_proof_narrative_argument_discourse_roles(arguments)
    transitions = _toda_group_proof_narrative_argument_transition_by_conclusion_id(
        presentation, blocks, arguments
    )
    source_index = {id(argument): index for index, argument in enumerate(arguments)}

    print("=" * 80)
    print(f"n={n} k={k} source-order -> ordered:", tuple(source_index[id(a)] for a in ordered))

    for ordered_position, argument in enumerate(ordered):
        argument_index = source_index[id(argument)]
        if discourse[ordered_position].value == "detached":
            print(f"ARG pos={ordered_position} source={argument_index}: DETACHED")
            continue

        relevant_groups = extract_toda_group_proof_narrative_argument_relevant_groups(
            presentation, blocks, argument
        )
        evidence = extract_toda_group_proof_narrative_argument_method_evidence(
            presentation, blocks, sidecar, arguments, argument_index
        )
        components = build_toda_group_proof_narrative_exactness_method_components(evidence)
        primary = select_toda_group_proof_narrative_primary_exactness_component(
            relevant_groups, components
        )
        local = extract_toda_group_proof_narrative_argument_local_body_blocks(
            presentation, blocks, sidecar, arguments, argument_index
        )
        local_ids = {id(block) for block in local}
        evidence_ids = {id(block) for block in evidence}
        local = tuple(
            block for block in blocks
            if id(block) in local_ids or id(block) in evidence_ids
        )

        hidden = frozenset(
            id(step)
            for block in local
            for step in block.steps
            if (
                argument.role is not TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION
                and isinstance(step.conclusion, TodaEtaFamilyDefinitionStatement)
            )
        )
        hidden = hidden | _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
            presentation, blocks, local, sidecar, argument
        )

        transition = transitions.get(id(argument.conclusion_block))
        connector = None if transition is None else render_toda_group_proof_narrative_transition_connector(transition)
        derivation_source_ids = (
            frozenset()
            if transition is None or transition.role is not TodaGroupProofNarrativeTransitionRole.DERIVATION
            else frozenset(id(block) for block in transition.source_blocks)
        )
        conclusion = (
            None
            if connector is None
            else extract_toda_group_proof_narrative_argument_conclusion_step(argument)
        )
        direct = (
            ()
            if conclusion is None
            else extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
                argument, arguments
            )
        )

        body = render_toda_group_proof_narrative_argument_body_markdown(
            presentation,
            blocks,
            local,
            primary,
            connector_before_block_id=None if connector is None else id(argument.conclusion_block),
            connector_text=connector,
            conclusion_step=conclusion,
            direct_derivation_premises=direct,
            context_hidden_step_ids=hidden,
            preserve_provenance_block_ids=derivation_source_ids,
        )

        print()
        print(f"ARG pos={ordered_position} source={argument_index} role={argument.role.value}")
        print("DIRECT BODY:")
        print(body)

    print()
    print("FINAL MULTI:")
    print(render_toda_group_proof_narrative_multi_argument_markdown(
        presentation, blocks, sidecar, arguments
    ))


inspect(3, 3)
inspect(5, 3)
