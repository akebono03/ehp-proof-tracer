import ast
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply import FUNCTION, replace_function, apply


def test_replacement_removes_legacy_call():
    src = 'def _run_execute_command(generator_input, candidate_number=None):\n    return run_standard_repository_generator_user_execution_workflow(generator_input)\n'
    changed = replace_function(src, '_run_execute_command', FUNCTION)
    assert 'run_standard_repository_generator_user_execution_workflow' not in changed
    assert 'execute_typed_applicable_rules' in changed
    ast.parse(changed)


def test_other_functions_preserved():
    src = 'def before():\n    return 9\n\ndef _run_execute_command(x):\n    pass\n\ndef after():\n    return 12\n'
    new = replace_function(src, '_run_execute_command', FUNCTION)
    assert 'def before():' in new and 'def after():' in new


def test_missing_function_fails():
    with pytest.raises(RuntimeError):
        replace_function('def other():\n    pass\n', '_run_execute_command', FUNCTION)


def test_real_install_then_idempotent(tmp_path):
    (tmp_path / 'main.py').write_text('def _run_execute_command(generator_input, candidate_number=None):\n    return run_standard_repository_generator_user_execution_workflow(generator_input)\n')
    for name in ('toda_typed_execution.py', 'toda_typed_applicability.py', 'phase165_r27_r34_typed_lookup.py'):
        (tmp_path / name).write_text('')
    assert apply(tmp_path)['status'] == 'CHANGED'
    assert apply(tmp_path)['status'] == 'ALREADY_INSTALLED'


def test_nonmatching_cli_guard(tmp_path):
    (tmp_path / 'main.py').write_text('def _run_execute_command(generator_input, candidate_number=None):\n    return 123\n')
    for name in ('toda_typed_execution.py', 'toda_typed_applicability.py', 'phase165_r27_r34_typed_lookup.py'):
        (tmp_path / name).write_text('')
    with pytest.raises(RuntimeError, match='unrecognized'):
        apply(tmp_path)


def test_cli_function_has_all_three_states():
    assert 'TypedExecutionOutcome.NONE' in FUNCTION
    assert 'TypedExecutionOutcome.AMBIGUOUS' in FUNCTION
    assert 'TypedExecutionOutcome.EXECUTED' in FUNCTION
