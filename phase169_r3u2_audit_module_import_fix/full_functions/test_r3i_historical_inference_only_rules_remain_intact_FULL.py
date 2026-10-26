def test_r3i_historical_inference_only_rules_remain_intact(actual):
    _, _, _, _, _, given, goals = actual
    source_claims = tuple(step.conclusion for step in given)
    for goal in goals:
        original, = expand_registered_ehp_terminal_goal(goal, source_claims)
        assert all(p.proof_rule is ProofRule.INFERENCE for p in original.rule.premise_patterns)
        cited, = expand_cited_ehp_terminal_goal(goal, source_claims)
        assert cited.rule is not original.rule
        if isinstance(goal, TodaDeltaInjectiveStatement):
            assert tuple(p.proof_rule for p in cited.rule.premise_patterns) == (
                ProofRule.GIVEN, ProofRule.INFERENCE,
            )
            assert cited.rule.match_guard is not original.rule.match_guard
            assert cited.rule.conclusion_builder is not original.rule.conclusion_builder
        else:
            # Factories create fresh function objects on each invocation.
            # The code objects must still be the original mathematical rules.
            assert cited.rule.match_guard.__code__ is original.rule.match_guard.__code__
            assert cited.rule.conclusion_builder.__code__ is original.rule.conclusion_builder.__code__
