def inspect_public_provider() -> dict[str, object]:
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
    from phase165_r12_r11_prop42_unified import (
        TodaProp42GeneralExactnessStatement,
        prefer_universal_prop42_derivation,
    )
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
    from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource
    from phase174_r3_r6_r2_prop44_lemma54.source import (
        attach_earlier_verified_lemma54,
    )
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase174_r3_r3_injective_delta_zero.audit import proof_has_cited_leaf
    from phase174_r3_r3_injective_delta_zero.rule import delta_e_injectivity_inputs
    from proof import ProofRule
    from toda_rules import TodaDeltaZeroStatement

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=5, k=3)
    if len(goals) != 1:
        raise ValueError("Expected a single registered typed pi_8^5 target")
    target = goals[0]
    citation = resolve_specialized_goal_citing_id(bridge, target)
    if citation is None:
        raise ValueError("No actual pi_8^5 publication position")
    amended = attach_earlier_verified_lemma54(bridge, citation)
    if amended is bridge:
        raise ValueError("Verified Lemma 5.4 must precede this proof target")
    bridge = amended
    screened = screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citation,
        explicit_publication_target=True,
    )
    screened = prefer_universal_prop42_derivation(screened)
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    zero_delta = TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(7, 7), TodaPrimaryGroup(5, 3),
    ))
    if zero_delta in available:
        raise ValueError("Zero Delta has been promoted to a source GIVEN")
    provider = shared_expansion_provider(screened, proof_target=target)
    proposals = provider(zero_delta)
    integrated = tuple(p for p in proposals if getattr(p.rule,"name",None) == RULE_NAME)
    if len(integrated) != 1:
        raise ValueError("The general Delta rule is not uniquely connected to the public provider")
    if integrated[0].subgoals != delta_e_injectivity_inputs(zero_delta):
        raise ValueError("Public subgoals diverge from the reviewed EHP inference")
    # Preserve First Successful Proof Search. An older valid route can win
    # before the new proposal; verify the new rule with a diagnostic root filter.
    # Subsidiary goals still use the actual citation-screened public provider.
    def new_rule_for_root(query: object):
        options = provider(query)
        if query != zero_delta:
            return options
        return tuple(
            proposal for proposal in options
            if getattr(proposal.rule, "name", None) == RULE_NAME
        )

    step = reconstruct_registered_goal(
        zero_delta, screened, citation, new_rule_for_root,
        lookup_mode="typed_reference",
    )
    if (
        step.rule is not ProofRule.INFERENCE or step.conclusion != zero_delta
        or getattr(step.inference_rule, "name", None) != RULE_NAME
        or len(step.premises) != 2
        or any(prior.rule is not ProofRule.INFERENCE for prior in step.premises)
        or not proof_has_cited_leaf(step.premises[0], TodaProp44UniversalStatement())
        or not proof_has_cited_leaf(step.premises[0], TodaLemma54TypedSource())
        or not proof_has_cited_leaf(step.premises[1], TodaProp42GeneralExactnessStatement())
    ):
        raise ValueError("Connected rule lacks real public source ancestry")

    selected = reconstruct_registered_goal(
        zero_delta, screened, citation, provider, lookup_mode="typed_reference",
    )
    if selected.rule is not ProofRule.INFERENCE or selected.conclusion != zero_delta:
        raise ValueError("Ordinary public provider cannot reconstruct Delta zero")
    return {
        "root_goal_type": type(target).__name__,
        "zero_delta_goal_type": type(zero_delta).__name__,
        "publication_citing_assertion_id": citation,
        "screened_source_count": len(available),
        "new_public_provider_proposals": len(integrated),
        "new_rule_name": RULE_NAME,
        "ordinary_first_success_rule": getattr(selected.inference_rule, "name", None),
        "premise_types": [type(x.conclusion).__name__ for x in step.premises],
        "premises_both_inferred": True,
        "source_ancestry_checked": True,
        "delta_zero_publicly_reconstructed": True,
        "named_group_goal_complete": False,
        "new_given": 0,
    }
