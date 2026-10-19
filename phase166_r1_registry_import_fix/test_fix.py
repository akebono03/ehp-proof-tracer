"""R1 import failure must not be misreported as a completed audit."""
import inspect
from pathlib import Path
import audit


def test_audit_main_fails_closed_if_registry_unavailable(monkeypatch, tmp_path):
    monkeypatch.setattr(audit, 'HERE', tmp_path)
    monkeypatch.setattr(audit, 'CSV_FILE', tmp_path / 'sample.csv')
    (tmp_path / 'sample.csv').write_text('n,k,reference\n3,1,(5.3)\n', encoding='utf-8')
    monkeypatch.setattr(audit, 'get_registry', lambda: (None, 'ModuleNotFoundError: test'))
    assert audit.main() == 2


def test_missing_registry_never_produces_verified_relation():
    rows, _ = audit.inspect([{'n': '3', 'k': '1', 'reference': '(5.3)'}], None)
    assert rows[0]['proof_step_granted'] is False
    assert rows[0]['typed_relation_verified'] is False
