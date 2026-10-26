def test_r3i_derived_terminal_steps_have_exact_cited_ancestors(actual):
    _, context, goal, citing, _, given, goals = actual
    source_claims = tuple(step.conclusion for step in given)
    provider = shared_expansion_provider(context, proof_target=goal)
    for terminal in goals:
        option, = expand_cited_ehp_terminal_goal(terminal, source_claims)
        inferred = reconstruct_registered_goal(
            terminal, context, citing, provider,
            lookup_mode="typed_reference_publication",
        )
        assert inferred.rule is ProofRule.INFERENCE
        assert inferred.conclusion == terminal
        assert tuple(p.conclusion for p in inferred.premises) == option.subgoals
        if isinstance(terminal, TodaDeltaInjectiveStatement):
            cited, diagonal = inferred.premises
            assert cited.rule is ProofRule.GIVEN
            assert diagonal.rule is ProofRule.INFERENCE
            assert len(diagonal.premises) == 1
            assert diagonal.premises[0].rule is ProofRule.GIVEN
            assert diagonal.premises[0].inference_rule.literature_reference.locator == "(5.1)"
        else:
            assert all(p.rule is ProofRule.GIVEN and not p.premises for p in inferred.premises)
