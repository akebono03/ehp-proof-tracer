from pathlib import Path
import ast
import json

NAMES = {
    'toda_pi4_3_delta_image_free_cyclic_inference_rule',
    'toda_pi4_3_finite_cyclic_inference_rule',
    'toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule',
    'toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule',
    'toda_pi4_3_eta3_generator_inference_rule',
    'toda_45_pi4_3_finite_cyclic_transport_inference_rule',
}
ROOT = Path(__file__).resolve().parent.parent

def test_removed_catalog_entries():
    src = (ROOT / 'standard_production_applicability_catalog.py').read_text(encoding='utf-8')
    for name in NAMES:
        assert f'"{name}":' not in src

def test_removed_production_definitions_and_imports():
    for path in ROOT.glob('*.py'):
        tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
        assert not any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in NAMES for n in tree.body), path
        assert not any(isinstance(n, ast.ImportFrom) and any(a.name in NAMES for a in n.names) for n in ast.walk(tree)), path

def test_report_and_absent_adapter():
    here = Path(__file__).resolve().parent
    data = json.loads((here / 'audit_result.json').read_text(encoding='utf-8'))
    assert data['status'] in {'REMOVED', 'ALREADY_ABSENT'}
    assert data['full_pytest_run'] is False
    assert not (ROOT / 'phase165_r52_r23_existing_rule_adapter.py').exists()
