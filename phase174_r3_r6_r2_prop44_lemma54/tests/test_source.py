"""Source-checking and typed conditional-Proposition-4.4 proof tests."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_37c_reference_projection import project_reference_bodies
from phase169_r4b_prop44_injectivity.rule import (
    expand_cited_prop44_injectivity,
    prop44_hopf_four_injectivity_rule,
)
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
)
from phase174_r3_r6_r2_prop44_lemma54.source import (
    PRELUDE_ASSERTION_ID,
    PRELUDE_LOCATOR,
    TodaPreProp44SplittingStatement,
    attach_earlier_verified_lemma54,
    build_cited_preprop44_splitting,
    expand_cited_preprop44_splitting,
    verify_prelude_source,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule


def _injection() -> MapInjective:
    return MapInjective(TodaSuspensionMap(
        TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4),
    ))


def test_preprop44_is_an_independent_sourced_remark() -> None:
    assert verify_prelude_source() == 7250
    bridge = build_cited_preprop44_splitting()
    assert tuple(bridge.registry._assertions) == (PRELUDE_ASSERTION_ID,)
    assert len(bridge.proof_links) == 1
    claim = bridge.proof_links[0].step
    assert claim is not None
    assert claim.rule is ProofRule.GIVEN
    assert claim.conclusion == TodaPreProp44SplittingStatement()
    refs = project_reference_bodies(bridge.registry, (PRELUDE_ASSERTION_ID,))
    assert len(refs) == 1
    assert "E+h_*" in refs[0]
    assert "H(h)" not in refs[0]


def test_wrong_source_paragraph_is_refused(tmp_path: Path) -> None:
    original = Path(__file__).resolve().parents[2]
    manuscript = original / "sources/toda/Toda_04_2.tex"
    updated = tmp_path / "sources/toda/Toda_04_2.tex"
    updated.parent.mkdir(parents=True, exist_ok=True)
    updated.write_bytes(manuscript.read_bytes().replace(
        b"Hopf fibration", b"unverified fibration", 1,
    ))
    with pytest.raises(ValueError, match="unverified Toda Chapter IV"):
        verify_prelude_source(root=tmp_path)


def test_conditioned_prop44_refuses_missing_lemma() -> None:
    prop44 = TodaProp44UniversalStatement()
    lemma = TodaLemma54TypedSource()
    assert not hasattr(prop44, "preceding_hopf_fibration_dimensions")
    assert expand_cited_prop44_injectivity(_injection(), (prop44,)) == ()
    proposals = expand_cited_prop44_injectivity(_injection(), (prop44, lemma))
    assert len(proposals) == 1
    assert proposals[0].subgoals == (prop44, canonical_hopf_relation())
    assert expand_cited_prop44_injectivity(_injection(), (prop44, lemma, lemma)) == ()
    bad = replace(prop44, includes_suspension_injectivity=False)
    assert expand_cited_prop44_injectivity(_injection(), (bad, lemma)) == ()


def test_prop44_guard_requires_actual_lemma54_given_ancestor() -> None:
    rule = prop44_hopf_four_injectivity_rule(_injection())
    given_prop = ProofStep(TodaProp44UniversalStatement(), (), ProofRule.GIVEN)
    given_lemma = ProofStep(TodaLemma54TypedSource(), (), ProofRule.GIVEN)
    inferred_hopf = ProofStep(canonical_hopf_relation(), (given_lemma,), ProofRule.INFERENCE)
    good = find_inference_matches_for_rule(rule, (given_prop, inferred_hopf))
    assert len(good) == 1
    assert find_inference_matches_for_rule(rule, (
        given_prop, ProofStep(canonical_hopf_relation(), (), ProofRule.INFERENCE),
    )) == ()
    assert find_inference_matches_for_rule(rule, (
        given_prop, ProofStep(canonical_hopf_relation(), (), ProofRule.GIVEN),
    )) == ()
    assert find_inference_matches_for_rule(rule, (
        given_prop, ProofStep(canonical_hopf_relation(), (
            ProofStep(TodaPreProp44SplittingStatement(), (), ProofRule.GIVEN),
        ), ProofRule.INFERENCE),
    )) == ()


def test_preprop44_rule_is_sourced_only_when_later_lemma_unavailable() -> None:
    older = TodaPreProp44SplittingStatement()
    assert len(expand_cited_preprop44_splitting(_injection(), (older,))) == 1
    assert expand_cited_preprop44_splitting(_injection(), ()) == ()
    assert expand_cited_preprop44_splitting(_injection(), (
        older, TodaLemma54TypedSource(),
    )) == ()


def test_live_public_pi85_injection_requires_lemma54() -> None:
    bridge = build_shared_typed_bridge()
    target, = registered_group_goal_candidates(bridge, n=5, k=3)
    citing = resolve_specialized_goal_citing_id(bridge, target)
    assert citing is not None
    new_bridge = attach_earlier_verified_lemma54(bridge, citing)
    screened = screen_shared_proof_context(
        new_bridge, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    provider = shared_expansion_provider(screened, proof_target=target)
    assert len(expand_cited_prop44_injectivity(_injection(), (
        TodaProp44UniversalStatement(), TodaLemma54TypedSource(),
    ))) == 1
    actual = reconstruct_registered_goal(
        _injection(), screened, citing, provider, lookup_mode="typed_reference",
    )
    assert actual.rule is ProofRule.INFERENCE
    assert len(actual.premises) == 2
    assert actual.premises[1].conclusion == canonical_hopf_relation()
    assert actual.premises[1].premises[0].conclusion == TodaLemma54TypedSource()


def test_historical_hopf_paragraph_is_not_a_created_relation() -> None:
    source = Path(__file__).resolve().parents[2] / "phase168_r3_5_model_renderer.py"
    text = source.read_text(encoding="utf-8")
    assert r"$h:S^7\to S^4$ により" not in text
    assert "Do not invoke the later Lemma 5.4" not in text
    assert PRELUDE_LOCATOR != "Proposition 4.4"
