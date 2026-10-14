from pathlib import Path
import ast
import importlib.util
import pytest

spec = importlib.util.spec_from_file_location('r53_r1', Path(__file__).with_name('apply.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

SRC = '''from proof_repository import ProofRepository
from phase164_r7_repository_root_resolution import validate_repository_internal_proof_roots
from standard_production_repository import build_standard_production_proof_repository
from toda_calculation_report import build_toda_calculation_report_result
from toda_calculation_report_result import TodaCalculationReportResult
from toda_group_query import TodaGroupQuery

def build_toda_report(repository: ProofRepository, n: int, k: int) -> TodaCalculationReportResult:
    query = TodaGroupQuery(n=n, k=k)
    return build_toda_calculation_report_result(repository, query)

def build_standard_toda_report(n: int, k: int) -> TodaCalculationReportResult:
    repository = build_standard_production_proof_repository()
    validate_repository_internal_proof_roots(repository)
    return build_toda_report(repository, n=n, k=k)

def build_toda_partial_result(query: TodaGroupQuery):
    from toda_typed_group_facade import build_toda_partial_result as run_typed_search
    return run_typed_search(query)

def build_standard_toda_partial_result(n: int, k: int):
    from toda_typed_group_facade import build_standard_toda_partial_result as run_typed_search
    return run_typed_search(n, k)
'''

def function_body(src, name):
    return next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == name).body

def test_removes_eager_imports():
    out, changed = m.transform(SRC)
    assert changed
    assert not any(isinstance(n, ast.ImportFrom) and n.module in m.LEGACY for n in ast.parse(out).body)

def test_preserves_legacy_bodies_except_imports():
    out, _ = m.transform(SRC)
    for name in m.TARGETS:
        before = function_body(SRC, name)
        after = [n for n in function_body(out, name) if not isinstance(n, ast.ImportFrom)]
        assert ast.dump(ast.Module(body=before, type_ignores=[])) == ast.dump(ast.Module(body=after, type_ignores=[]))

def test_keeps_typed_api_bodies():
    out, _ = m.transform(SRC)
    for name in m.TYPED:
        assert ast.dump(ast.Module(body=function_body(SRC,name),type_ignores=[])) == ast.dump(ast.Module(body=function_body(out,name),type_ignores=[]))

def test_accepts_different_legacy_body():
    changed_src = SRC.replace('return build_toda_report(repository, n=n, k=k)', 'return build_toda_report(repository=repository, n=n, k=k)')
    out, flag = m.transform(changed_src)
    assert flag and 'repository=repository' in out

def test_idempotent():
    out, _ = m.transform(SRC)
    assert m.transform(out) == (out, False)

def test_missing_typed_api():
    with pytest.raises(RuntimeError): m.transform(SRC.replace('def build_toda_partial_result', 'def other'))

def test_reject_other_runtime_use():
    with pytest.raises(RuntimeError): m.transform(SRC + '\ndef unrelated():\n    return build_standard_production_proof_repository()\n')

def test_apply_reapply(tmp_path):
    (tmp_path/'toda_calculation_facade.py').write_text(SRC)
    (tmp_path/'toda_typed_group_facade.py').write_text('pass\n')
    assert m.apply(tmp_path)['status'] == 'CHANGED'
    assert m.apply(tmp_path)['status'] == 'ALREADY_INSTALLED'
    assert (tmp_path/'phase165_r27_r53_r1_backup/toda_calculation_facade.py').exists()

def test_missing_typed_guard(tmp_path):
    (tmp_path/'toda_calculation_facade.py').write_text(SRC)
    with pytest.raises(RuntimeError): m.apply(tmp_path)
