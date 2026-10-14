from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location("r22_installer", Path(__file__).with_name("apply.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_r22_r1_accepts_multiline_and_singleline_imports():
    source = '''from dataclasses import dataclass
from toda_calculation_facade import build_standard_toda_report
from toda_human_readable_renderer import (render_toda_group_result_latex,)
from toda_group_query import TodaGroupQuery

def build_standard_web_group_query_view(n, k):
    report = build_standard_toda_report(n=n, k=k)
    return report
'''
    patched, modified = module.patch_source(source)
    assert modified
    assert "build_standard_toda_report" not in patched
    assert "search_group_structure_automatically(n=n, k=k)" in patched


def test_r22_r1_idempotent():
    source = '''def build_standard_web_group_query_view(n, k):
    return search_group_structure_automatically(n=n, k=k)
'''
    patched, changed = module.patch_source(source)
    assert not changed
    assert patched == source


def test_r22_r1_rejects_unknown_function():
    import pytest
    source = '''def build_standard_web_group_query_view(n, k):
    return 0
'''
    with pytest.raises(RuntimeError, match="Unrecognized"):
        module.patch_source(source)
