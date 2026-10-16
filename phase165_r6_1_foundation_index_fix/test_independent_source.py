from pathlib import Path
from phase165_r14_r36_adopted_backward import adopted_leaf_steps
from phase165_r14_r16_foundational_suspension import instantiate_foundational_identity_suspension
from phase165_r14_r34_backward_search import pi32_goal
from phase165_r14_r35_leaf_binding import backward_leaf_goals

TEX = Path(__file__).resolve().parent.parent / "phase165_r14_r39_toda51.tex"

def test_foundation_is_iota1_to_iota2():
    steps = adopted_leaf_steps(TEX)
    foundation = [s for s in steps if s.foundational_reference is not None]
    assert len(foundation) == 1
    assert foundation[0].conclusion == instantiate_foundational_identity_suspension(1).statement

def test_all_nine_legacy_leaf_conclusions_preserved():
    steps = adopted_leaf_steps(TEX)
    leaves = backward_leaf_goals(pi32_goal())
    assert len(steps) == len(leaves) == 9
    assert all(sum(s.conclusion == g for s in steps) == 1 for g in leaves)
