from pathlib import Path
from phase165_r14_r36_adopted_backward import adopted_leaf_steps
from phase165_r14_r34_backward_search import pi32_goal
from phase165_r14_r35_leaf_binding import backward_leaf_goals
from proof import ProofRule

TEX = Path(__file__).resolve().parent.parent / "phase165_r14_r39_toda51.tex"

def test_reference_leaves_match_original_frontier():
    leaves = adopted_leaf_steps(TEX)
    goals = backward_leaf_goals(pi32_goal())
    assert len(leaves) == len(goals) == 9
    assert all(sum(step.conclusion == goal for step in leaves) == 1 for goal in goals)
    assert all(step.rule is ProofRule.GIVEN for step in leaves)

def test_source_catalog_does_not_trace_fixed_goal(monkeypatch):
    import phase165_r14_r36_adopted_backward as module
    monkeypatch.setattr(module, "backward_leaf_goals",
                        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("legacy frontier called")))
    monkeypatch.setattr(module, "pi32_goal",
                        lambda: (_ for _ in ()).throw(AssertionError("fixed goal called")))
    assert len(module.adopted_leaf_steps(TEX)) == 9

def test_reference_registry_keeps_nine_cited_steps():
    from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry
    bridge = build_adopted_typed_reference_registry(TEX)
    assert len(bridge.proof_links) == 9
