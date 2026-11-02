"""Connect the verified Toda (5.6) pi_7^4 route to ordinary typed search.

Only the exact registered (n,k)=(4,3) target is eligible. This module
never turns a database group goal, an archive row, or a Hopf equation into
an assumed mathematical proof.
"""
from __future__ import annotations

from pathlib import Path

from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase173_r4_r1_lemma54_source_bridge.source import (
    ADOPTED_ASSERTION_ID,
    TodaLemma54TypedSource,
    add_verified_lemma54_source,
    expand_cited_lemma54_hopf,
)
from phase173_r4_r1_source_bound_56.rule import expand_source_bound_toda56
from proof import ProofRule
from unified_statement_registry import AssertionOrigin


def prepare_pi74_public_connection(*, bridge, goal, citing_assertion_id,
                                   prior_conclusions: tuple):
    """Return a screened (bridge, citing ID, provider) or decline safely.

    Fixed source assertions must be checked before any new candidate is
    offered, and the ordinary backward engine still proves every subgoal.
    """
    candidates = registered_group_goal_candidates(bridge, n=4, k=3)
    if len(candidates) != 1 or candidates[0] != goal:
        return None
    exact_id = resolve_specialized_goal_citing_id(bridge, goal)
    if exact_id is None:
        return None
    if citing_assertion_id is not None and citing_assertion_id != exact_id:
        return None
    if ADOPTED_ASSERTION_ID in bridge.registry._assertions:
        # Do not silently trust an externally supplied, pre-adopted claim.
        return None
    root = Path(__file__).resolve().parents[1]
    chapter = (root / "sources" / "toda" / "Toda_05_2.tex").read_text(
        encoding="utf-8-sig",
    )
    augmented = add_verified_lemma54_source(
        bridge, citing_assertion_id=exact_id, chapter=chapter,
    )
    screened = prefer_universal_prop42_derivation(
        screen_shared_proof_context(
            augmented, goal=goal, citing_assertion_id=exact_id,
            explicit_publication_target=True,
        )
    )
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
    )
    if sum(type(item) is TodaLemma54TypedSource for item in available) != 1:
        return None
    if len(expand_source_bound_toda56(
        goal, available, screened, proof_target=goal,
    )) != 1:
        return None

    def verified_pi74_extensions(statement: object):
        hopf = expand_cited_lemma54_hopf(statement, available)
        if hopf:
            return hopf
        return expand_source_bound_toda56(
            statement, available, screened, proof_target=goal,
        )

    from phase165_r52_r9_shared_math import shared_expansion_provider
    provider = shared_expansion_provider(
        screened, extra_providers=(verified_pi74_extensions,),
        proof_target=goal, prior_conclusions=prior_conclusions,
    )
    return augmented, exact_id, provider
