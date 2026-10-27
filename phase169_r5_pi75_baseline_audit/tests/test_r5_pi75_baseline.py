"""Phase 169 R5: non-mutating mathematical boundary tests for pi7^5."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule
from phase165_r52_partial_proof import ProofSearchStatus
from phase169_r3o_stable_composite_rule import expand_cited_toda45_composite_transport
from phase165_r52_r27_r5_literature import _toda45_universal_statement
from phase169_r5_pi75_baseline_audit.audit import _format_report


def test_r5_structured_goal_dimensions_and_stable_boundary():
    lower = database_structured_group_goal_candidates(n=4, k=2)
    higher = database_structured_group_goal_candidates(n=5, k=2)
    assert len(lower) == len(higher) == 1
    assert lower[0].lhs == TodaPrimaryGroup(6, 4)
    assert higher[0].lhs == TodaPrimaryGroup(7, 5)
    assert 4 >= 2 + 2
    assert not (3 >= 2 + 2)


def test_r5_toda45_candidate_depends_on_three_unproved_subgoals():
    lower = database_structured_group_goal_candidates(n=4, k=2)[0]
    higher = database_structured_group_goal_candidates(n=5, k=2)[0]
    candidates = expand_cited_toda45_composite_transport(
        higher, (lower, _toda45_universal_statement()),
    )
    assert len(candidates) == 1
    assert len(candidates[0].subgoals) == 3
    assert candidates[0].subgoals[0] == lower
    assert candidates[0].subgoals[1].map.source_group == lower.lhs
    assert candidates[0].subgoals[1].map.target_group == higher.lhs
    assert candidates[0].subgoals[2].source_generator == lower.rhs.generator
    assert candidates[0].subgoals[2].target_generator == higher.rhs.generator


def test_r5_registered_goal_is_not_self_cited_after_screening():
    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=5, k=2)
    assert len(candidates) == 1
    target = candidates[0]
    assert target.lhs == TodaPrimaryGroup(7, 5)
    citing = resolve_specialized_goal_citing_id(bridge, target)
    if citing is not None:
        screened = screen_shared_proof_context(
            bridge, goal=target, citing_assertion_id=citing,
            explicit_publication_target=True,
        )
        assert all(link.step is None or link.step.rule is not ProofRule.GIVEN
                   or link.step.conclusion != target
                   for link in screened.proof_links)


def test_r5_report_does_not_promote_partial_to_complete():
    report = {
        "git_head": "fixture", "candidate_count": 1, "lower_goal_count": 1,
        "toda45_stable_range_n4_k2": True,
        "screened_lower_relation_available": False,
        "screened_toda45_available": True,
        "cited_toda45_root_options": 0,
        "search_status": ProofSearchStatus.PARTIAL.value, "proof_steps": 1,
        "open_goals": ["unproved"], "proof_tree_verified": False,
        "web_key": "generic-partial-proof", "root_expansion_rule_names": [],
        "citations": [], "verification_error": None, "web_error": None,
    }
    narrative = _format_report(report)
    assert "`partial`" in narrative
    assert "unproved" in narrative
    assert "complete" not in narrative.split("## 未解決 Goal")[0]
