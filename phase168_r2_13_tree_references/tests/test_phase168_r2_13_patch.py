from pathlib import Path
import ast
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from apply import FUNCTION, MARKER, patch_text


def test_patch_preserves_function_and_syntax():
    old = 'def ' + FUNCTION + '(presentation):\n' + MARKER + '      (), {},\n    )\n  )\n  return reference_section\n'
    new, function = patch_text(old)
    assert 'reachable_step_ids' in function
    assert 'reference_section = (' in function
    ast.parse(new)


def test_patch_refuses_duplicate_application():
    old = 'def ' + FUNCTION + '(presentation):\n' + MARKER + '      (), {},\n    )\n  )\n  return reference_section\n'
    new, _ = patch_text(old)
    try:
        patch_text(new)
    except RuntimeError as error:
        assert 'already patched' in str(error)
    else:
        raise AssertionError('duplicate patch must be rejected')
