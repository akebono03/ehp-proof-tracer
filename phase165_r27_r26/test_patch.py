import ast
from pathlib import Path
import pytest
from apply import transform_catalog, _imports, blocking_imports

SOURCE = '''from rule_catalog import InferenceRuleCatalog
from standard_production_repository import (\n  build_standard_production_proof_repository,\n)\n\ndef other():\n  return 42\n\ndef build_standard_production_applicability_catalog(\n) -> InferenceRuleCatalog:\n  repository = build_standard_production_proof_repository()\n  return repository\n'''

def test_catalog_retires_only_standard_entry():
    result=transform_catalog(SOURCE)
    assert not _imports(ast.parse(result),'standard_production_repository')
    assert 'def other():' in result
    assert 'return 42' in result
    assert 'raise RuntimeError' in result

def test_catalog_repeated_application_safe():
    once=transform_catalog(SOURCE)
    assert transform_catalog(once)==once

def test_catalog_rejects_ambiguous_old_call():
    with pytest.raises(RuntimeError):
        transform_catalog(SOURCE+'\ndef other_old():\n  return build_standard_production_proof_repository()\n')

def test_live_repository_has_no_new_builder_import_after_catalog_change():
    root=Path(__file__).resolve().parent.parent
    catalog=root/'standard_production_applicability_catalog.py'
    if not catalog.exists():
        pytest.skip('No checkout mounted here')
    converted=transform_catalog(catalog.read_text(encoding='utf-8-sig'))
    assert not blocking_imports(converted)
