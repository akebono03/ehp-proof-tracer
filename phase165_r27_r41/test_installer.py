import importlib.util
from pathlib import Path
import tempfile
import pytest

spec = importlib.util.spec_from_file_location('r41_apply', Path(__file__).with_name('apply.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


@pytest.fixture
def root(tmp_path):
    (tmp_path/'repository_operation_query.py').write_text('def parse_repository_operation_query(value):\n    return value\n',encoding='utf-8')
    (tmp_path/'phase165_r27_r34_typed_lookup.py').write_text('from repository_operation_query import parse_repository_operation_query\n',encoding='utf-8')
    (tmp_path/'cli.py').write_text('''from proof_repository import ProofRepository
from typing import TextIO
from repository_element_facade import explore_repository_generator

def resolve_generator_input(x):
    return x

def _write_markdown(a, b):
    pass

def _run_element_command(repository: ProofRepository, generator_input: str, stdout: TextIO, stderr: TextIO) -> int:
    return explore_repository_generator(repository, generator_input)
''',encoding='utf-8')
    return tmp_path


def test_prepare_parser_is_standalone(root):
    result = module.prepare(root)
    assert 'parse_repository_operation_query' in result[root/'toda_operation_query.py']
    assert 'from toda_operation_query import' in result[root/'phase165_r27_r34_typed_lookup.py']


def test_prepare_element_uses_typed_search(root):
    result = module.prepare(root)
    source = result[root/'cli.py']
    assert 'search_typed_generator_statements' in source
    assert 'from repository_element_facade import' not in source


def test_installer_reentrant(root):
    module.install(root)
    module.install(root)
    assert (root/'toda_operation_query.py').exists()


def test_missing_lookup_fails_closed(root):
    (root/'phase165_r27_r34_typed_lookup.py').unlink()
    with pytest.raises(FileNotFoundError):
        module.prepare(root)


def test_backup_conflict_is_rejected(root):
    (root/'phase165_r27_r41_backup').mkdir()
    (root/'phase165_r27_r41_backup'/'cli.py').write_text('different',encoding='utf-8')
    with pytest.raises(ValueError, match='backup collision'):
        module.install(root)
