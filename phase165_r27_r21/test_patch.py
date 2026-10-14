from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parent.parent
SOURCE = (ROOT / 'phase165_r52_r5_auto_search.py').read_text(encoding='utf-8')
TREE = ast.parse(SOURCE)
FN = next(n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name == 'search_group_structure_automatically')


def test_r27_r21_legacy_calculation_not_used_in_typed_search():
    assert 'from toda_calculation_facade import build_standard_toda_report' not in SOURCE
    assert 'search_shared_group_goal' not in ast.get_source_segment(SOURCE, FN)


def test_r27_r21_registry_discovery_preserved():
    body = ast.get_source_segment(SOURCE, FN)
    assert 'discover_goal_search_inputs()' in body
    assert '_typed_structure_candidates(bridge, group)' in body


def test_r27_r21_does_not_modify_group_query_facade():
    source = (ROOT / 'toda_calculation_facade.py').read_text(encoding='utf-8')
    assert 'def build_standard_toda_report(' in source
    assert 'build_standard_production_proof_repository' in source
