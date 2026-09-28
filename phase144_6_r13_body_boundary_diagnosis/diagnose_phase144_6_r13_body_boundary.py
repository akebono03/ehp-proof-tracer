from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_argument_ordering import order_toda_group_proof_narrative_arguments
from toda_group_proof_narrative_argument_discourse import classify_toda_group_proof_narrative_argument_discourse_roles
from toda_group_proof_narrative_arguments import extract_toda_group_proof_narrative_argument_conclusion_step
from toda_group_proof_narrative_argument_local_body import extract_toda_group_proof_narrative_argument_local_body_blocks
from toda_group_proof_narrative_argument_method_evidence import extract_toda_group_proof_narrative_argument_method_evidence
from toda_group_proof_narrative_argument_exactness_components import extract_toda_group_proof_narrative_argument_exactness_components
from toda_group_proof_narrative_argument_exactness_selection import select_toda_group_proof_narrative_primary_exactness_component
from toda_group_proof_narrative_argument_direct_premises import extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises
from toda_group_proof_narrative_argument_multi_renderer import (
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
    render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_argument_body_renderer import render_toda_group_proof_narrative_argument_body_markdown
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step

def inspect(n,k):
    presentation, blocks, sidecar, arguments = _method_evidence_data(n,k)
    ordered = order_toda_group_proof_narrative_arguments(arguments)
    source_index = {id(a): i for i,a in enumerate(arguments)}
    print("="*80)
    print(f"n={n} k={k} source-order -> ordered:", tuple(source_index[id(a)] for a in ordered))
    for pos,arg in enumerate(ordered):
        ai=source_index[id(arg)]
        local=extract_toda_group_proof_narrative_argument_local_body_blocks(
            presentation, blocks, sidecar, arguments, ai
        )
        evidence=extract_toda_group_proof_narrative_argument_method_evidence(
            presentation, blocks, sidecar, arguments, ai
        )
        local_ids={id(b) for b in local}
        evidence_ids={id(b) for b in evidence}
        merged=tuple(b for b in blocks if id(b) in local_ids or id(b) in evidence_ids)
        hidden=_toda_group_proof_narrative_argument_frontier_hidden_step_ids(
            presentation, blocks, merged, sidecar, arg
        )
        components=extract_toda_group_proof_narrative_argument_exactness_components(
            presentation, blocks, sidecar, arg
        )
        primary=select_toda_group_proof_narrative_primary_exactness_component(components)
        conclusion=extract_toda_group_proof_narrative_argument_conclusion_step(arg)
        direct=() if conclusion is None else extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(arg, arguments)
        body=render_toda_group_proof_narrative_argument_body_markdown(
            presentation,
            blocks,
            merged,
            primary,
            conclusion_step=conclusion,
            direct_derivation_premises=direct,
            context_hidden_step_ids=hidden,
        )
        print()
        print(f"ORDERED ARG pos={pos} source={ai} role={arg.role.value}")
        print("DIRECT BODY:")
        print(body)
    print()
    print("FINAL MULTI:")
    print(render_toda_group_proof_narrative_multi_argument_markdown(
        presentation, blocks, sidecar, arguments
    ))

inspect(3,3)
inspect(5,3)
