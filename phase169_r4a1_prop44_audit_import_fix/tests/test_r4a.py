"""Focused R4A source and typed-provider tests; no production modifications."""
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r12_r12_ehp_consequences import expand_ehp_exactness_consequences
from phase165_r12_r15_toda51 import expand_cited_toda51_zero
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement, _toda45_universal_statement
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3o_stable_composite_rule import expand_cited_toda45_composite_transport
from proof import ProofRule


def test_r4a_original_prop53_explicitly_uses_prop44_injectivity():
    root = Path(__file__).resolve().parents[2]
    chapter = (root / "sources" / "toda" / "Toda_05_2.tex").read_text(encoding="utf-8")
    start = chapter.index(r"\begin{proposition}\label{prop:5.3}")
    end = chapter.index(r"\qed", start)
    proof = chapter[start:end]
    assert "Prop4.4" in proof
    assert r"\pi_5^3\xrightarrow{E}\pi_6^4" in proof
    assert r"\pit{6}{7}=0" in proof


def test_r4a_prop44_is_prior_and_screened_with_no_self_given():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=4, k=2)
    assert len(goals) == 1
    citing = resolve_specialized_goal_citing_id(bridge, goals[0])
    assert citing is not None
    prior = [a for a in bridge.registry._assertions.values()
             if type(a.content) is TodaProp44UniversalStatement]
    assert len(prior) == 1
    assert precedes_citing_assertion(bridge, prior[0].assertion_id, citing)
    screened = screen_shared_proof_context(
        bridge, goal=goals[0], citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    source_ids = {link.assertion_id for link in screened.proof_links}
    assert prior[0].assertion_id in source_ids
    assert citing not in source_ids


def test_r4a_pi67_zero_and_ehp_surjectivity_are_real_goals_not_proofs():
    bridge = build_shared_typed_bridge()
    goal = registered_group_goal_candidates(bridge, n=4, k=2)[0]
    citing = resolve_specialized_goal_citing_id(bridge, goal)
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    claims = tuple(link.step.conclusion for link in screened.proof_links
                   if link.step is not None and link.step.rule is ProofRule.GIVEN)
    zero = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(6, 7))
    assert len(expand_cited_toda51_zero(zero, claims)) == 1
    source = TodaPrimaryGroup(5, 3)
    target = TodaPrimaryGroup(6, 4)
    options = expand_ehp_exactness_consequences(MapSurjective(TodaSuspensionMap(source, target)))
    assert len(options) == 1
    assert options[0].subgoals[1] == zero


def test_r4a_toda45_out_of_range_remains_rejected():
    bridge = build_shared_typed_bridge()
    lower = registered_group_goal_candidates(bridge, n=3, k=2)
    higher = registered_group_goal_candidates(bridge, n=4, k=2)
    assert len(lower) == len(higher) == 1
    assert expand_cited_toda45_composite_transport(
        higher[0], (lower[0], _toda45_universal_statement()),
    ) == ()
