"""Public literature-linked finite-cyclic zero-image proposal provider."""
from __future__ import annotations

from typing import Callable

from map_property_rules import ImageZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import (
    expand_source_bound_zero_image_chain,
)
from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
    screened_general_law,
)
from phase175_r4r14r9_literature_zero_image.rule import (
    expand_literature_zero_image,
)

PROVIDER_ID = "phase175.r4r14r9.linked_literature_cyclic_zero_image"


def build_literature_zero_image_provider(
    *, bridge: RegistryBridgeResult, proof_target: object,
) -> Callable[[object], tuple[GoalExpansion, ...]]:
    """Reuse source-screened candidate selection without adopting its DB witness."""
    cited_laws = screened_general_law(bridge)

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        if not cited_laws or not isinstance(goal, ImageZeroStatement):
            return ()
        candidates = expand_source_bound_zero_image_chain(goal, cited_laws)
        if len(candidates) != 1 or len(candidates[0].subgoals) != 2:
            return ()
        presentation, generator_zero = candidates[0].subgoals
        expansions = expand_literature_zero_image(
            goal, presentation, proof_target=proof_target, bridge=bridge,
        )
        if len(expansions) != 1 or expansions[0].subgoals != (presentation, generator_zero):
            return ()
        return expansions

    return expand
