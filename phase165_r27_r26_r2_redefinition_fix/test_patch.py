import ast
from pathlib import Path
import pytest
from apply import transform_catalog, _imports, blocking_imports

SOURCE = '''from rule_catalog import InferenceRuleCatalog
from standard_production_repository import (
  build_standard_production_proof_repository,
)

def other():
  return 42

def build_standard_production_applicability_catalog(
) -> InferenceRuleCatalog:
  repository = build_standard_production_proof_repository()
  return repository
'''


def test_catalog_retires_only_standard_entry():
    result = transform_catalog(SOURCE)
    assert not _imports(ast.parse(result), 'standard_production_repository')
    assert 'def other():' in result
    assert 'return 42' in result
    assert 'raise RuntimeError' in result


def test_catalog_repeated_application_safe():
    once = transform_catalog(SOURCE)
    assert transform_catalog(once) == once


def test_catalog_rejects_ambiguous_old_call():
    with pytest.raises(RuntimeError):
        transform_catalog(SOURCE + '\ndef other_old():\n  return build_standard_production_proof_repository()\n')


def test_catalog_absent_standard_entry_is_idempotent():
    source = 'from rule_catalog import InferenceRuleCatalog\n\ndef other():\n  return 42\n'
    assert transform_catalog(source) == source


def test_catalog_absent_standard_entry_with_legacy_import_is_blocked():
    source = 'from standard_production_repository import build_standard_production_proof_repository\n'
    with pytest.raises(RuntimeError, match='function absent'):
        transform_catalog(source)


def test_catalog_absent_standard_entry_with_legacy_call_is_blocked():
    source = 'def other():\n  return build_standard_production_proof_repository()\n'
    with pytest.raises(RuntimeError, match='outside standard'):
        transform_catalog(source)


def test_live_repository_has_no_new_builder_import_after_catalog_change():
    root = Path(__file__).resolve().parent.parent
    catalog = root / 'standard_production_applicability_catalog.py'
    if not catalog.exists():
        pytest.skip('No checkout mounted here')
    converted = transform_catalog(catalog.read_text(encoding='utf-8-sig'))
    assert not blocking_imports(converted)


def test_catalog_multiple_overrides_are_supported():
    source = SOURCE + "\n_phase_original_builder = build_standard_production_applicability_catalog\n" + (
        "def build_standard_production_applicability_catalog():\n"
        "  return _phase_original_builder()\n"
    )
    converted = transform_catalog(source)
    assert not _imports(ast.parse(converted), 'standard_production_repository')
    assert converted.count('def build_standard_production_applicability_catalog(') == 2
    assert converted.count('Legacy production applicability catalog is retired') == 2
    assert transform_catalog(converted) == converted


def test_catalog_rejects_old_builder_in_other_function_with_overrides():
    source = SOURCE + """
def outsider():
  return build_standard_production_proof_repository()

def build_standard_production_applicability_catalog():
  return 0
"""
    with pytest.raises(RuntimeError, match='outside standard catalog entry'):
        transform_catalog(source)
