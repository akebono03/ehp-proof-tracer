from __future__ import annotations

import pytest

from phase176_r2_n3_source_frontier_audit import audit


def test_source_anchors_on_fixture(tmp_path) -> None:
    for name, (path, anchors) in audit.EVIDENCE.items():
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('a', encoding='utf-8') as stream:
            stream.write(' '.join(anchors) + '\n')
    result = audit.inspect_sources(tmp_path)
    assert set(result) == set(audit.EVIDENCE)
    assert all(row['anchors_present'] for row in result.values())


def test_missing_anchor_not_forgiven(tmp_path) -> None:
    for path in {p for p, anchors in audit.EVIDENCE.values()}:
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('unrelated source\n', encoding='utf-8')
    assert all(not record['anchors_present'] for record in audit.inspect_sources(tmp_path).values())


def test_normalize_source_spacing() -> None:
    assert audit.normalize(' H(\\alpha \\circ  E\\beta)\n') == audit.normalize('H(\\alpha\\circ E\\beta)')


def test_dry_run_never_launches_worker(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr(audit, 'ROOT', tmp_path)
    monkeypatch.setattr(audit, 'preflight', lambda: {'head': 'test-head'})
    monkeypatch.setattr(audit, 'run_worker', lambda timeout: pytest.fail('worker invoked'))
    monkeypatch.setenv('LOCALAPPDATA', str(tmp_path))
    monkeypatch.setattr('sys.argv', ['audit', '--dry-run'])
    assert audit.main() == 0
