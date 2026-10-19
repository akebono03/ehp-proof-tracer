import ast
from recover import safe_source


def test_accepts_authentic_minimal_helper_shape():
    ok, message = safe_source(b'def _method_evidence_data(n, k):\n    return n, k\n')
    assert ok, message


def test_rejects_obsolete_probe_dependency():
    ok, message = safe_source(b'from probes.x import y\ndef _method_evidence_data(n, k):\n    return y(n, k)\n')
    assert not ok
    assert 'retired' in message


def test_rejects_missing_export():
    ok, message = safe_source(b'def unrelated():\n    return 1\n')
    assert not ok
    assert 'no _method_evidence_data' in message


def test_rejects_invalid_syntax():
    ok, message = safe_source(b'def _method_evidence_data(:\n')
    assert not ok
    assert 'cannot parse' in message
