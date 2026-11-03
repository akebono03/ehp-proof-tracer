"""Independent source screen for zero-group instances of Toda Proposition 4.4.

Neither a zero DB target nor a source archive is upgraded into a theorem.
The existing original Lemma 5.4 source validator is reused unchanged.
"""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step
from phase173_r4_r10_general_toda56_core.core import checked_general_inputs
from phase173_r4_r1_lemma54_source_bridge.source import (
    ADOPTED_ASSERTION_ID,
    TodaLemma54TypedSource,
    _validated_archive,
)
from proof import ProofRule
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    UnifiedStatementRegistry,
)


def screened_zero_toda56_context(
    bridge: RegistryBridgeResult, *, goal: object, chapter: str,
) -> RegistryBridgeResult | None:
    """Screen real Proposition 4.4 and Lemma 5.4 citations for a zero goal.

    A DB prior may not be replaced by a competing direct fixed-statement leaf.
    Such direct leaves are excluded only after the same authenticated DB-prior
    admission check used in the inference guard; ambiguous leaves fail closed.
    All registered assertions and their references are retained in the registry.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("Expected a typed registry bridge")
    if not isinstance(goal, TodaPrimaryGroupZeroStatement):
        return None
    inputs = checked_general_inputs(goal)
    if inputs is None or any(
        not isinstance(item, TodaPrimaryGroupZeroStatement) for item in inputs
    ):
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

    for prior in inputs:
        # Refuse any ambiguity instead of quietly selecting a preferred proof.
        matched = tuple(
            link for link in screened.proof_links
            if link.step is not None and link.step.conclusion == prior
        )
        if len(matched) > 1:
            return None
        if matched:
            step = admitted_db_step(prior, proof_target=goal, bridge=screened)
            if step is None:
                return None
            selected = matched[0]
            assertion = screened.registry.assertion(selected.assertion_id)
            if not (
                selected.step.rule is ProofRule.GIVEN
                and not selected.step.premises
                and assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and assertion.content == prior
            ):
                return None
            screened = RegistryBridgeResult(
                screened.registry, screened.records,
                tuple(link for link in screened.proof_links
                      if link.assertion_id != selected.assertion_id),
            )

    lemma_links = tuple(
        link for link in screened.proof_links
        if link.assertion_id == ADOPTED_ASSERTION_ID
        and link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == TodaLemma54TypedSource()
    )
    theorem_links = tuple(
        link for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and type(link.step.conclusion) is TodaProp44UniversalStatement
        and link.step.conclusion == TodaProp44UniversalStatement()
    )
    if len(lemma_links) != 1 or len(theorem_links) != 1:
        return None
    if any(link.step is not None and link.step.conclusion == goal
           for link in screened.proof_links):
        return None
    if any(link.step is not None and link.step.conclusion in inputs
           for link in screened.proof_links):
        return None
    return screened
