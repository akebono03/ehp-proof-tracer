"""Source-backed reading of Toda (5.11) into registered typed presentations.

Only the existing HyoujiGen identifier correspondence may change notation.
No extra group result, arbitrary symbol substitution or proof leaf is created.
"""
from __future__ import annotations

from expression import MapApplication
from map_facts import EHP_DELTA_MAP
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from phase175_r4r10_cited_58_prop25_public.provider import screened_cited_facts
from phase175_r4r12r10r1_cited_511_public.source import CitedToda511, canonical_511
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule, Relation, RelationType

RULE_NAME = "read cited Toda (5.11) as verified typed Delta equality"


def same_registered_cited_511(goal: object) -> bool:
    """Admit only exactly typed, independently registered notation variants.

    HyoujiGen ID identity is the same source-anchored operation already used
    by the existing group-presentation comparison. The goal is never changed.
    In particular nu_4 and E nu-prime are different registered factors.
    """
    cited = canonical_511()
    if (type(goal) is not Relation
            or goal.relation_type is not RelationType.EQUALITY
            or type(goal.lhs) is not MapApplication
            or goal.lhs.map != EHP_DELTA_MAP
            or typed_endpoints(goal.lhs.expression) != typed_endpoints(cited.lhs.expression)
            or typed_endpoints(goal.rhs) != typed_endpoints(cited.rhs)):
        return False
    from phase168_r2_8_3_generator_identity.identity import (
        _generator_identity, _master_records,
    )
    try:
        records = _master_records()
    except (OSError, ValueError, KeyError, UnicodeError):
        return False
    source_lhs = _generator_identity(cited.lhs.expression, records)
    source_rhs = _generator_identity(cited.rhs, records)
    goal_lhs = _generator_identity(goal.lhs.expression, records)
    goal_rhs = _generator_identity(goal.rhs, records)
    return (source_lhs is not None and source_rhs is not None
            and source_lhs == goal_lhs and source_rhs == goal_rhs)


def expand_cited_511(goal: object, available: tuple[object, ...]) -> tuple[GoalExpansion, ...]:
    """Require the precisely cited GIVEN and registered expression identity."""
    if not same_registered_cited_511(goal):
        return ()
    source = canonical_511()
    matches = tuple(x for x in available if type(x) is CitedToda511
                    and x.locator == "(5.11)" and x.statement == source)
    if len(matches) != 1:
        return ()
    citation = matches[0]

    def guard(premises, bindings):
        return (len(premises) == 1 and premises[0].rule is ProofRule.GIVEN
                and not premises[0].premises and premises[0].conclusion == citation
                and citation.statement == source and same_registered_cited_511(goal))

    return (GoalExpansion(InferenceRule(
        name=RULE_NAME,
        description=(
            "Use exactly cited Toda (5.11) with only HyoujiGen-registered "
            "factor identities and verified sphere endpoints. No new equality is asserted."
        ),
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
