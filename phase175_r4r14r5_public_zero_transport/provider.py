"""Public backward proposals for proved composite-image-zero transport.

Only the cited general law that passed the existing R41 screening may select
an unproved composition-zero obligation. No root-group fact or proof leaf is
created by this provider; the shared DFS must prove both parent goals.
"""
from __future__ import annotations

from typing import Callable

from expression import Composition, Zero
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
    canonical_annihilator_instance,
)
from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import (
    lifted_stable_composition,
    valid_suspension,
)
from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
    screened_general_law,
)
from phase175_r4r14r4_general_zero_transport.rule import (
    expand_proved_composite_zero_image,
)
from proof import Relation, RelationType

PROVIDER_ID = "phase175.r4r14r5.cited_composite_zero_transport"


def build_public_composite_zero_transport_provider(
    bridge: RegistryBridgeResult,
) -> Callable[[object], tuple[GoalExpansion, ...]]:
    """Offer the generic two-premise rule only for a screened cited zero law.

    This works for any typed stable composite whose *entire* lifted value
    matches a cited annihilator. Longer composites can also use this rule
    after independently proved reassociation; no factor-count restriction
    is introduced here.
    """
    laws = screened_general_law(bridge)

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        if (len(laws) != 1
                or not isinstance(goal, GeneratorImage)
                or not valid_suspension(goal.map)
                or not isinstance(goal.target_generator, Zero)):
            return ()
        lifted = lifted_stable_composition(goal.source_generator)
        if not isinstance(lifted, Composition):
            return ()
        mapping = goal.map
        from phase169_r10eq_r1_universal_stable_definition.definition import (
            typed_element_span,
        )
        if typed_element_span(goal.source_generator) != (
            mapping.source_group.group_dimension,
            mapping.source_group.sphere_dimension,
        ):
            return ()
        if typed_element_span(lifted) != (
            mapping.target_group.group_dimension,
            mapping.target_group.sphere_dimension,
        ):
            return ()
        from phase174_r3_r7_r9_composition_associativity.rule import (
            typed_composition_factors,
        )
        factors = typed_composition_factors(lifted)
        if not factors:
            return ()
        cited_relation = canonical_annihilator_instance(laws[0], factors[0].dimension)
        if cited_relation != Relation(lifted, Zero(), RelationType.EQUALITY):
            return ()
        image = GeneratorImage(mapping, goal.source_generator, lifted)
        return expand_proved_composite_zero_image(goal, image)

    return expand
