import ast
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply as installer


def test_r36_web_functions_have_typed_search_only():
    for filename, (name, replacement) in installer.REPLACEMENTS.items():
        ast.parse(replacement)
        assert 'search_typed_generator_statements' in replacement
        assert 'build_standard_repository' not in replacement
        assert 'explore_standard_repository' not in replacement
        assert 'run_standard_repository' not in replacement


def test_r36_cli_function_replacements_are_complete():
    for name, source in installer.CLI_FUNCTIONS.items():
        tree = ast.parse(source)
        assert len(tree.body) == 1 and tree.body[0].name == name
        assert 'search_typed_generator_statements' in source


def test_r36_ast_replacement_is_idempotent():
    original = 'def example(value):\n  return value\n\nX = 2\n'
    replacement = 'def example(value):\n  return value + 1\n'
    once = installer.replace_function(original, 'example', replacement)
    assert installer.replace_function(once, 'example', replacement) == once
    assert 'X = 2' in once


def test_r36_missing_functions_abort():
    import pytest
    with pytest.raises(RuntimeError):
        installer.replace_function('x = 1\n', 'missing', 'def missing():\n  pass\n')


def test_r36_metadata_added_only_once():
    original = '''from dataclasses import dataclass
@dataclass(frozen=True)
class WebGeneratorProofView:
  name: str
  def __post_init__(self):
    pass
'''
    changed = installer.fields_if_needed(original, 'WebGeneratorProofView')
    assert installer.fields_if_needed(changed, 'WebGeneratorProofView') == changed
    assert 'open_goal_count: int' in changed


def test_r36_incomplete_proof_is_not_fabricated():
    body = installer.REPLACEMENTS['web_generator_proof.py'][1]
    assert 'result.proven_steps' in body
    assert 'result.status.value' in body
    assert '未証明' in body


def test_r36_applicability_and_execution_not_certified():
    a = installer.REPLACEMENTS['web_generator_applicability.py'][1]
    b = installer.REPLACEMENTS['web_generator_execution.py'][1]
    assert 'search_status="not_evaluated"' in a
    assert 'search_status="not_executed"' in b
    assert 'RepositoryGeneratorUserExecutionWorkflowStatus.NONE' in b


def test_r36_syntax_and_expected_scope():
    assert set(installer.REPLACEMENTS) == {
        'web_generator_proof.py', 'web_generator_proof_scope.py',
        'web_generator_applicability.py', 'web_generator_execution.py',
    }
    for _, source in installer.REPLACEMENTS.values():
        ast.parse(source)
