import ast
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply import transform_generator, transform_operation, transform_main


def test_generator_ast_cutover():
    src = '''from dataclasses import dataclass
@dataclass
class WebGeneratorExplorationView:
  generator_input: str
  def __post_init__(self):
    pass

def build_standard_web_generator_exploration_view(generator_input):
  return None
'''
    result = transform_generator(src)
    ast.parse(result)
    assert 'search_typed_generator_statements' in result
    assert 'search_status: str' in result
    assert transform_generator(result) == result


def test_operation_ast_cutover():
    src = '''from dataclasses import dataclass
@dataclass
class WebOperationQueryView:
  query_input: str
  def __post_init__(self):
    pass

def build_standard_web_operation_query_view(query_input):
  return None
'''
    result = transform_operation(src)
    ast.parse(result)
    assert 'search_typed_operation_statements' in result
    assert transform_operation(result) == result


def test_cli_cutover():
    source = 'def _run_explore_command(generator_input):\n  return 1\n'
    result = transform_main(source)
    assert 'search_typed_generator_statements' in result
    assert transform_main(result) == result


def test_function_guard():
    import pytest
    with pytest.raises(RuntimeError):
        transform_main('def some_other_function():\n  pass\n')
