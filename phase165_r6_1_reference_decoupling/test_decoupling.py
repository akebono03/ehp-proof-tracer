from __future__ import annotations
import ast
import inspect
import textwrap
from pathlib import Path

from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry
from phase165_r14_r34_backward_search import pi32_goal
from phase165_r14_r35_leaf_binding import backward_leaf_goals
from phase165_r14_r36_adopted_backward import adopted_leaf_steps
from proof import ProofRule
from unified_statement_registry import AssertionOrigin


def _tex():
    root = Path(__file__).resolve().parent.parent
    return root / 'phase165_r14_r39_toda51.tex'


def test_reference_join_uses_typed_step_conclusions_not_fixed_root():
    source = inspect.getsource(build_adopted_typed_reference_registry)
    tree = ast.parse(textwrap.dedent(source))
    call_names = {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert 'backward_leaf_goals' not in call_names
    assert 'pi32_goal' in call_names  # Internal historic goal remains, no false full-retirement claim.


def test_adopted_fixed_leaves_preserved_exactly():
    tex = _tex()
    original_steps = adopted_leaf_steps(tex)
    expected_frontier = backward_leaf_goals(pi32_goal())
    bridge = build_adopted_typed_reference_registry(tex)
    assert len(bridge.proof_links) == len(expected_frontier) == 9
    assertion_by_id = {a.assertion_id: a for a in bridge.registry._assertions.values()}
    assert all(assertion_by_id[link.assertion_id].origin is AssertionOrigin.FIXED_STATEMENT for link in bridge.proof_links)
    assert all(link.step.rule is ProofRule.GIVEN for link in bridge.proof_links)
    for goal in expected_frontier:
        assert sum(link.step.conclusion == goal for link in bridge.proof_links) == 1
        assert sum(step.conclusion == goal for step in original_steps) == 1


def test_internal_goal_never_promoted_to_fixed_leaf():
    bridge = build_adopted_typed_reference_registry(_tex())
    assert all(link.step.conclusion != pi32_goal() for link in bridge.proof_links)
