"""R4-4 stage 5: general injective + surjective => isomorphism rule."""


def injective_and_surjective_imply_isomorphism_inference_rule():
    from proof import InferenceRule, PatternVariable, PremisePattern

    group_map = PatternVariable(name="group_map")
    return InferenceRule(
        name="injectivity and surjectivity imply isomorphism",
        description="A map which is both injective and surjective is an isomorphism.",
        premise_patterns=(
            PremisePattern(
                statement_type=InjectiveMapStatement,
                statement_pattern=InjectiveMapStatement(map=group_map),
            ),
            PremisePattern(
                statement_type=SurjectiveMapStatement,
                statement_pattern=SurjectiveMapStatement(map=group_map),
            ),
        ),
        conclusion_pattern=IsomorphismStatement(map=group_map),
    )
