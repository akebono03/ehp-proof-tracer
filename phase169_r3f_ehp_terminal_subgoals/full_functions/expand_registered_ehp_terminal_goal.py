def expand_registered_ehp_terminal_goal(
    goal: object, screened_claims: tuple[object, ...]
) -> tuple[GoalExpansion, ...]:
    """Expose only the existing n=3 terminal rules and their unproved premises.

    screened_claims must come from the common provider's citation-screened
    FIXED_STATEMENT GIVEN context. A cited composite is used to bind the exact
    target subgoal; the historical rule still insists on an INFERENCE step.
    No conclusion, ProofStep or GIVEN is created here.
    """
    if not isinstance(screened_claims, tuple):
        raise TypeError("screened_claims must be a tuple")

    from phase161_r4_literature_premise_matching import expand_phase161_r4_literature_goal
    from toda_rules import (
        TodaDeltaInjectiveStatement,
        TodaHopfInvariantSurjectiveStatement,
        TodaProp51FiniteDimensionalStatement,
    )

    plan = expand_phase161_r4_literature_goal(goal)
    if plan is None:
        return ()
    claims = tuple(
        claim for claim in screened_claims
        if isinstance(claim, TodaProp51FiniteDimensionalStatement)
    )
    if len(claims) != 1:
        return ()
    proposition = claims[0]

    if isinstance(goal, TodaDeltaInjectiveStatement):
        # The historical rule demands a separately derived INFERENCE,
        # rather than accepting the screened literature GIVEN itself.
        return (GoalExpansion(plan.inference_rule, (proposition,)),)

    if isinstance(goal, TodaHopfInvariantSurjectiveStatement):
        # This exact mathematical prerequisite is dictated by the already
        # registered n=3 historical rule. It is a GOAL, not an assertion.
        from expression import GeneratorSymbol, HomotopyElement, MapApplication
        from map_facts import EHP_H_MAP
        from proof import Relation, RelationType

        nu_prime = HomotopyElement(
            name="ν′", dimension=3, source=6, target=3,
            generator=GeneratorSymbol(family="ν", decoration="′"),
        )
        eta5 = HomotopyElement(
            name="η₅", dimension=5, source=6, target=5,
            generator=GeneratorSymbol(family="η", index=5),
        )
        required_relation = Relation(
            lhs=MapApplication(map=EHP_H_MAP, expression=nu_prime),
            rhs=eta5,
            relation_type=RelationType.EQUALITY,
        )
        return (GoalExpansion(
            plan.inference_rule, (required_relation, proposition),
        ),)
    return ()
