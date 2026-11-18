"""Translate only the independently cited (5.11) wrapper into an inferred equality."""
from __future__ import annotations

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
from phase175_r4r10_cited_58_prop25_public.provider import screened_cited_facts
from phase175_r4r12r10r1_cited_511_public.source import CitedToda511, canonical_511
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule, Relation

RULE_NAME = "read cited Toda (5.11) as verified typed Delta equality"


def expand_cited_511(goal: object, available: tuple[object, ...]) -> tuple[GoalExpansion, ...]:
    if type(goal) is not Relation or goal != canonical_511():
        return ()
    matches = tuple(x for x in available if type(x) is CitedToda511
                    and x.locator == "(5.11)" and x.statement == goal)
    if len(matches) != 1:
        return ()
    citation = matches[0]

    def guard(premises, bindings):
        return (len(premises) == 1 and premises[0].rule is ProofRule.GIVEN
                and not premises[0].premises and premises[0].conclusion == citation
                and citation.statement == goal)

    return (GoalExpansion(InferenceRule(
        name=RULE_NAME,
        description="Infer only the typed Delta equality explicitly printed in Toda (5.11).",
        literature_reference=LiteratureReference(label="Toda (5.11)", locator="(5.11)"),
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN, statement_type=CitedToda511,
            statement_pattern=citation,
        ),),
        match_guard=guard,
        conclusion_pattern=goal,
    ), (citation,)),)


def build_cited_511_provider(bridge: RegistryBridgeResult):
    available = screened_cited_facts(bridge)

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        return expand_cited_511(goal, available)

    return expand
