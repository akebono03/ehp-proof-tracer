"""Specialize the already cited independent Hopf-fibration splitting.

No new GIVEN, no conditional Proposition 4.4 witness, no public wiring.
"""
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import GoalExpansion
from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource
from phase174_r3_r6_r2_prop44_lemma54.source import (
    PRELUDE_LOCATOR, TodaPreProp44SplittingStatement,
)
from phase176_r3r48_cited_finite_delta_kernel.rule import linked_cited_steps
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule

RULE_NAME = 'cited Hopf-fibration splitting implies suspension injectivity'
SOURCE = TodaPreProp44SplittingStatement()


def splitting_inputs(goal):
    """Concrete one-fold suspension into a dimension covered by the source."""
    if type(goal) is not MapInjective or type(goal.map) is not TodaSuspensionMap:
        return None
    a, b = goal.map.source_group, goal.map.target_group
    if type(a) is not TodaPrimaryGroup or type(b) is not TodaPrimaryGroup:
        return None
    q, n, p, m = a.group_dimension, a.sphere_dimension, b.group_dimension, b.sphere_dimension
    if (any(type(v) is not int for v in (q, n, p, m))
            or m not in SOURCE.dimensions or q < max(2, n)
            or p != q + 1 or m != n + 1):
        return None
    return (SOURCE,)


def screened_splitting_steps(bridge):
    """Accept only the existing positioned and cited source in a screened bridge."""
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError('screened typed registry bridge required')
    steps = linked_cited_steps(bridge, SOURCE)
    if len(steps) != 1:
        return ()
    links = tuple(link for link in bridge.proof_links if link.step is steps[0])
    if len(links) != 1:
        return ()
    assertion = bridge.registry.assertion(links[0].assertion_id)
    ref = bridge.registry.reference(assertion.reference_id)
    if ref.locator != PRELUDE_LOCATOR or ref.publication_position != 7250:
        return ()
    citation = steps[0].inference_rule.literature_reference
    if citation.locator != PRELUDE_LOCATOR:
        return ()
    return steps


def prefer_existing_lemma54(goal, bridge):
    """Retain the existing n=4 source preference; it does not apply to n=8."""
    return (goal.map.target_group.sphere_dimension == 4
            and any(type(link.step.conclusion) is TodaLemma54TypedSource
                    for link in bridge.proof_links if link.step is not None
                    and link.step.rule is ProofRule.GIVEN))


def splitting_injectivity_rule(goal, *, bridge):
    required = splitting_inputs(goal)
    if required is None or len(screened_splitting_steps(bridge)) != 1:
        raise ValueError('valid suspension and uniquely linked cited splitting required')
    if prefer_existing_lemma54(goal, bridge):
        raise ValueError('preserve existing Lemma 5.4 route for n=4')

    def guard(premises, bindings):
        return (len(premises) == 1
                and premises[0].rule is ProofRule.GIVEN
                and premises[0].conclusion == SOURCE
                and not premises[0].premises
                and splitting_inputs(goal) == required
                and not prefer_existing_lemma54(goal, bridge)
                and len(screened_splitting_steps(bridge)) == 1
                and premises[0] in screened_splitting_steps(bridge))

    return InferenceRule(
        name=RULE_NAME,
        description='The first summand inclusion followed by the cited E+h_* isomorphism is E, hence injective.',
        premise_patterns=(PremisePattern(proof_rule=ProofRule.GIVEN,
                          statement_type=TodaPreProp44SplittingStatement,
                          statement_pattern=SOURCE),),
        conclusion_pattern=goal,
        match_guard=guard,
        literature_reference=LiteratureReference(label='Toda Chapter IV prelude', locator=PRELUDE_LOCATOR),
    )


def expand_splitting_injectivity(goal, *, bridge):
    """A single backward obligation; do not supply an inferred proof as GIVEN."""
    required = splitting_inputs(goal)
    if required is None or len(screened_splitting_steps(bridge)) != 1:
        return ()
    if prefer_existing_lemma54(goal, bridge):
        return ()
    return (GoalExpansion(splitting_injectivity_rule(goal, bridge=bridge), required),)
