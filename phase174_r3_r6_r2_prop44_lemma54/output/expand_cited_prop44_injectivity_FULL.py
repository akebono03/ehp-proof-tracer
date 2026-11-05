def expand_cited_prop44_injectivity(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Propose the conditional theorem only when Lemma 5.4 is source-screened."""
    from phase173_r4_r1_lemma54_source_bridge.source import (
        TodaLemma54TypedSource,
        canonical_hopf_relation,
    )

    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not _is_hopf_four_suspension(goal):
        return ()
    proposition = TodaProp44UniversalStatement()
    lemma = TodaLemma54TypedSource()
    if available.count(proposition) != 1 or available.count(lemma) != 1:
        return ()
    return (GoalExpansion(
        prop44_hopf_four_injectivity_rule(goal),
        (proposition, canonical_hopf_relation()),
    ),)
