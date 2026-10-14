import ast
from pathlib import Path
import pytest
from repository_operation_query_facade import query_standard_repository_operation_input
from repository_operation_query_lookup import RepositoryOperationQueryResult


def test_standard_operation_does_not_claim_old_repository_evidence(monkeypatch):
    import standard_production_repository
    def fail():
        raise AssertionError('legacy builder must not run')
    monkeypatch.setattr(standard_production_repository, 'build_standard_production_proof_repository', fail)
    result = query_standard_repository_operation_input('E(nu_5)')
    assert isinstance(result, RepositoryOperationQueryResult)
    assert result.found is False
    assert result.matches == ()


def test_standard_operation_rejects_invalid_query():
    with pytest.raises(ValueError):
        query_standard_repository_operation_input('not_an_operation')


def test_operation_facade_no_legacy_builder_import_or_call():
    path = Path(__file__).resolve().parents[1] / 'repository_operation_query_facade.py'
    source = path.read_text(encoding='utf-8')
    tree = ast.parse(source)
    imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) for alias in node.names}
    assert 'build_standard_production_proof_repository' not in imported
    assert 'validate_repository_internal_proof_roots' not in imported
    standard = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'query_standard_repository_operation_input')
    assert not any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id.startswith('build_standard_production') for node in ast.walk(standard))
