def composition_eta_suspension_image_rule(goal: GeneratorImage) -> InferenceRule:
    """Suspend a composite only from two verified component suspensions."""
    expected = _composition_eta_suspensions(goal)
    if expected is None:
        raise ValueError("goal must be a typed composite of consecutive eta suspensions")

    def guard(premises, bindings):
        return (len(premises) == 2
                and all(step.rule is ProofRule.INFERENCE for step in premises)
                and tuple(step.conclusion for step in premises) == expected)

    return InferenceRule(
        name="suspension preserves composition of proved eta generators",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=GeneratorSuspension),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=GeneratorSuspension),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


