from pathlib import Path
import ast
from install import _patched_source


def test_existing_single_line_source():
    source = 'def build_shared_typed_bridge():\n    production = object()\n    sources = (production, 2)\n    return sources\n'
    patched, status = _patched_source(source)
    assert status == "INSTALLED"
    assert 'sources = (production, 2) + (literature,)' in patched
    ast.parse(patched)


def test_preserves_multiline_source():
    source = 'def build_shared_typed_bridge():\n    production = object()\n    sources = (\n        production,\n        2,\n    )\n    return sources\n'
    patched, status = _patched_source(source)
    assert status == "INSTALLED"
    assert "literature = build_typed_literature_bridge(production)" in patched
    assert 'return sources' in patched
    ast.parse(patched)


def test_installer_idempotent():
    source = 'def build_shared_typed_bridge():\n    production = object()\n    sources = (production, 2)\n'
    patched, _ = _patched_source(source)
    assert _patched_source(patched)[1] == 'ALREADY_INSTALLED'


def test_refuses_unrecognized_shape():
    source = 'def build_shared_typed_bridge():\n    sources = (42,)\n'
    try:
        _patched_source(source)
    except RuntimeError:
        return
    raise AssertionError('Unexpected source shape should abort')
