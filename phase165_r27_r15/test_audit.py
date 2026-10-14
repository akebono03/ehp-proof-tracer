from pathlib import Path
import pytest
from audit import inspect


def _fixture(tmp_path: Path) -> Path:
    for p in ('repository_operation_query_facade.py', 'repository_element_facade.py', 'standard_production_repository.py'):
        (tmp_path / p).write_text('def ' + ({'repository_operation_query_facade.py': 'query_standard_repository_operation_input', 'repository_element_facade.py': 'explore_standard_repository_generator_input', 'standard_production_repository.py': 'build_standard_production_proof_repository'}[p]) + '():\n    return build_standard_production_proof_repository()\n', encoding='utf-8')
    for p in ('main.py', 'cli.py', 'web_operation_query.py', 'web_generator_exploration.py', 'web_operation_query_proof.py'):
        (tmp_path / p).write_text('def f():\n    return None\n', encoding='utf-8')
    return tmp_path


def test_classification_is_read_only(tmp_path):
    root = _fixture(tmp_path)
    before = {p.name: p.read_bytes() for p in root.iterdir()}
    result = inspect(root)
    assert result['production_files_modified'] is False
    assert result['deletion_authorized'] is False
    assert {p.name: p.read_bytes() for p in root.iterdir()} == before


def test_function_boundaries_identified(tmp_path):
    result = inspect(_fixture(tmp_path))
    assert len(result['public_function_boundaries']) == 3
    assert all('build_standard_production_proof_repository' in x['legacy_calls'] for x in result['public_function_boundaries'])


def test_missing_required_file_fails_closed(tmp_path):
    root = _fixture(tmp_path)
    (root / 'main.py').unlink()
    with pytest.raises(FileNotFoundError):
        inspect(root)
