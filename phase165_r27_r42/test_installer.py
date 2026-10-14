import ast
from pathlib import Path
import sys
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply import MODULE, transform, install

BASE = '''from repository_generator_user_execution_facade import (\n    RepositoryGeneratorUserExecutionWorkflowStatus,\n)\n\nclass View:\n    status: RepositoryGeneratorUserExecutionWorkflowStatus\n\ndef build():\n    return RepositoryGeneratorUserExecutionWorkflowStatus.NONE\n'''


def test_status_rewritten_without_import():
    result = transform(BASE)
    assert 'from repository_generator_user_execution_facade' not in result
    assert 'TypedGeneratorExecutionStatus.NONE' in result
    ast.parse(result)


def test_fails_closed_when_legacy_workflow_still_called():
    text = BASE.replace('    RepositoryGeneratorUserExecutionWorkflowStatus,', '    RepositoryGeneratorUserExecutionWorkflowStatus,\n    run_standard_repository_generator_user_execution_workflow,') + '\nrun_standard_repository_generator_user_execution_workflow("x")\n'
    with pytest.raises(ValueError, match='still used'):
        transform(text)


def test_already_migrated_idempotent():
    result = transform(BASE)
    assert transform(result) == result


def test_installer_and_repeat(tmp_path):
    (tmp_path/'web_generator_execution.py').write_text(BASE, encoding='utf-8')
    first=install(tmp_path)
    second=install(tmp_path)
    assert first['status']=='CHANGED'
    assert second['status']=='ALREADY_INSTALLED'
    assert (tmp_path/'toda_typed_execution_status.py').read_text(encoding='utf-8')==MODULE


def test_module_conflict_is_rejected(tmp_path):
    (tmp_path/'web_generator_execution.py').write_text(BASE, encoding='utf-8')
    (tmp_path/'toda_typed_execution_status.py').write_text('different', encoding='utf-8')
    with pytest.raises(ValueError, match='conflict'):
        install(tmp_path)
