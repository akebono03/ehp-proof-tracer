"""Prepare a source-certified Toda (5.6) zero-group root for standard search.

The guard is derived from typed group contents and source identities, not from
an enumerated list of stems. No target conclusion is ever a GIVEN leaf.
"""
from __future__ import annotations

from pathlib import Path

from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase173_r4_r10_general_toda56_core.core import (
    checked_general_inputs,
    expand_general_toda56,
)
from phase173_r4_r11_zero_public_connection.source import (
    screened_zero_toda56_context,
)
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    expand_cited_lemma54_hopf,
)
from proof import ProofRule
from unified_statement_registry import AssertionOrigin


def prepare_zero_toda56_public_connection(
    *, bridge: object, goal: object,
) -> tuple[object, object] | None:
    """Return a screened context and proof provider, not a completed proof."""
    if not isinstance(goal, TodaPrimaryGroupZeroStatement):
        return None
    if checked_general_inputs(goal) is None:
        return None
    root = Path(__file__).resolve().parents[1]
    chapter = (root / "sources" / "toda" / "Toda_05_2.tex").read_text(
        encoding="utf-8-sig",
    )
    screened = screened_zero_toda56_context(bridge, goal=goal, chapter=chapter)
    if screened is None:
        return None
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
    )
    if (sum(type(item) is TodaProp44UniversalStatement for item in available) != 1
            or sum(type(item) is TodaLemma54TypedSource for item in available) != 1):
        return None
    if len(expand_general_toda56(
        goal, available, proof_target=goal, bridge=screened,
    )) != 1:
        return None

    def verified_extensions(statement: object):
        hopf = expand_cited_lemma54_hopf(statement, available)
        if hopf:
            return hopf
        return expand_general_toda56(
            statement, available, proof_target=goal, bridge=screened,
        )

    provider = shared_expansion_provider(
        screened, extra_providers=(verified_extensions,), proof_target=goal,
        prior_conclusions=(),
    )
    return screened, provider
