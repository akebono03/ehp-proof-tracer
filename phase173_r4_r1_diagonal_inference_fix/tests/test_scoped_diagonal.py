"""Focused real-project tests for the certified Toda (5.1) diagonal route."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r3_recursive_search import (
    SourceBoundGoal, reconstruct_registered_goal,
)
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import (
    build_shared_typed_bridge, search_shared_group_goal, shared_expansion_provider,
)
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r57_r20_general_specialization import expand_cited_general_specialization
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource, add_verified_lemma54_source,
    expand_cited_lemma54_hopf,
)
from phase173_r4_r1_source_bound_56.rule import expand_source_bound_toda56
from proof import ProofRule
from unified_statement_registry import AssertionOrigin


@pytest.fixture(scope='module')
def screened_context():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=4, k=3)
    assert len(goals) == 1
    goal = goals[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    assert citing_id is not None
    chapter = (Path(__file__).resolve().parents[2] / 'sources/toda/Toda_05_2.tex').read_text(encoding='utf-8-sig')
    augmented = add_verified_lemma54_source(
        bridge, citing_assertion_id=citing_id, chapter=chapter,
    )
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        augmented, goal=goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    ))
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
    )
    assert sum(isinstance(x, TodaLemma54TypedSource) for x in available) == 1
    return augmented, screened, goal, citing_id, available


def test_diagonal_uses_only_cited_toda51_scalar_inference(screened_context) -> None:
    augmented, screened, goal, citing_id, available = screened_context
    roots = expand_source_bound_toda56(goal, available, screened, proof_target=goal)
    assert len(roots) == 1
    diagonal = roots[0].subgoals[2]
    assert isinstance(diagonal, SourceBoundGoal)
    assert diagonal.conclusion == registered_group_goal_candidates(augmented, n=7, k=0)[0]
    assert len(expand_cited_general_specialization(diagonal.conclusion, available)) == 1
    routes = expand_cited_general_specialization(diagonal.conclusion, available)
    assert routes[0].subgoals == (diagonal.source,)


def test_diagonal_subgoal_is_inference_not_database_given(screened_context) -> None:
    augmented, screened, goal, citing_id, available = screened_context
    diagonal = expand_source_bound_toda56(goal, available, screened, proof_target=goal)[0].subgoals[2]
    provider = shared_expansion_provider(screened, proof_target=goal)
    inferred = reconstruct_registered_goal(
        diagonal, screened, citing_id, provider,
        lookup_mode='typed_reference_publication',
    )
    assert inferred.rule is ProofRule.INFERENCE
    assert inferred.conclusion == diagonal.conclusion
    assert len(inferred.premises) == 1
    assert inferred.premises[0].conclusion == diagonal.source
    assert inferred.premises[0].rule is ProofRule.GIVEN


def test_complete_source_bound_pi74_root(screened_context) -> None:
    augmented, screened, goal, citing_id, available = screened_context

    def extra(statement: object):
        hopf = expand_cited_lemma54_hopf(statement, available)
        if hopf:
            return hopf
        return expand_source_bound_toda56(
            statement, available, screened, proof_target=goal,
        )

    provider = shared_expansion_provider(
        screened, extra_providers=(extra,), proof_target=goal,
    )
    result = search_shared_group_goal(
        n=4, k=3, group_structure=goal.rhs,
        bridge=augmented, citing_assertion_id=citing_id,
        expansion_provider=provider,
    )
    assert result.status.value == 'complete', (
        result.status.value, result.diagnostics, result.open_goals,
    )
    assert result.conclusion == goal
    assert any(step.rule is ProofRule.INFERENCE and step.conclusion == goal
               for step in result.proven_steps)
