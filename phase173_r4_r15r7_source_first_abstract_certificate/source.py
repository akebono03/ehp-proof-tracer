"""Build a source-screened n=4 context for an abstract Toda 4.4 consequence.

The registered target is used solely to choose and validate earlier database
priors. It is never inserted as a source or inferred named-group conclusion.
"""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step
from phase173_r4_r10_general_toda56_core.core import checked_abstract_inputs
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


def screened_abstract_context(
    bridge: RegistryBridgeResult, *, proof_target: object, chapter: str,
) -> RegistryBridgeResult | None:
    """Reuse the exact original Lemma 5.4 archive and source-first screening.

    A directly cited predecessor is removed ONLY if its separately admitted
    database counterpart can be verified. This avoids a direct literature leaf
    taking the place of the required adopted-DB hypothesis.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("A typed source registry is required")
    inputs = checked_abstract_inputs(proof_target)
    if inputs is None or ADOPTED_ASSERTION_ID in bridge.registry._assertions:
        return None
    archive = _validated_archive(bridge, chapter)
    reference = bridge.registry.reference(archive.reference_id)
    if (type(reference.publication_position) is not int
            or reference.publication_position < 1):
        return None

    registry = UnifiedStatementRegistry()
    for item in bridge.registry._references.values():
        registry.add_reference(item)
    for item in bridge.registry._assertions.values():
        registry.add_assertion(item)
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
    screened = screen_independent_sources_for_derived_goal(
        augmented, goal=proof_target,
    )
    for prior in inputs:
        matches = tuple(
            link for link in screened.proof_links
            if link.step is not None and link.step.conclusion == prior
        )
        if len(matches) > 1:
            return None
        if matches:
            if admitted_db_step(prior, proof_target=proof_target, bridge=screened) is None:
                return None
            link = matches[0]
            assertion = screened.registry.assertion(link.assertion_id)
            if (link.step.rule is not ProofRule.GIVEN
                    or link.step.premises
                    or assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                    or assertion.content != prior):
                return None
            screened = RegistryBridgeResult(
                screened.registry, screened.records,
                tuple(item for item in screened.proof_links
                      if item.assertion_id != link.assertion_id),
            )

    theorem = TodaProp44UniversalStatement()
    lemma = TodaLemma54TypedSource()
    for expected in (theorem, lemma):
        links = tuple(
            item for item in screened.proof_links
            if item.step is not None
            and type(item.step.conclusion) is type(expected)
            and item.step.conclusion == expected
            and item.step.rule is ProofRule.GIVEN
            and not item.step.premises
            and screened.registry.assertion(item.assertion_id).origin
            is AssertionOrigin.FIXED_STATEMENT
        )
        if len(links) != 1:
            return None
    if any(
        item.step is not None
        and (item.step.conclusion == proof_target
             or item.step.conclusion in inputs)
        for item in screened.proof_links
    ):
        return None
    return screened
