import ast

import pytest

from phase178_r15r2_toda512_public.installer import (
    SOURCE_ANCHOR, SOURCE_INSERT, PROVIDER_ANCHOR, PROVIDER_INSERT,
    proposed_source, digest,
)


def fixture():
    return ('def build_shared_typed_bridge():\n    if default_sources:\n' + SOURCE_ANCHOR
            + '    return sources\n\ndef shared_expansion_provider():\n' + PROVIDER_ANCHOR
            + '    return extra_providers\n')


def test_minimal_exact_anchors():
    original = fixture()
    updated = proposed_source(original)
    assert updated.replace(SOURCE_INSERT, '').replace(PROVIDER_INSERT, '') == original
    assert len(ast.parse(updated).body) == 2


@pytest.mark.parametrize('anchor', [SOURCE_ANCHOR, PROVIDER_ANCHOR])
def test_missing_anchor(anchor):
    with pytest.raises(RuntimeError):
        proposed_source(fixture().replace(anchor, ''))


@pytest.mark.parametrize('anchor', [SOURCE_ANCHOR, PROVIDER_ANCHOR])
def test_duplicate_anchor(anchor):
    with pytest.raises(RuntimeError):
        proposed_source(fixture().replace(anchor, anchor + anchor))


def test_double_install_refused():
    with pytest.raises(RuntimeError):
        proposed_source(proposed_source(fixture()))


def test_windows_line_endings():
    assert digest(b'a\r\nb\r\n') == digest(b'a\nb\n')
