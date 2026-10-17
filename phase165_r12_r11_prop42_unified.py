"""One cited Toda Proposition 4.2 schema and generic EHP specialization.

The universally quantified statement is a source leaf. Each concrete window
is an INFERENCE consequence with explicit reference ancestry.
"""
from __future__ import annotations

from dataclasses import dataclass

from homotopy_groups import TodaPrimaryGroup, TodaEHPExactnessWindow
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
from phase165_r14_r26_prop42_typed import SOURCE_ID, validate_prop42_source
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule, ProofStep
from toda_rules import TodaProp42ExactnessStatement
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)

GENERAL_ASSERTION_ID = "adopted:assertion:prop42:general"
GENERAL_REFERENCE_ID = "adopted:reference:prop42:general"


@dataclass(frozen=True)
class TodaProp42GeneralExactnessStatement:
    """The universally quantified exact EHP sequence in Proposition 4.2 (4.4)."""
    source_assertion_id: str = SOURCE_ID


def build_adopted_prop42_general_reference() -> RegistryBridgeResult:
    """Register one adopted-translation source, not any special-case windows.

    This matches the existing adopted-TeX trust policy, and does not purport
    to verify the original printed edition or override proof-use ordering.
    """
    archive, _ = build_phase165_r5_manifest_bridge()
    validate_prop42_source(archive)
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=GENERAL_REFERENCE_ID,
        kind=ReferenceKind.PROPOSITION,
        locator="Proposition 4.2 (4.4)",
        source_id="Toda adopted Japanese TeX:Proposition 4.2 (original edition unverified)",
    ))
    statement = TodaProp42GeneralExactnessStatement()
    registry.add_assertion(AssertionEntry(
        assertion_id=GENERAL_ASSERTION_ID,
        reference_id=GENERAL_REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=statement,
        origin=AssertionOrigin.FIXED_STATEMENT,
    ))
    given = ProofStep(
        conclusion=statement, premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Toda Proposition 4.2 universal EHP exact sequence",
            literature_reference=LiteratureReference(
                label="Toda Proposition 4.2", locator="Proposition 4.2 (4.4)"
            ),
        ),
    )
    return RegistryBridgeResult(registry, (), (ProofStepLink(GENERAL_ASSERTION_ID, step=given),))


def prop42_exactness_indices(statement: object) -> tuple[int, int, str] | None:
    """Identify mathematically valid consecutive windows, not names alone."""
    if not isinstance(statement, TodaProp42ExactnessStatement):
        return None
    w = statement.window
    if not isinstance(w, TodaEHPExactnessWindow):
        return None
    a, b, c = w.source_term, w.middle_term, w.target_term
    if not all(isinstance(x, TodaPrimaryGroup) for x in (a, b, c)):
        return None
    if any(type(v) is not int for x in (a, b, c)
           for v in (x.group_dimension, x.sphere_dimension)):
        return None
    if (w.first_map, w.second_map) == (EHP_DELTA_MAP, EHP_E_MAP):
        n, i, kind = b.sphere_dimension, c.group_dimension, "delta_e"
        required = ((i+1, 2*n+1), (i-1, n), (i, n+1))
    elif (w.first_map, w.second_map) == (EHP_E_MAP, EHP_H_MAP):
        n, i, kind = a.sphere_dimension, b.group_dimension, "e_h"
        required = ((i-1, n), (i, n+1), (i, 2*n+1))
    elif (w.first_map, w.second_map) == (EHP_H_MAP, EHP_DELTA_MAP):
        n, i, kind = c.sphere_dimension, a.group_dimension, "h_delta"
        required = ((i, n+1), (i, 2*n+1), (i-2, n))
    else:
        return None
    if n < 1 or i < 2 or i < n+1:
        return None
    actual = tuple((x.group_dimension, x.sphere_dimension) for x in (a, b, c))
    if actual != required:
        return None
    return n, i, kind


def prop42_specialization_inference_rule(goal: TodaProp42ExactnessStatement) -> InferenceRule:
    """ProofStep matcher checks the exact universal premise and valid index arithmetic."""
    if prop42_exactness_indices(goal) is None:
        raise ValueError("not a valid Proposition 4.2 EHP exactness window")

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].conclusion == TodaProp42GeneralExactnessStatement()
            and prop42_exactness_indices(goal) is not None
        )

    def conclusion(premises):
        return goal

    return InferenceRule(
        name="Toda Proposition 4.2: generic consecutive EHP specialization",
        description="Specialize the cited universal EHP exact sequence to two consecutive maps.",
        premise_patterns=(PremisePattern(statement_type=TodaProp42GeneralExactnessStatement),),
        match_guard=guard,
        conclusion_builder=conclusion,
    )


def expand_cited_prop42_exactness(
    goal: object, available: tuple[object, ...]
) -> tuple[GoalExpansion, ...]:
    """Only screened general-schema witnesses can be used as premises."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    source = TodaProp42GeneralExactnessStatement()
    if source not in available or prop42_exactness_indices(goal) is None:
        return ()
    return (GoalExpansion(prop42_specialization_inference_rule(goal), (source,)),)


def build_prop42_specialization_provider(bridge: RegistryBridgeResult):
    """Bind specialization solely to the already screened GIVEN proof links."""
    available = tuple(
        link.step.conclusion for link in bridge.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == bridge.registry.assertion(link.assertion_id).content
        and bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and link.step.conclusion == TodaProp42GeneralExactnessStatement()
    )
    def expand(goal):
        return expand_cited_prop42_exactness(goal, available)
    return expand


def prefer_universal_prop42_derivation(bridge: RegistryBridgeResult) -> RegistryBridgeResult:
    """Prefer the screened universal Proposition 4.2 over older concrete GIVENs.

    Retain the reference registry untouched. Use this after citation and proof-use
    screening, so the universal source cannot bypass a denied citation. If the
    universal source is absent, retain all previously available concrete leaves.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    approved = any(
        link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == TodaProp42GeneralExactnessStatement()
        and bridge.registry.assertion(link.assertion_id).content == link.step.conclusion
        and bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        for link in bridge.proof_links
    )
    if not approved:
        return bridge
    kept = tuple(
        link for link in bridge.proof_links
        if not (
            link.step is not None
            and link.step.rule is ProofRule.GIVEN
            and isinstance(link.step.conclusion, TodaProp42ExactnessStatement)
            and prop42_exactness_indices(link.step.conclusion) is not None
        )
    )
    return RegistryBridgeResult(bridge.registry, bridge.records, kept)
