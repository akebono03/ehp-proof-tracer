"""Connect the three separately certified source-first Toda (5.6) roots to public search.

Only exact registered (n,k)=(4,4),(4,5),(4,6) goals are eligible.
The source screen and all inference guards are unchanged.  In particular,
this module never promotes a requested group, an archive, or a raw database
row into an independent mathematical theorem.
"""
from __future__ import annotations

from pathlib import Path

from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    expand_cited_lemma54_hopf,
)
from phase173_r4_r7_source_first_rule.rule import (
    checked_inputs,
    expand_source_first_toda56,
)
from phase173_r4_r7_source_first_rule.source import screened_source_first_context
from proof import ProofRule
from unified_statement_registry import AssertionOrigin


def prepare_pi4_higher_public_connection(
    *, bridge: object, goal: object, prior_conclusions: tuple,
) -> tuple[object, object] | None:
    """Prepare only vetted sources and a bounded backward expansion provider.

    Return (screened_context, provider) or decline without mutating the bridge.
    No target citation position is ever fabricated.  The pi_8^4 context keeps
    its reviewed suppression of a same-Proposition-5.8 direct prior leaf.
    """
    if not isinstance(prior_conclusions, tuple):
        return None
    if checked_inputs(goal) is None:
        return None
    root = Path(__file__).resolve().parents[1]
    chapter = (root / "sources" / "toda" / "Toda_05_2.tex").read_text(
        encoding="utf-8-sig",
    )
    screened = screened_source_first_context(bridge, goal=goal, chapter=chapter)
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
    if len(expand_source_first_toda56(
        goal, available, proof_target=goal, bridge=screened,
    )) != 1:
        return None

    def verified_extensions(statement: object):
        hopf = expand_cited_lemma54_hopf(statement, available)
        if hopf:
            return hopf
        return expand_source_first_toda56(
            statement, available, proof_target=goal, bridge=screened,
        )

    provider = shared_expansion_provider(
        screened, extra_providers=(verified_extensions,),
        proof_target=goal, prior_conclusions=prior_conclusions,
    )
    return screened, provider
