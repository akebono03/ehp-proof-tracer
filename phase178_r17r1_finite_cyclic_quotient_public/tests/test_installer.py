import ast

import pytest

from phase178_r17r1_finite_cyclic_quotient_public.installer import (
    SOURCE_ANCHOR, SOURCE_INSERT, proposed_source, digest,
)


def fixture():
    return ('def build_shared_typed_bridge():\n    return None\n\n'
            + 'def shared_expansion_provider():\n' + SOURCE_ANCHOR + '    return extra_providers\n')


def test_minimal_exact_anchor():
    original = fixture()
    updated = proposed_source(original)
    assert updated.replace(SOURCE_INSERT, '') == original
    assert len(ast.parse(updated).body) == 2
    assert ast.dump(ast.parse(updated).body[0]) == ast.dump(ast.parse(original).body[0])


@pytest.mark.parametrize('replacement', ['', SOURCE_ANCHOR + SOURCE_ANCHOR])
def test_missing_or_duplicate_anchor(replacement):
    with pytest.raises(RuntimeError):
        proposed_source(fixture().replace(SOURCE_ANCHOR, replacement))


def test_double_install_refused():
    with pytest.raises(RuntimeError):
        proposed_source(proposed_source(fixture()))


def test_windows_line_endings():
    assert digest(b'a\r\nb\r\n') == digest(b'a\nb\n')
