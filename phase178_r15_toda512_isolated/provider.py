"""Read a cited typed claim without relaxing any existing inference guard."""
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import GoalExpansion
from phase175_r4r10_cited_58_prop25_public.provider import screened_cited_facts
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule
from .source import CitedToda512, canonical_512

RULE_NAME = 'read cited Toda (5.12) typed Delta injectivity'


def expand_cited_512(goal, available):
    if type(goal) is not MapInjective:
        return ()
    matches = tuple(c for c in available if type(c) is CitedToda512
                    and type(c.n) is int and c.n in (4, 5, 6)
                    and c == canonical_512(c.n) and c.statement == goal)
    if len(matches) != 1:
        return ()
    claim = matches[0]

    def guard(premises, bindings):
        return (len(premises) == 1 and premises[0].rule is ProofRule.GIVEN
                and not premises[0].premises and premises[0].conclusion == claim
                and claim == canonical_512(claim.n) and claim.statement == goal)

    return (GoalExpansion(InferenceRule(
        name=RULE_NAME, literature_reference=LiteratureReference(label='Toda (5.12)', locator='(5.12)'),
        premise_patterns=(PremisePattern(proof_rule=ProofRule.GIVEN,
            statement_type=CitedToda512, statement_pattern=claim),),
        match_guard=guard, conclusion_pattern=goal), (claim,)),)


def build_cited_512_provider(bridge):
    available = screened_cited_facts(bridge)

    def expand(goal):
        return expand_cited_512(goal, available)

    return expand
