import ast

import pytest

from phase178_r16r2_toda513_public.installer import (
    SOURCE_ANCHOR, SOURCE_INSERT, proposed_source, digest,
)


def fixture():
    return ('def build_shared_typed_bridge():\n    if default_sources:\n' + SOURCE_ANCHOR
            + '    return sources\n\ndef shared_expansion_provider():\n    return None\n')


def test_minimal_exact_anchor():
    original = fixture()
    updated = proposed_source(original)
    assert updated.replace(SOURCE_INSERT, '') == original
    assert len(ast.parse(updated).body) == 2
    assert ast.dump(ast.parse(updated).body[1]) == ast.dump(ast.parse(original).body[1])


@pytest.mark.parametrize('replacement', ['', SOURCE_ANCHOR + SOURCE_ANCHOR])
def test_missing_or_duplicate_anchor(replacement):
    with pytest.raises(RuntimeError):
        proposed_source(fixture().replace(SOURCE_ANCHOR, replacement))


def test_double_install_refused():
    with pytest.raises(RuntimeError):
        proposed_source(proposed_source(fixture()))


def test_windows_line_endings():
    assert digest(b'a\r\nb\r\n') == digest(b'a\nb\n')
