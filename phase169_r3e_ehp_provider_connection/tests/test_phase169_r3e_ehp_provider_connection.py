"""R3E: common provider proposes EHP subgoals without fabricating proof leaves."""
from __future__ import annotations

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionIsomorphismStatement, TodaSuspensionMap
from phase165_r14_r5_ehp_connection import expand_registered_ehp_goal
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule
from toda_rules import TodaProp42ExactnessStatement, TodaSuspensionInjectiveStatement, TodaSuspensionSurjectiveStatement


@pytest.fixture(scope="module")
def screened_provider():
    bridge = build_shared_typed_bridge()
    goal, = registered_group_goal_candidates(bridge, n=3, k=2)
    citation = resolve_specialized_goal_citing_id(bridge, goal)
    assert citation is not None
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citation, explicit_publication_target=True,
    )
    screened = prefer_universal_prop42_derivation(screened)
    return screened, shared_expansion_provider(screened, proof_target=goal)


def _iso():
    return TodaSuspensionIsomorphismStatement(
        TodaSuspensionMap(TodaPrimaryGroup(4, 2), TodaPrimaryGroup(5, 3))
    )


def test_common_provider_connects_one_existing_iso_rule(screened_provider):
    _, provider = screened_provider
    previous, = expand_registered_ehp_goal(_iso())
    equivalent = [item for item in provider(_iso())
                  if item.rule.name == previous.rule.name and item.subgoals == previous.subgoals]
    assert len(equivalent) == 1
    assert tuple(type(x) for x in equivalent[0].subgoals) == (
        TodaSuspensionInjectiveStatement, TodaSuspensionSurjectiveStatement,
    )


def test_common_provider_connects_both_historical_branches(screened_provider):
    _, provider = screened_provider
    original, = expand_registered_ehp_goal(_iso())
    for child in original.subgoals:
        previous, = expand_registered_ehp_goal(child)
        matches = [p for p in provider(child) if p.rule.name == previous.rule.name
                   and p.subgoals == previous.subgoals]
        assert len(matches) == 1
        assert isinstance(previous.subgoals[1], TodaProp42ExactnessStatement)
        assert provider(previous.subgoals[1])


def test_unrelated_suspension_is_not_an_ehp_fact(screened_provider):
    _, provider = screened_provider
    unrelated = TodaSuspensionIsomorphismStatement(
        TodaSuspensionMap(TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4))
    )
    assert expand_registered_ehp_goal(unrelated) == ()
    assert not any("n=3 suspension isomorphism" in o.rule.name for o in provider(unrelated))


def test_provider_does_not_add_given_steps(screened_provider):
    screened, provider = screened_provider
    before = tuple(screened.proof_links)
    provider(_iso())
    assert screened.proof_links == before
    assert all(link.step is None or link.step.rule is ProofRule.GIVEN for link in before)
    assert not any(link.step is not None and link.step.conclusion == _iso() for link in before)


def test_historical_endpoints_are_not_given_by_connection(screened_provider):
    _, provider = screened_provider
    root, = expand_registered_ehp_goal(_iso())
    for branch in root.subgoals:
        current = branch
        for _ in range(2):
            expansion, = expand_registered_ehp_goal(current)
            current = expansion.subgoals[0]
        assert expand_registered_ehp_goal(current) == ()
        assert not provider(current)


def test_complete_function_has_one_local_import():
    from pathlib import Path
    path = Path(__file__).resolve().parent.parent / "full_functions" / "shared_expansion_provider.py"
    source = path.read_text(encoding="utf-8")
    assert source.count("from phase165_r14_r5_ehp_connection import expand_registered_ehp_goal") == 1
    assert source.count("extra_providers = (expand_registered_ehp_goal,)") == 1
