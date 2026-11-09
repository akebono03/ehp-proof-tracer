"""Source-bound Proposition 2.7 provider for the canonical backward search.

R29 intentionally does not register this provider in the ordinary Web route.
The checked universal literature leaf is the sole GIVEN in the isolated bridge;
every specialized result is produced by the canonical inference engine.
"""
from __future__ import annotations

from pathlib import Path

from phase165_r3_recursive_search import GoalExpansion, reconstruct_registered_goal
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r6_2_unified_registry_r3_r3.provider_registry import (
    UnifiedExpansionProviderRegistry,
)
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27GeneralTheoremPremise, Prop27TypedHopfDeltaStatement,
    prop27_typed_specialization_rule, typed_specialization,
)
from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
    ASSERTION_ID, Prop27UniversalLiteratureStatement,
    prop27_literature_to_premise_rule, register_universal_prop27,
)
from proof import ProofRule, ProofStep
from unified_statement_registry import AssertionOrigin

PROVIDER_ID = "phase174.r3.r7.r29.toda_prop27_source_bound_specialization"


def expand_cited_prop27_goal(goal: object) -> tuple[GoalExpansion, ...]:
    """Suggest two general source-bound rules; never create a proof step.

    The concrete n is read from the typed requested goal, not a hard-coded
    special case. Invalid domains and forged typed statements offer no rule.
    """
    if type(goal) is Prop27GeneralTheoremPremise:
        if goal != Prop27GeneralTheoremPremise():
            return ()
        return (GoalExpansion(
            prop27_literature_to_premise_rule(),
            (Prop27UniversalLiteratureStatement(),),
        ),)
    if type(goal) is Prop27TypedHopfDeltaStatement:
        try:
            if typed_specialization(goal.n) != goal:
                return ()
            rule = prop27_typed_specialization_rule(goal.n)
        except (ValueError, TypeError):
            return ()
        return (GoalExpansion(rule, (Prop27GeneralTheoremPremise(),)),)
    return ()


def build_canonical_prop27_context(root: Path):
    """Reuse the shared typed registry merger and common provider registry."""
    if not isinstance(root, Path):
        raise TypeError("root must be pathlib.Path")
    literature = register_universal_prop27(root)
    bridge = build_shared_typed_bridge(sources=(literature,))
    matches = tuple(
        assertion for assertion in bridge.registry._assertions.values()
        if assertion.origin is AssertionOrigin.FIXED_STATEMENT
        and type(assertion.content) is Prop27UniversalLiteratureStatement
    )
    if len(matches) != 1 or matches[0].assertion_id != "shared:0:" + ASSERTION_ID:
        raise RuntimeError("shared literature registration is not unique")
    links = tuple(link for link in bridge.proof_links
                  if link.assertion_id == matches[0].assertion_id)
    if (len(links) != 1 or not isinstance(links[0].step, ProofStep)
            or links[0].step.rule is not ProofRule.GIVEN
            or links[0].step.conclusion != matches[0].content):
        raise RuntimeError("typed source ProofStepLink is absent or invalid")
    providers = UnifiedExpansionProviderRegistry()
    providers.register(
        PROVIDER_ID, expand_cited_prop27_goal, origin="SHARED_CITED_CONTEXT",
    )
    return bridge, providers


def search_canonical_prop27_instance(root: Path, n: int) -> ProofStep:
    """Run the actual shared backward-proof engine on the cited typed instance."""
    target = typed_specialization(n)
    bridge, providers = build_canonical_prop27_context(root)
    return reconstruct_registered_goal(
        target, bridge, "shared:0:" + ASSERTION_ID,
        providers.providers()[0], lookup_mode="typed_reference",
    )
