def expand_cited_ehp_terminal_goal(
    goal: object, screened_claims: tuple[object, ...]
) -> tuple[GoalExpansion, ...]:
    """Expand terminal EHP goals using cited facts and certified prerequisites.

    The historical rule supplies the mathematical Delta conclusion and guard.
    Delta injectivity additionally requires a proved free-cyclic domain, derived
    from the previously screened diagonal statement (5.1).  The result is a
    GOAL expansion, never a fabricated source or a completed proof step.
    """
    from dataclasses import replace

    from homotopy_groups import FreeCyclicGroup
    from phase165_r57_r20_general_specialization import specialize_typed_statement
    from proof import PremisePattern, ProofRule, Relation, RelationType
    from toda_rules import TodaDeltaInjectiveStatement

    if not isinstance(screened_claims, tuple):
        raise TypeError("screened_claims must be a tuple")
    proposals = expand_registered_ehp_terminal_goal(goal, screened_claims)
    if len(proposals) != 1:
        return ()
    proposal = proposals[0]
    original = proposal.rule
    patterns = original.premise_patterns
    if len(patterns) != len(proposal.subgoals) or not all(
        pattern.proof_rule is ProofRule.INFERENCE for pattern in patterns
    ):
        raise RuntimeError("historical EHP premise contract changed")
    if original.match_guard is None or original.conclusion_builder is None:
        raise RuntimeError("historical EHP rule has no mathematical contract")
    for prerequisite in proposal.subgoals:
        if sum(
            type(source) is type(prerequisite) and source == prerequisite
            for source in screened_claims
        ) != 1:
            return ()

    if isinstance(goal, TodaDeltaInjectiveStatement):
        proposition = proposal.subgoals[0]
        delta_relation = proposition.delta_iota5_relation
        domain = Relation(
            lhs=delta_relation.map.source_group,
            rhs=FreeCyclicGroup(delta_relation.element),
            relation_type=RelationType.EQUALITY,
        )
        codomain = proposition.pi3_2_group_relation
        if not (
            isinstance(codomain, Relation)
            and codomain.relation_type is RelationType.EQUALITY
            and codomain.lhs == delta_relation.map.target_group
            and isinstance(codomain.rhs, FreeCyclicGroup)
            and codomain.rhs.generator == delta_relation.positive_value.expression
        ):
            return ()
        diagonal_sources = tuple(
            source for source in screened_claims
            if specialize_typed_statement(source, domain) is not None
        )
        if len(diagonal_sources) != 1:
            return ()

        def guard(premises, bindings):
            if len(premises) != 2:
                return False
            cited, diagonal_step = premises
            return (
                original.match_guard((cited,), bindings)
                and diagonal_step.rule is ProofRule.INFERENCE
                and diagonal_step.conclusion == domain
                and len(diagonal_step.premises) == 1
                and diagonal_step.premises[0].rule is ProofRule.GIVEN
                and diagonal_step.premises[0].conclusion == diagonal_sources[0]
                and specialize_typed_statement(
                    diagonal_step.premises[0].conclusion, domain
                ) is not None
            )

        def conclusion(premises):
            return original.conclusion_builder((premises[0],))

        justified = replace(
            original,
            name="cited prior sources and derived diagonal: " + original.name,
            premise_patterns=(
                replace(patterns[0], proof_rule=ProofRule.GIVEN),
                PremisePattern(
                    proof_rule=ProofRule.INFERENCE,
                    statement_type=Relation,
                    relation_type=RelationType.EQUALITY,
                ),
            ),
            match_guard=guard,
            conclusion_builder=conclusion,
        )
        return (GoalExpansion(justified, (proposition, domain)),)

    cited_rule = replace(
        original,
        name="cited prior sources: " + original.name,
        premise_patterns=tuple(
            replace(pattern, proof_rule=ProofRule.GIVEN)
            for pattern in patterns
        ),
    )
    return (GoalExpansion(cited_rule, proposal.subgoals),)
