import ast
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("r22_r3_installer", Path(__file__).with_name("apply.py"))
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


def test_r22_r3_replaces_incomplete_modern_function():
    source = '''from toda_group_query import TodaGroupQuery

def build_standard_web_group_query_view(n, k):
    result = search_group_structure_automatically(n=n,k=k)
    return WebGroupQueryView(n=n,k=k,status=TodaCalculationStatus.NOT_FOUND,result_latex=None)
'''
    patched, changed = installer.patch_source(source)
    assert changed
    assert "result.status is ProofSearchStatus.COMPLETE" in patched
    assert "build_toda_group_structure_presentation(conclusion.rhs)" in patched
    assert "from phase165_r52_r5_auto_search import search_group_structure_automatically" in patched
    ast.parse(patched)


def test_r22_r3_repairs_imports_without_losing_other_functions():
    source = '''from toda_group_query import TodaGroupQuery

def unrelated():
    return 41

''' + installer.NEW_FUNCTION
    patched, changed = installer.patch_source(source)
    assert changed
    assert "def unrelated():" in patched
    assert "return 41" in patched
    assert "from proof import Relation" in patched
    twice, changed_again = installer.patch_source(patched)
    assert not changed_again
    assert twice == patched


def test_r22_r3_rejects_unknown_function():
    with pytest.raises(RuntimeError, match="Unrecognized"):
        installer.patch_source('def build_standard_web_group_query_view(n,k):\n    return None\n')
