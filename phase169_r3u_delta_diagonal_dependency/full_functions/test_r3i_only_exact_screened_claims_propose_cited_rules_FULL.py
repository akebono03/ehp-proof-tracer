def test_r3i_only_exact_screened_claims_propose_cited_rules(actual):
    _, _, _, _, _, given, goals = actual
    sources = tuple(step.conclusion for step in given)
    for goal in goals:
        proposals = expand_cited_ehp_terminal_goal(goal, sources)
        assert len(proposals) == 1
        option = proposals[0]
        patterns = option.rule.premise_patterns
        assert len(option.subgoals) == len(patterns)
        if isinstance(goal, TodaDeltaInjectiveStatement):
            assert tuple(p.proof_rule for p in patterns) == (
                ProofRule.GIVEN, ProofRule.INFERENCE,
            )
            from proof import Relation
            assert isinstance(option.subgoals[1], Relation)
            assert option.subgoals[1].lhs == goal.map.source_group
        else:
            assert all(p.proof_rule is ProofRule.GIVEN for p in patterns)
        assert option.rule.conclusion_builder is not None
        assert option.rule.match_guard is not None
