"""Scoped source-bound Proposition 4.4 proof tests."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity
from proof import ProofRule


def _goal(n: int = 3, k: int = 2) -> MapInjective:
    return MapInjective(TodaSuspensionMap(TodaPrimaryGroup(n + k, n), TodaPrimaryGroup(n + k + 1, n + 1)))


def test_r4b_source_bound_dim4_has_one_proposal():
    goal = _goal()
    proposal = expand_cited_prop44_injectivity(goal, (TodaProp44UniversalStatement(),))
    assert len(proposal) == 1
    assert proposal[0].subgoals == (TodaProp44UniversalStatement(),)
    assert proposal[0].rule.literature_reference.locator == "Proposition 4.4"


def test_r4b_no_unverified_source_or_tampered_claim():
    goal = _goal()
    assert expand_cited_prop44_injectivity(goal, ()) == ()
    assert expand_cited_prop44_injectivity(goal, (TodaProp44UniversalStatement(),) * 2) == ()
    fake = replace(TodaProp44UniversalStatement(), includes_suspension_injectivity=False)
    assert expand_cited_prop44_injectivity(goal, (fake,)) == ()


def test_r4b_no_unrelated_dimension_or_invalid_map():
    cited = (TodaProp44UniversalStatement(),)
    assert expand_cited_prop44_injectivity(_goal(n=4), cited) == ()
    incorrect = MapInjective(TodaSuspensionMap(TodaPrimaryGroup(5, 3), TodaPrimaryGroup(7, 4)))
    assert expand_cited_prop44_injectivity(incorrect, cited) == ()


def test_r4b_live_screened_context_creates_real_inference():
    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=4, k=2)
    assert len(candidates) == 1
    target = candidates[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    assert citing is not None
    screened = screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    provider = shared_expansion_provider(screened, proof_target=target)
    wanted = _goal()
    options = provider(wanted)
    assert any(option.rule.name == "Toda Proposition 4.4 Hopf dimension-four suspension injectivity"
               for option in options)
    proof = reconstruct_registered_goal(
        wanted, screened, citing,
        provider, lookup_mode="typed_reference",
    )
    assert proof.rule is ProofRule.INFERENCE
    assert proof.conclusion == wanted
    assert len(proof.premises) == 1
    assert proof.premises[0].rule is ProofRule.GIVEN
    assert proof.premises[0].conclusion == TodaProp44UniversalStatement()


def test_r4b_prior_pi53_and_source_literature_not_promoted_to_fact():
    bridge = build_shared_typed_bridge()
    target = registered_group_goal_candidates(bridge, n=4, k=2)[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    screened = screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    available = tuple(link.step.conclusion for link in screened.proof_links if link.step is not None
                      and link.step.rule is ProofRule.GIVEN)
    assert available.count(TodaProp44UniversalStatement()) == 1
    assert len(expand_cited_prop44_injectivity(_goal(), available)) == 1
    assert not any(item == _goal() for item in available)


def test_r4b_hopf_dimension_four_existence_occurs_before_prop44():
    root = Path(__file__).resolve().parents[2]
    source = (root / "sources" / "toda" / "Toda_04_2.tex").read_text(encoding="utf-8")
    head = source.split(r"\begin{proposition}\label{prop:4.4}", 1)[0]
    assert "n=2,4,8" in head
    assert r"S^n\hookrightarrow S^{2n-1}\xrightarrow{h} S^n" in head
