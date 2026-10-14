from pathlib import Path
import ast
import sys
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply import apply, replace_function, WEB_FUNCTION, CLI_FUNCTION

def test_replace_function_preserves_neighbor():
    source = 'def x():\n    return 1\n\ndef y():\n    return 2\n'
    result = replace_function(source, 'x', 'def x():\n    return 3\n')
    assert 'return 3' in result and 'return 2' in result

def test_replace_function_requires_unique():
    with pytest.raises(RuntimeError):
        replace_function('def x():\n    pass\ndef x():\n    pass\n', 'x', 'def x():\n    pass\n')

def test_new_functions_syntactically_valid():
    ast.parse(WEB_FUNCTION)
    ast.parse(CLI_FUNCTION)

def test_missing_typed_api_blocks_install(tmp_path):
    with pytest.raises(RuntimeError, match='R27-R43'):
        apply(tmp_path)

def test_install_and_repeat(tmp_path):
    (tmp_path/'toda_typed_applicability.py').write_text('pass\n')
    for file, name in (('main.py','_run_explore_applicable_command'),('web_generator_applicability.py','build_standard_web_generator_applicability_view')):
        (tmp_path/file).write_text(f'def {name}(generator_input):\n    return 0\n',encoding='utf-8')
    first = apply(tmp_path)
    assert len(first['modified_files']) == 2
    assert apply(tmp_path)['status'] == 'ALREADY_INSTALLED'
    assert (tmp_path/'phase165_r27_r44_backup'/'main.py').exists()

def test_fail_closed_on_missing_target(tmp_path):
    (tmp_path/'toda_typed_applicability.py').write_text('pass\n')
    (tmp_path/'main.py').write_text('def unrelated():\n    pass\n')
    with pytest.raises(RuntimeError):
        apply(tmp_path)
