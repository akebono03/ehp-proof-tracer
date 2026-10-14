from pathlib import Path
from tempfile import TemporaryDirectory
import json

from apply import imports_of, plan, apply


def _root():
    return TemporaryDirectory()


def test_imports_ast_static_and_literal_dynamic():
    found = imports_of('import repository_proof_scope\nfrom repository_symbolic_sigma_specialization import f\nimport_module("repository_foundational_group_specialization")\n')
    assert {'repository_proof_scope', 'repository_symbolic_sigma_specialization', 'repository_foundational_group_specialization'} <= found


def test_no_false_positive_on_string_literals():
    assert not imports_of('name = "repository_proof_scope"\n')


def test_active_import_is_not_deletable():
    with _root() as location:
        root = Path(location)
        (root / 'toda_calculation.py').write_text('import repository_proof_scope\n')
        (root / 'repository_proof_scope.py').write_text('VALUE=1\n')
        audit = plan(root)
        assert audit['remaining_legacy_modules'] == ['repository_proof_scope']
        assert audit['non_legacy_importers']['repository_proof_scope'] == ['toda_calculation']
        assert not audit['unreferenced_legacy_candidates']


def test_orphan_reported_but_not_deleted():
    with _root() as location:
        root = Path(location)
        target = root / 'repository_proof_scope.py'
        target.write_text('VALUE=1\n')
        report = apply(root)
        assert report['unreferenced_legacy_candidates'] == ['repository_proof_scope']
        assert target.exists()


def test_typed_facade_guard():
    with _root() as location:
        root = Path(location)
        (root / 'toda_typed_group_facade.py').write_text('from repository_proof_scope import build\n')
        (root / 'repository_proof_scope.py').write_text('def build(): pass\n')
        import pytest
        with pytest.raises(RuntimeError, match='Typed facade'):
            plan(root)


def test_legacy_report_path_reported():
    with _root() as location:
        root = Path(location)
        (root / 'toda_calculation.py').write_text('from repository_foundational_group_specialization import f\n')
        (root / 'repository_foundational_group_specialization.py').write_text('def f(): pass\n')
        (root / 'toda_calculation_report.py').write_text('from toda_calculation import build\n')
        audit = plan(root)
        assert audit['active_legacy_imports']['toda_calculation'] == ['repository_foundational_group_specialization']
        assert audit['legacy_group_calculation_replaced'] is False


def test_audit_written_and_repeatable():
    with _root() as location:
        root = Path(location)
        (root / 'toda_typed_group_facade.py').write_text('from phase165_r52_r5_auto_search import search_group_structure_automatically\n')
        first = apply(root)
        second = apply(root)
        assert first == second
        assert json.loads((root / 'phase165_r27_r54_audit.json').read_text()) == second
