"""Cited, root-scoped public connection of R40's verified adopted-DB rule.

No DB result is converted to an independent literature theorem. The R38
source-bound chain remains the prerequisite selector, and the R40 rule
re-checks prior admission at every actual inference match.
"""
from __future__ import annotations

from typing import Callable

from homotopy_groups import TodaPrimaryGroup
from map_property_rules import ImageZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e4_ordered_db_prior.db_prior import group_coordinates
from phase174_r3_r7_r12_toda59_annihilator_source.source import (
    CitedFamilyAnnihilator,
    reviewed_toda59_annihilator_schema,
)
from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import (
    expand_source_bound_zero_image_chain,
)
from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import (
    expand_adopted_prior_zero_image,
)
from proof import ProofRule, ProofStep
from unified_statement_registry import AssertionOrigin

PROVIDER_ID = "phase174.r3.r7.r41.cited_adopted_db_zero_image"
SOURCE_LOCATOR = "(5.9)"


def screened_general_law(bridge: RegistryBridgeResult) -> tuple[CitedFamilyAnnihilator, ...]:
    """Require the actual fixed-source, citation-linked Toda (5.9) GIVEN."""
    if not isinstance(bridge, RegistryBridgeResult):
        return ()
    expected = reviewed_toda59_annihilator_schema()
    laws = []
    for link in bridge.proof_links:
        step = link.step
        if (not isinstance(step, ProofStep)
                or step.rule is not ProofRule.GIVEN
                or step.premises
                or type(step.conclusion) is not CitedFamilyAnnihilator
                or step.conclusion != expected):
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        reference = bridge.registry.reference(assertion.reference_id)
        cited = getattr(getattr(step, "inference_rule", None), "literature_reference", None)
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or assertion.content != step.conclusion
                or reference.locator != SOURCE_LOCATOR
                or type(reference.publication_position) is not int
                or reference.publication_position < 1
                or cited is None or cited.locator != SOURCE_LOCATOR):
            continue
        laws.append(step.conclusion)
    return tuple(laws) if len(laws) == 1 else ()


def build_public_adopted_zero_image_provider(
    *, bridge: RegistryBridgeResult, proof_target: object,
) -> Callable[[object], tuple[GoalExpansion, ...]]:
    """Return an inert provider unless the root and the source are legitimate.

    Never use a database result to select a final root. Only the caller's
    independently specified group proof root controls the prior-order check.
    """
    lawful = (isinstance(bridge, RegistryBridgeResult)
              and group_coordinates(proof_target) is not None)
    sources = screened_general_law(bridge) if lawful else ()

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        if not sources or not isinstance(goal, ImageZeroStatement):
            return ()
        mapping = goal.map
        if (not isinstance(getattr(mapping, "source_group", None), TodaPrimaryGroup)
                or not isinstance(getattr(mapping, "target_group", None), TodaPrimaryGroup)):
            return ()
        # Source-first: R38 must independently propose this exact typed
        # cyclic presentation and generator-image goal from the cited law.
        screened = expand_source_bound_zero_image_chain(goal, sources)
        if len(screened) != 1 or len(screened[0].subgoals) != 2:
            return ()
        presentation, zero_generator = screened[0].subgoals
        proposed = expand_adopted_prior_zero_image(
            goal, presentation, proof_target=proof_target, bridge=bridge,
        )
        if (len(proposed) != 1
                or proposed[0].subgoals != (presentation, zero_generator)):
            return ()
        return proposed

    return expand
