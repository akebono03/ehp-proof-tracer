"""Source-first shared provider for the generic signed eta-torsion normalization.

A cited (5.8) source generates only a possible intermediate signed target.
Its R4R10 / Proposition 2.5 ProofStep, eta-family definition, and the actual
order-zero ProofStep remain mandatory search goals.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, MapApplication
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase175_r4r10_cited_58_prop25_public.provider import screened_cited_facts
from phase175_r4r10_cited_58_prop25_public.source import (
    CitedToda58SignedDelta, canonical_toda58,
)
from phase175_r4r11_signed_eta_torsion_public.rule import (
    expand_signed_eta_two_torsion,
)
from proof import Relation
from toda_rules import TodaDeltaImageUpToSignStatement


def build_signed_eta_torsion_provider(bridge: RegistryBridgeResult):
    """Build only legitimate backward proposals from an exact screened source."""
    available = screened_cited_facts(bridge)
    pinned = canonical_toda58()
    candidates = tuple(
        claim.statement for claim in available
        if type(claim) is CitedToda58SignedDelta
        and claim.locator == "(5.8)"
        and claim.statement == pinned
    )

    def expand(goal: object):
        if (not isinstance(goal, Relation)
                or not isinstance(goal.lhs, MapApplication)
                or not isinstance(goal.rhs, Composition)
                or not isinstance(goal.rhs.right, HomotopyElement)
                or not isinstance(goal.lhs.expression, HomotopyElement)):
            return ()
        beta = goal.rhs.right
        gamma = goal.lhs.expression
        proposals = []
        for source in candidates:
            source_value = source.positive_value
            if source_value is None:
                continue
            signed = TodaDeltaImageUpToSignStatement(
                map=TodaDeltaMap(
                    TodaPrimaryGroup(gamma.source, gamma.target),
                    TodaPrimaryGroup(beta.source, source_value.left.expression.target),
                ),
                element=gamma,
                positive_value=Composition(source_value, beta),
            )
            proposals.append(signed)
        return expand_signed_eta_two_torsion(goal, tuple(proposals))

    return expand
