def expand_cited_ehp_terminal_goal(
    goal: object, screened_claims: tuple[object, ...]
) -> tuple[GoalExpansion, ...]:
    """Derive the existing n=3 EHP conclusions from exact cited GIVENs.

    The legacy rule remains untouched. Its mathematical guard and conclusion
    builder are reused with explicitly cited proof leaves as premises; only
    its historical requirement that the leaves be INFERENCE is specialized.
    The shared caller supplies citation-screened, fixed-statement GIVEN values.
    No proof leaf, conclusion, or mathematical fact is manufactured here.
    """
    from dataclasses import replace
    from proof import ProofRule

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
    # Exactly one cited typed GIVEN must match *each* mathematical prerequisite.
    # A mere registered assertion without a screened proof link is insufficient.
    for prerequisite in proposal.subgoals:
        if sum(
            type(source) is type(prerequisite) and source == prerequisite
            for source in screened_claims
        ) != 1:
            return ()
    cited_rule = replace(
        original,
        name="cited prior sources: " + original.name,
        premise_patterns=tuple(
            replace(pattern, proof_rule=ProofRule.GIVEN)
            for pattern in patterns
        ),
    )
    return (GoalExpansion(cited_rule, proposal.subgoals),)
