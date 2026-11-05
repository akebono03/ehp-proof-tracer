def prop44_hopf_four_injectivity_rule(goal: MapInjective) -> InferenceRule:
    """Apply conditional Proposition 4.4 to a proved Lemma 5.4 Hopf witness."""
    from phase173_r4_r1_lemma54_source_bridge.source import (
        TodaLemma54TypedSource,
        canonical_hopf_relation,
    )
    from proof import Relation, RelationType

    if not _is_hopf_four_suspension(goal):
        raise ValueError("goal must be an n=4 suspension injectivity")
    hopf = canonical_hopf_relation()
    proposition = TodaProp44UniversalStatement()

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.GIVEN
            and premises[0].conclusion == proposition
            and premises[1].rule is ProofRule.INFERENCE
            and premises[1].conclusion == hopf
            and len(premises[1].premises) == 1
            and premises[1].premises[0].rule is ProofRule.GIVEN
            and type(premises[1].premises[0].conclusion) is TodaLemma54TypedSource
            and premises[1].premises[0].conclusion == TodaLemma54TypedSource()
            and _is_hopf_four_suspension(goal)
        )

    return InferenceRule(
        name="Toda Proposition 4.4 using separately proved Hopf invariant",
        description=(
            "Proposition 4.4 is conditional; independently prove H(nu_4)=iota_7 "
            "from the earlier, screened Lemma 5.4 before specializing it."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=TodaProp44UniversalStatement,
                statement_pattern=proposition,
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=hopf,
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Proposition 4.4", locator="Proposition 4.4",
        ),
    )
