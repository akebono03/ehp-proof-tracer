"""Conditioned Proposition 4.4: independent Lemma 5.4 and earlier splitting."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
)
from phase174_r3_r6_r2_prop44_lemma54.source import (
    TodaPreProp44SplittingStatement,
    attach_earlier_verified_lemma54,
    expand_cited_preprop44_splitting,
)
from proof import ProofRule


def _goal(n: int = 3, k: int = 2) -> MapInjective:
    return MapInjective(TodaSuspensionMap(
        TodaPrimaryGroup(n + k, n), TodaPrimaryGroup(n + k + 1, n + 1),
    ))


def test_r4b_source_bound_dim4_has_two_real_premises():
    proposition = TodaProp44UniversalStatement()
    lemma = TodaLemma54TypedSource()
    proposals = expand_cited_prop44_injectivity(_goal(), (proposition, lemma))
    assert len(proposals) == 1
    assert proposals[0].subgoals == (proposition, canonical_hopf_relation())
    assert proposals[0].rule.literature_reference.locator == "Proposition 4.4"


def test_r4b_no_unverified_hopf_or_tampered_source():
    proposition = TodaProp44UniversalStatement()
    lemma = TodaLemma54TypedSource()
    assert expand_cited_prop44_injectivity(_goal(), ()) == ()
    assert expand_cited_prop44_injectivity(_goal(), (proposition,)) == ()
    assert expand_cited_prop44_injectivity(_goal(), (proposition, proposition, lemma)) == ()
    fake = replace(proposition, includes_suspension_injectivity=False)
    assert expand_cited_prop44_injectivity(_goal(), (fake, lemma)) == ()


def test_r4b_unrelated_dimensions_and_bad_map_are_rejected():
    citations = (TodaProp44UniversalStatement(), TodaLemma54TypedSource())
    assert expand_cited_prop44_injectivity(_goal(n=4), citations) == ()
    invalid = MapInjective(TodaSuspensionMap(TodaPrimaryGroup(5, 3), TodaPrimaryGroup(7, 4)))
    assert expand_cited_prop44_injectivity(invalid, citations) == ()


def test_r4b_live_screened_lemma54_hopf_inference():
    bridge = build_shared_typed_bridge()
    candidate, = registered_group_goal_candidates(bridge, n=5, k=3)
    citing = resolve_specialized_goal_citing_id(bridge, candidate)
    assert citing is not None
    bridge = attach_earlier_verified_lemma54(bridge, citing)
    screened = screen_shared_proof_context(
        bridge, goal=candidate, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    provider = shared_expansion_provider(screened, proof_target=candidate)
    wanted = _goal()
    proof = reconstruct_registered_goal(
        wanted, screened, citing, provider, lookup_mode="typed_reference",
    )
    assert proof.rule is ProofRule.INFERENCE
    assert proof.conclusion == wanted
    assert len(proof.premises) == 2
    assert proof.premises[0].rule is ProofRule.GIVEN
    assert proof.premises[0].conclusion == TodaProp44UniversalStatement()
    assert proof.premises[1].rule is ProofRule.INFERENCE
    assert proof.premises[1].conclusion == canonical_hopf_relation()
    assert len(proof.premises[1].premises) == 1
    assert proof.premises[1].premises[0].conclusion == TodaLemma54TypedSource()


def test_r4b_earlier_group_still_uses_printed_splitting():
    bridge = build_shared_typed_bridge()
    candidate, = registered_group_goal_candidates(bridge, n=4, k=2)
    citing = resolve_specialized_goal_citing_id(bridge, candidate)
    assert citing is not None
    assert attach_earlier_verified_lemma54(bridge, citing) is bridge
    screened = screen_shared_proof_context(
        bridge, goal=candidate, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    available = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    assert available.count(TodaPreProp44SplittingStatement()) == 1
    assert available.count(TodaLemma54TypedSource()) == 0
    assert len(expand_cited_preprop44_splitting(_goal(), available)) == 1
    assert expand_cited_prop44_injectivity(_goal(), available) == ()


def test_r4b_prelude_precedes_proposition_without_hopf_invariant_assumption():
    root = Path(__file__).resolve().parents[2]
    text = (root / "sources/toda/Toda_04_2.tex").read_text(encoding="utf-8")
    paragraph = text.split(r"\begin{proposition}\label{prop:4.4}", 1)[0]
    assert "$n=2,4,8$ のとき, Hopf fibration" in paragraph
    assert r"E+h_*:" in paragraph
    assert not hasattr(TodaProp44UniversalStatement(), "preceding_hopf_fibration_dimensions")
