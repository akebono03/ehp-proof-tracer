from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parent.parent


def test_fixed_pi32_goal_and_legacy_search_absent():
    assert not (ROOT / 'phase165_r14_r34_backward_search.py').exists()
    for filename, forbidden in (
        ('phase165_r14_r35_leaf_binding.py', ('backward_leaf_goals', 'audit_r35')),
        ('phase165_r14_r36_adopted_backward.py', ('reconstruct_adopted_tex_goal', 'audit_r36')),
        ('phase165_r14_r38_direct_registry.py', ('reconstruct_registered_pi32', 'audit_completion')),
    ):
        tree = ast.parse((ROOT / filename).read_text(encoding='utf-8'))
        defined = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
        assert not defined.intersection(forbidden)


def test_adopted_source_registration_remains():
    from pathlib import Path
    from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry
    bridge = build_adopted_typed_reference_registry(ROOT / 'phase165_r14_r39_toda51.tex')
    assert len(bridge.proof_links) == 9
    assert all('pi32' not in a.assertion_id for a in bridge.registry._assertions.values())


def test_common_search_still_importable():
    from phase165_r52_r9_shared_math import search_shared_group_goal
    assert callable(search_shared_group_goal)
