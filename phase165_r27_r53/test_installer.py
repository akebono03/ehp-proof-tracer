from pathlib import Path
import ast
import importlib.util
import pytest

p=Path(__file__).with_name('apply.py')
spec=importlib.util.spec_from_file_location('r53_installer',p)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

SOURCE='''from proof_repository import ProofRepository
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

def test_deferred_imports():
    s,changed=module.transform(SOURCE)
    assert changed
    t=ast.parse(s)
    assert not any(isinstance(n,ast.ImportFrom) and n.module in module.OLD_IMPORTS for n in t.body)
    assert 'if TYPE_CHECKING:' in s

def test_retains_all_functions():
    s,_=module.transform(SOURCE)
    assert {n.name for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)}=={'build_toda_report','build_standard_toda_report','build_toda_partial_result','build_standard_toda_partial_result'}

def test_deferred_imports_in_legacy_only():
    s,_=module.transform(SOURCE)
    t=ast.parse(s)
    f=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='build_standard_toda_report')
    assert any(isinstance(n,ast.ImportFrom) and n.module=='standard_production_repository' for n in ast.walk(f))

def test_idempotent():
    s,_=module.transform(SOURCE)
    assert module.transform(s)==(s,False)

def test_reject_mismatched_legacy():
    with pytest.raises(RuntimeError):module.transform(SOURCE.replace('return build_toda_report(repository, n=n, k=k)','return None'))

def test_reject_missing_typed_api():
    with pytest.raises(RuntimeError):module.transform(SOURCE.replace('def build_toda_partial_result','def different'))

def test_apply_and_reapply(tmp_path):
    (tmp_path/'toda_calculation_facade.py').write_text(SOURCE)
    (tmp_path/'toda_typed_group_facade.py').write_text('pass\n')
    assert module.apply(tmp_path)['status']=='CHANGED'
    assert module.apply(tmp_path)['status']=='ALREADY_INSTALLED'
    assert (tmp_path/'phase165_r27_r53_backup/toda_calculation_facade.py').exists()

def test_missing_r52_guard(tmp_path):
    (tmp_path/'toda_calculation_facade.py').write_text(SOURCE)
    with pytest.raises(RuntimeError):module.apply(tmp_path)
