"""General prior-domain discovery for the existing finite-cyclic zero-image rules."""
from __future__ import annotations

from homotopy_groups import TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step
from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import expand_adopted_prior_zero_image
from phase175_r4r14r9_literature_zero_image.rule import expand_literature_zero_image


def build_prior_zero_image_provider(*, bridge, proof_target):
    """Propose the existing two-premise inference without stable-family preconditions.

    The prior's presentation selects a goal; only the ordinary resolver may
    accept the source ProofStep. A linked literature route retains priority.
    Neither the generator image nor the final zero map is assumed here.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError('typed registry bridge required')

    def expand(goal):
        if type(goal) is not ImageZeroStatement or type(goal.map) is not TodaSuspensionMap:
            return ()
        prior = admitted_prior_group_step(goal.map.source_group,
                                          proof_target=proof_target, bridge=bridge)
        if prior is None:
            return ()
        presentation = prior.conclusion
        literature = expand_literature_zero_image(goal, presentation,
                        proof_target=proof_target, bridge=bridge)
        if literature:
            return literature
        return expand_adopted_prior_zero_image(goal, presentation,
                        proof_target=proof_target, bridge=bridge)

    return expand
