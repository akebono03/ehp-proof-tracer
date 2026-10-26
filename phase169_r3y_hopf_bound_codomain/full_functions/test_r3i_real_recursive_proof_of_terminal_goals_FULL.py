def test_r3i_real_recursive_proof_of_terminal_goals(actual):
    _, screened, goal, citing, _, _, terminals = actual
    provider = shared_expansion_provider(screened, proof_target=goal)
    for terminal in terminals:
        step = reconstruct_registered_goal(
            terminal, screened, citing, provider,
            lookup_mode="typed_reference_publication",
        )
        assert step.rule is ProofRule.INFERENCE
        assert step.conclusion == terminal
        assert step.inference_rule is not None
        assert step.inference_rule.name.startswith("cited prior sources")
        if isinstance(terminal, TodaDeltaInjectiveStatement):
            assert len(step.premises) == 2
            assert step.premises[0].rule is ProofRule.GIVEN
            assert step.premises[1].rule is ProofRule.INFERENCE
            assert len(step.premises[1].premises) == 1
            assert step.premises[1].premises[0].rule is ProofRule.GIVEN
        else:
            assert tuple(p.rule for p in step.premises) == (
                ProofRule.GIVEN, ProofRule.GIVEN, ProofRule.INFERENCE,
            )
            assert len(step.premises[-1].premises) == 1
            assert step.premises[-1].premises[0].rule is ProofRule.GIVEN
