"""Construct an isolated source-first context without assigning a target citation rank.

The previously verified Lemma 5.4 archive is checked byte-for-byte through the
existing validator. Only the lemma's already registered publication metadata
is reused; no new publication positions, citations or target claims are made.
"""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase173_r4_r1_lemma54_source_bridge.source import (
    ADOPTED_ASSERTION_ID,
    TodaLemma54TypedSource,
    _validated_archive,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    UnifiedStatementRegistry,
)


def screened_source_first_context(
    bridge: RegistryBridgeResult, *, goal: object, chapter: str,
) -> RegistryBridgeResult | None:
    """Return a verified isolated context or fail closed.

    A missing target citation position is not synthesized; source-first uses
    only the source's independent, already registered reference position.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("Expected a typed registry bridge")
    if not (
        isinstance(goal, Relation)
        and goal.relation_type is RelationType.EQUALITY
        and isinstance(goal.lhs, TodaPrimaryGroup)
        and goal.lhs.sphere_dimension == 4
        and type(goal.lhs.group_dimension) is int
        and goal.lhs.group_dimension in (8, 9, 10)
    ):
        return None
    if resolve_specialized_goal_citing_id(bridge, goal) is not None:
        return None
    if ADOPTED_ASSERTION_ID in bridge.registry._assertions:
        return None
    archive = _validated_archive(bridge, chapter)
    original_reference = bridge.registry.reference(archive.reference_id)
    if (type(original_reference.publication_position) is not int
            or original_reference.publication_position < 1):
        return None
    registry = UnifiedStatementRegistry()
    for reference in bridge.registry._references.values():
        registry.add_reference(reference)
    for assertion in bridge.registry._assertions.values():
        registry.add_assertion(assertion)
    registry.add_assertion(AssertionEntry(
        assertion_id=ADOPTED_ASSERTION_ID,
        reference_id=archive.reference_id,
        kind=AssertionKind.STATEMENT,
        content=TodaLemma54TypedSource(),
        origin=AssertionOrigin.FIXED_STATEMENT,
        component_position=archive.component_position,
        scope=("source-first: independently registered Lemma 5.4",),
    ))
    augmented = RegistryBridgeResult(registry, bridge.records, bridge.proof_links)
    screened = screen_independent_sources_for_derived_goal(augmented, goal=goal)
    lemma_links = tuple(
        link for link in screened.proof_links
        if link.assertion_id == ADOPTED_ASSERTION_ID
        and link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == TodaLemma54TypedSource()
    )
    prop44_links = tuple(
        link for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and type(link.step.conclusion) is TodaProp44UniversalStatement
    )
    if len(lemma_links) != 1 or len(prop44_links) != 1:
        return None
    if any(link.step is not None and link.step.conclusion == goal
           for link in screened.proof_links):
        return None
    return screened
