import ast
import pytest
from apply import patch_function, change

def test_patch_function_replace():
    result = patch_function('def x():\n    return 1\n\ndef y():\n    return 2\n', 'x', 'def x():\n    return 3\n')
    tree = ast.parse(result)
    assert [x.name for x in tree.body] == ['x', 'y']
    assert 'return 3' in result

def test_patch_function_missing_refuses():
    with pytest.raises(ValueError):
        patch_function('def x():\n    return 1\n', 'y', None)

def test_prop51_expectation():
    assert change('assert components[-1].range_text is None\n', 'tests/test_phase157_r2_literature_statement_boundary.py') == 'assert components[-1].range_text == "n >= 3"\n'

def test_beta_expectation():
    assert '== r"\\beta"' in change('assert value == r"\\\\beta"\n', 'tests/test_phase150_rc4_5b_3_r1_beta_latex.py')
